# Sprints

Rule: this is a living plan. Update checkboxes during work, and move items between sprints as reality changes.

## Sprint 1 (YYYY-MM-DD .. YYYY-MM-DD)
Goals:
- [ ] Define scope for Sprint 1 (fill dates and goals).
- [ ] Pick next API slice from api-contracts.yaml.
- [ ] Implement + tests + update HANDOFF.md.
- [ ] Update PROJECT-TREE.txt.

## Sprint 2 (YYYY-MM-DD .. YYYY-MM-DD)
Goals:
- [ ] TBD

## Sprint 3 (YYYY-MM-DD .. YYYY-MM-DD)
Goals:
- [ ] TBD
## 2025-12-17  Parsing: source/depth wiring (contract  backend)

Goal:
- Make moderator start-parsing accept {depth, source} per SSoT and wire it through backend  parser_service.

Done:
- [x] api-contracts.yaml: add requestBody StartParsingRequestDTO to POST /moderator/requests/{requestId}/start-parsing.
- [x] api-contracts.yaml: add ParsingRunSource enum (google|yandex|both).
- [x] backend: StartParsingRequestDTO updated to match SSoT (depth nullable, source nullable; removed resume).
- [x] backend: start_parsing accepts body payload; defaults depth=10, source=both; forwards to parser_service /parse.

Bugs/notes:
- [x] ruff F821: ParsingRunSource referenced before declaration  fixed via from __future__ import annotations in backend/app/transport/schemas/moderator_parsing.py.

Next:
- [ ] parser_service: accept source in /parse and implement google/yandex/both behavior (currently yandex-only).
- [ ] backend: optionally propagate per-URL/per-group source into ParsingDomainGroupDTO.source (requires parser_service to return source metadata).

