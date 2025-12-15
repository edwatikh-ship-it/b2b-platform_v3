"""
In-memory storage for parsing runs (MVP; no DB yet).
Stores: runId -> {requestId, status, keys: {keyId -> {status, items, error}}}
Thread-safe via asyncio dict access (single-process uvicorn).
"""

import uuid
from typing import Any

_runs: dict[str, dict[str, Any]] = {}


def create_run(request_id: int, key_ids: list[int]) -> str:
    """Create a new parsing run and return runId."""
    run_id = str(uuid.uuid4())
    _runs[run_id] = {
        "requestId": request_id,
        "status": "queued",
        "keys": {kid: {"status": "queued", "items": [], "error": None} for kid in key_ids},
    }
    return run_id


def get_run(run_id: str) -> dict[str, Any] | None:
    """Get run data by runId."""
    return _runs.get(run_id)


def get_latest_run_by_request(request_id: int) -> tuple[str, dict[str, Any]] | None:
    """Get latest run for a given requestId (MVP: just return last by creation order)."""
    candidates = [(rid, r) for rid, r in _runs.items() if r["requestId"] == request_id]
    if not candidates:
        return None
    return candidates[-1]


def update_run_status(run_id: str, status: str) -> None:
    """Update overall run status."""
    if run_id in _runs:
        _runs[run_id]["status"] = status


def update_key_status(
    run_id: str, key_id: int, status: str, items: list[dict], error: str | None = None
) -> None:
    """Update parsing status for a specific key."""
    if run_id in _runs and key_id in _runs[run_id]["keys"]:
        _runs[run_id]["keys"][key_id] = {"status": status, "items": items, "error": error}
