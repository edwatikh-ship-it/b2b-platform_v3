$ErrorActionPreference = "Stop"

Write-Host "B2B Platform: new chat prompt v2 (generated)"
Write-Host ""

Write-Host "HARD RULES / GATES:"
Write-Host "0) NO GUESSING. Facts first."
Write-Host "1) SSoT: api-contracts.yaml is the only API source of truth."
Write-Host "2) Safety: backups for any changed files + git status before/after."
Write-Host "3) Agent learning: AGENT-KNOWLEDGE.md = reusable patterns; HANDOFF.md = factual change log."
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
Write-Host "Test-Path .\DOCS-INDEX.md"
Write-Host "Test-Path .\SPRINTS.md"
Write-Host "Test-Path .\AGENT-KNOWLEDGE.md"
Write-Host "git status -sb"
Write-Host ""
Write-Host "# Show how backend is started (no execution)"
Write-Host "just -n dev-noreload"
Write-Host "just -n dev"
Write-Host ""
Write-Host "# BASE_URL fact: set $Env:BASE_URL to the real running backend URL in THIS shell (no defaults)."
Write-Host "# Pre-flight HTTP checks (only after backend is running):"
Write-Host 'Invoke-RestMethod "$Env:BASE_URL/health"'
Write-Host 'Invoke-RestMethod "$Env:BASE_URL/openapi.json" | Out-Null'
Write-Host ""
Write-Host "# Shell env snapshot:"
Write-Host 'python -c "import os; print(''PYTHONPATH='',os.getenv(''PYTHONPATH'')); print(''DATABASEURL='',os.getenv(''DATABASEURL'')); print(''DATABASE_URL='',os.getenv(''DATABASE_URL''))"'
Write-Host ""
Write-Host "# If something fails: paste the full error + outputs into chat (no guesses)."
Write-Host ""

Write-Host "----- BEGIN CHAT BUNDLE (paste into chat) -----"
Write-Host ""

# 1) Run bundle copier (creates D:\b2bplatform\Prompt and copies files)
$bundle = Join-Path (Get-Location) "tools\new-chat-bundle.ps1"
if (Test-Path $bundle) {
  & $bundle
} else {
  Write-Host "MISSING: tools/new-chat-bundle.ps1"
}

Write-Host ""
Write-Host "=== NEW CHAT BUNDLE (paste into chat) ==="
Write-Host ""

# 2) ctx.ps1 output
$ctx = Join-Path (Get-Location) "ctx.ps1"
Write-Host "## ctx.ps1"
if (Test-Path $ctx) { & $ctx } else { Write-Host "MISSING: ctx.ps1" }

Write-Host ""
Write-Host "## git status -sb"
git status -sb 2>$null

Write-Host ""
Write-Host "FILES COPIED TO:"
Write-Host "D:\b2bplatform\Prompt"
Write-Host ""
Write-Host "FILES TO ATTACH (drag & drop into chat):"
Write-Host "- api-contracts.yaml"
Write-Host "- PROJECT-RULES.md"
Write-Host "- PROJECT-DOC.md"
Write-Host "- DOCS-INDEX.md"
Write-Host "- SPRINTS.md"
Write-Host "- AGENT-KNOWLEDGE.md"
Write-Host "- PROJECT-TREE.txt"
Write-Host "- HANDOFF.md"
Write-Host "- INCIDENTS.md"
Write-Host "- DECISIONS.md"
Write-Host "- ctx.ps1"
Write-Host ""
Write-Host "----- END CHAT BUNDLE -----"