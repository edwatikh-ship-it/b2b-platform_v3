$ErrorActionPreference = "Stop"

$txt = @"
You are starting work in the B2B Platform repo.

RULES (must follow):
- API contracts: ONLY api-contracts.yaml (repo root).
- Process rules: PROJECT-RULES.md (repo root).
- Docs language: English only. Chat language: Russian is OK.

START (copy/paste):
1) Show project context (always):
   - Set-Location D:\b2bplatform; .\ctx.ps1

2) If you are debugging API/runtime (only if backend is running):
   - Set BASE_URL explicitly (no placeholders):
     - `$BASE_URL = "http://127.0.0.1:8000"
     - `$BASE_URL
   - Fetch OpenAPI:
     - Invoke-RestMethod "`$BASE_URL/openapi.json" | Select-Object -First 5

If you need a specific section from docs (paste text, no file uploads):
- Get-Content -Encoding UTF8 .\PROJECT-RULES.md -Raw
- Select-String -Path .\PROJECT-RULES.md -Pattern "<anchor>" -Context 0,20

Repo change safety (before editing any file):
- git status -sb
- Make a backup under D:\b2bplatform\.tmp\backups\
- After changes: git status -sb + provide rollback command
"@

Write-Host $txt
