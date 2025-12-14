# B2B Platform — Жёсткие правила разработки

**Версия:** 1.0  
**Дата:** 13.12.2025  
**Статус:** КОНСТИТУЦИЯ (не менять без согласования)

---

## 1. Single Source of Truth (SSoT)

### Правило: API контракты — в `api-contracts.yaml`, только в нём

- **Все HTTP пути** (`/api/v1/*`) описаны в `api-contracts.yaml` (OpenAPI 3.0).
- **Все схемы запросов/ответов** фиксируются в YAML перед тем, как писать код.
- **Любое изменение API** (новый параметр, новый статус, новое поле) → сначала в YAML, потом в коде.
- **При противоречии между кодом и YAML:** YAML всегда прав; код — баг.

**Следствие:** Если переезжаем с FastAPI на Node, контракт не меняется. Меняется только реализация.

---

## 2. Архитектура (Clean + Hexagonal упрощённо)

### Обязательные слои

```
backend/
  app/
    main.py                    # Только wiring и подключение роутеров
    config.py                  # Конфигурация (только env)
    
    transport/
      routers/                 # FastAPI роуты (путь, параметры, Pydantic DTO)
        __init__.py
        requests.py
        suppliers.py
        moderator.py
      schemas/                 # Pydantic DTO (вход/выход по API)
        __init__.py
        request_schemas.py
        supplier_schemas.py
      errors.py                # ErrorResponse, HTTPException helpers
      auth.py                  # JWT, зависимости для роутов
    
    usecases/                  # Бизнес-логика (сценарии)
      __init__.py
      create_request.py        # CreateRequestUseCase
      submit_request.py
      search_suppliers.py
      send_email.py
      (и т.д.)
    
    domain/                    # Модели, правила, типы (БЕЗ фреймворка)
      __init__.py
      models.py                # @dataclass Request, Supplier, Key, etc
      errors.py                # DomainError, ValidationError
      rules.py                 # Бизнес-правила (e.g., is_valid_supplier, PDF_MAX_PAGES)
    
    adapters/                  # Интеграции (БД, почта, внешние API)
      db/
        __init__.py
        models.py              # SQLAlchemy модели (ТОЛЬКО здесь)
        repositories.py        # RequestRepository, SupplierRepository
        session.py             # get_db(), SessionLocal
      smtp/
        __init__.py
        client.py              # SMTP отправка
      imap/
        __init__.py
        client.py              # IMAP приём
      checko/
        __init__.py
        client.py              # Интеграция с Checko API
      storage/
        __init__.py
        file_storage.py        # Загрузка файлов
    
    shared/                    # Общие утилиты
      logger.py
      utils.py
      constants.py

  tests/
    unit/                      # domain + usecases (без БД)
    integration/               # с адаптерами (БД, SMTP)
    contract/                  # Проверка соответствия api-contracts.yaml

  requirements.txt
  .env.example
  alembic/                     # Миграции
    versions/
```

### Правила слоёв

1. **`transport`** (тонкий):
   - Только парсит HTTP request → DTO (Pydantic).
   - Только вызывает usecase.
   - Только возвращает HTTP response (DTO → JSON).
   - **Никакой бизнес-логики.**

2. **`usecases`** (средний):
   - Бизнес-логика сценариев (e.g., "отправить письмо поставщику").
   - Вызывает domain правила и адаптеры.
   - Может быть async (для I/O в адаптерах).
   - **Не знает про FastAPI, SQLAlchemy, Pydantic.**

3. **`domain`** (ядро):
   - Чистый Python (dataclass, @dataclass, типизация).
   - Бизнес-правила (валидация, статусы, константы).
   - Никаких импортов из других слоёв.
   - Никаких fastapi, sqlalchemy, requests.
   - **Переносимо на Node/Go/Java без изменений (логика).**

4. **`adapters`** (конкретика):
   - SQLAlchemy модели (ТОЛЬКО здесь).
   - Интеграции с внешними сервисами (SMTP, IMAP, HTTP, S3).
   - Repositories (QueryObject pattern).
   - **Если заменяем БД с Postgres на MySQL: меняем только здесь.**

---

## 3. Конфигурация (12-Factor)

### Правило: Все настройки только через environment переменные

- Ни одного hardcode'а в коде.
- Ключи, пароли, URL — только в `.env` (не коммитятся).
- `.env.example` — пример всех требуемых переменных (безопасный).
- Поток: `config.py` читает env → Pydantic Settings → используется везде.

**Пример `config.py`:**
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    API_PREFIX: str = "/api/v1"
    DATABASE_URL: str
    CHECKO_API_KEY: str
    PDF_MAX_PAGES: int = 3
    TRGM_SIMILARITY: float = 0.78
    JWT_SECRET: str
    
    class Config:
        env_file = ".env"

settings = Settings()
```

---

## 4. DTO ≠ Domain

### Правило: Входные/выходные схемы (Pydantic) отделены от доменных моделей

**Пример:**
```python
# ❌ НЕПРАВИЛЬНО (domain и API одно и то же):
class Request(Base):  # SQLAlchemy ORM
    id: int
    status: str
    # ... и это же возвращаем в API

# ✅ ПРАВИЛЬНО:

# domain/models.py — логика
@dataclass
class Request:
    id: int
    status: RequestStatus  # Enum
    title: str | None
    # ... только поля, нужные для логики

# adapters/db/models.py — БД
class RequestModel(Base):
    __tablename__ = "requests"
    id = Column(Integer, primary_key=True)
    status = Column(String(50))
    # ... поля БД

# transport/schemas.py — API
class RequestResponse(BaseModel):
    id: int
    status: str  # Сериализуется как строка в JSON
    title: str | None
```

**Почему:** 
- API может отличаться от БД.
- Domain не должен менять при изменении API.
- При переезде на Node: domain логика одна, но Pydantic → TypeScript/class-validator.

---

## 5. Контракт-тесты (скоро)

### Правило: Есть тесты, проверяющие что реальный API соответствует `api-contracts.yaml`

- `tests/contract/` — используют Schemathesis или OpenAPI-validator.
- Гонят на каждый коммит (или CI/CD).
- **Если API нарушает контракт → build падает, не мёржим.**

---

## 6. Никаких "быстрых хаков" в коде

### Правило: Недопустимо

❌ Помещение пароля в `main.py`  
❌ SQL запросы inline (без repository)  
❌ `# TODO` комментарии (todo перемещаются в Issues)  
❌ Импортирование `app` из других модулей (circular imports)  
❌ Глобальное состояние (кроме конфига)  
❌ Async/await в domain слое (domain синхронен)  

### Допустимо

✅ Новая фичка как отдельный usecase (даже если временный)  
✅ Mock адаптеры для тестов  
✅ Feature flags через env (если нужно)  

---

## 7. Привязка к фреймворку (запрещено в domain и usecases)

### Правило: FastAPI и SQLAlchemy — только в `transport` и `adapters`

**Покрыто выше (архитектура), но ещё раз:**

```python
# ❌ В domain/usecases:
from fastapi import HTTPException
from sqlalchemy.orm import Session
import requests

# ✅ Вместо этого:
# - domain выбрасывает DomainError, usecase переводит в HTTPException
# - Repositories (адаптеры) работают с ORMs
# - Адаптеры вызывают внешние API, domain не знает про requests
```

---

## 8. Переезд на Node должен быть возможен

### Правило: Код пишется "транспортабельно"

**Что это значит:**
- Usecase = чистая функция (можно переписать на Node такую же логику).
- Domain модели = просто структуры данных + правила (портируются как классы/интерфейсы).
- Adapters = заменяемые блоки (SQLAlchemy → Prisma/TypeORM).
- Tests, которые тестируют поведение (а не реализацию), остаются актуальны.

**Что НЕ должно быть в коде:**
- FastAPI decorators внутри usecases.
- SQLAlchemy sessions, passed into usecases.
- Зависимости от Python-специфичных фич (если можно по-универсальнее).

---

## 9. Версионирование и совместимость

### Правило: API версируется через путь `/api/v1`, `/api/v2`, etc.

- Добавление нового поля в ответе = можно (backward compatible).
- Удаление поля = новая версия API.
- Переименование поля = новая версия.
- Изменение типа = новая версия.

**Пока всегда v1, но скелет нужен.**

---

## 10. Логирование и мониторинг

### Правило: Структурированный логирование

```python
import logging
from pythonjsonlogger import jsonlogger

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
handler.setFormatter(formatter)
logger.addHandler(handler)
```

**Что логируем:**
- ✅ Начало/конец usecase (с временем)
- ✅ Ошибки (с трассировкой)
- ✅ Интеграции (запросы к Checko, SMTP, БД)
- ❌ Пароли, JWT, приватные ключи

---

## 11. Тесты (обязательны)

### Слои тестов

1. **Unit (`tests/unit/`)**: domain + usecases, БЕЗ БД
   - Быстрые, изолированные.
   - Mock адаптеров.

2. **Integration (`tests/integration/`)**: с адаптерами (БД, SMTP)
   - Медленнее, но реальные интеграции.
   - На сейчас: с тестовой БД.

3. **Contract (`tests/contract/`)**: API соответствует контракту
   - Schemathesis или openapi-spec-validator.

**Минимум покрытия:**
- Успешный сценарий (happy path).
- Основные ошибки (валидация, не найдено, конфликт).

---

## 12. Зависимости (requirements.txt)

**Минимум для MVP:**
```
fastapi==0.109.2
uvicorn[standard]==0.27.0
pydantic==2.5.3
pydantic-settings==2.1.0
sqlalchemy==2.0.23
psycopg2-binary==2.9.9
asyncpg==0.29.0
alembic==1.13.1
python-dotenv==1.0.0
python-multipart==0.0.6
aiofiles==23.2.1
```

**Запрещено:**
- Старые версии (без типизации, без async).
- Дублирующие пакеты (e.g., requests + httpx одновременно).

---

## 13. Как запускать без заглушек

### Правило: Каждый endpoint реален, работает, протестирован

Если endpoint нужен, но логика "позже":
1. Добавить в OpenAPI.
2. Реализовать как `NotImplementedError` (или 501 Not Implemented).
3. Или реализовать MVP версию (не mock, а настоящая, но может быть простая).

**Пример: `/user/requests` (создание)**
- Вход: file (multipart) или JSON с ключами.
- Выход: RequestResponse (id, status=draft, ...).
- **Это работает и всегда** (парсинг файла может быть упрощён, но структура честная).

---

## 14. Workflow при разработке

### Шаг 1: Обновить контракт
```bash
# Отредактировать api-contracts.yaml
# Добавить новый endpoint / новое поле / новый статус
```

### Шаг 2: Реализовать в коде
```bash
# 1. domain/ — добавить правило / модель
# 2. usecases/ — добавить usecase
# 3. transport/routers — добавить роут
# 4. adapters — добавить интеграцию (если нужна)
# 5. tests/ — добавить тесты
```

### Шаг 3: Проверить контракт
```bash
# Запустить tests/contract/
# Проверить Swagger UI на http://localhost:8000/docs
# Убедиться что сгенерированный OpenAPI == api-contracts.yaml
```

### Шаг 4: Коммит
```bash
git add -A
git commit -m "feat: [TAG] описание"
# Примеры TAG: USER_REQUEST, SUPPLIER_SEARCH, MODERATOR_TASK
```

---

## 15. Состояние проекта фиксируется в HANDOFF.md

Когда чат заканчивается → обновляем `HANDOFF.md` с текущим статусом, чтобы в новом чате не потерять контекст.

**Это КРИТИЧНО для непрерывности.**

---

## Итог: "Конституция" соблюдается потому что:

1. **Код долгий** — система должна жить месяцы/годы.
2. **Переезд возможен** — FastAPI → Node без переписывания домена.
3. **Новый разработчик быстро ориентируется** — структура и правила ясны.
4. **Не становится свалкой** — строгая архитектура и запреты.

**Нарушение правил = код на review не пройдёт.**

---

Версия: 1.0 от 13.12.2025

## Environment defaults

- Default API port: **8000**.
- Default API prefix: **/api/v1**.
- Default DB stack: **SQLAlchemy 2.0 async + asyncpg** (sync psycopg2 не используем).
- Local Postgres: фиксируем один режим (локально установленный или Docker compose) и отражаем это в `ENV.md`.
- Правило: если в репозитории есть `ENV.md`, то вопросы про окружение (Python/Postgres/DB stack/port/path) повторно не задаём — используем значения из `ENV.md`.


## Process logging (hard rule)
- After EACH successfully completed step/milestone: append ONE entry to HANDOFF.md (append-only).
  Include: datetime MSK, what changed (files/endpoints/migrations), how verified (exact command + expected output).
- If a step FAILED or caused breakage: DO NOT write to HANDOFF.md; write to INCIDENTS.md (append-only).
  Include: datetime MSK, symptom, root cause, fix/mitigation, verification.
- No “fake progress”: do not add endpoints to main.py if they cannot work end-to-end, unless they explicitly return 501 Not Implemented and this is logged.

## Windows workflow: write scripts only (hard rule)
- Any change to repo files must be delivered as a PowerShell script/commands that write or overwrite the target files (no "edit manually in editor" instructions).
- Use UTF-8 without BOM when writing text files (PowerShell can add BOM in some cases).
  Preferred approach:
  - $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
  - [System.IO.File]::WriteAllText(path, content, $utf8NoBom)
- Each step must include:
  - "Write" commands (create/overwrite exact paths)
  - "Verification" commands (Select-String / python -c import / pytest / curl/Invoke-RestMethod)
- No temporary scripts that will be deleted later; if a helper script is introduced, it must live under /tools and be reusable.

