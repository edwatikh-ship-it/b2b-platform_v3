# INCIDENTS
- 2025-12-14 11:54 MSK: INCIDENT tests failed with multiple 404 after switching API prefix to /apiv1 (SSoT). Root cause: integration tests still used old base path /api/v1. Fix: bulk replaced /api/v1/ -> /apiv1/ in tests/integration/*.py. Verification: D:\b2bplatform\backend\.venv\Scripts\python.exe -m pytest -q (all passed).

- 2025-12-14 11:54 MSK: INCIDENT 404 failures after switching API base path to /apiv1 (SSoT). Root cause: integration tests used old /api/v1. Fix: bulk replace /api/v1/ -> /apiv1/ in tests/integration/*.py. Verification: D:\b2bplatform\backend\.venv\Scripts\python.exe -m pytest -q -> 12 passed.

- 2025-12-14 11:55 MSK: INCIDENT contract test failed (FileNotFoundError) because it looked for api-contracts.yaml in backend/. Root cause: wrong relative path assumption. Fix: search parents for api-contracts.yaml. Note: HANDOFF entry was mistakenly added while pytest was failing; do not remove (append-only). Verification: D:\b2bplatform\backend\.venv\Scripts\python.exe -m pytest -q (all passed).

- 2025-12-14 11:58 MSK: INCIDENT contract-paths test surfaced mismatch: implementation exposed /apiv1/userattachments and /apiv1/userblacklistinn while SSoT requires /apiv1/user/attachments and /apiv1/user/blacklist/inn. Fix: renamed router paths + updated integration tests. Verification: D:\b2bplatform\backend\.venv\Scripts\python.exe -m pytest -q -> 14 passed.

