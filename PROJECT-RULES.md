<!-- write-test 2025-12-16T20:00:42.8821983+03:00 -->
# B2B Platform Р Р†Р вЂљРІР‚Сњ PROJECT RULES (SSoT)

Version: 1.3
Date: 2025-12-15

## 1) SSoT (Single Source of Truth)
- API (endpoints, DTOs, responses) = ONLY api-contracts.yaml at repo root: D:\b2bplatform\api-contracts.yaml.
- If implementation and contract diverge Р Р†Р вЂљРІР‚Сњ it's an error. Align code to contract (or change contract intentionally).
- Priority: api-contracts.yaml Р Р†РІР‚В РІР‚в„ў PROJECT-RULES.md Р Р†РІР‚В РІР‚в„ў PROJECT-DOC.md.
- SSoT files must live in repo root D:\b2bplatform\ (no duplicates inside backend\).
- Progress = state of GitHub main branch, not chat memory.

## 2) Architecture (fixed)
transport Р Р†РІР‚В РІР‚в„ў usecases Р Р†РІР‚В РІР‚в„ў domain Р Р†РІР‚В РІР‚в„ў adapters

Short meaning:
- transport: HTTP routes + input/output validation; no business decisions.
- usecases: business scenarios.
- domain: pure models/rules (no FastAPI/SQLAlchemy).
- adapters: DB/SMTP/HTTP clients and other integrations.

## 3) SAFETY GUARDS (mandatory before any repo changes)
Before any change:
- Verify D:\b2bplatform\ exists and api-contracts.yaml is present.
- Backup every changed file: *.bak.<timestamp>.
- Show git status before and after.
- Provide rollback: restore from .bak and/or git restore.

## 4) PRE-FLIGHT before any Р Р†Р вЂљРЎС™fix routes/endpointsР Р†Р вЂљРЎСљ
Do NOT guess defaults.

First discover:
- BASE_URL (host:port) and API_PREFIX (e.g. apiv1).
  - Plan A: read from runtime env / start config.
  - Plan B: ask user explicitly.

Run checks (expected results):
1) Invoke-RestMethod "{BASE_URL}/{API_PREFIX}/health"
   - Expect JSON with status = "ok" (or contract equivalent).
2) Invoke-RestMethod "{BASE_URL}/openapi.json" | Out-Null
   - Expect 200 and valid JSON.
3) python -c "import os; print(os.getenv('DATABASEURL'), os.getenv('DATABASE_URL'))"
   - Must be non-None only if routes/import-time DB requires it.

If any check fails Р Р†Р вЂљРІР‚Сњ provide Plan B commands first (how to start backend / set env), then propose code changes.

## 5) Р Р†Р вЂљРЎС™6 toolsР Р†Р вЂљРЎСљ standard (check availability first)
Tools: ruff, pre-commit, pyclean, uv, direnv, just.

Rule:
- Always check first: Get-Command ruff/pre-commit/pyclean/uv/direnv/just
- If missing Р Р†Р вЂљРІР‚Сњ use Plan B (no assumptions).

Usage:
- Lint/format:
  - ruff check backend
  - ruff format backend
  - (CI: ruff check + ruff format --check)
- Hooks:
  - pre-commit run --all-files
- Routine commands:
  - just fmt / just test / just dev / just clean (if present)
- Cleanup:
  - pyclean . (if present)
  - Plan B: remove __pycache__ via PowerShell
- Dependencies:
  - prefer uv
  - Plan B: python -m venv + pip install
- Env:
  - prefer direnv
  - Plan B: set env vars explicitly in the same shell session

## 6) Windows / PowerShell pitfalls
- Do not use bash heredoc in PowerShell (e.g. python - << PY).
- PowerShell: $ref inside strings must be escaped as ` $ref ` (otherwise treated as a variable).
- .NET Regex in PowerShell:
  - avoid [regex]::Replace with RegexOptions (can bind to matchTimeout overload),
  - correct: New-Object Regex(pattern, [RegexOptions]::Singleline) then .Replace().
- Text file writes: UTF-8 without BOM (unless strong reason). Prefer .NET WriteAllText with UTF8Encoding(false).

## 7) Progress logging (mandatory)
- Success Р Р†РІР‚В РІР‚в„ў HANDOFF.md (append-only) + update PROJECT-TREE.txt + commit + push origin/main.
- Failure Р Р†РІР‚В РІР‚в„ў INCIDENTS.md (append-only) + commit + push.

HANDOFF/INCIDENTS format:
- Datetime (MSK)
- What happened / what was done
- Root cause
- Fix/Mitigation
- Verification (command + expected output)

### Chat safety: Step 0 / Question gate (2025-12-15)
- Step 0 for any new chat: run Р Р†Р вЂљРЎС™Detect backend + PRE-FLIGHTР Р†Р вЂљРЎСљ PowerShell script to discover BASE_URL and verify /{API_PREFIX}/health + /openapi.json.
- Do NOT assume BASE_URL / API_PREFIX. Use detection or explicit user confirmation.
- Default: never auto-kill processes. Provide a separate explicit command to stop a PID if needed.
- Question gate: if a critical question is asked (BASE_URL/API_PREFIX/DATABASEURL/etc) and no answer is given, do not proceed; repeat the question in one short line and wait.
- Goal: minimize wasted time on wrong port/env/shell.

### Env: DATABASEURL source (2025-12-15)
- DATABASEURL must be stored in D:\b2bplatform\backend.env (local-only, do not commit).
- Before uvicorn/alembic, ensure this shell loads backend.env (or explicitly exports DATABASEURL).
- Verify: python -c "import os; print(os.getenv('DATABASEURL'), os.getenv('DATABASE_URL'))" must not show None None.

### Alembic on Windows: always set PYTHONPATH (2025-12-15)
- Before alembic on Windows set: ="D:\b2bplatform\backend"
- Verify: cd D:\b2bplatform\backend; alembic current runs and prints current revision.

## 8) Language policy (SSoT docs)
- Source language for SSoT docs is English (ASCII preferred for maximum compatibility).
- Do NOT maintain mandatory RU+EN duplicates for every update (avoids double work and noisy logs).
- Russian docs live under docs-ru/ as NOT SSoT explanations only.
- For append-only logs (HANDOFF.md / INCIDENTS.md / DECISIONS.md): one entry = one language, no required translation; keep the required structure and verification commands.
## PowerShell path safety (mandatory)

- Always anchor scripts to repo root (use Set-Location D:\b2bplatform or $PSScriptRoot + Join-Path), never rely on current working directory.
- Do not use Resolve-Path for a file that does not exist yet; write using a direct path (Join-Path) or create the file first.
- Any script that changes directory must restore it (Push-Location + Pop-Location in inally) to avoid breaking subsequent commands.


### Runtime base URL & port rules (2025-12-15)
- Never assume API prefix. Always discover it from the running OpenAPI: GET {BASE_URL}/openapi.json.
- If OpenAPI paths start with '/apiv1', use '{BASE_URL}/apiv1/...' (example: /apiv1/health).
- If OpenAPI paths do NOT start with '/apiv1' (paths like '/health', '/user/...', '/moderator/...'), then API_PREFIX is empty and health is '{BASE_URL}/health'.
- Always validate the chosen base before changing code: request the exact health endpoint that exists in OpenAPI.

### Port hygiene / avoiding \"wrong port\" (2025-12-15)
- Always check ports before starting services:
  - Backend default: 8000
  - Parser service default: 9001
  - Chrome CDP default: 9222

### Parser service preflight (mandatory)
- If Moderator parsing endpoints are used (/moderator/requests/{requestId}/start-parsing):
  - Ensure parser_service is running and reachable BEFORE debugging backend logic.
  - Symptom: parsing-status shows status=failed with error "All connection attempts failed" for keys.
  - Fix: start parser_service (default http://127.0.0.1:9001) and re-run start-parsing.

PowerShell checks:
- Plan A (if available): Get-NetTCPConnection -LocalPort 9001 -State Listen
- Plan B (Windows-safe): netstat -ano | findstr ":9001"
- HTTP ping (404 is OK; connection refused is NOT OK):
  - try { Invoke-WebRequest "http://127.0.0.1:9001/" -UseBasicParsing -TimeoutSec 2 | Select-Object StatusCode } catch { $_.Exception.Message }

Start command (run in a separate shell):
- Set-Location D:\b2bplatform\parser_service
- python -m uvicorn app.main:app --host 127.0.0.1 --port 9001
- PowerShell checks:
  - Get-NetTCPConnection -LocalPort 8000 -State Listen
  - Get-NetTCPConnection -LocalPort 9001 -State Listen
  - Get-NetTCPConnection -LocalPort 9222 -State Listen
- If a port is occupied, do NOT guess. Identify owning PID and command line, then stop explicitly:
  - \8424 = (Get-NetTCPConnection -LocalPort 8000 -State Listen | Select-Object -First 1).OwningProcess
  - Get-CimInstance Win32_Process -Filter \"ProcessId=\8424\" | Select-Object ProcessId, Name, CommandLine
  - Stop-Process -Id \8424 -Force
- Always run backend and parser_service in separate shells and stop them via Ctrl+C when done.

<!-- PRE-FLIGHT-RULE-BEGIN -->
## Mandatory preflight (START HERE)

- Before any work (dev/debug) and before any commit: run .\tools\preflight.ps1 from D:\b2bplatform.
- If preflight fails: fix environment/services first (follow the script hints). Do not commit/push while failing.
- Only push to main after preflight passes in the current session.
<!-- PRE-FLIGHT-RULE-END -->

Preflight example (Windows PowerShell):
- Set-Location D:\b2bplatform
- .\tools\preflight.ps1 -BackendBaseUrl "http://127.0.0.1:8000"

Interpretation rule:
- If preflight says Detected API_PREFIX is empty and health path is /health, then use BASE_URL + /health and other root paths (no /apiv1).
- If preflight says API_PREFIX is "apiv1", then use BASE_URL + /apiv1/health, etc.
## One-click dev run (justfile)

- This repo uses 'just' and a repo-root 'justfile' as the canonical way to start services locally.
- Quick start (two terminals): run 'just up' (starts backend on 127.0.0.1:8000 and parser_service on 127.0.0.1:9001), then run 'just smoke' to verify endpoints.
- Manual start: 'just dev-noreload' (backend) and 'just parser' (parser_service). Use Ctrl+C to stop.
- If 'just' is missing, install it (Plan B: run uvicorn commands manually as documented in justfile).

## Assistant Response Format (WHY/EXPECT/IF FAIL)

When the assistant provides commands or steps, each step MUST include a short explanation block in Russian:

- WHY: why we do this step (plain language).
- EXPECT: what output/result is expected.
- IF FAIL: what to do if the expectation is not met.
- SA-note: a short systems-analyst note (risk, assumption, dependency, acceptance signal).

This is mandatory for any multi-step instruction, any repo change, and any debugging flow.


## Chat Efficiency Guardrails (CTX-FIRST)

- CTX-FIRST: Before asking for help or applying fixes, run `.\ctx.ps1` from repo root and paste the output into chat.
  This reduces wrong commands due to missing context (cwd, env vars, tools, git state).
- NO-PLACEHOLDERS: Never paste commands with placeholders like `<FILE>`, `<PORT>`, `http://host:port`.
  If a value is unknown, first run a command that prints the real value (example: "last migration file") and then use it.
- NO-RAW-SETCONTENT: Avoid rewriting important repo files with `Set-Content` / `Out-File` (encoding/BOM risk).
  Prefer deterministic patches or `.NET` `WriteAllText` with UTF-8 *without BOM* where possible.
- PRE-COMMIT-FIX-LOOP: If pre-commit hooks modify files, the commit will fail by design.
  Run `git status`, then `git add -A`, then retry `git commit`.




## Clarifying Questions Gate (Bold Questions)

- Diagnostics are allowed with partial context (to gather facts), but MUST state assumptions and expected signals.
- Repo changes (code/docs) MUST NOT proceed if there is ambiguity in requirements, acceptance criteria, base URL/prefix, env vars, or target files.
- In such cases, the assistant MUST ask up to 3 clarifying questions (formatted in **bold**) and wait for answers.
- If there is a critical blocker/risk, the assistant MAY ask more than 3 questions, but MUST justify why the extra questions are required.
- If answers are missing, provide a short Plan B: commands to discover the missing facts instead of guessing.


## PROJECT-TREE DoD (Key Artifacts)

- PROJECT-TREE.txt is a curated list of key artifacts (not a full file dump).
- Update PROJECT-TREE.txt at the end of a milestone (when adding/renaming/moving key files or changing structure), together with HANDOFF entry.
- Use: powershell: Set-Location D:\b2bplatform; .\tools\update_project_tree.ps1


## Project tree command (Preferred)

- Preferred: `just tree`
- Plan B: powershell: Set-Location D:\b2bplatform; .\tools\update_project_tree.ps1
- When the assistant asks for project structure context, provide the output of `just tree` (or Plan B).


TITLE B2B Platform PROJECT RULES SSoT - Anti-Guessing Protocol (FACT-LOCK)
Date: 2025-12-16
Status: HARD RULES (must follow)

HARD RULE 5  FACT-LOCK (NO GUESSING)
- The assistant MUST NOT propose any code patch, refactor, or API change unless the following FACT-LOCK bundle is present in the chat (copy/paste outputs).
- If any item is missing: the assistant MUST provide only commands to collect facts (no fixes, no "likely", no "should", no assumptions).

FACT-LOCK bundle (required):
1) Repo root & SSoT presence:
   - Run from repo root (D:\b2bplatform):
     - Test-Path .\api-contracts.yaml
     - Test-Path .\PROJECT-RULES.md
2) Git state:
   - git status -sb
3) Runtime base:
   - Invoke-RestMethod "$BASE_URL/openapi.json" | Out-Null  (expect 200)
   - Detect API prefix from OpenAPI paths; do NOT assume.
4) DB env in CURRENT SHELL:
   - python -c "import os; print(os.getenv('DATABASEURL'), os.getenv('DATABASE_URL'))"
5) Target code snapshot for EVERY file to be patched:
   - Provide exact function content using either:
     - Get-Content <path> -Raw
     - OR Select-String <path> -Pattern "<anchor>" -Context <n>,<n>

HARD RULE 6  STOP-ON-MISMATCH (PATCH SAFETY)
- Any deterministic patch MUST validate that the expected anchor block exists.
- If the anchor block is NOT found (e.g. "Expected block not found"):
  - The assistant MUST STOP.
  - The assistant MUST request a fresh code snapshot (FACT-LOCK item #5) and only then re-generate a patch.
- "Fallback guess patches" are forbidden.

HARD RULE 7  ATOMIC CROSS-LAYER CHANGES
- If a change modifies a data shape between layers (transport <-> adapters <-> domain):
  - The assistant MUST patch ALL impacted ends in the same instruction block (atomic change).
  - Example: if transport expects (url, comment, created_at), adapters MUST be patched in the same step to return exactly that.
- Partial rollouts are forbidden.

HARD RULE 8  WINDOWS-SAFE EXECUTION ONLY
- PowerShell quoting pitfalls are treated as a risk; verification commands MUST be Windows-safe.
- Forbidden:
  - multi-line python -c
  - fragile CLI invocations that depend on escaping (psql -c in PowerShell)
- Allowed (preferred):
  - Create a temporary .py/.sql file via .NET WriteAllText (UTF-8 no BOM), then execute it.
  - Or use just recipes (just dev/test/smoke).

HARD RULE 9  VERIFY OR ROLLBACK (MANDATORY)
- Every patch instruction MUST include:
  - SAFETY GUARDS:
    - backup of every changed file: <file>.bak.<timestamp>
    - git status before and after
    - rollback commands (restore from .bak and/or git restore)
  - Verification commands (must be runnable):
    - python -m py_compile <changed files> OR python -m compileall <dir>
    - ruff check backend (Plan B if missing: python -m compileall backend)
    - minimal API smoke (exact endpoints from OpenAPI)

HARD RULE 10  QUESTION GATE
- If any critical fact is unknown (BASE_URL, API_PREFIX, env var names, target function text),
  the assistant MUST ask up to 3 short questions (bold) OR provide commands to discover the fact,
  then wait. No further steps until answered.

TITLE Draft files policy (no repo trash)
- Rule: Any new file created during experiments is TEMP by default and must not land in main unless it is needed for production/dev workflow.
- Draft/WIP storage:
  - Preferred: keep drafts outside the repo (e.g., D:\b2bplatform__WIP\) and copy into repo only when promoted.
  - If a draft must be in repo temporarily, it must be in a clearly named folder and ignored by git (do not leave random ?? files in backend/).
- Promote-to-repo checklist (required):
  - The file is referenced/used (imported, executed, wired) by the codebase or documented tooling flow.
  - Verification exists and is runnable: pre-commit run --all-files (and/or just test / API smoke when relevant).
  - Documentation updated when needed: PROJECT-DOC.md and PROJECT-TREE.txt (key artifacts only).
- Commit gate:
  - Before commit/push: git status --porcelain must be clean (no accidental ?? files).
- Added: 2025-12-16 23:03 MSK
