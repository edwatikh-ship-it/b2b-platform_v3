$ErrorActionPreference = "Continue"

Write-Host "=== NEW CHAT BUNDLE (paste into chat) ==="
Write-Host ""

# ctx.ps1 (mandatory)
$ctx = Join-Path (Get-Location) "ctx.ps1"
Write-Host "## ctx.ps1"
if (Test-Path $ctx) {
  & $ctx
} else {
  Write-Host "MISSING: ctx.ps1"
}

Write-Host ""
Write-Host "## git status -sb"
git status -sb 2>$null

Write-Host ""
Write-Host "=== END BUNDLE ==="