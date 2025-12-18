# TOOLS.md

Реестр repo-root tools (задокументировано, чтобы использовать в новых чатах).

## tools/regen_logs.py
- Назначение: регенерировать `HANDOFF.md` и `INCIDENTS.md` в канонический формат без дублей.
- Важное: перед перезаписью всегда архивирует оригиналы в `_log_archive/{YYYYMMDD-HHMMSS}/`.
- Вход: текущие `HANDOFF.md`, `INCIDENTS.md` (repo root).
- Выход: перезаписанные `HANDOFF.md`, `INCIDENTS.md` (repo root) + архив.
- Запуск:
  - `python .\tools\regen_logs.py --dry-run`
  - `python .\tools\regen_logs.py`
- Safety:
  - Проверка что после регенерации есть минимум 20 строк с `MSK`.
  - Проверка что слово `INCIDENT` не исчезло полностью.