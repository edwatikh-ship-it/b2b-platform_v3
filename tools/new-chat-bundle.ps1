$ErrorActionPreference = "Stop"

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
Write-Host "=== FILE BUNDLE (copied to D:\b2bplatform\Prompt) ==="

$bundleDir = "D:\b2bplatform\Prompt"
New-Item -ItemType Directory -Force -Path $bundleDir | Out-Null

$filesToCopy = @(
  "api-contracts.yaml",
  "PROJECT-RULES.md",
  "PROJECT-DOC.md",
  "DOCS-INDEX.md",
  "SPRINTS.md",
  "PROJECT-TREE.txt",
  "HANDOFF.md",
  "INCIDENTS.md",
  "DECISIONS.md",
  "ctx.ps1"
)

foreach ($rel in $filesToCopy) {
  $src = Join-Path (Get-Location) $rel
  if (Test-Path $src) {
    Copy-Item -Force $src (Join-Path $bundleDir $rel)
    Write-Host ("COPIED: " + $rel)
  } else {
    Write-Host ("MISSING: " + $rel)
  }
}

Write-Host "=== END BUNDLE ==="
