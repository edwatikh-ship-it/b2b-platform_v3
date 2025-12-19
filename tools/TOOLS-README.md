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

## append_handoff_incidents.ps1 (daily usage)

Goal: Append ONE verified entry to HANDOFF.md or ONE incident entry to INCIDENTS.md without manual editing.

Rules:
- Preferred (PowerShell): & .\tools\append_handoff_incidents.ps1 ...
- Do NOT use: powershell.exe -File .\tools\append_handoff_incidents.ps1 ... (argument binding issues for string[]).
- Any literal text containing $ (examples: $env:NAME, $true, $false) MUST be passed in single quotes to avoid interpolation.

Verification:
- Use Select-String on HANDOFF.md / INCIDENTS.md to confirm the new entry exists (timestamp or unique phrase).
Из корня репо:

- Dry-run:
  - `python .\tools\regen_logs.py --dry-run`

- Реальный прогон:
  - `python .\tools\regen_logs.py`

## Политика записи файлов
- UTF-8 без BOM
- LF окончания строк