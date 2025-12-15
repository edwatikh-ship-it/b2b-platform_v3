# INCIDENTS — B2B Platform

## Rules (owned here)
- Log problems/failures here (append-only).
- Format per entry:
  - datetime MSK
  - symptom
  - root cause
  - fix/mitigation
  - verification (command + expected output)
- Keep it short (1–3 lines per incident). Do not paste long stacktraces.

## Entries (append-only)

## Entries (append-only)
# INCIDENTS.md Р Р†Р вЂљРІР‚Сњ known issues / pitfalls (append-only)

Rule:
- Log important failures/incidents here.
- Format: datetime MSK Р Р†Р вЂљРІР‚Сњ symptom Р Р†Р вЂљРІР‚Сњ root cause Р Р†Р вЂљРІР‚Сњ fix/mitigation Р Р†Р вЂљРІР‚Сњ verification.
- 1Р Р†Р вЂљРІР‚Сљ3 lines per incident, no long stacktraces.

## Entries (append-only)
- 2025-12-13 23:49 MSK pytest on Windows failed with "Event loop is closed" when hitting Postgres via asyncpg in integration tests Р Р†Р вЂљРІР‚Сњ root cause: global SQLAlchemy async engine not disposed on app shutdown Р Р†Р вЂљРІР‚Сњ fix: FastAPI lifespan + `await engine.dispose()` in `app/main.py` Р Р†Р вЂљРІР‚Сњ verification: `python -m pytest -q` -> `2 passed`.
- 2025-12-13 23:49 MSK pytest on Windows failed with "Event loop is closed" when hitting Postgres via asyncpg Р Р†Р вЂљРІР‚Сњ root cause: SQLAlchemy async engine created globally and not disposed on shutdown Р Р†Р вЂљРІР‚Сњ fix: FastAPI lifespan + await engine.dispose() Р Р†Р вЂљРІР‚Сњ verification: python -m pytest -q => 2 passed.

- 2025-12-13 23:56 MSK RequestDetail implemented with suppliers=[] and normalizedtext=rawtext as placeholder Р Р†Р вЂљРІР‚Сњ mitigation: later add supplier matching + normalization Р Р†Р вЂљРІР‚Сњ verification: python -m pytest -q => 4 passed.
- 2025-12-14 00:05 MSK FAILED Attachments implementation: pytest collection crashed due to SyntaxError in app/adapters/db/models.py (broken 'from sqlalchemy import' line after patch). Fix: restored import block and converted AttachmentModel to SQLAlchemy 2.0 style; verification: python -c 'from app.adapters.db.models import ...' -> models import ok.
- 2025-12-14 00:05Р Р†Р вЂљРІР‚Сљ00:24 MSK INCIDENT: backend/alembic failed due to missing DATABASE_URL in .env and mismatch between expected DB user/db (b2buser/b2bplatform) and actual (b2b_user/b2b_platform); also migration 0dc050e5c206 was applied with empty upgrade(). Fix: wrote DATABASE_URL to .env, aligned DATABASE_URL to b2b_user/b2b_platform, created new migration bbff04c57403 to create attachments table. Verified with alembic current + psql \dt.
- 2025-12-14 00:35Р Р†Р вЂљРІР‚Сљ00:36 MSK INCIDENT: pytest failed with unexpected line: '\\ufeff[pytest]' because pytest.ini was written with UTF-8 BOM by PowerShell Set-Content; fix: rewrite pytest.ini as UTF-8 without BOM via .NET UTF8Encoding(false). Verified: pytest -q => 10 passed.
- 2025-12-14 00:05Р Р†Р вЂљРІР‚Сљ00:24 MSK INCIDENT: DB/env mismatch and missing DATABASE_URL caused alembic/settings failures; actual role/db were b2b_user/b2b_platform. Fix: added DATABASE_URL to .env pointing to b2b_user/b2b_platform and created migration bbff04c57403 to add attachments table. Verified with alembic current + psql \dt.
- 2025-12-14 00:35Р Р†Р вЂљРІР‚Сљ00:36 MSK INCIDENT: pytest failed with unexpected line '\ufeff[pytest]' because pytest.ini was written with UTF-8 BOM; fix: rewrite pytest.ini as UTF-8 without BOM via .NET UTF8Encoding(false). Verified: pytest -q => 10 passed.
- 2025-12-14 00:35Р Р†Р вЂљРІР‚Сљ00:36 MSK INCIDENT: pytest.ini written with UTF-8 BOM caused pytest error (unexpected line '\ufeff[pytest]'). Fix: rewrite pytest.ini UTF-8 without BOM via .NET UTF8Encoding(false). Verified: pytest -q => 10 passed.
- 2025-12-14 0016 MSK INCIDENT <symptom>. Root cause: <root_cause>. Fix/mitigation: <fix>. Verification: <command> -> <expected>.
- 2025-12-14 01:23 MSK INCIDENT <symptom> Root cause: <root_cause> Fix/mitigation: <fix_or_mitigation> Verification: <command> -> <expected>
- 2025-12-14 01:35 MSK INCIDENT Attachments API contract mismatch (paths + response field casing) caused 404/KeyError in integration tests Р Р†Р вЂљРІР‚Сњ root cause: implementation/tests used '/api/v1/user/attachments' and camelCase DTO aliases (originalFilename), while SSoT requires '/api/v1/userattachments' and lowercase fields (originalfilename) Р Р†Р вЂљРІР‚Сњ fix: aligned router prefix to '/userattachments', replaced Attachment DTO aliases to match api-contracts.yaml, updated integration tests to contract paths/fields Р Р†Р вЂљРІР‚Сњ verification: .\.venv\Scripts\pytest.exe -q -k attachments -> 2 passed.
- 2025-12-14 10:13 MSK Р Р†Р вЂљРІР‚Сњ INCIDENT Р Р†Р вЂљРІР‚Сњ api-contracts.yaml patching failed: (1) script looked for .\api-contracts.yaml from backend folder instead of repo root; (2) schemas insertion had broken indentation and made YAML invalid. Fix: rollback to .bak, reapply patcher v3 that inserts under '  schemas:' with correct indentation. Verification: python yaml.safe_load => OK; Select-String finds /user/blacklist/inn and '^  AddUserBlacklistInnRequest:'.


- 2025-12-14 09:49 MSK Р С—РЎвЂ”Р вЂ¦ INCIDENT Р С—РЎвЂ”Р вЂ¦ UserMessaging recipients attempt broke backend imports/tests. Root cause: bad alembic revision header (invalid quotes) + wrong SQLAlchemy model style inserted into app/adapters/db/models.py (Column not imported / not 2.0 style) + bad escaping inserted into repositories.py docstring; consequence: alembic upgrade failed, pytest collection failed with ImportError. Fix: removed broken revision db107ba8e332, removed injected recipients model block from models.py, removed injected upsert_recipients block and stale RequestRecipientModel import from repositories.py; verified: .\.venv\Scripts\pytest.exe -q -> 11 passed; python import RequestRepository -> ok.
 - 2025-12-14 10:20РІР‚вЂњ10:49 MSK РІР‚вЂќ INCIDENT: backend failed to start (main.py syntax/import errors + domain ports conflict + settings prefix mismatch; plus wrong URL checks). Root cause: text-based patching + Python module/package name collision (domain/ports.py vs domain/ports/) + inconsistent Settings field name/API_PREFIX usage. Fix: rewrite app/main.py to valid state, move UserBlacklist port to non-conflicting module, patch imports, use API_PREFIX=/api/v1 per api-contracts.yaml; verification: uvicorn starts; GET http://localhost:8000/api/v1/user/blacklist/inn -> 501; openapi.json contains /api/v1/user/blacklist/inn and /{inn}.

- 2025-12-14 11:33 MSK INCIDENT Symptom: python -m pytest -q -> No module named pytest. Root cause: system Python used because venv not activated. Fix: cd D:\b2bplatform\backend; .\.venv\Scripts\Activate.ps1. Verification: python -m pytest -q -> 11 passed.
- 2025-12-14 12:29 MSK INCIDENT: Git commands failed with 'fatal: not a git repository' because no .git exists under D:\b2bplatform. Root cause: project folder not under git (not cloned/initialized). Mitigation: decide (A) add proper remote and re-clone, or (B) git init locally and commit snapshot. Verification: Test-Path D:\b2bplatform\.git -> False; git status -> fatal.
- 2025-12-14 12:41 MSK INCIDENT Uvicorn failed to bind on 0.0.0.0:8000 (WinError 10048).
  Symptom: uvicorn app.main:app --port 8000 -> [Errno 10048] only one usage of socket address.
  Root cause: Another process is already listening on TCP 8000.
  Fix/Mitigation: Find PID on :8000 and stop it, or run uvicorn on a free port.
  Verification: netstat shows :8000 free; uvicorn starts; then smoke endpoints respond (health/openapi/authpolicy).
- 2025-12-14 14:01 MSK MSK INCIDENT: HandOff duplicate entry and wrong alembic migration filename (REPLACE_ME_*) created by PowerShell script misuse. Root cause: placeholder path not replaced; WriteAllText created a new file; Messaging MVP entry appended twice. Fix: removed REPLACE_ME migration file, rewrote correct de99d41dff72 migration, kept HANDOFF append-only and documented incident. Verification: alembic current shows de99d41dff72 applied; pg_tables contains user_blacklist_inn.
- 2025-12-14 16:25 MSK: INCIDENT request_recipients inserts failed with NOT NULL violation (created_at/updated_at were NULL). Root cause: Alembic revision fbb98b9e9fc9 was created/applied with empty upgrade() (pass), so DB schema/defaults were not guaranteed; table/defaults were repaired manually to unblock. Fix: created request_recipients table via backend/tools/ensure_request_recipients_table.py, set DEFAULT now() + backfilled NULLs via backend/tools/fix_request_recipients_defaults.py, and added Alembic migration be4136aa1c68_request_recipients_defaults.py to make defaults/backfill repeatable. Verification: cd D:\b2bplatform\backend; alembic current -> be4136aa1c68 (head); python -m pytest -q -> 40 passed.- 2025-12-14 17:01 MSK INCIDENT: Port 8000 stuck on Windows (uvicorn bind fails with WinError 10048). Symptom: netstat/Get-NetTCPConnection shows LISTEN on 0.0.0.0:8000 with PID, but tasklist/taskkill cannot find PID (phantom), so port cannot be freed normally. Mitigation: run backend on port 8002; if 8000 required then run admin 'netsh winsock reset' + 'netsh int ip reset' and reboot. Verification: http://localhost:8002/docs -> 200; http://localhost:8002/apiv1/health -> status ok.
- 2025-12-14 17:01 MSK INCIDENT: pytest from repo root failed with ModuleNotFoundError: no module named 'app'. Root cause: missing PYTHONPATH when running from D:\b2bplatform. Fix: run tests from D:\b2bplatform\backend OR set $env:PYTHONPATH to backend path. Verification: cd D:\b2bplatform\backend; .\.venv\Scripts\python.exe -m pytest -q -> 40 passed.
- 2025-12-15 10:46 MSK INCIDENT PRE-FLIGHT checks failed with invalid URI when BASE_URL was set to placeholder 'http://<host>:<port>'. Root cause: placeholder values were not replaced; PowerShell Uri parsing fails before making HTTP request. Fix/Mitigation: use real BASE_URL (e.g. http://127.0.0.1:8000) and APIPREFIX=apiv1. Verification: Invoke-RestMethod http://127.0.0.1:8000/apiv1/health -> status ok; openapi.json reachable.

- 2025-12-15 10:46 MSK INCIDENT Attempted to run 'python - << PY' (bash heredoc) in Windows PowerShell causing parser errors and mixed Python/PS commands. Root cause: heredoc syntax is not supported in PowerShell. Fix/Mitigation: use 'python -c "...";' or write a temporary .py file then run 'python script.py'. Verification: python script.py exits 0 and changes are applied.

- 2025-12-15 10:46 MSK INCIDENT Contract patching via regex failed: could not locate supplierssearch block and also Regex.Replace overload was misused (RegexOptions passed where matchTimeout is expected). Root cause: api-contracts.yaml formatting differs (lots of blank lines / schema: {} patterns), and .NET Regex.Replace signature requires RegexOptions in constructor or different overload. Fix/Mitigation: either do deterministic line-based patching (Select-String anchors + manual edit) or use a YAML-aware tool/script; when using .NET regex, instantiate [regex]::new(pattern, [RegexOptions]::Singleline). Verification: Select-String finds patched  in supplierssearch response schema and openapi.json shows expected response schema reference.

- 2025-12-15 10:46 MSK NOTE PowerShell table output can display empty JSON arrays/objects confusingly (e.g. items shown as {}). Mitigation: validate response with 'Invoke-RestMethod ... | ConvertTo-Json -Depth 10'. Verification: JSON output matches expected structure.
- 2025-12-15 10:47 MSK INCIDENT Dev tooling missing on Windows shell: 'pyclean', 'uv', 'direnv' commands not recognized; only ruff/pre-commit/just were available. Root cause: tools not installed or not on PATH in current environment. Fix/Mitigation: use Plan B commands:
  - pyclean Plan B: remove __pycache__ via PowerShell (Get-ChildItem -Recurse -Directory -Filter __pycache__ | Remove-Item -Recurse -Force).
  - uv Plan B: use existing .venv + pip (python -m pip install ...) or standard venv bootstrap (python -m venv .venv).
  - direnv Plan B: set env vars explicitly in the same shell before running uvicorn/tests.
Verification: 'ruff check backend', 'ruff format backend', 'pre-commit run --all-files' succeed in current shell.
- 2025-12-15 10:48 MSK INCIDENT PRE-FLIGHT checks failed with invalid URI when BASE_URL was left as placeholder 'http://<host>:<port>'. Root cause: placeholder values not replaced; PowerShell Uri parsing fails. Fix/Mitigation: use real BASE_URL (http://127.0.0.1:8000) and APIPREFIX=apiv1. Verification: GET /apiv1/health -> status ok; GET /openapi.json -> 200.

- 2025-12-15 10:48 MSK INCIDENT Used bash heredoc syntax ('python - << PY') in Windows PowerShell which is not supported. Root cause: shell mismatch (bash vs PowerShell). Fix/Mitigation: run python via -c or create a .py file and execute it. Verification: python script.py exits 0 and changes applied.

- 2025-12-15 10:48 MSK INCIDENT Regex-based patching of api-contracts.yaml was fragile: pattern did not match actual file layout; additional mistake: called [regex]::Replace with RegexOptions in the overload position reserved for matchTimeout. Root cause: yaml uses many blank lines and schema: {} patterns; wrong .NET Regex overload. Fix/Mitigation: prefer deterministic, anchor-based PowerShell patching (Select-String + controlled replacement) or a YAML-aware script; when using .NET regex, instantiate [regex]::new(pattern, [RegexOptions]::Singleline). Verification: Select-String finds patched \ in api-contracts.yaml and openapi.json shows response schema reference.

- 2025-12-15 10:48 MSK INCIDENT Dev tooling missing in environment: 'pyclean', 'uv', 'direnv' commands not recognized (not installed or not on PATH). Fix/Mitigation: Plan B:
  - pyclean: delete __pycache__ via PowerShell.
  - uv: use existing .venv + pip / python -m venv.
  - direnv: set env vars explicitly in the same shell before running uvicorn/tests.
Verification: ruff + pre-commit available and pass ('ruff check', 'ruff format', 'pre-commit run --all-files').

- 2025-12-15 11:12 MSK INCIDENT PROJECT-RULES.md appears with broken encoding (garbled Cyrillic) when read in PowerShell. Root cause: file is not UTF-8 (or got corrupted by previous writes). Fix/Mitigation: do not append to PROJECT-RULES.md until encoding is normalized; prefer rewriting file as UTF-8 without BOM from a verified clean source. Verification: Get-Content shows readable Russian text and repo diff contains only intended doc changes.

- 2025-12-15 11:12 MSK INCIDENT PowerShell SSoT patching pitfalls: $ref inside strings caused parser error (PowerShell treated $ref as variable), and [regex]::Replace was called with RegexOptions which bound to matchTimeout overload and failed. Root cause: PowerShell variable interpolation + .NET Regex overload ambiguity. Fix/Mitigation: escape $ref as ` $ref `; create regex via New-Object Regex(pattern, [RegexOptions]::Singleline) and call .Replace(); prefer deterministic anchor-based patches or reusable tools/ scripts. Verification: patch runs without errors; git status shows expected files only; openapi.json loads 200.


- 2025-12-15 11:15 MSK INCIDENT PROJECT-RULES.md is stored in a broken/garbled encoding in git (git show and Get-Content display unreadable Cyrillic). Root cause: file encoding mismatch/corruption in repo history. Fix/Mitigation: avoid relying on this file until normalized; add new rules in readable ASCII/English block; plan separate milestone to rewrite PROJECT-RULES.md as UTF-8 without BOM from a verified source. Verification: after normalization, first lines are readable and diffs are intentional.

- 2025-12-15 11:15 MSK INCIDENT PowerShell SSoT patching pitfalls: $ref inside strings caused parser error (PowerShell treated $ref as variable), and [regex]::Replace was called with RegexOptions which bound to matchTimeout overload and failed. Root cause: PowerShell variable interpolation + .NET Regex overload ambiguity. Fix/Mitigation: escape $ref as ` $ref `; create regex via New-Object Regex(pattern, [RegexOptions]::Singleline) and call .Replace(); prefer deterministic anchor-based patches or reusable tools/ scripts. Verification: patch runs without errors; git status shows expected files only; openapi.json loads 200.


- 2025-12-15 18:26 MSK INCIDENT: OpenAPI diff script crashed in PowerShell with ParserError on '??'/'?.' and produced empty openapi-diff.csv (3 bytes) | root cause: used C# null-coalescing/safe-navigation operators not supported by PowerShell | fix: rewrote script without '??'/'?.' | verification: openapi-diff.csv = 11238 bytes and Group-Object (status, group) returns counts.
- 2025-12-15 18:26 MSK INCIDENT: OpenAPI diff script crashed in PowerShell with ParserError on '??'/'?.' and produced empty openapi-diff.csv (3 bytes) | root cause: used C# null-coalescing/safe-navigation operators not supported by PowerShell | fix: rewrote script without '??'/'?.' | verification: openapi-diff.csv = 11238 bytes and Group-Object (status, group) returns counts.
- 2025-12-15 19:29 MSK INCIDENT PowerShell $env:$name syntax error when loading backend.env. Root cause invalid dynamic env var assignment. Fix use Set-Item -Path "Env:${k}" -Value $v. Verification DATABASEURL loaded postgresql+asyncpg://... python -c "import os; print(os.getenv('DATABASEURL'))"
