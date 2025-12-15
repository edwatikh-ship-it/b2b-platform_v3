# PROJECT-RULES — пояснялка (RU, NOT SSoT)

Источник правды: **PROJECT-RULES.md** и в первую очередь **api-contracts.yaml**. Этот файл — только “человеческая” шпаргалка, чтобы быстрее работать. [NOT SSoT]

---

## 1) SSoT: что это значит на практике

SSoT = “единственный источник правды”. У нас это:
- API (эндпоинты/DTO/статусы) — только **api-contracts.yaml** (в корне репы).
- Если код не совпадает с контрактом — это **ошибка**, правим чтобы совпало (или осознанно меняем контракт).
- Приоритет доков: api-contracts.yaml → PROJECT-RULES.md → PROJECT-DOC.md.
- SSoT-файлы должны быть в корне D:\b2bplatform\ (не в backend\).

**Быстрые проверки**
- Проверить, что контракт на месте:
  - Test-Path D:\b2bplatform\api-contracts.yaml
- Проверить, что backend не подсунул “левый” контракт:
  - dir D:\b2bplatform\backend -Filter api-contracts.yaml -Recurse

---

## 2) Архитектура (как раскладывать код)

Слои строго такие:
transport → usecases → domain → adapters

Как понимать:
- transport: FastAPI ручки + DTO + валидация входа/выхода. Никакой бизнес-логики.
- usecases: бизнес-сценарии (“что делаем”).
- domain: чистые правила/модели. Никакого FastAPI/SQLAlchemy.
- adapters: БД/SMTP/HTTP и т.п.

**Красный флаг**
- Если в transport появилась логика типа “если инн в чс — то…” — это почти всегда надо вынести в usecases/domain.

---

## 3) Safety guards перед любыми правками (обязаловка)

Перед любыми изменениями:
1) Убедиться, что работаешь в D:\b2bplatform и SSoT на месте.
2) Сделать .bak копии всех файлов, которые будешь менять.
3) Показать git status до/после.
4) Держать rollback план (git restore и/или вернуть .bak).

**Шаблон-команды**
- Перед:
  - cd D:\b2bplatform
  - git status
- Бэкап (пример для одного файла):
  - 20251215-171341 = Get-Date -Format "yyyyMMdd-HHmmss"
  - Copy-Item .\PROJECT-DOC.md ".\PROJECT-DOC.md.bak.20251215-171341"
- Откат:
  - git restore -- .\PROJECT-DOC.md
  - # или
  - Copy-Item ".\PROJECT-DOC.md.bak.20251215-171341" ".\PROJECT-DOC.md" -Force

---

## 4) PRE-FLIGHT перед “чинить роуты/эндпоинты”

Запрещено угадывать BASE_URL и API_PREFIX “по умолчанию”.

Сначала выясняем:
- BASE_URL (host:port)
- API_PREFIX (например apiv1)

Проверки:
1) health:
   - Invoke-RestMethod "{BASE_URL}/{API_PREFIX}/health"
   - Ожидаем JSON со status="ok" (или эквивалент по контракту).
2) openapi.json:
   - Invoke-RestMethod "{BASE_URL}/openapi.json" | Out-Null
   - Ожидаем 200 + валидный JSON.
3) env на DB (если роуты/модули требуют БД при импорте):
   - python -c "import os; print(os.getenv('DATABASEURL'), os.getenv('DATABASE_URL'))"
   - Не должно быть None None, если проект реально требует DB env.

**Если что-то не проходит**
Сначала Plan B: как поднять backend/выставить env. Только потом правки.

---

## 5) “6 инструментов” проекта (и Plan B)

Инструменты: Ruff, pre-commit, pyclean, uv, direnv, just.

Сначала проверяем, что они есть:
- Get-Command ruff, pre-commit, pyclean, uv, direnv, just

### Ruff (lint/format)
- ruff check backend
- ruff format backend
CI обычно делает:
- ruff check backend
- ruff format --check backend

### pre-commit
- pre-commit run --all-files

### just (если есть)
- just fmt
- just test
- just dev
- just clean

### pyclean
- pyclean .

Plan B (если pyclean нет):
- Get-ChildItem -Recurse -Directory -Filter "__pycache__" | Remove-Item -Recurse -Force

### uv / deps
Prefer uv, но если нет:
- python -m venv .venv
- .\.venv\Scripts\activate
- python -m pip install -r requirements.txt

### direnv / env
Prefer direnv, но если нет:
- выставлять env vars в том же PowerShell, где запускаешь uvicorn/alembic/tests.

---

## 6) Windows / PowerShell ловушки (важное)

- PowerShell не bash: heredoc вида python - << PY не работает.
- Строка $ref в PowerShell — это попытка обратиться к переменной. Если надо написать текст $ref, экранируй как ` $ref `.
- Regex в PowerShell: аккуратно с перегрузками. Надёжнее:
  -  = New-Object System.Text.RegularExpressions.Regex("pattern", [System.Text.RegularExpressions.RegexOptions]::Singleline)
  -  = .Replace(, "replacement")
- Текстовые файлы писать как UTF‑8 **без BOM**:
  - System.Text.UTF8Encoding = New-Object System.Text.UTF8Encoding(False)
  - [System.IO.File]::WriteAllText(, , System.Text.UTF8Encoding)

---

## 7) Логи прогресса (как не терять историю)

- Успех шага → дописываем в HANDOFF.md (append-only) + обновляем PROJECT-TREE.txt + commit + push.
- Фейл → дописываем в INCIDENTS.md (append-only) + commit + push.

Мини-формат записи:
- Дата/время (MSK)
- Что случилось
- Root cause
- Fix/Mitigation
- Verification (команда + ожидаемый результат)

---

## 8) Chat safety: “Step 0” и “Question gate”

Step 0 для нового чата/новой проблемы:
- прогнать “Detect backend + PRE-FLIGHT” (или вручную сделать 3 проверки из PRE-FLIGHT).

Question gate:
- если задан критичный вопрос (BASE_URL/API_PREFIX/DATABASEURL…) и нет ответа — стопаемся и не делаем новых действий.