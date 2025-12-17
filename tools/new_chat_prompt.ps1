$ErrorActionPreference = "Stop"

function Write-Section([string]$title) {
  Write-Host ""
  Write-Host $title
}

Write-Host "B2B Platform: new chat prompt (generated)"
Write-Host ""
Write-Host "HARD RULES / GATES:"
Write-Host "0) NO GUESSING. Facts first."
Write-Host "1) SSoT: api-contracts.yaml is the only API source of truth."
Write-Host "2) Safety: backups for any changed files + git status before/after."
Write-Host ""

# --- PRE-FLIGHT ---
Write-Host ""
Write-Host "PRE-FLIGHT (must run, no guessing):"
Write-Host ""
Write-Host "COMMANDS TO RUN (copy/paste into PowerShell; no code changes):"
Write-Host "Set-Location D:\b2bplatform"
Write-Host ""
Write-Host "# SSoT + repo state"
Write-Host "Test-Path .\api-contracts.yaml"
Write-Host "Test-Path .\PROJECT-RULES.md"
Write-Host "Test-Path .\PROJECT-DOC.md"
Write-Host "git status -sb"
Write-Host ""
Write-Host "# Show how backend is started (no execution)"
Write-Host "just -n dev-noreload"
Write-Host "just -n dev"
Write-Host ""
Write-Host "# Determine BASE_URL from the just output above, then set it (example):"
Write-Host "`$BASE_URL=`"http://127.0.0.1:8000`""
Write-Host ""
Write-Host "# Pre-flight HTTP checks (contract/runtime)"
Write-Host "Invoke-RestMethod `"`$BASE_URL/health`""
Write-Host "Invoke-RestMethod `"`$BASE_URL/openapi.json`" | Out-Null"
Write-Host ""
Write-Host "# Shell env snapshot (important if DB required at import-time)"
Write-Host "python -c `"import os; print('PYTHONPATH=',os.getenv('PYTHONPATH')); print('DATABASEURL=',os.getenv('DATABASEURL')); print('DATABASE_URL=',os.getenv('DATABASE_URL'))`""
Write-Host ""
Write-Host "# If something fails: paste the full error + outputs into chat (no guesses)."
Write-Host ""
# repo root (needed for new-chat-bundle.ps1)
$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$just = Get-Command just -ErrorAction SilentlyContinue
Write-Host "----- BEGIN CHAT BUNDLE (paste into chat) -----"
Write-Host ""

# bundle generator (read-only)
$just = Get-Command just -ErrorAction SilentlyContinue
if ($null -ne $just) {
  Push-Location $repoRoot
  try {
    & powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $repoRoot "tools\new-chat-bundle.ps1")
  } finally {
    Pop-Location
  }
} else {
  Write-Host "WARN: 'just' not found in PATH; falling back to direct script call."
  & powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $repoRoot "tools\new-chat-bundle.ps1")
}

Write-Host ""
Write-Host "----- END CHAT BUNDLE -----"
Write-Host ""

Write-Host "FILES TO ATTACH (drag & drop into chat):"
Write-Host "- api-contracts.yaml"
Write-Host "- PROJECT-RULES.md"
Write-Host "- PROJECT-DOC.md"
Write-Host "- PROJECT-TREE.txt"
Write-Host "- HANDOFF.md"
Write-Host "- INCIDENTS.md"
Write-Host "- DECISIONS.md"
Write-Host ""