# AGENT-KNOWLEDGE (digital trace)

## System map
- backend: FastAPI (API = endpoints), health: GET /health
- parser_service: http://127.0.0.1:9001 (dependency = backend calls it)

## Contracts (SSoT)
- API & DTO: api-contracts.yaml (contract = agreed request/response shapes)

## Runbooks (incident response)
- TBD

## Incident patterns
### Just recipe verification (commands-first)

Trigger:
- Need to suggest running a `just {recipe}` command (or claim a recipe exists).

Checks (facts first):
- `just --list` (preferred) OR `just -n {recipe}`.
- If the recipe is missing: do NOT suggest it; switch to Plan B (explicit commands/script path).

Decision:
- If recipe exists: suggest the exact `just {recipe}` command.
- If recipe does not exist: suggest Plan B (e.g., `powershell -NoProfile -ExecutionPolicy Bypass -File .\tools\update_project_tree.ps1`).

Verify:
- Paste the output of `just --list` or `just -n {recipe}` before proceeding.

## Decisions pointers
- See DECISIONS.md and PROJECT-DOC.md
## 2025-12-17 23:37 MSK  Lesson: ruff F821 on forward type refs (Enum below DTO)

Context:
- backend/app/transport/schemas/moderator_parsing.py: StartParsingRequestDTO referenced ParsingRunSource declared later.

Symptom (verified):
- just fmt / ruff failed with: F821 Undefined name 'ParsingRunSource'.

Fix (applied):
- Added 'from __future__ import annotations' near top of module to defer evaluation of type annotations.

Verification (verified):
- just fmt 
- pre-commit run --all-files 


## 2025-12-17 23:40 MSK  Lesson: SSoT-first for API behavior (DECISIONS != contract)

Context:
- Requirement: moderator chooses parsing source google/yandex/both (mentioned in docs/decisions).
- SSoT rule: API shapes are ONLY api-contracts.yaml.

Action:
- Verified api-contracts.yaml had no requestBody for POST /moderator/requests/{requestId}/start-parsing.
- Updated api-contracts.yaml to add StartParsingRequestDTO + ParsingRunSource (google|yandex|both).
- Only after SSoT update, aligned backend DTO + router to accept payload and forward to parser_service.

Verification (verified):
- pre-commit run --all-files -> Passed (ruff, ruff-format, validate OpenAPI contract).


## 2025-12-17 23:40 MSK  Addendum: F821 verification outputs

Expected:
- just fmt -> 'All checks passed!' and 'files left unchanged'
- pre-commit run --all-files -> all hooks 'Passed'


## 2025-12-17 23:41 MSK  Pattern: AGENT-KNOWLEDGE vs HANDOFF

Rule:
- HANDOFF.md = what changed (facts + files + verification).
- AGENT-KNOWLEDGE.md = reusable patterns (trigger  checks  decision  verify), no long change logs.

Why:
- Prevents duplication and keeps agent memory actionable.

## 2025-12-17 23:41 MSK  Pattern: SSoT-first for API behavior (DECISIONS != contract)

Trigger:
- Requirement is described in DECISIONS/PROJECT-DOC, but not confirmed in api-contracts.yaml.

Checks:
- git grep -n '<endpoint>' api-contracts.yaml
- Confirm requestBody/DTO exists in api-contracts.yaml.

Decision:
- If contract lacks the shape, update api-contracts.yaml first (explicit commit), then align code.

Verify:
- pre-commit run --all-files -> all hooks Passed.

## 2025-12-17 23:41 MSK  Pattern: ruff F821 for forward type refs

Trigger:
- Ruff error F821: type annotation references a symbol defined later in the module.

Fix options:
- Preferred: add 'from __future__ import annotations' near the top of module.
- Alternative: reorder declarations or use string annotations.

Verify:
- just fmt -> All checks passed!
- pre-commit run --all-files -> Passed


- 2025-12-18 0342 MSK Pattern Cyrillic mojibake in parserservice /parse (query becomes '?????'). Trigger: Russian words break but hardcoded Cyrillic like 'купить' is OK. Checks: retry request with Content-Type: application/json; charset=utf-8. Decision: document canonical PS command with charset and add server-side guard (return 400 with hint) when query contains '?'. Verify: Invoke-RestMethod http://127.0.0.1:9001/parse with charset returns correct URLs for query='цемент'.

TITLE AGENT-KNOWLEDGE digital trace - 2025-12-18 2101 MSK Runbook Parsing failed 503 to parserservice

Trigger
- parsing-status shows status failed and error contains 503 for http://127.0.0.1:9001/parse.

Checks (facts-first)
- netstat -ano | Select-String -SimpleMatch ':9001'
- Invoke-WebRequest http://127.0.0.1:9001 -UseBasicParsing -TimeoutSec 2 | Select-Object StatusCode
- If backend is running, capture payload: Invoke-RestMethod http://127.0.0.1:8000/moderator/requests/1/parsing-status | ConvertTo-Json -Depth 20

Decision
- If port 9001 is not LISTENING or HTTP unreachable: fix environment (start parserservice / start CDP) BEFORE touching backend code.
- Only debug backend logic after parserservice is reachable.

Verify
- Invoke-WebRequest http://127.0.0.1:9001 -UseBasicParsing -TimeoutSec 2 - Expected StatusCode 404/200.
- Re-run parsing-status - Expected status not failed due to 503.

TITLE AGENT-KNOWLEDGE digital trace - 2025-12-18 2101 MSK Pattern OpenAPI dump and PowerShell safety

Trigger
- Need to save runtime openapi.json for diffing or contract checks.

Rule
- Do NOT use ConvertTo-Json for OpenAPI dumps (depth limit 100) and avoid Set-Content/Out-File for important UTF-8 docs.

Preferred commands
- Invoke-WebRequest http://127.0.0.1:8000/openapi.json -OutFile .\.tmp\runtime-openapi.json
- python -c "import json; json.load(open('.\\.tmp\\runtime-openapi.json','r',encoding='utf-8')); print('ok')"

Verify
- python prints ok and file is readable UTF-8.
