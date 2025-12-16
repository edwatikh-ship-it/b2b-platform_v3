$ErrorActionPreference = "Continue"

Write-Host "=== PWD ==="
Get-Location

Write-Host "`n=== Repo root check ==="
Test-Path "D:\b2bplatform\api-contracts.yaml"
Test-Path "D:\b2bplatform\PROJECT-RULES.md"

Write-Host "`n=== Git ==="
git rev-parse --show-toplevel 2>$null
git status -sb 2>$null

Write-Host "`n=== Tools presence ==="
"ruff","pre-commit","pyclean","uv","direnv","just","python","psql","alembic","git" | ForEach-Object {
  $cmd = Get-Command $_ -ErrorAction SilentlyContinue
  if ($cmd) { "{0} => {1}" -f $_, $cmd.Source } else { "{0} => MISSING" -f $_ }
}

Write-Host "`n=== Python ==="
python -V
python -c "import sys; print('exe=', sys.executable); print('PYTHONPATH=', __import__('os').getenv('PYTHONPATH'));"

Write-Host "`n=== DB env ==="
python -c "import os; print('DATABASE_URL=', os.getenv('DATABASE_URL')); print('DATABASEURL=', os.getenv('DATABASEURL'));"

Write-Host "`n=== Alembic quick ==="
python -m alembic current 2>&1 | Select-Object -First 40

Write-Host "`n=== Backend preflight (optional) ==="
Write-Host "If backend is running: try GET /openapi.json and /health per PROJECT-RULES."
