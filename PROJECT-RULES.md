# B2B Platform вЂ” Р–С‘СЃС‚РєРёРµ РїСЂР°РІРёР»Р° СЂР°Р·СЂР°Р±РѕС‚РєРё

**Р’РµСЂСЃРёСЏ:** 1.0  
**Р”Р°С‚Р°:** 13.12.2025  
**РЎС‚Р°С‚СѓСЃ:** РљРћРќРЎРўРРўРЈР¦РРЇ (РЅРµ РјРµРЅСЏС‚СЊ Р±РµР· СЃРѕРіР»Р°СЃРѕРІР°РЅРёСЏ)

---

## 1. Single Source of Truth (SSoT)

### РџСЂР°РІРёР»Рѕ: API РєРѕРЅС‚СЂР°РєС‚С‹ вЂ” РІ `api-contracts.yaml`, С‚РѕР»СЊРєРѕ РІ РЅС‘Рј

- **Р’СЃРµ HTTP РїСѓС‚Рё** (`/api/v1/*`) РѕРїРёСЃР°РЅС‹ РІ `api-contracts.yaml` (OpenAPI 3.0).
- **Р’СЃРµ СЃС…РµРјС‹ Р·Р°РїСЂРѕСЃРѕРІ/РѕС‚РІРµС‚РѕРІ** С„РёРєСЃРёСЂСѓСЋС‚СЃСЏ РІ YAML РїРµСЂРµРґ С‚РµРј, РєР°Рє РїРёСЃР°С‚СЊ РєРѕРґ.
- **Р›СЋР±РѕРµ РёР·РјРµРЅРµРЅРёРµ API** (РЅРѕРІС‹Р№ РїР°СЂР°РјРµС‚СЂ, РЅРѕРІС‹Р№ СЃС‚Р°С‚СѓСЃ, РЅРѕРІРѕРµ РїРѕР»Рµ) в†’ СЃРЅР°С‡Р°Р»Р° РІ YAML, РїРѕС‚РѕРј РІ РєРѕРґРµ.
- **РџСЂРё РїСЂРѕС‚РёРІРѕСЂРµС‡РёРё РјРµР¶РґСѓ РєРѕРґРѕРј Рё YAML:** YAML РІСЃРµРіРґР° РїСЂР°РІ; РєРѕРґ вЂ” Р±Р°Рі.

**РЎР»РµРґСЃС‚РІРёРµ:** Р•СЃР»Рё РїРµСЂРµРµР·Р¶Р°РµРј СЃ FastAPI РЅР° Node, РєРѕРЅС‚СЂР°РєС‚ РЅРµ РјРµРЅСЏРµС‚СЃСЏ. РњРµРЅСЏРµС‚СЃСЏ С‚РѕР»СЊРєРѕ СЂРµР°Р»РёР·Р°С†РёСЏ.

---

## 2. РђСЂС…РёС‚РµРєС‚СѓСЂР° (Clean + Hexagonal СѓРїСЂРѕС‰С‘РЅРЅРѕ)

### РћР±СЏР·Р°С‚РµР»СЊРЅС‹Рµ СЃР»РѕРё

```
backend/
  app/
    main.py                    # РўРѕР»СЊРєРѕ wiring Рё РїРѕРґРєР»СЋС‡РµРЅРёРµ СЂРѕСѓС‚РµСЂРѕРІ
    config.py                  # РљРѕРЅС„РёРіСѓСЂР°С†РёСЏ (С‚РѕР»СЊРєРѕ env)
    
    transport/
      routers/                 # FastAPI СЂРѕСѓС‚С‹ (РїСѓС‚СЊ, РїР°СЂР°РјРµС‚СЂС‹, Pydantic DTO)
        __init__.py
        requests.py
        suppliers.py
        moderator.py
      schemas/                 # Pydantic DTO (РІС…РѕРґ/РІС‹С…РѕРґ РїРѕ API)
        __init__.py
        request_schemas.py
        supplier_schemas.py
      errors.py                # ErrorResponse, HTTPException helpers
      auth.py                  # JWT, Р·Р°РІРёСЃРёРјРѕСЃС‚Рё РґР»СЏ СЂРѕСѓС‚РѕРІ
    
    usecases/                  # Р‘РёР·РЅРµСЃ-Р»РѕРіРёРєР° (СЃС†РµРЅР°СЂРёРё)
      __init__.py
      create_request.py        # CreateRequestUseCase
      submit_request.py
      search_suppliers.py
      send_email.py
      (Рё С‚.Рґ.)
    
    domain/                    # РњРѕРґРµР»Рё, РїСЂР°РІРёР»Р°, С‚РёРїС‹ (Р‘Р•Р— С„СЂРµР№РјРІРѕСЂРєР°)
      __init__.py
      models.py                # @dataclass Request, Supplier, Key, etc
      errors.py                # DomainError, ValidationError
      rules.py                 # Р‘РёР·РЅРµСЃ-РїСЂР°РІРёР»Р° (e.g., is_valid_supplier, PDF_MAX_PAGES)
    
    adapters/                  # РРЅС‚РµРіСЂР°С†РёРё (Р‘Р”, РїРѕС‡С‚Р°, РІРЅРµС€РЅРёРµ API)
      db/
        __init__.py
        models.py              # SQLAlchemy РјРѕРґРµР»Рё (РўРћР›Р¬РљРћ Р·РґРµСЃСЊ)
        repositories.py        # RequestRepository, SupplierRepository
        session.py             # get_db(), SessionLocal
      smtp/
        __init__.py
        client.py              # SMTP РѕС‚РїСЂР°РІРєР°
      imap/
        __init__.py
        client.py              # IMAP РїСЂРёС‘Рј
      checko/
        __init__.py
        client.py              # РРЅС‚РµРіСЂР°С†РёСЏ СЃ Checko API
      storage/
        __init__.py
        file_storage.py        # Р—Р°РіСЂСѓР·РєР° С„Р°Р№Р»РѕРІ
    
    shared/                    # РћР±С‰РёРµ СѓС‚РёР»РёС‚С‹
      logger.py
      utils.py
      constants.py

  tests/
    unit/                      # domain + usecases (Р±РµР· Р‘Р”)
    integration/               # СЃ Р°РґР°РїС‚РµСЂР°РјРё (Р‘Р”, SMTP)
    contract/                  # РџСЂРѕРІРµСЂРєР° СЃРѕРѕС‚РІРµС‚СЃС‚РІРёСЏ api-contracts.yaml

  requirements.txt
  .env.example
  alembic/                     # РњРёРіСЂР°С†РёРё
    versions/
```

### РџСЂР°РІРёР»Р° СЃР»РѕС‘РІ

1. **`transport`** (С‚РѕРЅРєРёР№):
   - РўРѕР»СЊРєРѕ РїР°СЂСЃРёС‚ HTTP request в†’ DTO (Pydantic).
   - РўРѕР»СЊРєРѕ РІС‹Р·С‹РІР°РµС‚ usecase.
   - РўРѕР»СЊРєРѕ РІРѕР·РІСЂР°С‰Р°РµС‚ HTTP response (DTO в†’ JSON).
   - **РќРёРєР°РєРѕР№ Р±РёР·РЅРµСЃ-Р»РѕРіРёРєРё.**

2. **`usecases`** (СЃСЂРµРґРЅРёР№):
   - Р‘РёР·РЅРµСЃ-Р»РѕРіРёРєР° СЃС†РµРЅР°СЂРёРµРІ (e.g., "РѕС‚РїСЂР°РІРёС‚СЊ РїРёСЃСЊРјРѕ РїРѕСЃС‚Р°РІС‰РёРєСѓ").
   - Р’С‹Р·С‹РІР°РµС‚ domain РїСЂР°РІРёР»Р° Рё Р°РґР°РїС‚РµСЂС‹.
   - РњРѕР¶РµС‚ Р±С‹С‚СЊ async (РґР»СЏ I/O РІ Р°РґР°РїС‚РµСЂР°С…).
   - **РќРµ Р·РЅР°РµС‚ РїСЂРѕ FastAPI, SQLAlchemy, Pydantic.**

3. **`domain`** (СЏРґСЂРѕ):
   - Р§РёСЃС‚С‹Р№ Python (dataclass, @dataclass, С‚РёРїРёР·Р°С†РёСЏ).
   - Р‘РёР·РЅРµСЃ-РїСЂР°РІРёР»Р° (РІР°Р»РёРґР°С†РёСЏ, СЃС‚Р°С‚СѓСЃС‹, РєРѕРЅСЃС‚Р°РЅС‚С‹).
   - РќРёРєР°РєРёС… РёРјРїРѕСЂС‚РѕРІ РёР· РґСЂСѓРіРёС… СЃР»РѕС‘РІ.
   - РќРёРєР°РєРёС… fastapi, sqlalchemy, requests.
   - **РџРµСЂРµРЅРѕСЃРёРјРѕ РЅР° Node/Go/Java Р±РµР· РёР·РјРµРЅРµРЅРёР№ (Р»РѕРіРёРєР°).**

4. **`adapters`** (РєРѕРЅРєСЂРµС‚РёРєР°):
   - SQLAlchemy РјРѕРґРµР»Рё (РўРћР›Р¬РљРћ Р·РґРµСЃСЊ).
   - РРЅС‚РµРіСЂР°С†РёРё СЃ РІРЅРµС€РЅРёРјРё СЃРµСЂРІРёСЃР°РјРё (SMTP, IMAP, HTTP, S3).
   - Repositories (QueryObject pattern).
   - **Р•СЃР»Рё Р·Р°РјРµРЅСЏРµРј Р‘Р” СЃ Postgres РЅР° MySQL: РјРµРЅСЏРµРј С‚РѕР»СЊРєРѕ Р·РґРµСЃСЊ.**

---

## 3. РљРѕРЅС„РёРіСѓСЂР°С†РёСЏ (12-Factor)

### РџСЂР°РІРёР»Рѕ: Р’СЃРµ РЅР°СЃС‚СЂРѕР№РєРё С‚РѕР»СЊРєРѕ С‡РµСЂРµР· environment РїРµСЂРµРјРµРЅРЅС‹Рµ

- РќРё РѕРґРЅРѕРіРѕ hardcode'Р° РІ РєРѕРґРµ.
- РљР»СЋС‡Рё, РїР°СЂРѕР»Рё, URL вЂ” С‚РѕР»СЊРєРѕ РІ `.env` (РЅРµ РєРѕРјРјРёС‚СЏС‚СЃСЏ).
- `.env.example` вЂ” РїСЂРёРјРµСЂ РІСЃРµС… С‚СЂРµР±СѓРµРјС‹С… РїРµСЂРµРјРµРЅРЅС‹С… (Р±РµР·РѕРїР°СЃРЅС‹Р№).
- РџРѕС‚РѕРє: `config.py` С‡РёС‚Р°РµС‚ env в†’ Pydantic Settings в†’ РёСЃРїРѕР»СЊР·СѓРµС‚СЃСЏ РІРµР·РґРµ.

**РџСЂРёРјРµСЂ `config.py`:**
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

## 4. DTO в‰  Domain

### РџСЂР°РІРёР»Рѕ: Р’С…РѕРґРЅС‹Рµ/РІС‹С…РѕРґРЅС‹Рµ СЃС…РµРјС‹ (Pydantic) РѕС‚РґРµР»РµРЅС‹ РѕС‚ РґРѕРјРµРЅРЅС‹С… РјРѕРґРµР»РµР№

**РџСЂРёРјРµСЂ:**
```python
# вќЊ РќР•РџР РђР’РР›Р¬РќРћ (domain Рё API РѕРґРЅРѕ Рё С‚Рѕ Р¶Рµ):
class Request(Base):  # SQLAlchemy ORM
    id: int
    status: str
    # ... Рё СЌС‚Рѕ Р¶Рµ РІРѕР·РІСЂР°С‰Р°РµРј РІ API

# вњ… РџР РђР’РР›Р¬РќРћ:

# domain/models.py вЂ” Р»РѕРіРёРєР°
@dataclass
class Request:
    id: int
    status: RequestStatus  # Enum
    title: str | None
    # ... С‚РѕР»СЊРєРѕ РїРѕР»СЏ, РЅСѓР¶РЅС‹Рµ РґР»СЏ Р»РѕРіРёРєРё

# adapters/db/models.py вЂ” Р‘Р”
class RequestModel(Base):
    __tablename__ = "requests"
    id = Column(Integer, primary_key=True)
    status = Column(String(50))
    # ... РїРѕР»СЏ Р‘Р”

# transport/schemas.py вЂ” API
class RequestResponse(BaseModel):
    id: int
    status: str  # РЎРµСЂРёР°Р»РёР·СѓРµС‚СЃСЏ РєР°Рє СЃС‚СЂРѕРєР° РІ JSON
    title: str | None
```

**РџРѕС‡РµРјСѓ:** 
- API РјРѕР¶РµС‚ РѕС‚Р»РёС‡Р°С‚СЊСЃСЏ РѕС‚ Р‘Р”.
- Domain РЅРµ РґРѕР»Р¶РµРЅ РјРµРЅСЏС‚СЊ РїСЂРё РёР·РјРµРЅРµРЅРёРё API.
- РџСЂРё РїРµСЂРµРµР·РґРµ РЅР° Node: domain Р»РѕРіРёРєР° РѕРґРЅР°, РЅРѕ Pydantic в†’ TypeScript/class-validator.

---

## 5. РљРѕРЅС‚СЂР°РєС‚-С‚РµСЃС‚С‹ (СЃРєРѕСЂРѕ)

### РџСЂР°РІРёР»Рѕ: Р•СЃС‚СЊ С‚РµСЃС‚С‹, РїСЂРѕРІРµСЂСЏСЋС‰РёРµ С‡С‚Рѕ СЂРµР°Р»СЊРЅС‹Р№ API СЃРѕРѕС‚РІРµС‚СЃС‚РІСѓРµС‚ `api-contracts.yaml`

- `tests/contract/` вЂ” РёСЃРїРѕР»СЊР·СѓСЋС‚ Schemathesis РёР»Рё OpenAPI-validator.
- Р“РѕРЅСЏС‚ РЅР° РєР°Р¶РґС‹Р№ РєРѕРјРјРёС‚ (РёР»Рё CI/CD).
- **Р•СЃР»Рё API РЅР°СЂСѓС€Р°РµС‚ РєРѕРЅС‚СЂР°РєС‚ в†’ build РїР°РґР°РµС‚, РЅРµ РјС‘СЂР¶РёРј.**

---

## 6. РќРёРєР°РєРёС… "Р±С‹СЃС‚СЂС‹С… С…Р°РєРѕРІ" РІ РєРѕРґРµ

### РџСЂР°РІРёР»Рѕ: РќРµРґРѕРїСѓСЃС‚РёРјРѕ

вќЊ РџРѕРјРµС‰РµРЅРёРµ РїР°СЂРѕР»СЏ РІ `main.py`  
вќЊ SQL Р·Р°РїСЂРѕСЃС‹ inline (Р±РµР· repository)  
вќЊ `# TODO` РєРѕРјРјРµРЅС‚Р°СЂРёРё (todo РїРµСЂРµРјРµС‰Р°СЋС‚СЃСЏ РІ Issues)  
вќЊ РРјРїРѕСЂС‚РёСЂРѕРІР°РЅРёРµ `app` РёР· РґСЂСѓРіРёС… РјРѕРґСѓР»РµР№ (circular imports)  
вќЊ Р“Р»РѕР±Р°Р»СЊРЅРѕРµ СЃРѕСЃС‚РѕСЏРЅРёРµ (РєСЂРѕРјРµ РєРѕРЅС„РёРіР°)  
вќЊ Async/await РІ domain СЃР»РѕРµ (domain СЃРёРЅС…СЂРѕРЅРµРЅ)  

### Р”РѕРїСѓСЃС‚РёРјРѕ

вњ… РќРѕРІР°СЏ С„РёС‡РєР° РєР°Рє РѕС‚РґРµР»СЊРЅС‹Р№ usecase (РґР°Р¶Рµ РµСЃР»Рё РІСЂРµРјРµРЅРЅС‹Р№)  
вњ… Mock Р°РґР°РїС‚РµСЂС‹ РґР»СЏ С‚РµСЃС‚РѕРІ  
вњ… Feature flags С‡РµСЂРµР· env (РµСЃР»Рё РЅСѓР¶РЅРѕ)  

---

## 7. РџСЂРёРІСЏР·РєР° Рє С„СЂРµР№РјРІРѕСЂРєСѓ (Р·Р°РїСЂРµС‰РµРЅРѕ РІ domain Рё usecases)

### РџСЂР°РІРёР»Рѕ: FastAPI Рё SQLAlchemy вЂ” С‚РѕР»СЊРєРѕ РІ `transport` Рё `adapters`

**РџРѕРєСЂС‹С‚Рѕ РІС‹С€Рµ (Р°СЂС…РёС‚РµРєС‚СѓСЂР°), РЅРѕ РµС‰С‘ СЂР°Р·:**

```python
# вќЊ Р’ domain/usecases:
from fastapi import HTTPException
from sqlalchemy.orm import Session
import requests

# вњ… Р’РјРµСЃС‚Рѕ СЌС‚РѕРіРѕ:
# - domain РІС‹Р±СЂР°СЃС‹РІР°РµС‚ DomainError, usecase РїРµСЂРµРІРѕРґРёС‚ РІ HTTPException
# - Repositories (Р°РґР°РїС‚РµСЂС‹) СЂР°Р±РѕС‚Р°СЋС‚ СЃ ORMs
# - РђРґР°РїС‚РµСЂС‹ РІС‹Р·С‹РІР°СЋС‚ РІРЅРµС€РЅРёРµ API, domain РЅРµ Р·РЅР°РµС‚ РїСЂРѕ requests
```

---

## 8. РџРµСЂРµРµР·Рґ РЅР° Node РґРѕР»Р¶РµРЅ Р±С‹С‚СЊ РІРѕР·РјРѕР¶РµРЅ

### РџСЂР°РІРёР»Рѕ: РљРѕРґ РїРёС€РµС‚СЃСЏ "С‚СЂР°РЅСЃРїРѕСЂС‚Р°Р±РµР»СЊРЅРѕ"

**Р§С‚Рѕ СЌС‚Рѕ Р·РЅР°С‡РёС‚:**
- Usecase = С‡РёСЃС‚Р°СЏ С„СѓРЅРєС†РёСЏ (РјРѕР¶РЅРѕ РїРµСЂРµРїРёСЃР°С‚СЊ РЅР° Node С‚Р°РєСѓСЋ Р¶Рµ Р»РѕРіРёРєСѓ).
- Domain РјРѕРґРµР»Рё = РїСЂРѕСЃС‚Рѕ СЃС‚СЂСѓРєС‚СѓСЂС‹ РґР°РЅРЅС‹С… + РїСЂР°РІРёР»Р° (РїРѕСЂС‚РёСЂСѓСЋС‚СЃСЏ РєР°Рє РєР»Р°СЃСЃС‹/РёРЅС‚РµСЂС„РµР№СЃС‹).
- Adapters = Р·Р°РјРµРЅСЏРµРјС‹Рµ Р±Р»РѕРєРё (SQLAlchemy в†’ Prisma/TypeORM).
- Tests, РєРѕС‚РѕСЂС‹Рµ С‚РµСЃС‚РёСЂСѓСЋС‚ РїРѕРІРµРґРµРЅРёРµ (Р° РЅРµ СЂРµР°Р»РёР·Р°С†РёСЋ), РѕСЃС‚Р°СЋС‚СЃСЏ Р°РєС‚СѓР°Р»СЊРЅС‹.

**Р§С‚Рѕ РќР• РґРѕР»Р¶РЅРѕ Р±С‹С‚СЊ РІ РєРѕРґРµ:**
- FastAPI decorators РІРЅСѓС‚СЂРё usecases.
- SQLAlchemy sessions, passed into usecases.
- Р—Р°РІРёСЃРёРјРѕСЃС‚Рё РѕС‚ Python-СЃРїРµС†РёС„РёС‡РЅС‹С… С„РёС‡ (РµСЃР»Рё РјРѕР¶РЅРѕ РїРѕ-СѓРЅРёРІРµСЂСЃР°Р»СЊРЅРµРµ).

---

## 9. Р’РµСЂСЃРёРѕРЅРёСЂРѕРІР°РЅРёРµ Рё СЃРѕРІРјРµСЃС‚РёРјРѕСЃС‚СЊ

### РџСЂР°РІРёР»Рѕ: API РІРµСЂСЃРёСЂСѓРµС‚СЃСЏ С‡РµСЂРµР· РїСѓС‚СЊ `/api/v1`, `/api/v2`, etc.

- Р”РѕР±Р°РІР»РµРЅРёРµ РЅРѕРІРѕРіРѕ РїРѕР»СЏ РІ РѕС‚РІРµС‚Рµ = РјРѕР¶РЅРѕ (backward compatible).
- РЈРґР°Р»РµРЅРёРµ РїРѕР»СЏ = РЅРѕРІР°СЏ РІРµСЂСЃРёСЏ API.
- РџРµСЂРµРёРјРµРЅРѕРІР°РЅРёРµ РїРѕР»СЏ = РЅРѕРІР°СЏ РІРµСЂСЃРёСЏ.
- РР·РјРµРЅРµРЅРёРµ С‚РёРїР° = РЅРѕРІР°СЏ РІРµСЂСЃРёСЏ.

**РџРѕРєР° РІСЃРµРіРґР° v1, РЅРѕ СЃРєРµР»РµС‚ РЅСѓР¶РµРЅ.**

---

## 10. Р›РѕРіРёСЂРѕРІР°РЅРёРµ Рё РјРѕРЅРёС‚РѕСЂРёРЅРі

### РџСЂР°РІРёР»Рѕ: РЎС‚СЂСѓРєС‚СѓСЂРёСЂРѕРІР°РЅРЅС‹Р№ Р»РѕРіРёСЂРѕРІР°РЅРёРµ

```python
import logging
from pythonjsonlogger import jsonlogger

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter()
handler.setFormatter(formatter)
logger.addHandler(handler)
```

**Р§С‚Рѕ Р»РѕРіРёСЂСѓРµРј:**
- вњ… РќР°С‡Р°Р»Рѕ/РєРѕРЅРµС† usecase (СЃ РІСЂРµРјРµРЅРµРј)
- вњ… РћС€РёР±РєРё (СЃ С‚СЂР°СЃСЃРёСЂРѕРІРєРѕР№)
- вњ… РРЅС‚РµРіСЂР°С†РёРё (Р·Р°РїСЂРѕСЃС‹ Рє Checko, SMTP, Р‘Р”)
- вќЊ РџР°СЂРѕР»Рё, JWT, РїСЂРёРІР°С‚РЅС‹Рµ РєР»СЋС‡Рё

---

## 11. РўРµСЃС‚С‹ (РѕР±СЏР·Р°С‚РµР»СЊРЅС‹)

### РЎР»РѕРё С‚РµСЃС‚РѕРІ

1. **Unit (`tests/unit/`)**: domain + usecases, Р‘Р•Р— Р‘Р”
   - Р‘С‹СЃС‚СЂС‹Рµ, РёР·РѕР»РёСЂРѕРІР°РЅРЅС‹Рµ.
   - Mock Р°РґР°РїС‚РµСЂРѕРІ.

2. **Integration (`tests/integration/`)**: СЃ Р°РґР°РїС‚РµСЂР°РјРё (Р‘Р”, SMTP)
   - РњРµРґР»РµРЅРЅРµРµ, РЅРѕ СЂРµР°Р»СЊРЅС‹Рµ РёРЅС‚РµРіСЂР°С†РёРё.
   - РќР° СЃРµР№С‡Р°СЃ: СЃ С‚РµСЃС‚РѕРІРѕР№ Р‘Р”.

3. **Contract (`tests/contract/`)**: API СЃРѕРѕС‚РІРµС‚СЃС‚РІСѓРµС‚ РєРѕРЅС‚СЂР°РєС‚Сѓ
   - Schemathesis РёР»Рё openapi-spec-validator.

**РњРёРЅРёРјСѓРј РїРѕРєСЂС‹С‚РёСЏ:**
- РЈСЃРїРµС€РЅС‹Р№ СЃС†РµРЅР°СЂРёР№ (happy path).
- РћСЃРЅРѕРІРЅС‹Рµ РѕС€РёР±РєРё (РІР°Р»РёРґР°С†РёСЏ, РЅРµ РЅР°Р№РґРµРЅРѕ, РєРѕРЅС„Р»РёРєС‚).

---

## 12. Р—Р°РІРёСЃРёРјРѕСЃС‚Рё (requirements.txt)

**РњРёРЅРёРјСѓРј РґР»СЏ MVP:**
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

**Р—Р°РїСЂРµС‰РµРЅРѕ:**
- РЎС‚Р°СЂС‹Рµ РІРµСЂСЃРёРё (Р±РµР· С‚РёРїРёР·Р°С†РёРё, Р±РµР· async).
- Р”СѓР±Р»РёСЂСѓСЋС‰РёРµ РїР°РєРµС‚С‹ (e.g., requests + httpx РѕРґРЅРѕРІСЂРµРјРµРЅРЅРѕ).

---

## 13. РљР°Рє Р·Р°РїСѓСЃРєР°С‚СЊ Р±РµР· Р·Р°РіР»СѓС€РµРє

### РџСЂР°РІРёР»Рѕ: РљР°Р¶РґС‹Р№ endpoint СЂРµР°Р»РµРЅ, СЂР°Р±РѕС‚Р°РµС‚, РїСЂРѕС‚РµСЃС‚РёСЂРѕРІР°РЅ

Р•СЃР»Рё endpoint РЅСѓР¶РµРЅ, РЅРѕ Р»РѕРіРёРєР° "РїРѕР·Р¶Рµ":
1. Р”РѕР±Р°РІРёС‚СЊ РІ OpenAPI.
2. Р РµР°Р»РёР·РѕРІР°С‚СЊ РєР°Рє `NotImplementedError` (РёР»Рё 501 Not Implemented).
3. РР»Рё СЂРµР°Р»РёР·РѕРІР°С‚СЊ MVP РІРµСЂСЃРёСЋ (РЅРµ mock, Р° РЅР°СЃС‚РѕСЏС‰Р°СЏ, РЅРѕ РјРѕР¶РµС‚ Р±С‹С‚СЊ РїСЂРѕСЃС‚Р°СЏ).

**РџСЂРёРјРµСЂ: `/user/requests` (СЃРѕР·РґР°РЅРёРµ)**
- Р’С…РѕРґ: file (multipart) РёР»Рё JSON СЃ РєР»СЋС‡Р°РјРё.
- Р’С‹С…РѕРґ: RequestResponse (id, status=draft, ...).
- **Р­С‚Рѕ СЂР°Р±РѕС‚Р°РµС‚ Рё РІСЃРµРіРґР°** (РїР°СЂСЃРёРЅРі С„Р°Р№Р»Р° РјРѕР¶РµС‚ Р±С‹С‚СЊ СѓРїСЂРѕС‰С‘РЅ, РЅРѕ СЃС‚СЂСѓРєС‚СѓСЂР° С‡РµСЃС‚РЅР°СЏ).

---

## 14. Workflow РїСЂРё СЂР°Р·СЂР°Р±РѕС‚РєРµ

### РЁР°Рі 1: РћР±РЅРѕРІРёС‚СЊ РєРѕРЅС‚СЂР°РєС‚
```bash
# РћС‚СЂРµРґР°РєС‚РёСЂРѕРІР°С‚СЊ api-contracts.yaml
# Р”РѕР±Р°РІРёС‚СЊ РЅРѕРІС‹Р№ endpoint / РЅРѕРІРѕРµ РїРѕР»Рµ / РЅРѕРІС‹Р№ СЃС‚Р°С‚СѓСЃ
```

### РЁР°Рі 2: Р РµР°Р»РёР·РѕРІР°С‚СЊ РІ РєРѕРґРµ
```bash
# 1. domain/ вЂ” РґРѕР±Р°РІРёС‚СЊ РїСЂР°РІРёР»Рѕ / РјРѕРґРµР»СЊ
# 2. usecases/ вЂ” РґРѕР±Р°РІРёС‚СЊ usecase
# 3. transport/routers вЂ” РґРѕР±Р°РІРёС‚СЊ СЂРѕСѓС‚
# 4. adapters вЂ” РґРѕР±Р°РІРёС‚СЊ РёРЅС‚РµРіСЂР°С†РёСЋ (РµСЃР»Рё РЅСѓР¶РЅР°)
# 5. tests/ вЂ” РґРѕР±Р°РІРёС‚СЊ С‚РµСЃС‚С‹
```

### РЁР°Рі 3: РџСЂРѕРІРµСЂРёС‚СЊ РєРѕРЅС‚СЂР°РєС‚
```bash
# Р—Р°РїСѓСЃС‚РёС‚СЊ tests/contract/
# РџСЂРѕРІРµСЂРёС‚СЊ Swagger UI РЅР° http://localhost:8000/docs
# РЈР±РµРґРёС‚СЊСЃСЏ С‡С‚Рѕ СЃРіРµРЅРµСЂРёСЂРѕРІР°РЅРЅС‹Р№ OpenAPI == api-contracts.yaml
```

### РЁР°Рі 4: РљРѕРјРјРёС‚
```bash
git add -A
git commit -m "feat: [TAG] РѕРїРёСЃР°РЅРёРµ"
# РџСЂРёРјРµСЂС‹ TAG: USER_REQUEST, SUPPLIER_SEARCH, MODERATOR_TASK
```

---

## 15. РЎРѕСЃС‚РѕСЏРЅРёРµ РїСЂРѕРµРєС‚Р° С„РёРєСЃРёСЂСѓРµС‚СЃСЏ РІ HANDOFF.md

РљРѕРіРґР° С‡Р°С‚ Р·Р°РєР°РЅС‡РёРІР°РµС‚СЃСЏ в†’ РѕР±РЅРѕРІР»СЏРµРј `HANDOFF.md` СЃ С‚РµРєСѓС‰РёРј СЃС‚Р°С‚СѓСЃРѕРј, С‡С‚РѕР±С‹ РІ РЅРѕРІРѕРј С‡Р°С‚Рµ РЅРµ РїРѕС‚РµСЂСЏС‚СЊ РєРѕРЅС‚РµРєСЃС‚.

**Р­С‚Рѕ РљР РРўРР§РќРћ РґР»СЏ РЅРµРїСЂРµСЂС‹РІРЅРѕСЃС‚Рё.**

---

## РС‚РѕРі: "РљРѕРЅСЃС‚РёС‚СѓС†РёСЏ" СЃРѕР±Р»СЋРґР°РµС‚СЃСЏ РїРѕС‚РѕРјСѓ С‡С‚Рѕ:

1. **РљРѕРґ РґРѕР»РіРёР№** вЂ” СЃРёСЃС‚РµРјР° РґРѕР»Р¶РЅР° Р¶РёС‚СЊ РјРµСЃСЏС†С‹/РіРѕРґС‹.
2. **РџРµСЂРµРµР·Рґ РІРѕР·РјРѕР¶РµРЅ** вЂ” FastAPI в†’ Node Р±РµР· РїРµСЂРµРїРёСЃС‹РІР°РЅРёСЏ РґРѕРјРµРЅР°.
3. **РќРѕРІС‹Р№ СЂР°Р·СЂР°Р±РѕС‚С‡РёРє Р±С‹СЃС‚СЂРѕ РѕСЂРёРµРЅС‚РёСЂСѓРµС‚СЃСЏ** вЂ” СЃС‚СЂСѓРєС‚СѓСЂР° Рё РїСЂР°РІРёР»Р° СЏСЃРЅС‹.
4. **РќРµ СЃС‚Р°РЅРѕРІРёС‚СЃСЏ СЃРІР°Р»РєРѕР№** вЂ” СЃС‚СЂРѕРіР°СЏ Р°СЂС…РёС‚РµРєС‚СѓСЂР° Рё Р·Р°РїСЂРµС‚С‹.

**РќР°СЂСѓС€РµРЅРёРµ РїСЂР°РІРёР» = РєРѕРґ РЅР° review РЅРµ РїСЂРѕР№РґС‘С‚.**

---

Р’РµСЂСЃРёСЏ: 1.0 РѕС‚ 13.12.2025

## Environment defaults

- Default API port: **8000**.
- Default API prefix: **/api/v1**.
- Default DB stack: **SQLAlchemy 2.0 async + asyncpg** (sync psycopg2 РЅРµ РёСЃРїРѕР»СЊР·СѓРµРј).
- Local Postgres: С„РёРєСЃРёСЂСѓРµРј РѕРґРёРЅ СЂРµР¶РёРј (Р»РѕРєР°Р»СЊРЅРѕ СѓСЃС‚Р°РЅРѕРІР»РµРЅРЅС‹Р№ РёР»Рё Docker compose) Рё РѕС‚СЂР°Р¶Р°РµРј СЌС‚Рѕ РІ `ENV.md`.
- РџСЂР°РІРёР»Рѕ: РµСЃР»Рё РІ СЂРµРїРѕР·РёС‚РѕСЂРёРё РµСЃС‚СЊ `ENV.md`, С‚Рѕ РІРѕРїСЂРѕСЃС‹ РїСЂРѕ РѕРєСЂСѓР¶РµРЅРёРµ (Python/Postgres/DB stack/port/path) РїРѕРІС‚РѕСЂРЅРѕ РЅРµ Р·Р°РґР°С‘Рј вЂ” РёСЃРїРѕР»СЊР·СѓРµРј Р·РЅР°С‡РµРЅРёСЏ РёР· `ENV.md`.


## Process logging (hard rule)
- After EACH successfully completed step/milestone: append ONE entry to HANDOFF.md (append-only).
  Include: datetime MSK, what changed (files/endpoints/migrations), how verified (exact command + expected output).
- If a step FAILED or caused breakage: DO NOT write to HANDOFF.md; write to INCIDENTS.md (append-only).
  Include: datetime MSK, symptom, root cause, fix/mitigation, verification.
- No вЂњfake progressвЂќ: do not add endpoints to main.py if they cannot work end-to-end, unless they explicitly return 501 Not Implemented and this is logged.

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




## рџ› пёЏ РРЅСЃС‚СЂСѓРјРµРЅС‚С‹ РїСЂРѕРµРєС‚Р° (РІСЃРµ РїРѕРґРєР»СЋС‡РµРЅС‹ вњ…)

| РРЅСЃС‚СЂСѓРјРµРЅС‚ | Р РѕР»СЊ | РљРѕРјР°РЅРґР° Р·Р°РїСѓСЃРєР° |
|------------|------|-----------------|
| **Ruff** | Р›РёРЅС‚РµСЂ + С„РѕСЂРјР°С‚С‚РµСЂ | `just fmt` |
| **pre-commit** | РџСЂРѕРІРµСЂРєРё РїРµСЂРµРґ РєРѕРјРјРёС‚РѕРј | `backend\.venv\Scripts\pre-commit.exe run --all-files` |
| **GitHub Actions** | CI РЅР° РєР°Р¶РґС‹Р№ push/PR | РђРІС‚РѕРјР°С‚РёС‡РµСЃРєРё РІ Checks |
| **just** | Task runner | `just fmt`, `just dev`, `just test` |
| **pyclean** | РЈР±РѕСЂРєР° __pycache__ | `pyclean backend` |
| **uv** | Р‘С‹СЃС‚СЂС‹Р№ pip | `uv pip install -r requirements.txt` |

**РџСЂР°РІРёР»Рѕ**: РїРµСЂРµРґ РєРѕРјРјРёС‚РѕРј/РїСѓС€РµРј РІСЃРµРіРґР° `just fmt` + pre-commit.

### Absolute rule for assistant
- If the response implies ANY repo change (code, config, docs, CI, migrations) the assistant MUST provide runnable commands (PowerShell) that:
  - create/overwrite exact file paths, or
  - apply exact deterministic patches (no manual editor steps).
- If commands are not provided, the response is considered invalid and must be rewritten with scripts.
- Default format for file writes: UTF-8 without BOM via:
  - $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
  - [System.IO.File]::WriteAllText(path, content, $utf8NoBom)


## Communication rules for assistant (hard rule)
- Treat the user as a product owner / Р·Р°РєР°Р·С‡РёРє, not as СЂСЏРґРѕРІРѕР№ СЂР°Р·СЂР°Р±РѕС‚С‡РёРє.
- Questions must be in simple, human language (Р±РµР· РїРµСЂРµРіСЂСѓР·Р° С‚РµСЂРјРёРЅР°РјРё), СЃ РјРёРЅРёРјСѓРјРѕРј РІРЅСѓС‚СЂРµРЅРЅРµР№ РєСѓС…РЅРё.
- Technical details (С‚РёРїС‹, РїСѓС‚Рё С„Р°Р№Р»РѕРІ, РєРѕРјР°РЅРґС‹) РґР°РІР°С‚СЊ, РЅРѕ РѕР±СЉСЏСЃРЅРµРЅРёСЏ С„РѕСЂРјСѓР»РёСЂРѕРІР°С‚СЊ С‚Р°Рє, С‡С‚РѕР±С‹ РёС… РјРѕР¶РЅРѕ Р±С‹Р»Рѕ РїРѕРЅРёРјР°С‚СЊ РЅР° СѓСЂРѕРІРЅРµ вЂњС‡С‚Рѕ СЌС‚Рѕ РґР°С‘С‚ РїСЂРѕРґСѓРєС‚СѓвЂќ.
- Р•СЃР»Рё РЅСѓР¶РЅРѕ СЃРїСЂРѕСЃРёС‚СЊ РїСЂРѕ Р°СЂС…РёС‚РµРєС‚СѓСЂСѓ/СЂРµС€РµРЅРёРµ, СЃРЅР°С‡Р°Р»Р° РєРѕСЂРѕС‚РєРѕ СЃС„РѕСЂРјСѓР»РёСЂРѕРІР°С‚СЊ СЃСѓС‚СЊ РІС‹Р±РѕСЂР° (РІР°СЂРёР°РЅС‚ A/РІР°СЂРёР°РЅС‚ B) РѕР±С‹С‡РЅС‹Рј СЏР·С‹РєРѕРј, Р° СѓР¶Рµ РїРѕС‚РѕРј вЂ” С‚РµС…РЅРёС‡РµСЃРєРёРµ РґРµС‚Р°Р»Рё.


## GitHub progress as SSoT (hard rule)
- Progress and current state are tracked in GitHub (main branch) to avoid losing context between chats.
- After each completed milestone:
  - Update HANDOFF.md (append-only) with datetime MSK, what changed, how verified (exact command + expected output).
  - Commit and push to origin/main.
- When a milestone fails or causes breakage:
  - Write to INCIDENTS.md (append-only), then commit and push.
- Start-of-chat protocol:
  - Provide raw links to api-contracts.yaml, PROJECT-RULES.md, HANDOFF.md (and INCIDENTS.md if relevant) at HEAD of main.


---

## Start-of-work preflight (mandatory)

Before changing wiring/routers/tests, run a preflight to avoid guesswork:

- Tools presence check: ruff, pre-commit, pyclean, uv, direnv, just; if missing, use Plan B commands.

- Environment check: DATABASEURL or DATABASE_URL must be set for any code paths that import DB/session at import-time.

- Run backend only from a shell where env is explicitly set (or via a single dev script) to avoid “works in one console, fails in another”.

- Verification baseline: /apiv1/health returns ok and /openapi.json is reachable.



PowerShell reference preflight snippet:

- Activate venv, set PYTHONPATH, set DATABASEURL and DATABASE_URL, then start uvicorn.

---
