# B2B Platform PROJECT RULES (SSoT)

Version: 1.4
Date: 2025-12-17

This document is SSoT for the development process (not for API).
Priority order (SSoT): api-contracts.yaml -> PROJECT-RULES.md -> PROJECT-DOC.md.

================================================================
HARD RULE 0: NO GUESSING / FACTS FIRST (ABSOLUTE)
================================================================
- Any debugging, commands, patches, refactors, API changes, or docs edits MUST start with facts.
- Forbidden: guessing file names, paths, base urls, prefixes, ports, env vars, endpoints, or shapes.
- Forbidden language: "probably", "likely", "should be", "it must be", when not proven by commands/output.
- If something is unknown: run commands to discover it, or ask the user and STOP.

================================================================
1) SSoT (Single Source of Truth)
================================================================
- API (endpoints, DTOs, responses) = ONLY api-contracts.yaml at repo root:
  D:\b2bplatform\api-contracts.yaml
- If implementation and contract diverge: it is an error.
  Fix by aligning code to the contract OR change the contract intentionally (with explicit commit).
- SSoT files must live in repo root D:\b2bplatform\ only.
  Forbidden: duplicates inside backend\.

================================================================
2) Architecture (fixed)
================================================================
Layer order is fixed and MUST NOT be violated:
transport -> usecases -> domain -> adapters

Meaning:
- transport: HTTP routes + IO validation only. NO business decisions.
- usecases: business scenarios and orchestration.
- domain: pure models/rules (no FastAPI/SQLAlchemy).
- adapters: DB/SMTP/HTTP clients and integrations.

================================================================
3) SAFETY GUARDS (MANDATORY BEFORE ANY REPO CHANGE)
================================================================
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
   - Forbidden for important files: Set-Content / Out-File rewrites (encoding risk).
   - Preferred: deterministic patch OR .NET WriteAllText with UTF8Encoding(false).

Artifacts policy (mandatory):
- Temporary files and backups MUST NOT clutter repo root.
- Allowed locations only:
  - D:\b2bplatform\.tmp\backups\
  - D:\b2bplatform\.tmp\tmp\
- Forbidden: creating/keeping repo-root tmp\ folder.

================================================================
4) PRE-FLIGHT (MANDATORY BEFORE ROUTE/WIRING/ENDPOINT CLAIMS)
================================================================
Do NOT assume defaults. BASE_URL and API_PREFIX MUST be discovered.

FACTS to collect (in THIS shell):
1) Runtime base URL (BASE_URL):
   - Plan A: read from launch config / env.
   - Plan B: ask the user for the exact running host:port.

2) Confirm backend is running:
   - If backend is NOT running: do NOT run HTTP checks yet.
   - Provide only start commands (just dev / just dev-noreload or Plan B), then re-run this PRE-FLIGHT.
   - Ensure you run checks against the actually running instance (host:port from the start command output).

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

================================================================
5) Standard tooling: "6 tools" (check availability first)
================================================================
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

================================================================
6) Windows / PowerShell pitfalls (MANDATORY)
================================================================
- Forbidden: bash heredoc in PowerShell (python - << PY).
- PowerShell: $ref inside strings must be escaped.
- Prefer Windows-safe commands. Avoid fragile quoting.
- Regex: avoid [regex]::Replace overload pitfalls; prefer Regex object then .Replace.
- Always write text as UTF-8 without BOM.

================================================================
7) Progress logging (MANDATORY)
================================================================
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

Chat safety / question gate:
- If a critical fact is missing (BASE_URL, API_PREFIX, env vars, target file content):
  ask up to 3 bold questions OR provide commands to discover the facts, then STOP.

================================================================
8) Language policy (SSoT docs)
================================================================
- SSoT docs language is English (ASCII preferred).
- docs-ru/ is NOT SSoT (explanations only).
- Append-only logs: one entry = one language, no forced translation.

================================================================
9) PowerShell path safety (MANDATORY)
================================================================
- Always anchor scripts to repo root:
  - Set-Location D:\b2bplatform OR use $PSScriptRoot + Join-Path
- Do not use Resolve-Path for non-existing targets.
- Any script that changes directory MUST restore it (Push-Location/Pop-Location).

================================================================
10) Mandatory preflight script (START HERE)
================================================================
- Before any work (dev/debug) and before any commit: run:
  - Set-Location D:\b2bplatform
  - .\tools\preflight.ps1 -BackendBaseUrl "<actual base url>"
- If preflight fails: fix environment/services first. Do NOT commit/push.

================================================================
11) One-click dev run (justfile)
================================================================
- Canonical local run uses repo-root justfile.
- If just is missing: use Plan B manual uvicorn commands from justfile docs.

================================================================
12) Assistant Response Format (WHY/EXPECT/IF FAIL/SA-note)
================================================================
Any multi-step instruction MUST include:
- WHY
- EXPECT
- IF FAIL
- SA-note

================================================================
13) CTX-FIRST + NO-PLACEHOLDERS (STRICT)
================================================================
- CTX-FIRST: run .\ctx.ps1 from repo root and paste output before fixes.
- NO-PLACEHOLDERS: commands must not contain placeholders like <FILE>, <PORT>, http://host:port.
  If unknown: first run a command that prints the real value, then proceed.

================================================================
14) Anti-Guessing Protocol (FACT-LOCK) (HARD)
================================================================
The assistant MUST NOT propose any patch/refactor/API change unless ALL items are present:

1) Repo root & SSoT presence:
   - Set-Location D:\b2bplatform
   - Test-Path .\api-contracts.yaml
   - Test-Path .\PROJECT-RULES.md

2) Git state:
   - git status -sb

3) Runtime base:
   - Invoke-RestMethod "$BASE_URL/openapi.json" | Out-Null (expect 200)
   - API_PREFIX is derived from OpenAPI paths (no assumptions).

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
- If a change modifies a data shape between layers:
  patch ALL impacted ends in the same instruction block. Partial rollouts forbidden.

WINDOWS-SAFE EXECUTION ONLY:
- Prefer .py/.sql temp files via WriteAllText, then run them.
- Avoid fragile quoting.

VERIFY OR ROLLBACK (MANDATORY):
- Each patch instruction MUST include backups + git status + rollback + verification commands.

QUESTION GATE:
- If critical facts are unknown: ask up to 3 bold questions or provide discovery commands, then STOP.

================================================================
15) Draft files policy (NO REPO TRASH)
================================================================
- New files created during experiments are TEMP by default.
- Preferred WIP location: D:\b2bplatform__WIP\
- If a draft must be in repo temporarily:
  - it MUST be in a clearly named folder and ignored by git.
- Before commit/push:
  - git status --porcelain must be clean (no accidental ?? files).

## Chat workflow additions (2025-12-17)

- Agent learning gate: Update AGENT-KNOWLEDGE.md / INCIDENTS.md only after a verified fix (commands + expected output).

- Error handling (human): When an error occurs, explain it in plain non-IT language and provide a recommendation.
- Incident logging timing: Always explain errors immediately, but write to INCIDENTS.md only after the issue is resolved (full picture: symptom, root cause, fix, verification).
- Dependent steps gate: If a next command depends on the previous command output, do not provide that next command until the user pasted the output.

================================================================
16) Communication style (project)
================================================================
- Tone: friendly "like a bro" (no flattery, only sober assessment).
- Emojis: allowed.
- Plain language: explain for non-IT stakeholders.
- Terminology: when using terms like API/DTO/pending/runbook, add short meaning in parentheses.
- After each multi-step instruction: add 2 short mentoring notes:
  - SA-note (for system analyst): purpose, architecture link, artifacts changed, alternatives.
  - Biz-note (for non-IT customer): what value it gives and why it matters.
- HARD: NO FALSE PROMISES. If something is unknown, collect facts first or ask, then STOP.

