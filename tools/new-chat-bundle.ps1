$ErrorActionPreference = "Continue"

Write-Host "=== NEW CHAT BUNDLE (paste into chat) ==="
Write-Host ""

# 1) ctx.ps1 (mandatory)
$ctx = Join-Path (Get-Location) "ctx.ps1"
if (Test-Path $ctx) {
  Write-Host "## ctx.ps1"
  & $ctx
} else {
  Write-Host "## ctx.ps1"
  Write-Host "MISSING: ctx.ps1"
}

Write-Host ""
Write-Host "## git status -sb"
git status -sb 2>$null

# 2) Project tree (read-only)
Write-Host ""
Write-Host "## PROJECT-TREE.txt (tail 200)"
if (Test-Path ".\PROJECT-TREE.txt") {
  Get-Content ".\PROJECT-TREE.txt" -Tail 200
} else {
  Write-Host "MISSING: PROJECT-TREE.txt"
  Write-Host "Hint: run 'just tree' manually to generate it."
}

# 3) Recent progress logs
Write-Host ""
Write-Host "## HANDOFF.md (tail 40)"
if (Test-Path ".\HANDOFF.md") { Get-Content ".\HANDOFF.md" -Tail 40 } else { Write-Host "MISSING: HANDOFF.md" }

Write-Host ""
Write-Host "## INCIDENTS.md (tail 40)"
if (Test-Path ".\INCIDENTS.md") { Get-Content ".\INCIDENTS.md" -Tail 40 } else { Write-Host "MISSING: INCIDENTS.md" }

# 4) Optional OpenAPI diff (only if python + tool exists)
Write-Host ""
Write-Host "## OpenAPI diff (optional)"
$py = Get-Command python -ErrorAction SilentlyContinue
$diff = Join-Path (Get-Location) "tools\openapidiff.py"
if ($py -and (Test-Path $diff)) {
  & python $diff
} else {
  if (-not $py) { Write-Host "SKIPPED: python missing" }
  if (-not (Test-Path $diff)) { Write-Host "SKIPPED: tools\openapidiff.py missing" }
}

Write-Host ""
Write-Host "=== END BUNDLE ==="