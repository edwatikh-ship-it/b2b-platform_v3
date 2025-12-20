# SSoT: все эндпоинты из api-contracts.yaml
Get-Content api-contracts.yaml -Raw | 
Select-String '^  /[^:]*:' | 
ForEach-Object { $_.Line.Trim() -replace '^  ', '' } | 
Sort-Object | 
Format-Wide -Column 3
