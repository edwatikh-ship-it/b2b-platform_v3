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

