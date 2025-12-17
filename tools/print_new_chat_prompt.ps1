$ErrorActionPreference = "Stop"

$txt = @"
You are starting work in the B2B Platform repo.

HARD RULES / GATES (must follow):
1) SSoT:
- API contracts = ONLY api-contracts.yaml (repo root).
- If runtime/implementation differs from api-contracts.yaml => treat as a bug; align code to contract (or change contract intentionally).
- Priority: api-contracts.yaml -> PROJECT-RULES.md -> PROJECT-DOC.md.
- SSoT files must be in repo root D:\b2bplatform (no duplicates in backend\).
- Progress = state of GitHub main branch, not chat memory.

2) Before asking to change any code:
Ask the user to DRAG&DROP these files into this chat:
- api-contracts.yaml
- PROJECT-RULES.md
- PROJECT-DOC.md (if present)
- PROJECT-TREE.txt
- HANDOFF.md
- INCIDENTS.md
- DECISIONS.md

3) PRE-FLIGHT / FACTS (no guessing defaults):
Ask user to run and paste outputs (as text):
A) PowerShell: Set-Location D:\b2bplatform; .\ctx.ps1
B) Confirm BASE_URL and API_PREFIX for the running backend (do not assume).
C) Run checks (use confirmed BASE_URL/API_PREFIX):
   - Invoke-RestMethod "{BASE_URL}/{API_PREFIX}/health"
   - Invoke-RestMethod "{BASE_URL}/openapi.json" | Out-Null
D) DB env check (do not require secret value):
   - python -c "import os; print(os.getenv('DATABASEURL'), os.getenv('DATABASE_URL'))"
If something fails => provide Plan B commands to start backend / set env, then retry checks.

4) Repo changes safety (mandatory):
Before any repo modification, always:
- Verify D:\b2bplatform exists + api-contracts.yaml exists.
- Backups and temporary files MUST go under D:\b2bplatform\.tmp\ (do not clutter repo root):
  - Backups: D:\b2bplatform\.tmp\backups\
  - Temp:    D:\b2bplatform\.tmp\tmp\
- Backup naming: {original_filename}.bak.{timestamp}
- Show git status before and after.
- Provide rollback commands (restore from .bak and/or git restore).
- Write text files as UTF-8 without BOM.

5) Patch safety (STOP-ON-MISMATCH):
- Prefer deterministic patches over whole-file rewrites (PowerShell BOM/encoding risk).
- Any patch must verify anchors exist; if anchor not found => STOP and request a fresh file snapshot.

Working style:
- If you find a discrepancy or ambiguous rule, ask ONE short clarifying question.
- After clarification, propose a deterministic patch that updates SSoT docs first (api-contracts.yaml / PROJECT-RULES.md / PROJECT-DOC.md) and then code.
- Avoid long explanations; prefer concrete commands + expected outputs.
"@

Write-Host $txt