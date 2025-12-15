# B2B Platform — PROJECT RULES (SSoT)

Version: 1.2
Date: 2025-12-15

## SSoT
- API single source of truth: D:\b2bplatform\api-contracts.yaml
- If code != contract: code must be aligned to api-contracts.yaml (or contract updated intentionally).
- Priority: api-contracts.yaml -> PROJECT-RULES.md -> PROJECT-DOC.md
- SSoT files must live in repo root (D:\b2bplatform\). Do not duplicate them under backend\.

## Architecture (fixed)
transport -> usecases -> domain -> adapters

## Safety guards (mandatory before any repo change)
- Verify SSoT exists (api-contracts.yaml).
- Backup every file you will change: .bak.<timestamp>
- Show git status before/after
- Provide rollback (restore from .bak and/or git restore)

## PRE-FLIGHT before "fix API/routes/wiring"
Never assume defaults unless confirmed.
Plan A: read BASE_URL and API_PREFIX from runtime env/settings.
Plan B: ask the user for current base url (host:port) and API prefix.

Run and confirm:
1) GET {BASE_URL}/{API_PREFIX}/health -> status ok (or equivalent per contract)
2) GET {BASE_URL}/openapi.json -> 200 OK and valid JSON
3) python -c "import os; print(os.getenv('DATABASEURL'), os.getenv('DATABASE_URL'))"

## Standard tools (check availability first)
- Ruff: ruff check / ruff format (CI: ruff check + ruff format --check)
- pre-commit: pre-commit run --all-files
- just: prefer just (fmt/test/dev/clean) if available
- pyclean: prefer pyclean ., else PowerShell Plan B
- uv: prefer uv, else venv + pip Plan B
- direnv: prefer direnv, else explicit env vars Plan B

## Windows / PowerShell pitfalls
- Do not use bash heredoc in PowerShell (e.g. "python - << PY").
- In PowerShell, always escape $ref as `` `$ref ``.
- Do not call [regex]::Replace with RegexOptions (can bind to matchTimeout overload).
  Use: New-Object Regex(pattern, [RegexOptions]::Singleline) then .Replace().

## Progress logging
- Success -> HANDOFF.md append-only + update PROJECT-TREE.txt + commit + push origin/main
- Failure -> INCIDENTS.md append-only + commit + push origin/main