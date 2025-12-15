# HANDOFF — пояснялка (RU, NOT SSoT)

Оригинал: HANDOFF.md (append-only). Здесь лог **успешных** шагов, с проверкой. Фейлы — только в INCIDENTS.md. [NOT SSoT] [file:34][file:38]

---

## Когда писать в HANDOFF, а когда в INCIDENTS

- Успешный шаг/фича/миграция → HANDOFF.md (с командой проверки). [file:34][file:38]
- Любой фейл/инцидент → INCIDENTS.md (symptom/root cause/fix/verification). [file:34][file:39]

Правило: в HANDOFF **нет** “сломалось/починили” — только “сделали и проверили”. [file:34]

---

## Формат хорошей записи в HANDOFF

Одна запись = 2–4 строки:
- дата/время (MSK),
- что сделали (фича/миграция/рефакторинг),
- как проверили (точная команда + ожидаемый результат). [file:34]

### Пример 1 (endpoint)
- 2025-..-.. ..:.. MSK: Добавили POST /api/v1/user/requests (create). Verify: python -m pytest -q -k create_request_manual -> PASSED; Invoke-RestMethod .../api/v1/user/requests -> 200, есть requestid. [file:34]

### Пример 2 (миграция)
- 2025-..-.. ..:.. MSK: Создали и применили миграцию X для таблицы Y. Verify: lembic current -> X; psql ... -c "\dt" показывает таблицу Y. [file:34]

---

## Что обязательно проверять перед записью

Минимальные DoD (Definition of Done) для инфраструктурных шагов:
- backend поднят и отвечает:
  - GET {BASE_URL}/{API_PREFIX}/health -> status = ok. [file:34][file:38]
  - GET {BASE_URL}/openapi.json -> 200 и валидный JSON. [file:34]
- если трогали БД:
  - alembic current показывает нужную ревизию,
  - таблицы/колонки реально есть в psql. [file:34]

---

## Быстрый runbook: как стартовать backend (напоминалка)

Из PowerShell:
1) cd D:\b2bplatform\backend
2) .\.venv\Scripts\activate
3) uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 [file:34]

Проверка:
- Invoke-RestMethod http://localhost:8000/api/v1/health → status = ok. [file:34]
- Invoke-RestMethod http://localhost:8000/openapi.json → 200. [file:34]

---

## Что в HANDOFF писать не надо

- Стектрейсы, симптомы падений, “почему не взлетело” — это в INCIDENTS. [file:34][file:39]
- Повторять один и тот же успех десятки раз — лучше дописать новый шаг (например: “добавили тесты / увеличили покрытие”). [file:34]

---

## Связка с PROJECT-RULES

PROJECT-RULES говорит: 
- после успешного шага → HANDOFF.md + обновить PROJECT-TREE.txt + commit + push origin/main; [file:38]
- после фейла → INCIDENTS.md + commit + push. [file:38]

HANDOFF.ru.md — только твоя пояснялка, SSoT остаётся в корневых файлах. [file:34][file:38]