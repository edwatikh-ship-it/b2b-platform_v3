param(
  [Parameter(Mandatory=$true)]
  [ValidateSet("INCIDENTS","HANDOFF")]
  [string]$Target,

  [Parameter(Mandatory=$true, ValueFromRemainingArguments=$true)]
  [string[]]$Lines,

  [switch]$WithTimestamp,

  [switch]$DryRun
)

$repoRoot = "D:\b2bplatform"
$handoffPath   = Join-Path $repoRoot "HANDOFF.md"
$incidentsPath = Join-Path $repoRoot "INCIDENTS.md"

if (!(Test-Path $handoffPath))   { throw "HANDOFF not found: $handoffPath" }
if (!(Test-Path $incidentsPath)) { throw "INCIDENTS not found: $incidentsPath" }

$targetPath = if ($Target -eq "HANDOFF") { $handoffPath } else { $incidentsPath }

$utf8NoBom = New-Object System.Text.UTF8Encoding($false)

$prefix = ""
if ($WithTimestamp) {
  $dt = [TimeZoneInfo]::ConvertTimeBySystemTimeZoneId([DateTime]::UtcNow, "Russian Standard Time")
  $ts = $dt.ToString("yyyy-MM-dd HH:mm 'MSK'")
  $prefix = "- " + $ts + ": "
}

$normalized = @()
foreach ($line in $Lines) {
  if ($null -eq $line) { continue }
  $normalized += $line
}

if ($normalized.Count -eq 0) { throw "No lines to append." }

$body = ""
if ($WithTimestamp) {
  $body = "`r`n" + $prefix + ($normalized -join "`r`n")
} else {
  $body = "`r`n" + ($normalized -join "`r`n")
}

if ($DryRun) {
  Write-Host "DRY-RUN target: $targetPath"
  Write-Host $body
  exit 0
}

$existingBytes = [System.IO.File]::ReadAllBytes($targetPath)
$entryBytes    = $utf8NoBom.GetBytes($body)
[System.IO.File]::WriteAllBytes($targetPath, $existingBytes + $entryBytes)

Write-Host "Appended OK: $targetPath"