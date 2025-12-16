$ErrorActionPreference = "Continue"

Write-Host "=== PWD ==="
Get-Location

Write-Host "`n=== SSoT presence ==="
"api-contracts.yaml","PROJECT-RULES.md","PROJECT-DOC.md","HANDOFF.md","INCIDENTS.md","PROJECT-TREE.txt" | ForEach-Object {
  "{0} => {1}" -f $_, (Test-Path (Join-Path "D:\b2bplatform" $_))
}

Write-Host "`n=== Git ==="
git rev-parse --show-toplevel 2>$null
git status -sb 2>$null

Write-Host "`n=== Tools presence ==="
"ruff","pre-commit","pyclean","uv","direnv","just","python","psql","git" | ForEach-Object {
  $cmd = Get-Command $_ -ErrorAction SilentlyContinue
  if ($cmd) { "{0} => {1}" -f $_, $cmd.Source } else { "{0} => MISSING" -f $_ }
}

Write-Host "`n=== Python ==="
python -V
python -c "import os, sys; print('exe=', sys.executable); print('PYTHONPATH=', os.getenv('PYTHONPATH'))"

Write-Host "`n=== DB env ==="
python -c "import os; print('DATABASE_URL=', os.getenv('DATABASE_URL')); print('DATABASEURL=', os.getenv('DATABASEURL'))"

Write-Host "`n=== Alembic quick (if backend configured) ==="
python -m alembic current 2>&1 | Select-Object -First 40
