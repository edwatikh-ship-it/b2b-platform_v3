# AGENT-KNOWLEDGE (reusable playbooks)

Version: 1.0
Date: 2025-12-18
Status: Active

Purpose:
- This file stores reusable troubleshooting and delivery patterns (how to act).
- It must NOT duplicate HANDOFF.md (what changed) or INCIDENTS.md (what failed).
- Keep entries short, actionable, and tool/command oriented.

SSoT reminder:
- API shapes/endpoints: api-contracts.yaml
- Process rules: PROJECT-RULES.md
- Product rules: PROJECT-DOC.md


## System map (local dev)

- backend: FastAPI, health endpoint is GET /health.
- parser_service: http://127.0.0.1:9001 (backend depends on it for parsing).


## Golden rules (agent)

- Facts first: never guess ports, prefixes, paths, env vars, or endpoint shapes.
- SSoT order: api-contracts.yaml -> PROJECT-RULES.md -> PROJECT-DOC.md.
- If something is unknown: collect facts via commands or ask, then STOP.
- Keep “what changed” out of this file (put it into HANDOFF.md).


## Playbooks

### Playbook: Just recipe verification (commands-first)
Trigger:
- Need to suggest running `just <recipe>` or claim a recipe exists.

Checks:
- `just --list` (preferred), or `just -n <recipe>`.

Decision:
- If recipe exists: suggest exact `just <recipe>`.
- If missing: do NOT suggest it; provide Plan B explicit commands.

Verify:
- Ask for pasted output of `just --list` or `just -n <recipe>` before continuing.


### Playbook: SSoT-first for API behavior
Trigger:
- A requirement is described in docs/chat, but not in api-contracts.yaml.

Checks:
- Confirm endpoint + request/response DTO exists in api-contracts.yaml.

Decision:
- If contract lacks the shape: update api-contracts.yaml first (explicit commit), then align backend.
- If contract has the shape: align backend to contract.

Verify:
- Run contract validation / tests (project-specific).
- Confirm runtime OpenAPI includes the path (GET /openapi.json) and contract diff is clean.


### Playbook: PRE-FLIGHT before any routing/wiring claims
Trigger:
- About to debug “endpoint not found”, “route missing”, “OpenAPI incomplete”, or “prefix mismatch”.

Checks (in the same shell):
1) Discover BASE_URL (do not assume).
2) `Invoke-RestMethod "$BASE_URL/openapi.json" | Out-Null` (expect 200).
3) Derive API_PREFIX from OpenAPI paths (do not assume).
4) `Invoke-RestMethod "$BASE_URL/health"` or `"$BASE_URL/$API_PREFIX/health"` (expect status="ok").
5) If DB may be required at import-time:
   `python -c "import os; print(os.getenv('DATABASEURL'), os.getenv('DATABASE_URL'))"`

Decision:
- If any check fails: fix runtime/env first (Plan B commands), do NOT propose code changes.

Verify:
- Repeat the checks above until green.


### Playbook: Ruff F821 on forward type refs (Python typing)
Trigger:
- Ruff error F821 due to type annotation referencing a symbol defined later in the module.

Fix options:
- Preferred: add `from __future__ import annotations` near the top of the module.
- Alternative: reorder declarations or use string annotations.

Verify:
- `ruff check`
- `ruff format --check`
- `pre-commit run --all-files`


### Playbook: Cyrillic mojibake in HTTP requests (Windows)
Trigger:
- Russian text in JSON request becomes `?????` on the server side.

Checks:
- Retry with explicit charset:
  `-ContentType "application/json; charset=utf-8"`

Decision:
- Document a canonical PowerShell request example using charset.
- Add a server-side guard for suspicious query containing '?' (return 400 with a hint).

Verify:
- Same request returns correct Cyrillic on the server side.
