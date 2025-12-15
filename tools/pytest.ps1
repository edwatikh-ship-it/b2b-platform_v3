param(
  [Parameter(ValueFromRemainingArguments=$true)]
  [string[]]$Args
)

$ErrorActionPreference = "Stop"

# Make imports like "from app.main import app" work when running from repo root.
$env:PYTHONPATH = (Join-Path $PSScriptRoot "..\backend")

Push-Location (Join-Path $PSScriptRoot "..\backend")
try {
  python -m pytest -q @Args
}
finally {
  Pop-Location
}