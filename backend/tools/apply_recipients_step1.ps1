# APPLY_RECIPIENTS_STEP1.ps1 (Part A)
# Creates DB table request_recipients + ORM model + repository method
# Run from backend root: D:\b2bplatform\backend

param()

$ErrorActionPreference = "Stop"
$env:PYTHONPATH="."

function Step([string]$msg) { Write-Host "==> $msg" -ForegroundColor Cyan }

function ReadText([string]$path) {
  return [System.IO.File]::ReadAllText($path, [System.Text.UTF8Encoding]::new($false))
}

function WriteText([string]$path, [string]$content) {
  $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
  [System.IO.File]::WriteAllText($path, $content, $utf8NoBom)
}

function BackupFile([string]$path) {
  if (Test-Path $path) {
    $ts = Get-Date -Format "yyyyMMdd-HHmmss"
    Copy-Item $path "$path.bak-$ts" -Force
  }
}

function AppendText([string]$path, [string]$text) {
  $existing = ""
  if (Test-Path $path) { $existing = ReadText $path }
  $nl = if ($existing.Length -eq 0 -or $existing.EndsWith("`r`n") -or $existing.EndsWith("`n")) { "" } else { "`r`n" }
  WriteText $path ($existing + $nl + $text)
}

Step "1) Create Alembic revision (request_recipients)"
$revOut = & .\.venv\Scripts\alembic.exe revision -m "create request_recipients table"
$revLine = ($revOut | Select-String -Pattern "Generating " | Select-Object -First 1)
if (-not $revLine) { throw "Cannot detect Alembic generated file. Output was: $($revOut -join "`n")" }

$revPath = ($revLine.ToString() -replace "^Generating\s+", "") -replace "\s+\.\.\.\s+done$", ""
$revPath = $revPath.Trim()

if (-not (Test-Path $revPath)) { throw "Revision file not found: $revPath" }

$revFile = Split-Path $revPath -Leaf
$revId = $revFile.Split("_")[0]

Step "2) Fill revision content: $revFile ($revId)"
$revContent = @"
""\"""create request_recipients table

Revision ID: $revId
Revises: bbff04c57403
Create Date: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
""\""" 

from alembic import op
import sqlalchemy as sa


revision = "$revId"
down_revision = "bbff04c57403"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "request_recipients",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("request_id", sa.Integer(), nullable=False),
        sa.Column("supplier_id", sa.Integer(), nullable=False),
        sa.Column("selected", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("send_status", sa.String(length=20), nullable=False, server_default=sa.text("'not_sent'")),
        sa.Column("reply_status", sa.String(length=20), nullable=False, server_default=sa.text("'no_reply'")),
        sa.Column("is_new", sa.Boolean(), nullable=False, server_default=sa.text("true")),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("request_id", "supplier_id", name="uq_request_recipients_request_supplier"),
    )

    op.create_index(
        "ix_request_recipients_request_id",
        "request_recipients",
        ["request_id"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_request_recipients_request_id", table_name="request_recipients")
    op.drop_table("request_recipients")
"@
WriteText $revPath $revContent

Step "3) Apply migration: alembic upgrade head"
& .\.venv\Scripts\alembic.exe upgrade head | Out-Null

Step "4) Patch ORM model: app\adapters\db\models.py"
$modelsPath = "app\adapters\db\models.py"
if (-not (Test-Path $modelsPath)) { throw "Not found: $modelsPath" }
BackupFile $modelsPath

$modelsText = ReadText $modelsPath

if ($modelsText -notmatch "class\s+RequestRecipientModel") {
  $block = @"

# ---- UserMessaging: request recipients ----
class RequestRecipientModel(Base):
    __tablename__ = "request_recipients"

    id = Column(Integer, primary_key=True)
    request_id = Column(Integer, nullable=False, index=True)
    supplier_id = Column(Integer, nullable=False)

    selected = Column(Boolean, nullable=False, default=False)
    send_status = Column(String(20), nullable=False, default="not_sent")
    reply_status = Column(String(20), nullable=False, default="no_reply")
    is_new = Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime(timezone=True), nullable=False)
    updated_at = Column(DateTime(timezone=True), nullable=False)
"@
  AppendText $modelsPath $block
  Step "   Added RequestRecipientModel block"
} else {
  Step "   RequestRecipientModel already present, skip"
}

Step "5) Patch repository: app\adapters\db\repositories.py"
$repoPath = "app\adapters\db\repositories.py"
if (-not (Test-Path $repoPath)) { throw "Not found: $repoPath" }
BackupFile $repoPath

$repoText = ReadText $repoPath

# Ensure RequestRecipientModel is importable in repositories.py:
# best-effort: if there is a line importing models, append RequestRecipientModel to it.
if ($repoText -notmatch "RequestRecipientModel") {
  $repoText2 = $repoText -replace "(from\s+app\.adapters\.db\.models\s+import\s+[^\r\n]+)", ('$1, RequestRecipientModel')
  if ($repoText2 -eq $repoText) {
    # no such import line found; do not guess. We'll require manual fix if project differs.
    Step "   WARN: could not auto-patch models import in repositories.py (no matching import line)."
  } else {
    $repoText = $repoText2
    Step "   Patched repositories.py import to include RequestRecipientModel"
  }
}

if ($repoText -notmatch "from\s+datetime\s+import\s+datetime") {
  $repoText = "from datetime import datetime`r`n" + $repoText
  Step "   Added datetime import"
}

WriteText $repoPath $repoText

# Add method block (append-only)
$repoText = ReadText $repoPath
if ($repoText -notmatch "async\s+def\s+upsert_recipients") {
  $method = @"

    async def upsert_recipients(self, request_id: int, recipients: list[dict]) -> list[dict]:
        \"\"\"MVP: replace recipients list for a request (no supplier<->request validation yet).\"\"\"
        now = datetime.utcnow()

        await self.session.execute(
            delete(RequestRecipientModel).where(RequestRecipientModel.request_id == request_id)
        )

        for rec in recipients:
            self.session.add(
                RequestRecipientModel(
                    request_id=request_id,
                    supplier_id=rec["supplier_id"],
                    selected=rec["selected"],
                    send_status="not_sent",
                    reply_status="no_reply",
                    is_new=True,
                    created_at=now,
                    updated_at=now,
                )
            )

        await self.session.commit()

        res = await self.session.execute(
            select(RequestRecipientModel)
            .where(RequestRecipientModel.request_id == request_id)
            .order_by(RequestRecipientModel.supplier_id.asc())
        )
        items = res.scalars().all()
        return [
            {
                "supplier_id": x.supplier_id,
                "selected": x.selected,
                "send_status": x.send_status,
                "reply_status": x.reply_status,
                "is_new": x.is_new,
            }
            for x in items
        ]
"@
  AppendText $repoPath $method
  Step "   Added upsert_recipients method block"
} else {
  Step "   upsert_recipients already present, skip"
}

Step "6) Import smoke checks"
& .\.venv\Scripts\python.exe -c "from app.adapters.db.models import RequestRecipientModel; print('model ok')" | Out-Null
& .\.venv\Scripts\python.exe -c "from app.adapters.db.repositories import RequestRepository; print('repo ok')" | Out-Null

Write-Host "PART A DONE" -ForegroundColor Green