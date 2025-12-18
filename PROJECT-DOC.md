# PROJECT-DOC — Product rules (SSoT after api-contracts.yaml and PROJECT-RULES.md)

Version: 1.0
Date: 2025-12-18
Status: Active

This document captures product/business rules that are NOT fully described in OpenAPI contracts.
If something here contradicts api-contracts.yaml, api-contracts.yaml wins and this doc must be updated.

SSoT order:
api-contracts.yaml -> PROJECT-RULES.md -> PROJECT-DOC.md


## Purpose

- Avoid repeated clarifications and “guessing” during backend/UI implementation.
- Keep all non-contract product rules in one place (workflow, moderation decisions, parsing, blacklist semantics, MVP limitations).  


## End-to-end process (User -> Moderator -> Delivery)

### 1) Request creation and keys
- User creates a Request and provides a list of “keys” (positions/items).
- Keys can be entered manually or appear after file recognition (future: file -> keys via AI).
- User reviews keys and confirms the request is correct.

### 2) “Get supplier contacts” (matching + moderator work)
When user triggers the action “Get supplier contacts”:
- System runs matching for each key using the existing supplier base (deterministic MVP matching, see below).
- In parallel, system creates Moderator work to process new/unknown findings (exact ModeratorTask mechanics is implementation detail; API endpoints are in api-contracts.yaml).

### 3) Moderator parsing workflow
- Moderator opens a task/workspace and manually starts parsing (MVP = manual start, no auto-start).
- Parsing uses search engines (Google/Yandex) and returns URLs for each key.
- Moderator reviews results grouped by domain and makes a decision per domain:
  - Create Supplier card
  - Create Reseller card
  - Add domain to global blacklist
  - Keep domain pending (no final decision yet)

### 4) Delivery to user
For each URL/domain found by parsing:
- If the domain is already moderated (supplier/reseller/blacklist decision exists), the system handles it immediately:
  - Supplier/reseller -> contact becomes available to the user.
  - Blacklist -> must not be shown in results (filtered server-side).
- If domain is new/unmoderated -> it stays in moderator flow until a decision is made.


## Definition: “Moderated supplier / moderated URL” (hard requirement)

A company/domain can be considered “ready to show to users” only if moderator provided at minimum:
- Company URL (domain/website)
- INN
- Company name
- Sales email (the contact mailbox for requests)

Only after this, the supplier/reseller becomes eligible for automatic delivery to users.


## Parsing: MVP rules

### Manual start (MVP)
- Parsing is started by moderator action from Moderator UI (button like “Get URLs”).
- No automatic parsing start in MVP.

### Depth
- Depth controls how many search result pages are fetched per key in the search engine.
- Default depth should be conservative (product-level default: 10 is allowed; tune later).
- Hard maximum depth is 50 (must follow api-contracts.yaml).

### Source selection
- Moderator selects parsing source: google / yandex / both (as per contract).
- When source=both, results are aggregated and de-duplicated (dedupe strategy is implementation detail; outcome must be stable).

### Hidden search prefix (RU word “kupit’”)
- Backend prepends a hidden search prefix "купить " only when querying search engines.
- This prefix MUST NOT be stored or displayed as part of the business key (keys stored/displayed remain clean).

### Results: domain accordion
- UI shows parsing results grouped by domain (accordion):
  - One domain row appears once.
  - Expanding a domain shows all collected URLs under that domain (different paths are separate URLs).
- For each URL/domain, UI shows which keys produced it (key -> url -> domain mapping).

### Partial failure preservation
- If parsing partially fails, already collected results must be preserved.
- System should return partial results where possible (do not discard success because one key failed).

### Resume behavior (per key)
- Resume is per keyId:
  - Next start-parsing should parse only failed keys.
  - Continue from the page where the key failed.
  - Successful keys are NOT re-parsed.

### Run history (moderator)
- Each manual run is stored in history (list + detail), so moderator can return to previous runs.


## Domain moderation decisions (4 statuses)

Moderation unit is the domain (root-domain aware).

Statuses (business meaning):
- supplier: create Supplier card (required fields: INN, company name, primary email; URL auto-filled from parsed domain/URL; extra emails allowed).
- reseller: create Reseller / Trading Organization card (same required fields; flagged as reseller for users).
- blacklist: add to global root-domain blacklist (blocks subdomains too); comment is optional.
- pending: keep in a pending queue; domain stays visible until a final decision is made.

Finalization rule:
- After decision supplier/reseller/blacklist, the domain must disappear from parsing results everywhere (it is no longer “pending work”).


## Global domain blacklist (root-domain rule)

Blacklist key is a root domain (hostname only), e.g. `cvetmetall.ru`:
- No scheme (no `https://`)
- No trailing slash

Global scope:
- The blacklist is global and shared across all requests and moderators.

Subdomain blocking:
- A blacklisted root domain blocks itself AND all subdomains
  (e.g., `pulscen.ru` blocks `spb.pulscen.ru`, `msk.pulscen.ru`, etc.).

Hard filtering requirement:
- Blacklisted domains (including subdomains) MUST NOT appear in parsing-results responses.
- Filtering is server-side (moderator should never see blacklisted items in parsing results).


## Logging / analytics: domain hits

Even if a domain is already decided/blacklisted, the system logs every occurrence:
- key -> url -> domain

Goal:
- moderator can see which keys keep producing the same domains
- debug / analytics visibility without polluting UI results


## Matching rules: “similar key” (MVP -> improvements)

Goal:
- Matching must return truly relevant suppliers for a key.

MVP approach (deterministic + explainable):
1) Normalize key text:
   - lowercasing, trimming, symbol unification (d/Д), normalize "ё/е"
   - numeric/size tokens are important (e.g., 100)
2) Extract “required parameters” (by patterns):
   - sizes/diameters (d=100), GOST, steel grade, etc.
3) Decision:
   - required parameters must match
   - text similarity must be above threshold (token overlap or trigram similarity)
4) Explainability:
   - store why it matched (which params/tokens matched)

Notes:
- In MVP, avoid ML/black-box matching.
- Thresholds and exact algorithm are tuned later on real data.


## What user sees (supplier card in UI)

For each supplier delivered to user, UI must show at minimum:
- Company name
- INN
- Company URL
- Additional company details from Checko (if available)
- Ability to send request to supplier (messaging branch)


## MVP limitation: messaging stub

Until user mailbox integration exists:
- actual email sending from service is a stub / not working (placeholder behavior).
- user can copy contacts and send requests manually from their own email.
- “sent / replied” statuses are placeholders until integration is implemented.


## Local backend preflight (Windows) — operational checklist

Note:
- Runtime base URL and API prefix must be discovered (no guessing).
- This section is a copy/paste helper for local checks.

1) Verify backend OpenAPI is reachable:
- Invoke-RestMethod "http://127.0.0.1:8000/openapi.json" | Out-Null

2) Verify health:
- Invoke-RestMethod "http://127.0.0.1:8000/health" | ConvertTo-Json -Depth 5
Expected: {"status":"ok"}

3) DB env in current shell (only if DB needed at import-time):
- python -c "import os; print(os.getenv('DATABASEURL'), os.getenv('DATABASE_URL'))"

4) Moderator parsing results contract expectations:
- Unique domains list (one domain once)
- Blacklisted domains must not appear at all
- URLs listed under domain accordion (paths preserved)
- Raw hits preserved in logs (duplicates allowed there)
