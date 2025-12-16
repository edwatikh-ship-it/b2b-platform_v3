param(
  [string]$RepoRoot = (Get-Location).Path,
  [string]$OutFile = "PROJECT-TREE.txt"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$repo = (Resolve-Path $RepoRoot).Path
$out = Join-Path $repo $OutFile

# Curated allowlist of "key artifacts" (keep it short and useful)
$includePaths = @(
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
  "justfile",
  "tools/*",
  "backend/app/**",
  "backend/alembic/**",
  "backend/tests/**"
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

foreach ($inc in $includePaths) {
  $paths = Get-ChildItem -Path (Join-Path $repo $inc) -Force -ErrorAction SilentlyContinue |
    Where-Object { -not $_.PSIsContainer } |
    ForEach-Object { $_.FullName.Substring($repo.Length).TrimStart('\','/') }

  foreach ($rel in $paths) {
    if (-not (Should-Exclude $rel)) {
      if ($seen.Add($rel)) { $items.Add($rel) | Out-Null }
    }
  }
}

$files = $items | Sort-Object

$content = @()
$content += "PROJECT TREE (key artifacts)"
$content += "Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
$content += ""
$content += $files

$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($out, ($content -join "`n"), $utf8NoBom)
Write-Host "Wrote $OutFile with $($files.Count) paths."