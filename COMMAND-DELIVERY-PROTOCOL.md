# Command Delivery Protocol (Chat -> PowerShell)

This repository follows an output contract: the assistant must respond with either (1) copy/paste PowerShell commands or (2) a full file replacement. This protocol defines how commands must be delivered so they are safe, deterministic, and reviewable.

## Rules

- Use a PowerShell code block for commands.
- Put only commands inside the code block (no explanations, no comments).
- One command per line.
- No aliases. Use full cmdlet names (for example: Invoke-RestMethod, not irm).
- No placeholders (for example: FILE, PORT, BASE_URL). If a value is unknown, first provide discovery commands and STOP.
- Prefer idempotent commands. If a command is destructive, include a verification step and a rollback step.
- Before any repo change: show git status, create backups in D:\b2bplatform.tmp, then apply changes, then verify.
- When writing important text files, write UTF-8 without BOM using .NET APIs. Do not use Set-Content or Out-File for important docs/yaml files.

## Minimal safety checklist for any repo edit

- Set-Location D:\b2bplatform
- git status -sb (before)
- Backup files to D:\b2bplatform.tmp\*.bak.TIMESTAMP
- Apply change
- Verification commands + expected output
- git status -sb (after)