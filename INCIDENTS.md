# INCIDENTS.md

## Rules (owned here)
- Log problems/failures here (append-only).
- Format: datetime MSK РІР‚вЂќ symptom РІР‚вЂќ root cause РІР‚вЂќ fix/mitigation РІР‚вЂќ verification.
- 1РІР‚вЂњ3 lines per entry, no long stacktraces.

## Entries (append-only)
# INCIDENTS.md РІР‚вЂќ known issues / pitfalls (append-only)

Rule:
- Log important failures/incidents here.
- Format: datetime MSK РІР‚вЂќ symptom РІР‚вЂќ root cause РІР‚вЂќ fix/mitigation РІР‚вЂќ verification.
- 1РІР‚вЂњ3 lines per incident, no long stacktraces.

## Entries (append-only)
- 2025-12-13 23:49 MSK pytest on Windows failed with "Event loop is closed" when hitting Postgres via asyncpg in integration tests РІР‚вЂќ root cause: global SQLAlchemy async engine not disposed on app shutdown РІР‚вЂќ fix: FastAPI lifespan + `await engine.dispose()` in `app/main.py` РІР‚вЂќ verification: `python -m pytest -q` -> `2 passed`.
- 2025-12-13 23:49 MSK pytest on Windows failed with "Event loop is closed" when hitting Postgres via asyncpg РІР‚вЂќ root cause: SQLAlchemy async engine created globally and not disposed on shutdown РІР‚вЂќ fix: FastAPI lifespan + await engine.dispose() РІР‚вЂќ verification: python -m pytest -q => 2 passed.

- 2025-12-13 23:56 MSK RequestDetail implemented with suppliers=[] and normalizedtext=rawtext as placeholder РІР‚вЂќ mitigation: later add supplier matching + normalization РІР‚вЂќ verification: python -m pytest -q => 4 passed.
- 2025-12-14 00:05 MSK FAILED Attachments implementation: pytest collection crashed due to SyntaxError in app/adapters/db/models.py (broken 'from sqlalchemy import' line after patch). Fix: restored import block and converted AttachmentModel to SQLAlchemy 2.0 style; verification: python -c 'from app.adapters.db.models import ...' -> models import ok.
- 2025-12-14 00:05РІР‚вЂњ00:24 MSK INCIDENT: backend/alembic failed due to missing DATABASE_URL in .env and mismatch between expected DB user/db (b2buser/b2bplatform) and actual (b2b_user/b2b_platform); also migration 0dc050e5c206 was applied with empty upgrade(). Fix: wrote DATABASE_URL to .env, aligned DATABASE_URL to b2b_user/b2b_platform, created new migration bbff04c57403 to create attachments table. Verified with alembic current + psql \dt.
- 2025-12-14 00:35РІР‚вЂњ00:36 MSK INCIDENT: pytest failed with unexpected line: '\\ufeff[pytest]' because pytest.ini was written with UTF-8 BOM by PowerShell Set-Content; fix: rewrite pytest.ini as UTF-8 without BOM via .NET UTF8Encoding(false). Verified: pytest -q => 10 passed.
- 2025-12-14 00:05РІР‚вЂњ00:24 MSK INCIDENT: DB/env mismatch and missing DATABASE_URL caused alembic/settings failures; actual role/db were b2b_user/b2b_platform. Fix: added DATABASE_URL to .env pointing to b2b_user/b2b_platform and created migration bbff04c57403 to add attachments table. Verified with alembic current + psql \dt.
- 2025-12-14 00:35РІР‚вЂњ00:36 MSK INCIDENT: pytest failed with unexpected line '\ufeff[pytest]' because pytest.ini was written with UTF-8 BOM; fix: rewrite pytest.ini as UTF-8 without BOM via .NET UTF8Encoding(false). Verified: pytest -q => 10 passed.
- 2025-12-14 00:35РІР‚вЂњ00:36 MSK INCIDENT: pytest.ini written with UTF-8 BOM caused pytest error (unexpected line '\ufeff[pytest]'). Fix: rewrite pytest.ini UTF-8 without BOM via .NET UTF8Encoding(false). Verified: pytest -q => 10 passed.
- 2025-12-14 0016 MSK INCIDENT <symptom>. Root cause: <root_cause>. Fix/mitigation: <fix>. Verification: <command> -> <expected>.
- 2025-12-14 01:23 MSK INCIDENT <symptom> Root cause: <root_cause> Fix/mitigation: <fix_or_mitigation> Verification: <command> -> <expected>
- 2025-12-14 01:35 MSK INCIDENT Attachments API contract mismatch (paths + response field casing) caused 404/KeyError in integration tests РІР‚вЂќ root cause: implementation/tests used '/api/v1/user/attachments' and camelCase DTO aliases (originalFilename), while SSoT requires '/api/v1/userattachments' and lowercase fields (originalfilename) РІР‚вЂќ fix: aligned router prefix to '/userattachments', replaced Attachment DTO aliases to match api-contracts.yaml, updated integration tests to contract paths/fields РІР‚вЂќ verification: .\.venv\Scripts\pytest.exe -q -k attachments -> 2 passed.
- 2025-12-14 10:13 MSK РІР‚вЂќ INCIDENT РІР‚вЂќ api-contracts.yaml patching failed: (1) script looked for .\api-contracts.yaml from backend folder instead of repo root; (2) schemas insertion had broken indentation and made YAML invalid. Fix: rollback to .bak, reapply patcher v3 that inserts under '  schemas:' with correct indentation. Verification: python yaml.safe_load => OK; Select-String finds /user/blacklist/inn and '^  AddUserBlacklistInnRequest:'.


- 2025-12-14 09:49 MSK РїС—Р… INCIDENT РїС—Р… UserMessaging recipients attempt broke backend imports/tests. Root cause: bad alembic revision header (invalid quotes) + wrong SQLAlchemy model style inserted into app/adapters/db/models.py (Column not imported / not 2.0 style) + bad escaping inserted into repositories.py docstring; consequence: alembic upgrade failed, pytest collection failed with ImportError. Fix: removed broken revision db107ba8e332, removed injected recipients model block from models.py, removed injected upsert_recipients block and stale RequestRecipientModel import from repositories.py; verified: .\.venv\Scripts\pytest.exe -q -> 11 passed; python import RequestRepository -> ok.
 - 2025-12-14 10:20вЂ“10:49 MSK вЂ” INCIDENT: backend failed to start (main.py syntax/import errors + domain ports conflict + settings prefix mismatch; plus wrong URL checks). Root cause: text-based patching + Python module/package name collision (domain/ports.py vs domain/ports/) + inconsistent Settings field name/API_PREFIX usage. Fix: rewrite app/main.py to valid state, move UserBlacklist port to non-conflicting module, patch imports, use API_PREFIX=/api/v1 per api-contracts.yaml; verification: uvicorn starts; GET http://localhost:8000/api/v1/user/blacklist/inn -> 501; openapi.json contains /api/v1/user/blacklist/inn and /{inn}.

- 2025-12-14 11:33 MSK INCIDENT Symptom: python -m pytest -q -> No module named pytest. Root cause: system Python used because venv not activated. Fix: cd D:\b2bplatform\backend; .\.venv\Scripts\Activate.ps1. Verification: python -m pytest -q -> 11 passed.
- 2025-12-14 12:29 MSK INCIDENT: Git commands failed with 'fatal: not a git repository' because no .git exists under D:\b2bplatform. Root cause: project folder not under git (not cloned/initialized). Mitigation: decide (A) add proper remote and re-clone, or (B) git init locally and commit snapshot. Verification: Test-Path D:\b2bplatform\.git -> False; git status -> fatal.
- 2025-12-14 12:41 MSK INCIDENT Uvicorn failed to bind on 0.0.0.0:8000 (WinError 10048).
  Symptom: uvicorn app.main:app --port 8000 -> [Errno 10048] only one usage of socket address.
  Root cause: Another process is already listening on TCP 8000.
  Fix/Mitigation: Find PID on :8000 and stop it, or run uvicorn on a free port.
  Verification: netstat shows :8000 free; uvicorn starts; then smoke endpoints respond (health/openapi/authpolicy).
- 2025-12-14 14:01 MSK MSK INCIDENT: HandOff duplicate entry and wrong alembic migration filename (REPLACE_ME_*) created by PowerShell script misuse. Root cause: placeholder path not replaced; WriteAllText created a new file; Messaging MVP entry appended twice. Fix: removed REPLACE_ME migration file, rewrote correct de99d41dff72 migration, kept HANDOFF append-only and documented incident. Verification: alembic current shows de99d41dff72 applied; pg_tables contains user_blacklist_inn.