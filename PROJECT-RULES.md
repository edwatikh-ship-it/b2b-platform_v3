# B2B Platform — PROJECT RULES (SSoT)

Version: 1.3
Date: 2025-12-15

## 1) SSoT (Single Source of Truth)
- API (endpoints, DTOs, responses) = ONLY api-contracts.yaml at repo root: D:\b2bplatform\api-contracts.yaml.
- If implementation and contract diverge — it's an error. Align code to contract (or change contract intentionally).
- Priority: api-contracts.yaml → PROJECT-RULES.md → PROJECT-DOC.md.
- SSoT files must live in repo root D:\b2bplatform\ (no duplicates inside backend\).
- Progress = state of GitHub main branch, not chat memory.

## 2) Architecture (fixed)
transport → usecases → domain → adapters

Short meaning:
- transport: HTTP routes + input/output validation; no business decisions.
- usecases: business scenarios.
- domain: pure models/rules (no FastAPI/SQLAlchemy).
- adapters: DB/SMTP/HTTP clients and other integrations.

## 3) SAFETY GUARDS (mandatory before any repo changes)
Before any change:
- Verify D:\b2bplatform\ exists and api-contracts.yaml is present.
- Backup every changed file: *.bak.<timestamp>.
- Show git status before and after.
- Provide rollback: restore from .bak and/or git restore.

## 4) PRE-FLIGHT before any “fix routes/endpoints”
Do NOT guess defaults.

First discover:
- BASE_URL (host:port) and API_PREFIX (e.g. apiv1).
  - Plan A: read from runtime env / start config.
  - Plan B: ask user explicitly.

Run checks (expected results):
1) Invoke-RestMethod "{BASE_URL}/{API_PREFIX}/health"
   - Expect JSON with status = "ok" (or contract equivalent).
2) Invoke-RestMethod "{BASE_URL}/openapi.json" | Out-Null
   - Expect 200 and valid JSON.
3) python -c "import os; print(os.getenv('DATABASEURL'), os.getenv('DATABASE_URL'))"
   - Must be non-None only if routes/import-time DB requires it.

If any check fails — provide Plan B commands first (how to start backend / set env), then propose code changes.

## 5) “6 tools” standard (check availability first)
Tools: ruff, pre-commit, pyclean, uv, direnv, just.

Rule:
- Always check first: Get-Command ruff/pre-commit/pyclean/uv/direnv/just
- If missing — use Plan B (no assumptions).

Usage:
- Lint/format:
  - ruff check backend
  - ruff format backend
  - (CI: ruff check + ruff format --check)
- Hooks:
  - pre-commit run --all-files
- Routine commands:
  - just fmt / just test / just dev / just clean (if present)
- Cleanup:
  - pyclean . (if present)
  - Plan B: remove __pycache__ via PowerShell
- Dependencies:
  - prefer uv
  - Plan B: python -m venv + pip install
- Env:
  - prefer direnv
  - Plan B: set env vars explicitly in the same shell session

## 6) Windows / PowerShell pitfalls
- Do not use bash heredoc in PowerShell (e.g. python - << PY).
- PowerShell: $ref inside strings must be escaped as ` $ref ` (otherwise treated as a variable).
- .NET Regex in PowerShell:
  - avoid [regex]::Replace with RegexOptions (can bind to matchTimeout overload),
  - correct: New-Object Regex(pattern, [RegexOptions]::Singleline) then .Replace().
- Text file writes: UTF-8 without BOM (unless strong reason). Prefer .NET WriteAllText with UTF8Encoding(false).

## 7) Progress logging (mandatory)
- Success → HANDOFF.md (append-only) + update PROJECT-TREE.txt + commit + push origin/main.
- Failure → INCIDENTS.md (append-only) + commit + push.

HANDOFF/INCIDENTS format:
- Datetime (MSK)
- What happened / what was done
- Root cause
- Fix/Mitigation
- Verification (command + expected output)

### Chat safety: Step 0 / Question gate (2025-12-15)
- Step 0 for any new chat: run “Detect backend + PRE-FLIGHT” PowerShell script to discover BASE_URL and verify /{API_PREFIX}/health + /openapi.json.
- Do NOT assume BASE_URL / API_PREFIX. Use detection or explicit user confirmation.
- Default: never auto-kill processes. Provide a separate explicit command to stop a PID if needed.
- Question gate: if a critical question is asked (BASE_URL/API_PREFIX/DATABASEURL/etc) and no answer is given, do not proceed; repeat the question in one short line and wait.
- Goal: minimize wasted time on wrong port/env/shell.

### Env: DATABASEURL source (2025-12-15)
- DATABASEURL must be stored in D:\b2bplatform\backend.env (local-only, do not commit).
- Before uvicorn/alembic, ensure this shell loads backend.env (or explicitly exports DATABASEURL).
- Verify: python -c "import os; print(os.getenv('DATABASEURL'), os.getenv('DATABASE_URL'))" must not show None None.

### Alembic on Windows: always set PYTHONPATH (2025-12-15)
- Before alembic on Windows set: ="D:\b2bplatform\backend"
- Verify: cd D:\b2bplatform\backend; alembic current runs and prints current revision.

## 8) Language policy (SSoT docs)
- Source language for SSoT docs is English (ASCII preferred for maximum compatibility).
- Do NOT maintain mandatory RU+EN duplicates for every update (avoids double work and noisy logs).
- Russian docs live under docs-ru/ as NOT SSoT explanations only.
- For append-only logs (HANDOFF.md / INCIDENTS.md / DECISIONS.md): one entry = one language, no required translation; keep the required structure and verification commands.
## PowerShell path safety (mandatory)

- Always anchor scripts to repo root (use Set-Location D:\b2bplatform or $PSScriptRoot + Join-Path), never rely on current working directory.
- Do not use Resolve-Path for a file that does not exist yet; write using a direct path (Join-Path) or create the file first.
- Any script that changes directory must restore it (Push-Location + Pop-Location in inally) to avoid breaking subsequent commands.


### Runtime base URL & port rules (2025-12-15)
- Never assume API prefix. Always discover it from the running OpenAPI: GET {BASE_URL}/openapi.json.
- If OpenAPI paths start with '/apiv1', use '{BASE_URL}/apiv1/...' (example: /apiv1/health).
- If OpenAPI paths do NOT start with '/apiv1' (paths like '/health', '/user/...', '/moderator/...'), then API_PREFIX is empty and health is '{BASE_URL}/health'.
- Always validate the chosen base before changing code: request the exact health endpoint that exists in OpenAPI.

### Port hygiene / avoiding \"wrong port\" (2025-12-15)
- Always check ports before starting services:
  - Backend default: 8000
  - Parser service default: 9001
  - Chrome CDP default: 9222

### Parser service preflight (mandatory)
- If Moderator parsing endpoints are used (/moderator/requests/{requestId}/start-parsing):
  - Ensure parser_service is running and reachable BEFORE debugging backend logic.
  - Symptom: parsing-status shows status=failed with error "All connection attempts failed" for keys.
  - Fix: start parser_service (default http://127.0.0.1:9001) and re-run start-parsing.

PowerShell checks:
- Plan A (if available): Get-NetTCPConnection -LocalPort 9001 -State Listen
- Plan B (Windows-safe): netstat -ano | findstr ":9001"
- HTTP ping (404 is OK; connection refused is NOT OK):
  - try { Invoke-WebRequest "http://127.0.0.1:9001/" -UseBasicParsing -TimeoutSec 2 | Select-Object StatusCode } catch { $_.Exception.Message }

Start command (run in a separate shell):
- Set-Location D:\b2bplatform\parser_service
- python -m uvicorn app.main:app --host 127.0.0.1 --port 9001
- PowerShell checks:
  - Get-NetTCPConnection -LocalPort 8000 -State Listen
  - Get-NetTCPConnection -LocalPort 9001 -State Listen
  - Get-NetTCPConnection -LocalPort 9222 -State Listen
- If a port is occupied, do NOT guess. Identify owning PID and command line, then stop explicitly:
  - \8424 = (Get-NetTCPConnection -LocalPort 8000 -State Listen | Select-Object -First 1).OwningProcess
  - Get-CimInstance Win32_Process -Filter \"ProcessId=\8424\" | Select-Object ProcessId, Name, CommandLine
  - Stop-Process -Id \8424 -Force
- Always run backend and parser_service in separate shells and stop them via Ctrl+C when done.

<!-- PRE-FLIGHT-RULE-BEGIN -->
## Mandatory preflight (START HERE)

- Before any work (dev/debug) and before any commit: run .\tools\preflight.ps1 from D:\b2bplatform.
- If preflight fails: fix environment/services first (follow the script hints). Do not commit/push while failing.
- Only push to main after preflight passes in the current session.
<!-- PRE-FLIGHT-RULE-END -->

Preflight example (Windows PowerShell):
- Set-Location D:\b2bplatform
- .\tools\preflight.ps1 -BackendBaseUrl "http://127.0.0.1:8000"

Interpretation rule:
- If preflight says Detected API_PREFIX is empty and health path is /health, then use BASE_URL + /health and other root paths (no /apiv1).
- If preflight says API_PREFIX is "apiv1", then use BASE_URL + /apiv1/health, etc.
