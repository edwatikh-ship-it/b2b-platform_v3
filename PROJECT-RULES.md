# B2B Platform — PROJECT RULES (SSoT)

Версия: 1.2
Дата: 2025-12-15

## 1) SSoT (единственный источник правды)
- API (эндпоинты, DTO, ответы) = только api-contracts.yaml в корне репо: D:\b2bplatform\api-contracts.yaml
- Если код и контракт расходятся — это ошибка: приводим к совпадению (либо меняем контракт осознанно).
- Приоритет источников: api-contracts.yaml → PROJECT-RULES.md → PROJECT-DOC.md
- SSoT-файлы должны лежать в корне D:\b2bplatform\ (в backend\ дубликатов быть не должно).
- Прогресс = состояние ветки main в GitHub, не “память чата”.

## 2) Архитектура (фикс)
transport → usecases → domain → adapters

Коротко:
- transport: HTTP-ручки, валидация входа/выхода, никаких бизнес-решений.
- usecases: бизнес-сценарии.
- domain: “чистые” модели/правила, без FastAPI/SQLAlchemy.
- adapters: БД/SMTP/HTTP-клиенты и т.п.

## 3) SAFETY GUARDS (обязательно перед любыми правками)
Перед любыми изменениями ассистент/исполнитель обязан:
- Проверить, что D:\b2bplatform\ существует и api-contracts.yaml на месте.
- Сделать backup всех изменяемых файлов: *.bak.<timestamp>
- Показать git status до и после.
- Дать rollback: восстановление из .bak и/или git restore.

## 4) PRE-FLIGHT перед любыми “чинить API/роуты/эндпоинты”
Нельзя “угадывать по умолчанию”.

Сначала выясняем:
- BASE_URL (host:port) и API_PREFIX (например apiv1).
  - Plan A: взять из env/настроек запуска.
  - Plan B: спросить у пользователя.

Проверки (и ожидаемые результаты):
1) Invoke-RestMethod "{BASE_URL}/{API_PREFIX}/health"
   - Ожидаем JSON со status="ok" (или эквивалент по контракту).
2) Invoke-RestMethod "{BASE_URL}/openapi.json" | Out-Null
   - Ожидаем 200 и валидный JSON.
3) python -c "import os; print(os.getenv('DATABASEURL'), os.getenv('DATABASE_URL'))"
   - Не None только если это реально нужно при импорте роутеров/модулей.

Если любая проверка не проходит — сначала Plan B (как запустить/выставить env), и только потом правки кода.

## 5) “6 инструментов” проекта (сначала проверка наличия)
Инструменты: Ruff, pre-commit, pyclean, uv, direnv, just.

Правило:
- Сначала проверять наличие: Get-Command ruff/pre-commit/pyclean/uv/direnv/just
- Если инструмента нет — использовать Plan B (без обещаний, что “точно стоит”).

Как используем:
- Линт/формат:
  - ruff check backend
  - ruff format backend
  - (в CI: ruff check + ruff format --check)
- Хуки:
  - pre-commit run --all-files
- Рутинные команды:
  - just fmt / just test / just dev / just clean (если есть)
- Чистка мусора:
  - pyclean . (если есть)
  - Plan B: удалить __pycache__ через PowerShell
- Депсы:
  - prefer uv
  - Plan B: python -m venv + pip install
- env:
  - prefer direnv
  - Plan B: явные env vars в том же shell

## 6) Windows / PowerShell pitfalls (важно)
- Не использовать bash heredoc в PowerShell (например: python - << PY).
- PowerShell: строка `$ref` должна быть экранирована как `` `$ref `` (иначе это воспринимается как переменная).
- .NET Regex в PowerShell:
  - не использовать [regex]::Replace с RegexOptions (может попасть в перегрузку matchTimeout),
  - правильно: New-Object Regex(pattern, [RegexOptions]::Singleline) и потом .Replace().
- Любая правка текстовых файлов: UTF-8 без BOM (если нет особой причины), писать через .NET WriteAllText с UTF8Encoding(false).

## 7) Лог прогресса (обязательно)
- Успех шага → HANDOFF.md (append-only) + обновить PROJECT-TREE.txt + commit + push origin/main
- Фейл/инцидент → INCIDENTS.md (append-only) + commit + push

Формат INCIDENTS/HANDOFF:
- Дата/время MSK
- Что случилось / что сделали
- Root cause
- Fix/Mitigation
- Verification (команда + ожидаемый результат)
## 8) Language policy (SSoT docs)
- Source language for SSoT docs is English (ASCII preferred for maximum compatibility).
- Do NOT maintain mandatory RU+EN duplicates for every update (avoids double work and noisy logs).
- Russian docs live under docs-ru/ as NOT SSoT explanations only.
- For append-only logs (HANDOFF.md / INCIDENTS.md / DECISIONS.md): one entry = one language, no required translation; keep the required structure and verification commands.
