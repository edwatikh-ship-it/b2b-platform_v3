# ENV — Local development defaults (Win11)

Если этот файл присутствует в репозитории, вопросы про окружение (Python/Postgres/DB stack/port/path/extensions)
повторно НЕ задаём — используем значения отсюда.

## Platform
- OS: Windows 11
- Repo root path (Win11): D:\b2bplatform

## Python
- Python: 3.12 (py -V -> Python 3.12)

## API
- API port: 8000
- API prefix: /api/v1

## Database
- PostgreSQL: 16
- Postgres runtime: local install (Windows 11), not Docker
- DB stack: async SQLAlchemy 2.0 + asyncpg (fixed; sync psycopg2 запрещён для проекта)
- Extensions enabled: pg_trgm, pgvector
- Database name / user / password: stored in backend/.env (not committed), example in backend/.env.example
