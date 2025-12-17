$ErrorActionPreference = "Stop"

# ANSI red, with a safe fallback for terminals that do not render ANSI.
$RED = [char]27 + "[31m"
$RST = [char]27 + "[0m"

function Mark-Doc([string]$name) {
  # If ANSI is not supported, the escape codes will show as garbage;
  # fallback markers still keep the name visible.
  return "$RED$name$RST"
}

$docs = @(
  "api-contracts.yaml",
  "PROJECT-RULES.md",
  "PROJECT-DOC.md",
  "PROJECT-TREE.txt",
  "HANDOFF.md",
  "INCIDENTS.md",
  "DECISIONS.md"
)

$docsMarked = $docs

$txt = @"
You are starting work in the B2B Platform repo.

HARD RULES / GATES (must follow):
0) NO GUESSING. Facts first. If unknown -> run commands to discover -> STOP.

1) SSoT:
- API contracts = ONLY api-contracts.yaml (repo root).
- Priority: api-contracts.yaml -> PROJECT-RULES.md -> PROJECT-DOC.md.
- If runtime/implementation differs from api-contracts.yaml => treat as a bug; align code to contract (or change contract intentionally).

2) Before asking to change any code:
Ask the user to DRAG&DROP these files into the chat:
- (See the red file list at the end of this prompt.)

3) PRE-FLIGHT / FACTS (no guessing defaults):
NO PLACEHOLDERS:
- Do NOT paste placeholders like {BASE_URL} / {API_PREFIX}. First print the real values.

A) Context dump:
- PowerShell: Set-Location D:\b2bplatform; .\ctx.ps1

B) BASE_URL:
- Confirm the exact running base url (host:port). Do NOT assume.

C) OpenAPI:
- Invoke-RestMethod '$BASE_URL/openapi.json' | Out-Null  (expect 200)

D) API_PREFIX (derive from OpenAPI paths):
- If OpenAPI has "/health" -> API_PREFIX is empty -> health is "<BASE_URL>/health"
- If OpenAPI has "/apiv1/health" -> API_PREFIX is "apiv1" -> health is "<BASE_URL>/apiv1/health"

E) Health:
- Invoke-RestMethod '$BASE_URL/health' (if API_PREFIX empty) OR '$BASE_URL/$API_PREFIX/health'

F) DB env in CURRENT shell (only if needed by imports/routers):
- python -c "import os; print(os.getenv('DATABASEURL'), os.getenv('DATABASE_URL'))"
4) Repo changes safety (mandatory):
- Backups and temporary files MUST go under D:\b2bplatform\.tmp\
- Show git status before and after.
- Provide rollback commands.
- Write text files as UTF-8 without BOM.

5) Patch safety (STOP-ON-MISMATCH):
- Prefer deterministic patches.
- If anchor not found => STOP and request a fresh snapshot.
"@

Write-Host $txt

Write-Host ""
Write-Host "FILES TO ATTACH (drag & drop into chat):" -ForegroundColor Red
foreach ($d in $docs) {
  Write-Host ("- " + $d) -ForegroundColor Red
}

# Fallback hint if ANSI looks ugly in user's terminal
Write-Host ""
Write-Host "If red highlight is not visible in this terminal, treat highlighted doc names as plain text."
