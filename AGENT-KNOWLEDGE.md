# AGENT-KNOWLEDGE (digital trace)

## System map
- backend: FastAPI (API = endpoints), health: GET /health
- parser_service: http://127.0.0.1:9001 (dependency = backend calls it)

## Contracts (SSoT)
- API & DTO: api-contracts.yaml (contract = agreed request/response shapes)

## Runbooks (incident response)
- TBD

## Incident patterns
- TBD

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

