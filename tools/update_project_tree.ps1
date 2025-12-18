param(
  [string]$RepoRoot = (Get-Location).Path,
  [string]$OutFile = "PROJECT-TREE.txt"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repo = (Resolve-Path $RepoRoot).Path
$out = Join-Path $repo $OutFile

# Curated allowlist of "key artifacts" (keep it short and useful)
$includeFiles = @(
  "api-contracts.yaml",
  "PROJECT-RULES.md",
  "PROJECT-DOC.md",
  "PROJECT-TREE.txt",
  "HANDOFF.md",
  "INCIDENTS.md",
  "DECISIONS.md",
  "README.md",
  "CHANGELOG.md",
  ".pre-commit-config.yaml",
  ".gitattributes",
  ".gitignore",
  "justfile"
)

# These are expanded via Get-ChildItem with -Recurse (PowerShell glob ** does not mean recursive)
$includeDirs = @(
  "tools",
  "backend/app",
  "backend/alembic",
  "backend/tests"
)
$excludeDirNames = @(
  ".git", ".venv", "venv", "__pycache__", ".pytest_cache", ".ruff_cache", ".mypy_cache",
  ".idea", ".vscode", "node_modules", "dist", "build", ".tox", ".eggs"
)

$excludePatterns = @("*.bak*","*.tmp","*.log","*~")

function Should-Exclude([string]$relPath) {
  $p = $relPath -replace "/", "\"

  foreach ($d in $excludeDirNames) {
    if ($p -like "*\$d\*") { return $true }
    if ($p -like "*\$d") { return $true }
  }

  $name = Split-Path $p -Leaf
  foreach ($pat in $excludePatterns) {
    if ($name -like $pat) { return $true }
  }

  return $false
}

$seen = New-Object System.Collections.Generic.HashSet[string]
$items = New-Object System.Collections.Generic.List[string]

foreach ($f in $includeFiles) {
  $full = Join-Path $repo $f
  if (Test-Path $full) {
    $rel = $full.Substring($repo.Length).TrimStart('\','/')
    if (-not (Should-Exclude $rel)) {
      if ($seen.Add($rel)) { $items.Add($rel) | Out-Null }
    }
  }
}

foreach ($d in $includeDirs) {
  $root = Join-Path $repo $d
  if (Test-Path $root) {
    $paths = Get-ChildItem -Path $root -File -Recurse -Force -ErrorAction SilentlyContinue |
      ForEach-Object { $_.FullName.Substring($repo.Length).TrimStart('\','/') }

    foreach ($rel in $paths) {
      if (-not (Should-Exclude $rel)) {
        if ($seen.Add($rel)) { $items.Add($rel) | Out-Null }
      }
    }
  }
}
$files = $items | Sort-Object

$keyPoints = @()
$keyPoints += "KEY POINTS (what to edit, where)"
$keyPoints += "SSoT"
$keyPoints += "  api-contracts.yaml                       - API contract and DTO shapes (SSoT)."
$keyPoints += "Docs / rules"
$keyPoints += "  PROJECT-RULES.md                         - Process rules (SSoT for workflow)."
$keyPoints += "  PROJECT-DOC.md                           - Product/behavior documentation."
$keyPoints += "  DECISIONS.md                             - Important decisions (fact-only)."
$keyPoints += "Logs (append-only)"
$keyPoints += "  HANDOFF.md                               - Success log with verification."
$keyPoints += "  INCIDENTS.md                             - Failure log with fix + verification."
$keyPoints += "Backend entrypoints"
$keyPoints += "  backend\app\main.py                       - FastAPI app wiring (routers, lifespan)."
$keyPoints += "Contract enforcement"
$keyPoints += "  backend\tests\contract\test_openapi_paths_match_contract.py - OpenAPI vs SSoT paths test."
$keyPoints += "HTTP routers"
$keyPoints += "  backend\app\transport\routers\            - HTTP endpoints (FastAPI routers)."
$keyPoints += "DTO schemas"
$keyPoints += "  backend\app\transport\schemas\            - Request/response DTOs."
$keyPoints += "Use cases"
$keyPoints += "  backend\app\usecases\                     - Business flows orchestration."
$keyPoints += "Domain"
$keyPoints += "  backend\app\domain\                       - Pure models and ports."
$keyPoints += "DB adapters"
$keyPoints += "  backend\app\adapters\db\                  - SQLAlchemy models/repositories/session."
$keyPoints += "Migrations"
$keyPoints += "  backend\alembic\                          - Alembic config + migrations."
$keyPoints += "Tooling"
$keyPoints += "  tools\preflight.ps1                       - Pre-flight checks (base url / openapi / deps)."
$keyPoints += "  tools\update_project_tree.ps1             - Regenerate PROJECT-TREE.txt (this script)."
$keyPoints += "  tools\validate_openapi_contract.py        - Contract validation helper."
$keyPoints += "  tools\openapi_diff.py                     - Diff runtime OpenAPI vs SSoT."
$keyPoints += "  tools\doc_edit.py                         - Deterministic doc patcher (anchors + backups)."
$keyPoints += ""

$content = @()
$content += "PROJECT TREE (key artifacts)"
$content += "Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
$content += ""
$content += $keyPoints
$content += $files

$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($out, ($content -join "`n"), $utf8NoBom)
