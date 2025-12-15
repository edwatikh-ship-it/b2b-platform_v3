# INCIDENTS — пояснялка (RU, NOT SSoT)

Оригинал: INCIDENTS.md (append-only). Этот файл — шпаргалка: как писать инциденты так, чтобы потом реально помогало. [NOT SSoT]

---

## Зачем нужен INCIDENTS.md

INCIDENTS.md — это “память о граблях”: что ломалось, почему, как починили, как проверить. [file:39]
Важно: это не чат-лог и не склад стектрейсов (иначе его перестанешь читать). [file:39]

---

## Жёсткий формат записи (обязательный)

Одна запись = 1–3 строки, и в ней всегда есть:
- datetime (MSK)
- symptom (что видно)
- root cause (почему)
- fix/mitigation (что сделали)
- verification (команда + ожидаемый результат) [file:39][file:38]

---

## Хорошие примеры (шаблоны)

### Пример 1: упал pytest на Windows
- 2025-..-.. ..:.. MSK INCIDENT: pytest падает с “Event loop is closed” на Windows → root cause: engine не закрывается → fix: lifespan + dispose() → verification: python -m pytest -q => PASS. [file:39]

### Пример 2: сломалась кодировка (UTF-8 BOM / кракозябры)
- 2025-..-.. ..:.. MSK INCIDENT: pytest ругается на '\\ufeff[pytest]' → root cause: файл записан с BOM → fix: переписать UTF‑8 без BOM через .NET UTF8Encoding(false) → verification: pytest -q => PASS. [file:39][file:38]

### Пример 3: не тот порт / backend не поднят
- 2025-..-.. ..:.. MSK INCIDENT: Invoke-RestMethod не коннектится → root cause: backend не слушает этот host:port → fix: найти свободный порт/запустить uvicorn → verification: GET /{prefix}/health => ok. [file:38]

---

## Что НЕ писать в INCIDENTS.md

- Длинные стектрейсы (лучше 1 строка “Symptom: …”, а детали в PR/коммите). [file:39]
- “Мы попробовали 10 способов” — оставь только финальную причину и рабочий фикс. [file:39]
- Дубликаты одной и той же проблемы (если повтор — добавь новую запись только если новый root cause/фикс). [file:39]

---

## Быстрые категории “типовых грабель” (чтобы быстрее диагностировать)

- ENV/DB:
  - DATABASEURL/DATABASE_URL не выставлен в текущем shell → alembic/импорт роутов падает. [file:38][file:39]
- PYTHONPATH:
  - pytest/alembic запускается не из той папки → ModuleNotFoundError (app не найден). [file:38][file:39]
- PowerShell ≠ bash:
  - heredoc не работает (python - << PY) → используем python -c или временный .py. [file:38][file:39]
- Кодировки:
  - Set-Content / неправильная запись файла → BOM/кракозябры → писать через WriteAllText + UTF8Encoding(false). [file:38][file:39]
- Порт 8000:
  - WinError 10048 → порт занят → либо прибить процесс, либо стартовать на другом порту. [file:39]

---

## Рулёжка по процессу

- Если шаг/задача завершилась фейлом → пишем в INCIDENTS.md и коммитим. [file:38]
- Если шаг успешный → пишем в HANDOFF.md (а не сюда). [file:34][file:38]