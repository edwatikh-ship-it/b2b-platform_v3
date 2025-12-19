## Parsing: implementation notes (MVP)

### Depth (search pages)
- Depth controls how many search result pages are fetched per key (pages in the search engine), not a max-URL limit.
- The parser stops when it reaches the depth page limit even if more results exist.
- Default depth should be conservative for MVP (e.g., 1-3 pages) to reduce rate limits/captcha risk; tune later based on real usage.

### Domain blacklist (root-domain)
- Blacklist is stored as root domains (e.g., pulscen.ru).
- Root-domain blacklist blocks the domain itself AND all subdomains (e.g., spb.pulscen.ru, msk.pulscen.ru).
- Blacklisted results must be filtered server-side and must not appear in parsing-results at all (moderator should never see them).

### Accordion (domain groups)
- UI shows parsing results grouped by domain (accordion): domain -> list of URLs.
- Grouping is done after blacklist filtering.
- Domain in results may include subdomains; blacklist matching must normalize URL hostname to root-domain for filtering logic.

### Processing pipeline (recommended)
- parser_service: collects raw URLs per key by querying search engines up to Depth pages.
- backend: normalizes domains, applies root-domain blacklist filtering, and groups results by domain before returning them to the moderator endpoints.

## Parsing MVP: depth, blacklist, accordion

### Depth = search pages (no URL cap)
- Depth controls how many search result pages are fetched per key in the search engine (Yandex/Google).
- There is no explicit "max URLs per key" cap in MVP: the number of URLs depends on the engine output for the selected number of pages.
- Depth should have a sane default (MVP) and a hard upper bound to reduce captcha/rate-limit risk; tune later.

### Blacklist domains = root-domain rule
- The blacklist stores root domains (example: pulscen.ru).
- A blacklisted root domain blocks itself AND all its subdomains (spb.pulscen.ru, msk.pulscen.ru, etc).
- Filtering must be server-side: blacklisted domains/URLs must not appear in moderator parsing results at all.

### "Accordion" UI grouping (domain -> urls)
- Moderator UI shows parsing results grouped by domain (accordion): one domain row, expandable list of URLs.
- Grouping happens after blacklist filtering.
- Domain in results may include subdomains; blacklist matching must normalize URL hostname to root-domain.

### Suggested pipeline (where logic lives)
- parser_service: queries search engines up to Depth pages and returns raw URLs per key.
- backend: normalizes domains, applies root-domain blacklist filtering, groups results into accordion structure, and returns it via API.

## Moderator LK decisions (parsing + blacklist + resume)

- Priority: Moderator processes incoming client requests first; in free time, uses parsing results to gradually fill the suppliers base.
- Parsing start: Manual action in moderator LK (button like "Get URLs"). No auto-start for MVP.
- Parsing results: Moderator reviews URL groups and either creates supplier cards or adds domains to the global blacklist.

### Global domain blacklist (root-domain)
- Blacklist key is a hostname/root-domain only (e.g. cvetmetall.ru), without scheme (https://) and without trailing slash (/).
- Blacklist is global (shared across all requests and moderators).
- Blacklisted domains (including subdomains) MUST NOT appear in parsing-results responses (server-side filtering).

### Resume behavior (per key)
- If parsing partially fails, already collected results are preserved.
- Resume is per keyId: next start-parsing should parse only failed keys and continue from the page where the key failed (successful keys are not re-parsed).
- Comment on blacklist add is optional.