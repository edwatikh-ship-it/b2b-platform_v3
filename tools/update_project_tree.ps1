param(
  [string]$RepoRoot = (Get-Location).Path,
  [string]$OutFile = "PROJECT-TREE.txt"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$excludeDirNames = @(
  ".git", ".venv", "venv", "__pycache__", ".pytest_cache", ".ruff_cache", ".mypy_cache",
  ".idea", ".vscode", "node_modules", "dist", "build", ".tox", ".eggs"
)
$excludeFileNames = @(".env", ".env.local", ".env.production", ".env.development")

function Should-Exclude([string]$fullPath) {
  foreach ($d in $excludeDirNames) {
    if ($fullPath -match [regex]::Escape([System.IO.Path]::DirectorySeparatorChar + $d + [System.IO.Path]::DirectorySeparatorChar)) { return $true }
    if ($fullPath.EndsWith([System.IO.Path]::DirectorySeparatorChar + $d)) { return $true }
  }
  $name = [System.IO.Path]::GetFileName($fullPath)
  if ($excludeFileNames -contains $name) { return $true }
  return $false
}

$repo = (Resolve-Path $RepoRoot).Path
$out = Join-Path $repo $OutFile

$files = Get-ChildItem -Path $repo -Recurse -Force |
  Where-Object { -not $_.PSIsContainer } |
  Where-Object { -not (Should-Exclude $_.FullName) } |
  ForEach-Object { $_.FullName.Substring($repo.Length).TrimStart('\','/') } |
  Sort-Object

$content = @()
$content += "PROJECT TREE (curated)"
$content += "Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
$content += ""
$content += $files

$utf8NoBom = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($out, ($content -join "`n"), $utf8NoBom)
Write-Host "Wrote $OutFile with $($files.Count) files."