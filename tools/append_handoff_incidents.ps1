$handoffPath   = "D:\b2bplatform\HANDOFF.md"
$incidentsPath = "D:\b2bplatform\INCIDENTS.md"
$utf8NoBom = New-Object System.Text.UTF8Encoding($false)

if (!(Test-Path $handoffPath))   { throw "HANDOFF not found" }
if (!(Test-Path $incidentsPath)) { throw "INCIDENTS not found" }

$dt = [TimeZoneInfo]::ConvertTimeBySystemTimeZoneId([DateTime]::UtcNow, "Russian Standard Time")
$ts = $dt.ToString("yyyy-MM-dd HH:mm 'MSK'")

$incidentEntry = "`r`n- " + $ts + ": INCIDENT request_recipients inserts failed with NOT NULL violation (created_at/updated_at were NULL). Root cause: Alembic revision fbb98b9e9fc9 was created/applied with empty upgrade() (pass), so DB schema/defaults were not guaranteed; table/defaults were repaired manually to unblock. Fix: created request_recipients table via backend/tools/ensure_request_recipients_table.py, set DEFAULT now() + backfilled NULLs via backend/tools/fix_request_recipients_defaults.py, and added Alembic migration be4136aa1c68_request_recipients_defaults.py to make defaults/backfill repeatable. Verification: cd D:\b2bplatform\backend; alembic current -> be4136aa1c68 (head); python -m pytest -q -> 40 passed."

$handoffEntry = "`r`n- " + $ts + ": Implemented UserMessaging recipients replace-all. Changes: api-contracts.yaml updated schemas UpdateRecipientsRequest + RecipientsResponse and PUT /apiv1/userrequests/{requestId}/recipients now returns 200 RecipientsResponse; backend implemented transport DTOs (app/transport/schemas/user_messaging.py), router PUT recipients (app/transport/routers/user_messaging.py), usecase (app/usecases/update_request_recipients.py), DB repo method replace_recipients (app/adapters/db/repositories.py), ORM model RequestRecipientModel fixes (app/adapters/db/models.py), and added integration test tests/integration/test_recipients_replace_all.py. DB: applied Alembic head be4136aa1c68. Verification: cd D:\b2bplatform\backend; python -m pytest -q -> 40 passed."

# append (raw bytes to avoid BOM)
$incidentsBytes = [System.IO.File]::ReadAllBytes($incidentsPath)
$handoffBytes   = [System.IO.File]::ReadAllBytes($handoffPath)

$incidentEntryBytes = $utf8NoBom.GetBytes($incidentEntry)
$handoffEntryBytes  = $utf8NoBom.GetBytes($handoffEntry)

[System.IO.File]::WriteAllBytes($incidentsPath, $incidentsBytes + $incidentEntryBytes)
[System.IO.File]::WriteAllBytes($handoffPath, $handoffBytes + $handoffEntryBytes)

Write-Host "Appended OK:"
Write-Host " - INCIDENTS: $incidentsPath"
Write-Host " - HANDOFF: $handoffPath"