# B2B Platform PROJECT RULES (SSoT)

Version: 2.0
Date: 2025-12-18

This document is SSoT for the development process (not for API).
Priority order (SSoT): api-contracts.yaml -> PROJECT-RULES.md -> PROJECT-DOC.md.

============================================================
HARD RULE 0: NO GUESSING / FACTS FIRST (ABSOLUTE)
============================================================
- Any debugging, commands, patches, refactors, API changes, or docs edits MUST start with facts.
- Forbidden: guessing file names, paths, base URLs, prefixes, ports, env vars, endpoints, or response shapes.
- Forbidden language: "probably", "likely", "should be", "it must be" unless proven by commands/output.
- If something is unknown: run commands to discover it OR ask the user a precise question and STOP.

============================================================
HARD RULE 1: COMMANDS-ONLY CHAT (COPY/PASTE POWERSHELL)
============================================================
- Every actionable instruction MUST be provided as PowerShell commands the user can copy-paste.
- Do not write "edit file X" without providing the exact command(s) that perform the change safely.
- If a next step depends on previous output: request the output first, then provide the next commands.
- Placeholders are forbidden (no <FILE>, <PORT>, http://host:port). If unknown: discover via commands first.

============================================================
1) SSoT (Single Source of Truth)
============================================================
- API (endpoints, DTOs, responses) = ONLY:
  D:\b2bplatform\api-contracts.yaml
- If implementation and contract diverge: it is an error.
  Fix by aligning code to the contract OR change the contract intentionally (with explicit commit).
- SSoT files must live in repo root D:\b2bplatform\ only.
  Forbidden: duplicates inside backend\.

============================================================
2) Architecture (fixed)
============================================================
Layer order is fixed and MUST NOT be violated:
transport -> usecases -> domain -> adapters

Meaning:
- transport: HTTP routes + IO validation only. NO business decisions.
- usecases: business scenarios and orchestration.
- domain: pure models/rules (no FastAPI/SQLAlchemy).
- adapters: DB/SMTP/HTTP clients and integrations.

============================================================
3) SAFETY GUARDS (MANDATORY BEFORE ANY REPO CHANGE)
============================================================
Before changing any tracked file:

1) Verify repo root and SSoT presence:
   - Set-Location D:\b2bplatform
   - Test-Path .\api-contracts.yaml
   - Test-Path .\PROJECT-RULES.md

2) Show git status BEFORE and AFTER:
   - git status -sb

3) Backup every changed file BEFORE editing:
   - Backups MUST go to: D:\b2bplatform\.tmp\backups\
   - Backup name: <file>.bak.<timestamp>

4) Rollback MUST be provided:
   - Restore from .bak OR `git restore <path>`

5) Encoding rule (mandatory):
   - Text files must be UTF-8 without BOM.
   - Forbidden for important files: Set-Content / Out-File full rewrites (encoding risk).
   - Preferred: deterministic patch OR .NET WriteAllText with UTF8Encoding(false).

Artifacts policy (mandatory):
- Temporary files and backups MUST NOT clutter repo root.
- Allowed locations only:
  - D:\b2bplatform\.tmp\backups\
  - D:\b2bplatform\.tmp\tmp\
- Forbidden: creating/keeping any other repo-root tmp folders.

============================================================
4) PRE-FLIGHT (MANDATORY BEFORE ROUTE/WIRING/ENDPOINT CLAIMS)
============================================================
Do NOT assume defaults. BASE_URL and API_PREFIX MUST be discovered.

FACTS to collect (in THIS shell):

1) Runtime base URL (BASE_URL):
   - Plan A: read from launch config / env.
   - Plan B: ask the user for the exact running host:port.

2) Confirm backend is running:
   - If backend is NOT running: do NOT run HTTP checks yet.
   - Provide only start commands (just dev / just dev-noreload or Plan B), then re-run this PRE-FLIGHT.
   - Ensure checks target the actually running instance (host:port from the start command output).

3) Runtime OpenAPI must be reachable:
   - Invoke-RestMethod "$BASE_URL/openapi.json" | Out-Null
   - Expect: HTTP 200 and valid JSON.

4) API_PREFIX detection rule:
   - Detect prefix from runtime OpenAPI paths. Do NOT assume apiv1.
   - If OpenAPI includes "/health": API_PREFIX is empty.
   - If OpenAPI includes "/apiv1/health": API_PREFIX is "apiv1".

5) Health check:
   - Invoke-RestMethod "$BASE_URL/$API_PREFIX/health" (or "$BASE_URL/health" if API_PREFIX is empty)
   - Expect: JSON with status="ok" (or contract equivalent).

6) DB env in CURRENT shell (only if routers/imports require DB):
   - python -c "import os; print(os.getenv('DATABASEURL'), os.getenv('DATABASE_URL'))"
   - If import-time DB is used and env is missing: STOP and fix env before debugging.

If any PRE-FLIGHT check fails:
- Provide only Plan B commands to fix environment/services first.
- Do NOT propose code changes.

============================================================
5) Standard tooling: "6 tools" (check availability first)
============================================================
Tools: ruff, pre-commit, pyclean, uv, direnv, just

Rule:
- Always check first (no assumptions):
  - Get-Command ruff, pre-commit, pyclean, uv, direnv, just -ErrorAction SilentlyContinue
- If missing:
  - Provide Plan B commands (no installation promises).

Usage:
- Lint/format:
  - ruff check backend
  - ruff format backend
  - CI: ruff check + ruff format --check
- Hooks:
  - pre-commit run --all-files
- Routine:
  - just fmt / just test / just dev / just clean (if present)
- Cleanup:
  - pyclean . (if present)
  - Plan B: remove __pycache__ via PowerShell
- Dependencies:
  - Prefer uv
  - Plan B: python -m venv + pip install
- Env:
  - Prefer direnv
  - Plan B: set env vars explicitly in the SAME shell as the running command

============================================================
6) Windows / PowerShell pitfalls (MANDATORY)
============================================================
- Forbidden: bash heredoc in PowerShell (python - << PY).
- PowerShell: $ref inside strings must be escaped.
- Prefer Windows-safe commands. Avoid fragile quoting.
- Regex: avoid [regex]::Replace overload pitfalls; prefer Regex object then .Replace.
- ConvertTo-Json has a hard max depth (100). Do not use it to dump OpenAPI.
- Always write text as UTF-8 without BOM.

============================================================
7) Progress logging (MANDATORY)
============================================================
Success:
- Append-only: HANDOFF.md
- Update: PROJECT-TREE.txt
- Commit + push origin/main

Failure:
- Append-only: INCIDENTS.md
- Commit + push origin/main

HANDOFF/INCIDENTS entry format:
- Datetime (MSK)
- What happened / what was done
- Root cause
- Fix/Mitigation
- Verification command + expected output
- Files touched (paths)

============================================================
8) Language policy (docs)
============================================================
- Repository documentation language is English only.
- Russian is allowed only for live chat communication.
- Append-only logs: one entry = one language, no forced translation.

============================================================
9) PowerShell path safety (MANDATORY)
============================================================
- Always anchor scripts to repo root:
  - Set-Location D:\b2bplatform OR use $PSScriptRoot + Join-Path
- Do not use Resolve-Path for non-existing targets.
- Any script that changes directory MUST restore it (Push-Location/Pop-Location).

============================================================
10) Mandatory preflight script (START HERE)
============================================================
- Before any work (dev/debug) and before any commit: run:
  - Set-Location D:\b2bplatform
  - .\tools\preflight.ps1 -BackendBaseUrl "<actual base url>"
- If preflight fails: fix environment/services first. Do NOT commit/push.

============================================================
11) One-click dev run (justfile)
============================================================
- Canonical local run uses repo-root justfile.
- If just is missing: use Plan B manual uvicorn commands from justfile docs.

============================================================
12) Assistant message format (chat)
Ambiguity gate (HARD):
- Before documenting a rule or giving a multi-step instruction, read the current target document section.
- Check that wording is unambiguous (no multiple interpretations).
- If ambiguity is detected: STOP, ask a clarifying question OR propose an exact rewrite, then wait for confirmation.
============================================================
Any multi-step instruction MUST include:
- WHY
- EXPECT
- IF FAIL

Additionally, every message must include two short explanations:
- Customer mode (plain Russian, no IT terms, focus on value/outcome).
- Junior analyst mode (simplified explanation + small metaphor).

============================================================
13) CTX-FIRST + NO-PLACEHOLDERS (STRICT)
============================================================
- CTX-FIRST: run .\ctx.ps1 from repo root and paste output before fixes.
- NO-PLACEHOLDERS: commands must not contain placeholders. If unknown: discover first.

============================================================
14) Anti-Guessing Protocol (FACT-LOCK) (HARD)
============================================================
The assistant MUST NOT propose any patch/refactor/API change unless ALL items are present:

1) Repo root & SSoT presence:
   - Set-Location D:\b2bplatform
   - Test-Path .\api-contracts.yaml
   - Test-Path .\PROJECT-RULES.md

2) Git state:
   - git status -sb

3) Runtime base:
   - Invoke-RestMethod "$BASE_URL/openapi.json" | Out-Null (expect 200)
   - API_PREFIX is derived from OpenAPI paths (no assumptions)

4) DB env in CURRENT shell:
   - python -c "import os; print(os.getenv('DATABASEURL'), os.getenv('DATABASE_URL'))"

5) Target code snapshot for EVERY file to be patched:
   - Get-Content <path> -Raw
   - OR Select-String <path> -Pattern "<anchor>" -Context <n>,<n>

If any item is missing:
- Provide only commands to collect facts.
- Then STOP.

STOP-ON-MISMATCH (PATCH SAFETY):
- Any patch MUST validate that expected anchor blocks exist.
- If anchor block is not found: STOP and request a fresh snapshot.
- Fallback/guess patches are forbidden.

ATOMIC CROSS-LAYER CHANGES:
- If a change modifies a data shape between layers: patch ALL impacted ends in the same instruction block.

VERIFY OR ROLLBACK (MANDATORY):
- Each patch instruction MUST include backups + git status + rollback + verification commands.

============================================================
15) Draft files policy (NO REPO TRASH)
============================================================
- New files created during experiments are TEMP by default.
- Preferred WIP location: D:\b2bplatform__WIP\
- If a draft must be in repo temporarily:
  - it MUST be in a clearly named folder and ignored by git.
- Before commit/push:
  - git status --porcelain must be clean (no accidental ?? files).

============================================================
16) Freedom + confirmation (structure evolution)
============================================================
- The assistant may propose new docs/folder structure to improve maintainability.
- Any deletion or merging of existing docs/log files requires explicit user confirmation.

============================================================
17) Documentation style guide (single style, fact-only)
============================================================
All operational documentation must follow the same style:

A) "RUNBOOK" entries (how to run / debug):
- Goal
- Preconditions
- Commands (PowerShell)
- Expected output
- If fail (Plan B)
- Artifacts touched (files/paths)

B) "LOG" entries (HANDOFF/INCIDENTS):
- Timestamp (MSK)
- Context (what feature/endpoint/service)
- Symptom or Change
- Root cause (if known)
- Fix/Mitigation
- Verification commands + expected output
- Files touched
