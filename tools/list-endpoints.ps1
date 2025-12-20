# tools/list-endpoints.ps1
Get-Content api-contracts.yaml -Raw | Select-String '^  /[^:]*:' | ForEach-Object { $_.Line.Trim() } | Sort-Object
