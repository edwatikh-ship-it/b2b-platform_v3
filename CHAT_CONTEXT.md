# CHAT_CONTEXT — B2B Platform (single-file context)

## Style / format (MANDATORY)
- Explain like for non-programmer.
- One step at a time: give 1–3 commands, then "Проверка" with expected output.
- No long multi-step plans. No abstractions until needed.
- If something depends on project structure, ask for `tree /f /a backend` or exact file path first.

## SSoT (priority)
1) api-contracts.yaml — ONLY truth for API paths/DTO/statuses.
2) PROJECT-RULES.md — clean/hex architecture rules.
If conflict: api-contracts.yaml > PROJECT-RULES.md.

## Architecture rules (short)
- transport: FastAPI routers + Pydantic DTO only (no business logic)
- usecases: business scenarios
- domain: pure models + rules (no FastAPI/SQLAlchemy)
- adapters: DB/SMTP/HTTP clients
No "dump everything into main.py".

## Local environment
- Windows 11
- repo: D:\b2bplatform
- backend: D:\b2bplatform\backend
- Python 3.12 (venv: backend\.venv)
- Postgres 16, host 127.0.0.1, port 5432
- API base: http://localhost:8000/api/v1

## How to start backend
PowerShell:
cd D:\b2bplatform\backend
.\.venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

## Verified
- GET /api/v1/health -> 200 {"status":"ok"}
- /docs and /openapi.json open

## DB (clean reset done)
- DATABASE_URL in backend/.env:
  postgresql+asyncpg://b2b_user:***@127.0.0.1:5432/b2b_platform
- DB recreated, role b2b_user recreated, privileges granted (public schema CREATE/USAGE).

## Alembic status
- Before alembic on Windows: $env:PYTHONPATH="."
- Created missing template backend/alembic/script.py.mako
- Created baseline revision: backend/alembic/versions/3315ed698ecb_init.py
- Applied: alembic upgrade head
- Verified: SELECT * FROM alembic_version -> 3315ed698ecb

## Goal (next)
Implement next endpoint from api-contracts.yaml. Default: POST /user/requests (manual keys).
