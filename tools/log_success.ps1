param(
  [Parameter(Mandatory=$true)][string]$What,
  [Parameter(Mandatory=$true)][string]$Why,
  [Parameter(Mandatory=$true)][string]$VerifyCmd,
  [Parameter(Mandatory=$true)][string]$Expected,

  [string]$Now = "",
  [string]$Next = "",
  [string]$CommitMessage = ""
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Require-File([string]$p) {
  if (-not (Test-Path $p)) { throw "Required file not found: $p" }
}

$repo = (Get-Location).Path
$handoff = Join-Path $repo "HANDOFF.md"
$treeTool = Join-Path $repo "tools\update_project_tree.ps1"

Require-File $handoff
Require-File $treeTool

# 1) Update PROJECT-TREE.txt
powershell -ExecutionPolicy Bypass -File $treeTool -RepoRoot $repo -OutFile "PROJECT-TREE.txt" | Out-Host

# 2) Append to HANDOFF.md (append-only)
$dt = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
$entry = @()
$entry += ""
$entry += "## $dt MSK"
$entry += "- What: $What"
$entry += "- Why: $Why"
$entry += "- Verify: $VerifyCmd"
$entry += "- Expected: $Expected"
if ($Now.Trim().Length -gt 0)  { $entry += "- Now: $Now" }
if ($Next.Trim().Length -gt 0) { $entry += "- Next: $Next" }

$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
$text = Get-Content -Raw -Encoding UTF8 $handoff
[System.IO.File]::WriteAllText($handoff, ($text + ($entry -join "`n")), $utf8NoBom)

# 3) Format + pre-commit (локальный gate)
just fmt | Out-Host
backend\.venv\Scripts\pre-commit.exe run --all-files | Out-Host

# 4) Commit + push
git add -A
if ($CommitMessage.Trim().Length -eq 0) {
  $CommitMessage = "chore: log progress"
}
git commit -m $CommitMessage | Out-Host
git push origin main | Out-Host

Write-Host "Logged to HANDOFF.md, updated PROJECT-TREE.txt, committed and pushed."