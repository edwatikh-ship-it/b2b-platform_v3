param(
  [int]$Port = 9001,
  [int]$CdpPort = 9222,
  [string]$BindHost = "127.0.0.1",
  [string]$ServiceDir = "D:\b2bplatform\parser_service",
  [switch]$AutoKillPort9001,
  [switch]$AutoKillCdpPort9222
)

$ErrorActionPreference = "Stop"

function Say($m){ Write-Host $m }

function Require-Cmd($name){
  $cmd = Get-Command $name -ErrorAction SilentlyContinue
  if (-not $cmd) { throw "Missing tool: $name" }
  return $cmd.Source
}

function Get-ListeningPid($port){
  $line = netstat -ano | Select-String -Pattern "LISTENING" | Select-String -Pattern ":$port\s"
  if (-not $line) { return $null }
  $listenerPid = ($line.Line -split "\s+")[-1]
  if ($listenerPid -match "^\d+$") { return [int]$listenerPid }
  return $null
}

function Get-ProcessCommandLine($processId){
  try {
    $w = Get-CimInstance Win32_Process -Filter "ProcessId=$processId" -ErrorAction Stop
    return $w.CommandLine
  } catch {
    return $null
  }
}

function Is-ParserServiceUvicorn($cmdLine){
  if (-not $cmdLine) { return $false }
  $c = $cmdLine.ToLowerInvariant()
  # accept both: "python -m uvicorn app.main:app" and direct uvicorn.exe
  $hasUvicorn = ($c -match "\buvicorn\b")
  $hasApp = ($c -match "app\.main:app")
  $hasServicePath = ($c -match "d:\\b2bplatform\\parser_service") -or ($c -match "\\parser_service\\")
  return $hasUvicorn -and ($hasApp -or $hasServicePath)
}

function Is-OurCdpChrome($cmdLine){
  if (-not $cmdLine) { return $false }
  $c = $cmdLine.ToLowerInvariant()
  return ($c -match "--remote-debugging-port=9222") -and ($c -match "--user-data-dir=d:\\b2bplatform\\.tmp\\chrome-cdp-profile")
}

function Ensure-PortFree($port){
  $listenerPid = Get-ListeningPid $port
  if (-not $listenerPid) { return }

  $p = Get-Process -Id $listenerPid -ErrorAction SilentlyContinue
  $cmdLine = Get-ProcessCommandLine $listenerPid

  if ($AutoKillPort9001 -and $port -eq 9001) {
    if (-not $p) { throw "Port $port is busy (PID=$listenerPid). AutoKillPort9001 refused (process not found). cmd=$cmdLine" }
    if ($p.ProcessName -ne "python") { throw "Port $port is busy (PID=$listenerPid, name=$($p.ProcessName)). AutoKillPort9001 refused (not python). cmd=$cmdLine" }
    if (-not (Is-ParserServiceUvicorn $cmdLine)) { throw "Port $port is busy (PID=$listenerPid, name=python). AutoKillPort9001 refused (not parserservice uvicorn). cmd=$cmdLine" }

    Say "Port $port is busy (PID=$listenerPid, name=python) and looks like parserservice => stopping..."
    Stop-Process -Id $listenerPid -Force
    Start-Sleep -Milliseconds 700

    $still = Get-ListeningPid $port
    if ($still) { throw "Tried to stop PID=$listenerPid but port $port is still busy (PID=$still)." }
    return
  }

  if ($p) { throw "Port $port is busy (PID=$listenerPid, name=$($p.ProcessName)). Stop it first. cmd=$cmdLine" }
  throw "Port $port is busy (PID=$listenerPid). Stop it first."
}

function Start-ChromeCdp($cdpPort){
  $chrome = "$env:ProgramFiles\Google\Chrome\Application\chrome.exe"
  if (-not (Test-Path $chrome)) { $chrome = "$env:ProgramFiles(x86)\Google\Chrome\Application\chrome.exe" }
  if (-not (Test-Path $chrome)) { throw "Chrome not found in Program Files." }

  $userData = "D:\b2bplatform\.tmp\chrome-cdp-profile"
  New-Item -ItemType Directory -Force -Path $userData | Out-Null

  Start-Process $chrome -ArgumentList @(
    "--remote-debugging-address=127.0.0.1",
    "--remote-debugging-port=$cdpPort",
    "--user-data-dir=$userData",
    "--no-first-run",
    "--no-default-browser-check",
    "about:blank"
  ) | Out-Null
}

function Wait-Cdp($cdpPort, $timeoutSec){
  $deadline = (Get-Date).AddSeconds($timeoutSec)
  while ((Get-Date) -lt $deadline) {
    $p = Get-ListeningPid $cdpPort
    if ($p) {
      try { Invoke-RestMethod "http://127.0.0.1:$cdpPort/json/version" | Out-Null; return $true } catch {}
    }
    Start-Sleep -Milliseconds 250
  }
  return $false
}

function Ensure-CdpHealthy($cdpPort){
  try { Invoke-RestMethod "http://127.0.0.1:$cdpPort/json/version" | Out-Null; return } catch {}

  $listenerPid = Get-ListeningPid $cdpPort
  if ($listenerPid) {
    $p = Get-Process -Id $listenerPid -ErrorAction SilentlyContinue
    $cmdLine = Get-ProcessCommandLine $listenerPid

    if (-not $AutoKillCdpPort9222) {
      throw "CDP port $cdpPort is busy/unhealthy (PID=$listenerPid, name=$($p.ProcessName)). AutoKillCdpPort9222 not enabled. cmd=$cmdLine"
    }
    if (-not $p) { throw "CDP port $cdpPort is busy/unhealthy (PID=$listenerPid). AutoKillCdpPort9222 refused (process not found). cmd=$cmdLine" }
    if ($p.ProcessName -ne "chrome") { throw "CDP port $cdpPort is busy/unhealthy (PID=$listenerPid, name=$($p.ProcessName)). AutoKillCdpPort9222 refused (not chrome). cmd=$cmdLine" }
    if (-not (Is-OurCdpChrome $cmdLine)) { throw "CDP port $cdpPort is busy/unhealthy (PID=$listenerPid, name=chrome). AutoKillCdpPort9222 refused (not our cdp chrome). cmd=$cmdLine" }

    Say "CDP port $cdpPort unhealthy but owned by our Chrome (PID=$listenerPid) => restarting..."
    Stop-Process -Id $listenerPid -Force
    Start-Sleep -Milliseconds 800
  }

  Say "Starting Chrome CDP..."
  Start-ChromeCdp $cdpPort
  if (-not (Wait-Cdp $cdpPort 15)) { throw "CDP not ready (port $cdpPort)." }
}

Say "== tools =="
Say ("python: " + (Require-Cmd python))
Say ("ruff: " + (Require-Cmd ruff))
$just = Get-Command just -ErrorAction SilentlyContinue
if ($just) { Say ("just: " + $just.Source) } else { Say "just: MISSING (ok)" }

Say "== ports =="
Ensure-PortFree $Port

Say "== CDP =="
Ensure-CdpHealthy $CdpPort
Say "CDP OK"

Say "== run parserservice =="
Set-Location $ServiceDir
$env:PYTHONUNBUFFERED="1"
python -m uvicorn app.main:app --host $BindHost --port $Port --log-level info