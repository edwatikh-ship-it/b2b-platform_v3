# CHAT_CONTEXT — пояснялка (RU, NOT SSoT)

Оригинал: CHAT_CONTEXT.md. Это “технический контекст одним файлом”: стиль общения + минимальные факты по окружению + что проверять первым делом. [NOT SSoT] [file:36]

---

## Зачем он нужен

Чтобы новый чат/новый участник не гадал:
- как давать команды (коротко, 1–3 за раз),
- где репа и какой стек,
- что считается SSoT,
- как стартовать backend и что проверить. [file:36]

---

## Главное правило стиля (MANDATORY)

- Объяснять простым языком.
- Давать 1–3 команды, потом “Проверка” с ожидаемым результатом.
- Не писать простыни и “планы на 20 шагов”. [file:36]

---

## SSoT и архитектура (коротко)

- api-contracts.yaml — единственная правда по API путям/DTO/статусам. [file:36]
- PROJECT-RULES.md — правила чистой архитектуры. [file:36]
- Слои: transport / usecases / domain / adapters, без свалки в main.py. [file:36]

---

## Окружение (что обычно важно помнить)

- Windows 11
- repo: D:\b2bplatform
- backend: D:\b2bplatform\backend
- Python 3.12, venv: backend\.venv
- Postgres 16 (обычно 127.0.0.1:5432)
- API base (пример из контекста): http://localhost:8000/api/v1 [file:36]

---

## Быстрый старт backend + проверки

Старт:
- cd D:\b2bplatform\backend
- .\.venv\Scripts\activate
- uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 [file:36]

Проверки:
- GET /api/v1/health -> 200 {""status"":""ok""}
- /docs и /openapi.json открываются [file:36]

---

## Про миграции (Windows)

Перед alembic на Windows часто нужен PYTHONPATH (чтобы импорты видели пакет app). [file:36]