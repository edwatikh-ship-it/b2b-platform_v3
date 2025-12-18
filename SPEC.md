# B2B Platform  Specification (supporting doc, non-SSoT)
Version: 0.1
Date: 2025-12-18
Status: Living document (update/remove obsolete items continuously)

SSoT order reminder:
- API shapes and endpoints = ONLY api-contracts.yaml.
- This SPEC describes business intent, use cases, FR/NFR, acceptance criteria.
- If SPEC contradicts api-contracts.yaml: api-contracts.yaml wins; SPEC must be updated.

============================================================
0) Scope and goals
============================================================
Business goal (BR):
- Provide a pipeline where client requests (with “keys/items”) are processed to find suppliers/resellers,
  with a moderator workflow that runs parsing, moderates domains, and grows an internal supplier base.

Primary actors:
- User (client): creates requests, provides keys, receives supplier contacts, sends messages to selected recipients.
- Moderator: runs parsing, reviews results, makes domain decisions (supplier/reseller/blacklist/pending),
  and maintains supplier cards and global domain blacklist.
- System (backend + parser_service): executes parsing and provides API for UI.

Out of scope (current MVP notes):
- Full automation of parsing without moderator action (manual start is the MVP approach).
- Perfect matching/ML ranking (MVP uses deterministic steps, can evolve later).

============================================================
1) Domain glossary
============================================================
Key (Request Key):
- A single item/position in a user request (e.g., “Фланец d100”), with pos and optional qty/unit.

Request:
- A collection of keys submitted by the user; has lifecycle statuses (exact strings are per contract/impl).

Parsing run:
- A manual moderator-triggered operation that queries search engines for each key to collect URLs,
  then returns results grouped by domain.

Domain (root-domain aware):
- The moderation unit is a domain; blacklist decisions are applied to root domains and block subdomains too.

Supplier card:
- A structured supplier/reseller entity with required fields (INN, name, email, urls, etc.).

============================================================
2) Decision log (in-spec)
============================================================
2025-12-18 (MSK)
Decision:
- Store the main project specification in a single root file: D:\b2bplatform\SPEC.md
Why:
- Faster navigation, lower risk of losing context, easier to paste/replace in chat.
Consequence:
- All new use cases and requirements must be appended/updated here.
How to verify:
- File exists in repo root and is referenced by team as the canonical spec entrypoint.

============================================================
3) Use Cases (UC)
============================================================

------------------------------------------------------------
UC-001 — System health check
------------------------------------------------------------
Primary actor:
- Dev/QA/Monitoring

Preconditions:
- Backend is running.

Trigger:
- Need to confirm service is alive.

Main success scenario:
1) Call GET /health.
2) Receive JSON indicating system status.

Acceptance criteria:
- GET /health returns HTTP 200 and schema HealthResponse with status string. (See api-contracts.yaml.)

Related API:
- GET /health [System] [api-contracts.yaml]

------------------------------------------------------------
UC-010 — User creates request manually
------------------------------------------------------------
Primary actor:
- User

Preconditions:
- User can access UI/API.

Trigger:
- User wants to create a new request by manually entering keys.

Main success scenario:
1) User submits a list of keys (pos, text, optional qty/unit).
2) System creates a request draft/record.
3) System returns requestId and status.

Alternate flows:
- Validation error on keys (empty list, invalid pos/text) -> 422.

Acceptance criteria:
- POST /user/requests accepts CreateRequestManualRequestDTO and returns CreateRequestResponseDTO. [api-contracts.yaml]
- GET /user/requests lists created requests with pagination params limit/offset. [api-contracts.yaml]

Related API:
- POST /user/requests [UserRequests]
- GET /user/requests [UserRequests]
- GET /user/requests/{requestId} [UserRequests]
- PUT /user/requests/{requestId}/keys [UserRequests]
- POST /user/requests/{requestId}/submit [UserRequests]
- POST /user/upload-and-create [UserRequests] (file upload + create)

------------------------------------------------------------
UC-020 — User manages recipients and sends messages
------------------------------------------------------------
Primary actor:
- User

Preconditions:
- There is an existing requestId.

Trigger:
- User wants to select recipients (suppliers) and send messages.

Main success scenario (recipients):
1) User updates recipients list for a request (replace-all semantics if documented in product rules/decisions).
2) System returns the current recipients list.

Main success scenario (messaging):
1) User sends request messages for requestId.
2) System accepts and returns success response (shape is currently generic object in contract).

Alternate flows:
- Validation error -> 422.
- If endpoints are not implemented in current MVP, they may return "Not Implemented" at runtime, but the contract still defines them.

Acceptance criteria:
- PUT /user/requests/{requestId}/recipients accepts UpdateRecipientsRequestDTO and returns RecipientsResponseDTO. [api-contracts.yaml]
- Message endpoints exist in OpenAPI contract per api-contracts.yaml. [api-contracts.yaml]

Related API:
- PUT /user/requests/{requestId}/recipients [UserMessaging]
- POST /user/requests/{requestId}/send [UserMessaging]
- POST /user/requests/{requestId}/send-new [UserMessaging]
- GET /user/requests/{requestId}/messages [UserMessaging]
- DELETE /user/messages/{messageId} [UserMessaging]

------------------------------------------------------------
UC-030 — User uploads attachments
------------------------------------------------------------
Primary actor:
- User

Preconditions:
- User has a file.

Trigger:
- User uploads a file (for later use in the request flow).

Main success scenario:
1) User uploads a file via multipart/form-data.
2) System stores attachment and returns AttachmentDTO.
3) User can list/get/delete/download attachments.

Acceptance criteria:
- Attachment endpoints and DTO shapes match api-contracts.yaml (AttachmentDTO, AttachmentListResponseDTO). [api-contracts.yaml]

Related API:
- POST /user/attachments
- GET /user/attachments
- GET /user/attachments/{attachmentId}
- DELETE /user/attachments/{attachmentId}
- GET /user/attachments/{attachmentId}/download

------------------------------------------------------------
UC-040 — Moderator starts parsing for a request
------------------------------------------------------------
Primary actor:
- Moderator

Preconditions:
- A request exists and is visible/accessible to moderator workflow.
- parser_service and Chrome CDP are running (runtime dependency).

Trigger:
- Moderator presses “Start parsing / Get URLs” in Moderator cabinet.

Main success scenario:
1) Moderator calls POST /moderator/requests/{requestId}/start-parsing with optional body:
   - depth (default 10, max 50 by contract)
   - source (google/yandex/both by contract)
2) System starts parsing and returns runId + status.
3) Moderator polls status and results endpoints.

Alternate flows:
- parser_service unavailable -> system cannot parse; should fail fast and surface error (exact error contract TBD).
- Captcha/rate-limit may cause partial results; partial results must be preserved (product rule).

Acceptance criteria:
- StartParsingRequestDTO includes optional depth and source; source enum includes google/yandex/both. [api-contracts.yaml]
- StartParsingResponseDTO returns requestId, runId, and status. [api-contracts.yaml]

Related API:
- POST /moderator/requests/{requestId}/start-parsing
- GET /moderator/requests/{requestId}/parsing-status
- GET /moderator/requests/{requestId}/parsing-results
- GET /moderator/parsing-runs
- GET /moderator/parsing-runs/{runId}

------------------------------------------------------------
UC-050 — Moderator reviews parsing results (domain accordion)
------------------------------------------------------------
Primary actor:
- Moderator

Preconditions:
- Parsing results exist for a run/request.

Trigger:
- Moderator opens results screen.

Main success scenario:
1) System returns results grouped by domain; each group contains URLs under the domain.
2) UI shows an accordion: domain row expands into URLs list.
3) Moderator can see which keys produced which domains/URLs (mapping requirement).

Acceptance criteria:
- Parsing results response uses ParsingResultsResponseDTO, containing results by key, each key contains groups of ParsingDomainGroupDTO (domain + urls). [api-contracts.yaml]
- ParsingDomainGroupDTO includes optional source (google/yandex) for the group when available. [api-contracts.yaml]

Related API:
- GET /moderator/requests/{requestId}/parsing-results
- GET /moderator/domains/{domain}/hits
- GET /moderator/urls/hits

------------------------------------------------------------
UC-060 — Moderator makes a domain decision (supplier/reseller/blacklist/pending)
------------------------------------------------------------
Primary actor:
- Moderator

Preconditions:
- A domain has appeared in parsing results or pending domains list.

Trigger:
- Moderator selects a decision for a domain.

Main success scenario:
1) Moderator requests current decision card for a domain (if exists).
2) Moderator submits decision with status and optional card data/comment.
3) System stores decision and returns decision state.

Decision statuses:
- supplier
- reseller
- blacklist
- pending

Acceptance criteria:
- GET /moderator/domains/{domain}/decision returns 200 with DomainDecisionResponseDTO or 404 if not found. [api-contracts.yaml]
- POST /moderator/domains/{domain}/decision accepts DomainDecisionRequestDTO and returns DomainDecisionResponseDTO. [api-contracts.yaml]
- DomainDecisionRequestDTO requires status and may include cardData/comment; card fields include inn, name, email. [api-contracts.yaml]

Related API:
- GET /moderator/domains/{domain}/decision
- POST /moderator/domains/{domain}/decision

------------------------------------------------------------
UC-070 — Global root-domain blacklist (moderator)
------------------------------------------------------------
Primary actor:
- Moderator

Preconditions:
- Moderator wants to block a domain globally.

Trigger:
- Moderator adds domain to blacklist.

Main success scenario:
1) Moderator submits a root domain (hostname only).
2) System stores it globally.
3) All parsing results must be server-side filtered so blacklisted domains (and subdomains) never appear to moderator.

Acceptance criteria:
- POST /moderator/blacklist/domains accepts AddModeratorBlacklistDomainRequestDTO and returns ModeratorBlacklistDomainDTO. [api-contracts.yaml]
- GET /moderator/blacklist/domains returns list response. [api-contracts.yaml]
- DELETE /moderator/blacklist/domains/{domain} removes domain. [api-contracts.yaml]

Related API:
- POST /moderator/blacklist/domains
- GET /moderator/blacklist/domains
- DELETE /moderator/blacklist/domains/{domain}

------------------------------------------------------------
UC-080 — User personal blacklist by INN
------------------------------------------------------------
Primary actor:
- User

Preconditions:
- User is authenticated (authorization header is optional in contract, but business-wise user scope implies auth).

Trigger:
- User blocks suppliers by INN for their own account.

Main success scenario:
1) User adds an INN to personal blacklist.
2) User can list/remove blacklisted INNs.

Acceptance criteria:
- POST /user/blacklist-inn, GET /user/blacklist-inn, DELETE /user/blacklist-inn/{inn} exist in contract and accept/return contract DTOs. [api-contracts.yaml]

Related API:
- POST /user/blacklist-inn
- GET /user/blacklist-inn
- DELETE /user/blacklist-inn/{inn}

------------------------------------------------------------
UC-090 — Auth via OTP (contract-level)
------------------------------------------------------------
Primary actor:
- User

Preconditions:
- User can receive OTP.

Trigger:
- User attempts to authenticate.

Main success scenario:
1) User requests OTP with email.
2) User verifies OTP with email + code.
3) User calls /auth/me to confirm identity.

Acceptance criteria:
- POST /auth/otp/request accepts AuthOtpRequestDTO. [api-contracts.yaml]
- POST /auth/otp/verify accepts AuthOtpVerifyDTO. [api-contracts.yaml]
- GET /auth/me accepts optional Authorization header. [api-contracts.yaml]

Related API:
- POST /auth/otp/request
- POST /auth/otp/verify
- GET /auth/me

============================================================
4) Functional Requirements (FR)
============================================================
FR-001 SSoT enforcement:
- API behavior and shapes must match api-contracts.yaml. Any mismatch is an error.

FR-002 Root-domain blacklist filtering:
- Blacklisted root domains must filter out both the domain and all subdomains in parsing results server-side.

FR-003 Parsing source selection:
- Parsing runs must support source=google, yandex, both as per contract.
- If parser_service cannot support it yet, the system must document and track the gap (incident + decision).

FR-004 Preserve partial results:
- If parsing partially fails, already collected results must be preserved and visible (at least for analysis).

FR-005 Results grouping:
- Parsing results returned to UI must be grouped by domain and presented as a unique domain list (accordion UX).

FR-006 Domain decision workflow:
- Domain decision must support statuses supplier/reseller/blacklist/pending with required data fields for supplier/reseller.

FR-007 Deterministic matching (MVP):
- Matching rules must be deterministic and explainable; store reasoning if possible.

============================================================
5) Non-Functional Requirements (NFR)
============================================================
NFR-001 Reliability:
- The system must fail fast when parser_service is down and provide actionable errors for operators.

NFR-002 Observability:
- Log key-url-domain hits for analytics/debugging even if UI shows only unique domains.

NFR-003 Performance:
- Pagination endpoints must enforce reasonable defaults and maximums (contract already caps limit on many endpoints).

NFR-004 Security:
- Auth endpoints must not leak user data without valid credentials (GET /auth/me must protect identity data).

NFR-005 Maintainability:
- Keep clean architecture boundaries: transport/usecases/domain/adapters.

============================================================
6) Open questions / TBD (must be resolved, not ignored)
============================================================
TBD-001 "both" semantics:
- Merge google+yandex results with de-duplication by URL/root-domain (team decision already stated in chat; confirm in implementation).

TBD-002 Exact request status lifecycle:
- Contract includes status fields but business lifecycle statuses need a single canonical list and transitions.

TBD-003 Error contract for parser_service failures:
- Define how failures are returned to moderator endpoints (HTTP codes + schema).

============================================================
7) Verification checklist (practical)
============================================================
- Contract:
  - api-contracts.yaml contains the endpoint and DTO shape.
- Runtime:
  - backend /openapi.json shows the same paths.
  - /health returns HealthResponse.
- Behavior:
  - Key workflows (UC-010, UC-040, UC-060, UC-070) have at least one runnable smoke test command or integration test.
