# tools/regen_logs.py

Назначение: привести `HANDOFF.md` и `INCIDENTS.md` к единому эталонному формату без дублей, **не теряя историю**.

## Что делает
- Берёт текущие файлы `D:\b2bplatform\HANDOFF.md` и `D:\b2bplatform\INCIDENTS.md`.
- Сохраняет их копии (оригиналы) в папку `_log_archive\{YYYYMMDD-HHMMSS}\`:
  - `_log_archive\{stamp}\HANDOFF.md`
  - `_log_archive\{stamp}\INCIDENTS.md`
- Генерирует новые канонические версии и **перезаписывает**:
  - `HANDOFF.md`
  - `INCIDENTS.md`

## Почему это не ломает append-only
Мы сохраняем полные оригиналы в `_log_archive` перед любым перезаписыванием, поэтому история не теряется.

## Safety checks
- Скрипт проверяет, что после генерации `INCIDENTS.md` содержит минимум 20 строк с `MSK`.
  Если меньше  падает с ошибкой, чтобы случайно не съесть файл неверным фильтром.

## Как запускать
Из корня репо:

- Dry-run:
  - `python .\tools\regen_logs.py --dry-run`

- Реальный прогон:
  - `python .\tools\regen_logs.py`

## Политика записи файлов
- UTF-8 без BOM
- LF окончания строк