param([Parameter(Mandatory)] [string]$Path)
Write-Host "Status: " -ForegroundColor Cyan
try {
    Invoke-RestMethod "http://127.0.0.1:8000=1" -ErrorAction Stop | Out-Null
    Write-Host "  → 200 OK (implemented)" -ForegroundColor Green
} catch {
    $status = $_.Exception.Response.StatusCode
    if ($status -eq 501) {
        Write-Host "  → 501 Not Implemented ✓" -ForegroundColor Yellow
    } else {
        Write-Host "  →  ERROR" -ForegroundColor Red
    }
}
