param(
  [string]$BackendBaseUrl = "http://127.0.0.1:8000",
  [string]$ParserBaseUrl  = "http://127.0.0.1:9001",
  [string]$CdpBaseUrl     = "http://127.0.0.1:9222"
)

$ErrorActionPreference = "Stop"



function Show-RunHint([string]$title, [string[]]$lines) {
  Write-Host ""
  $bar = ("=" * 12) + " HINT " + ("=" * 12)
  Write-Host $bar -ForegroundColor Yellow
  Write-Host $title -ForegroundColor Yellow

  foreach ($l in $lines) {
    Write-Host ("  {0}" -f $l) -ForegroundColor Black -BackgroundColor Green
  }

  Write-Host $bar -ForegroundColor Yellow
}
function Show-PortOwner([int]$port) {
  $c = Get-NetTCPConnection -LocalPort $port -State Listen -ErrorAction SilentlyContinue | Select-Object -First 1
  if ($null -eq $c) {
    Write-Host ("PORT {0}: FREE" -f $port)
    return
  }
  $owningPid = $c.OwningProcess
  $p = Get-CimInstance Win32_Process -Filter "ProcessId=$owningPid" -ErrorAction SilentlyContinue
  if ($null -eq $p) {
    Write-Host ("PORT {0}: LISTEN pid={1} (process details unavailable)" -f $port, $owningPid)
    return
  }
  Write-Host ("PORT {0}: LISTEN pid={1} name={2}" -f $port, $owningPid, $p.Name)
  Write-Host "  cmd: $($p.CommandLine)"
}

function Get-Json([string]$url) {
  try {
    return Invoke-RestMethod $url -TimeoutSec 10
  } catch {
    Write-Host ("FAILED: {0}" -f $url)
    Write-Host ("Reason: {0}" -f $_.Exception.Message)

    if ($url -match "127\.0\.0\.1:8000|localhost:8000") {
      Write-Host ""
      Show-RunHint "Run this command to start backend in a new PowerShell window:" @(
  "Set-Location D:\b2bplatform\backend",
  "python -m uvicorn app.main:create_app --factory --host 127.0.0.1 --port 8000"
)}

    if ($url -match "127\.0\.0\.1:9001|localhost:9001") {
      Write-Host ""
      Show-RunHint "Run this command to start parser_service in a new PowerShell window:" @(
  "Set-Location D:\b2bplatform\parser_service",
  "python -m uvicorn app.main:app --host 127.0.0.1 --port 9001"
)}

    if ($url -match "127\.0\.0\.1:9222|localhost:9222") {
      Write-Host ""
      Show-RunHint "Run this command to start Chrome CDP:" @(
  "chrome.exe --remote-debugging-port=9222 --user-data-dir=<some-dir>"
)}

    exit 1
  }
}

Write-Host "=== PORT CHECKS ==="
Show-PortOwner 8000
Show-PortOwner 9001
Show-PortOwner 9222

Write-Host ""
Write-Host "=== BACKEND OPENAPI ==="
$openapi = Get-Json "$BackendBaseUrl/openapi.json"

# Determine prefix from existing /health path
$paths = $openapi.paths.PSObject.Properties.Name
$healthPath = $paths | Where-Object { $_ -match '/health$' } | Select-Object -First 1
if (-not $healthPath) { throw "Cannot find any */health path in backend openapi.json" }

# Extract API prefix if any (e.g. /apiv1/health -> /apiv1)
$apiPrefix = ($healthPath -replace '/health$','')
Write-Host "Detected backend health path: $healthPath"
Write-Host "Detected API_PREFIX: '$apiPrefix'"

Write-Host ""
Write-Host "=== BACKEND HEALTH ==="
$health = Get-Json "$BackendBaseUrl$healthPath"
$health | ConvertTo-Json -Depth 5 | Write-Output

Write-Host ""
Write-Host "=== PARSER HEALTH ==="
$parserHealth = Get-Json "$ParserBaseUrl/health"
$parserHealth | ConvertTo-Json -Depth 5 | Write-Output

Write-Host ""
Write-Host "=== CDP CHECK ==="
try {
  $cdp = Get-Json "$CdpBaseUrl/json/version"
  $cdp | ConvertTo-Json -Depth 5 | Write-Output
} catch {
  Write-Host "CDP not reachable at $CdpBaseUrl (start Chrome with --remote-debugging-port=9222)"
  throw
}

Write-Host ""
Write-Host "OK: preflight passed"
