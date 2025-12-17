$ErrorActionPreference = "Stop"

Write-Host "B2B Platform: new chat prompt (generated)"
Write-Host ""
Write-Host "HARD RULES / GATES:"
Write-Host "0) NO GUESSING. Facts first."
Write-Host "1) SSoT: api-contracts.yaml is the only API source of truth."
Write-Host "2) Safety: backups for any changed files + git status before/after."
Write-Host ""
Write-Host "PRE-FLIGHT (must run):"
Write-Host "- Determine BASE_URL and API_PREFIX (do not assume)."
Write-Host "- Invoke-RestMethod ""`$BASE_URL/`$API_PREFIX/health"" (or contract path) -> expect status ok."
Write-Host "- Invoke-RestMethod ""`$BASE_URL/openapi.json"" | Out-Null -> expect 200."
Write-Host "- python -c ""import os; print(os.getenv('DATABASEURL'), os.getenv('DATABASE_URL'))"""
Write-Host ""

Write-Host "----- BEGIN CHAT BUNDLE (paste into chat) -----"
Write-Host ""

$repoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$just = Get-Command just -ErrorAction SilentlyContinue
if ($null -ne $just) {
  Push-Location $repoRoot
  try { & powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $repoRoot "tools\new-chat-bundle.ps1") } finally { Pop-Location }
} else {
  Write-Host "WARN: 'just' not found in PATH; falling back to direct script call."
  & powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $repoRoot "tools\new-chat-bundle.ps1")
}

Write-Host ""
Write-Host "----- END CHAT BUNDLE -----"

Write-Host "FILES TO ATTACH (drag & drop into chat):"
Write-Host "- api-contracts.yaml"
Write-Host "- PROJECT-RULES.md"
Write-Host "- PROJECT-DOC.md"
Write-Host "- PROJECT-TREE.txt"
Write-Host "- HANDOFF.md"
Write-Host "- INCIDENTS.md"
Write-Host "- DECISIONS.md"
Write-Host ""