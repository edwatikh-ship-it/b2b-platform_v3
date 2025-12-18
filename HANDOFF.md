# HANDOFF — B2B Platform

Canonical success log (append-only).

## Rules (DoD)
- Log successes here only.
- Each entry must include: datetime (MSK), what changed, verification command + expected output.
- If a step failed or was rolled back: log it in INCIDENTS.md (not here).

## Entries (append-only)

- 2025-12-13 22:40 MSK: Verified backend API is up; health/docs/openapi reachable. Verified: `Invoke-RestMethod http://localhost:8000/api/v1/health` -> 200 and {"status":"ok"}. [file:4]

- 2025-12-13 22:55 MSK: Reset Postgres clean (DB b2b_platform, role b2b_user) and aligned DATABASE_URL to 127.0.0.1. Verified: `psql -U b2b_user -h 127.0.0.1 -d b2b_platform` works; `\dt` shows baseline. [file:4]

- 2025-12-13 23:00 MSK: Fixed Alembic revision generation (added script.py.mako), created baseline migration 3315ed698ecb_init and applied head. Verified: `SELECT * FROM alembic_version;` -> 3315ed698ecb. [file:4]

- 2025-12-13 23:11 MSK: Added DB schema for UserRequests drafts (requests, request_keys) + ORM models. Verified: `alembic current` -> 552d97f8cc92 and `python -c "from app.adapters.db.models import RequestModel, RequestKeyModel; print('models ok')"` -> models ok. [file:4]

- 2025-12-13 23:18 MSK: Implemented DB repository for draft requests creation (RequestRepository). Verified: `python -c "from app.adapters.db.repositories import RequestRepository; print('repo ok')"` -> repo ok. [file:4]

- 2025-12-13 23:19 MSK: Added usecase for POST /user/requests (CreateRequestManualUseCase) with key validation and draft status. Verified: `python -c "from app.usecases.create_request_manual import CreateRequestManualUseCase; print('usecase ok')"` -> usecase ok. [file:4]

- 2025-12-13 23:20–23:24 MSK: Added DTOs + router for POST /api/v1/user/requests and wired into FastAPI app. Verified: `/openapi.json` contains `/api/v1/user/requests` and response schema includes `requestid`. [file:4]

- 2025-12-13 23:25 MSK: End-to-end POST /api/v1/user/requests works (creates DB row, returns draft). Verified: PowerShell POST returns `requestid` and `status="draft"`. [file:4]

- 2025-12-13 23:27–23:28 MSK: Added integration test for create request + pinned test deps (pytest/httpx). Verified: `python -m pytest -q` -> 1 passed. [file:4]

- 2025-12-13 23:37–23:40 MSK: Refactored usecase to depend on domain port (clean architecture), repository implements the port. Verified: tests still pass (`python -m pytest -q` -> 1 passed). [file:4]

- 2025-12-13 23:43–23:45 MSK: Implemented GET /api/v1/user/requests (list) with pagination and verified end-to-end. Verified: `Invoke-RestMethod "http://localhost:8000/api/v1/user/requests?limit=50&offset=0"` returns items. [file:4]

- 2025-12-13 23:49 MSK: Fixed Windows integration tests instability ("Event loop is closed") by disposing async engine on shutdown (FastAPI lifespan). Verified: `python -m pytest -q` -> 2 passed. [file:4]

- 2025-12-13 23:56 MSK: Implemented GET /api/v1/user/requests/{requestId} (RequestDetail) + integration test. Verified: `python -m pytest -q` passes. [file:4]

- 2025-12-14 00:00 MSK: Implemented PUT /api/v1/user/requests/{requestId}/keys + integration tests. Verified: `python -m pytest -q` -> 6 passed. [file:4]

- 2025-12-14 00:01 MSK: Implemented POST /api/v1/user/requests/{requestId}/submit + integration tests. Verified: `python -m pytest -q` passes. [file:4]

- 2025-12-14 00:26 MSK: DB: created attachments table via alembic revision bbff04c57403 (replacing earlier empty migration). Verified: `psql ... -c "\dt"` shows public.attachments. [file:4]

- 2025-12-14 01:35 MSK: Aligned Attachments endpoints and DTOs to SSoT contract (routes + lowercase fields) and updated tests. Verified: `.venv\Scripts\pytest.exe -q -k attachments` -> 2 passed. [file:4]

- 2025-12-14 10:13 MSK: Updated api-contracts.yaml (SSoT) with user personal blacklist by INN endpoints + schemas; YAML validated. Verified: `python -c "import yaml; yaml.safe_load(open('api-contracts.yaml','r',encoding='utf-8')); print('OK')"` -> OK. [file:4]

- 2025-12-14 10:49 MSK: User blacklist routes are visible in runtime OpenAPI (stubs returning 501 at that moment). Verified: request returns 501 and `/openapi.json` contains the paths. [file:4]

- 2025-12-14 12:47–12:48 MSK: Smoke: backend health + openapi reachable; auth policy endpoint exists (401 without token). Verified via Invoke-RestMethod on /apiv1/health and /openapi.json. [file:4]

- 2025-12-14 13:50 MSK: Messaging MVP: added integration tests asserting 501 Not Implemented behavior for messaging endpoints. Verified: `python -m pytest -q -k messaging_not_implemented` -> 4 passed. [file:4]

- 2025-12-14 13:59 MSK: Auth OTP core: added migration (users, otp_codes), created auth OTP usecases/JwtService skeleton, unit tests. Verified: `alembic current` -> a291dc92b69a and `python -m pytest -q -k "auth_otp_usecases or messaging_not_implemented"` -> 6 passed. [file:4]

- 2025-12-14 15:15 MSK: Contract compliance: hid non-SSoT auth endpoints from OpenAPI (`include_in_schema=False`) while keeping behavior. Verified: `python -m pytest -q` passes. [file:4]

- 2025-12-14 16:25 MSK: Implemented recipients replace-all semantics (contract + backend + migration be4136aa1c68) + integration test. Verified: `python -m pytest -q` -> 40 passed. [file:4]

- 2025-12-15 10:21 MSK: Added Suppliers Search router stub per contract (501 Not Implemented). Verified: `/health` ok; `/openapi.json` ok; GET `/apiv1/suppliers/search?q=test` -> 501. [file:4]

- 2025-12-15 10:40 MSK: Implemented Suppliers Search endpoint (temporary behavior returned 200). Verified: `/openapi.json` contains `/apiv1/suppliers/search`; GET works. [file:4]

- 2025-12-15 11:54 MSK: Standardized pagination safety in api-contracts.yaml (maximum: 200 for all limit params) via deterministic script. Verified: script becomes idempotent (no further diffs) and `/openapi.json` reachable. [file:4]

- 2025-12-15 18:49–18:50 MSK: Removed /apiv1 prefix from runtime API routes (API now at root paths like /health) and updated tests/contract checks accordingly. Verified: `python -m pytest -q` -> 39 passed, 1 skipped. [file:4]

- 2025-12-15 19:48 MSK: Hardened PowerShell workflow tooling: tools\pytest.ps1 now restores working directory; added path-safety rules into PROJECT-RULES.md. Verified: `.\\tools\\pytest.ps1` passes and returns to repo root; `git status` clean. [file:4]

- 2025-12-15 23:09 MSK: Git environment verified (repo has .git, branch main tracks origin/main, origin remote set). Verified: `Test-Path .\.git`; `git status`; `git remote -v`. [file:4]

- 2025-12-16 00:30 MSK: Implemented moderator parsing domain-group (“accordion”) results (contract + backend). Verified: `ruff check`, `ruff format --check`, `pre-commit run --all-files`; smoke: `/health` ok; start-parsing + parsing-status work. [file:4]

- 2025-12-16 11:47–11:52 MSK: Preflight verified backend base http://127.0.0.1:8000, API_PREFIX empty; backend + parser_service health ok; CDP 9222 not running (not required for backend health). Verified: `.\\tools\\preflight.ps1`. [file:4]

- 2025-12-16 14:33 MSK: Added CTX-FIRST guardrails + repo-root ctx.ps1 helper for reliable troubleshooting context. Verified: `Set-Location D:\b2bplatform; .\ctx.ps1` and `pre-commit run --all-files` pass. [file:4]

- 2025-12-16 16:45 MSK: Hardened OpenAPI diff tooling (offline file + optional live URL), and validated runtime OpenAPI vs SSoT. Verified: `python .\tools\openapi_diff.py` writes openapi-diff.csv with 0 missing/extra and expected ok count. [file:4]

- 2025-12-16 19:09 MSK: Aligned moderator tasks routes to SSoT (stubs returning 501). Verified: `/openapi.json` contains `/moderatortasks`; GET returns 501. [file:4]

## 2025-12-18 18:45:36 MSK  Stabilized new-chat prompt generator
- Changed: tools/print_new_chat_prompt.ps1 now prints safer copy/paste steps, includes explicit BASE_URL guidance, and uses -Pattern "<anchor>".
- Verification: Ran powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\print_new_chat_prompt.ps1 and confirmed prompt output contains <anchor>.
- Files: tools/print_new_chat_prompt.ps1, INCIDENTS.md, HANDOFF.md.


## 2025-12-18 18:50:45 MSK  New chat prompt stabilized
- Changed: tools/print_new_chat_prompt.ps1 rewritten; now prints -Pattern "<anchor>" and explicit BASE_URL steps.
- Verification: powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\print_new_chat_prompt.ps1 shows <anchor>.
- Files: tools/print_new_chat_prompt.ps1, HANDOFF.md, INCIDENTS.md.

