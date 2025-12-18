param(
  [int]$Port = 9222
)

$list = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
if ($list) {
  Write-Host "CDP already listening on $Port"
  exit 0
}

$chrome = $env:CHROME_EXE
if (-not $chrome) { $chrome = Join-Path $env:ProgramFiles 'Google\Chrome\Application\chrome.exe' }
if (-not (Test-Path $chrome)) { $chrome = Join-Path ${env:ProgramFiles(x86)} 'Google\Chrome\Application\chrome.exe' }

if (-not (Test-Path $chrome)) {
  Write-Error "Chrome not found. Install Chrome or set CHROME_EXE env var."
  exit 1
}

$ud = Join-Path $env:TEMP "b2bplatform-chrome-cdp"
New-Item -ItemType Directory -Force -Path $ud | Out-Null

Start-Process $chrome -ArgumentList @(
  "--remote-debugging-port=$Port",
  "--user-data-dir=$ud",
  "--profile-directory=Default"
)

Start-Sleep -Seconds 1

$list2 = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue
if (-not $list2) {
  Write-Error "Failed to start CDP on port $Port"
  exit 1
}

Write-Host "CDP started on port $Port"