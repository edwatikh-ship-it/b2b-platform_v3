"""
Moderator tasks router (includes parsing endpoints).
SSoT: api-contracts.yaml:
- POST /moderator/requests/{requestId}/start-parsing
- GET  /moderator/requests/{requestId}/parsing-status
- GET  /moderator/requests/{requestId}/parsing-results
"""

from __future__ import annotations

import uuid
from urllib.parse import urlparse

import httpx
from fastapi import APIRouter, HTTPException

from app.adapters import parsing_storage
from app.transport.schemas.moderator_parsing import (
    ParsingDomainGroupDTO,
    ParsingKeyStatusDTO,
    ParsingResultsByKeyDTO,
    ParsingResultsResponseDTO,
    ParsingRunStatus,
    ParsingStatusResponseDTO,
    StartParsingResponseDTO,
)

router = APIRouter(tags=["ModeratorTasks"])

PARSER_SERVICE_URL = "http://127.0.0.1:9001"
BACKEND_BASE_URL = "http://127.0.0.1:8000"


def extract_root_domain(domain: str) -> str:
    parts = domain.split(".")
    if len(parts) >= 2:
        return ".".join(parts[-2:])
    return domain


def is_blacklisted(domain: str, blacklist: set[str]) -> bool:
    root = extract_root_domain(domain)
    return domain in blacklist or root in blacklist


async def fetch_blacklist_domains() -> set[str]:
    """
    Fetch blacklist from backend endpoint.
    If endpoint is not implemented (501) or fails, treat as empty blacklist (MVP).
    """
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            r = await client.get(f"{BACKEND_BASE_URL}/moderator/blacklist/domains?limit=1000")
            if r.status_code == 501:
                return set()
            r.raise_for_status()
            data = r.json()
            return {item["domain"] for item in data.get("items", [])}
    except Exception:
        return set()


@router.get("/moderator/tasks")
async def list_moderator_tasks(status: str | None = None, limit: int = 50):
    raise HTTPException(status_code=501, detail="Not Implemented")


@router.get("/moderator/tasks/{taskId}")
async def get_moderator_task(taskId: int):
    raise HTTPException(status_code=501, detail="Not Implemented")


@router.post(
    "/moderator/requests/{requestId}/start-parsing", response_model=StartParsingResponseDTO
)
async def start_parsing(requestId: int):
    """
    Starts parsing for a request.
    MVP: request keys are mocked (later: fetch real keys from DB).
    """
    key_ids = [1, 2]
    keys_data = {
        1: {"text": "поставщик металлопроката"},
        2: {"text": "оптовый поставщик"},
    }

    run_id = str(uuid.uuid4())
    parsing_storage.create_run(
        requestId, key_ids
    )  # creates another uuid internally, ignore for now (MVP)
    # overwrite to keep consistent run_id in storage for MVP
    parsing_storage._runs[run_id] = parsing_storage._runs.pop(
        list(parsing_storage._runs.keys())[-1]
    )
    parsing_storage._runs[run_id]["requestId"] = requestId

    parsing_storage.update_run_status(run_id, "running")
    blacklist = await fetch_blacklist_domains()

    key_statuses: list[str] = []

    for kid in key_ids:
        query = keys_data[kid]["text"]
        try:
            async with httpx.AsyncClient(timeout=1800.0) as client:
                resp = await client.post(
                    f"{PARSER_SERVICE_URL}/parse",
                    json={"query": query, "depth": 1},
                )
                resp.raise_for_status()
                urls = resp.json().get("urls", [])

            grouped: dict[str, list[str]] = {}
            for url in urls:
                domain = urlparse(url).netloc
                if not domain:
                    continue
                if is_blacklisted(domain, blacklist):
                    continue
                grouped.setdefault(domain, []).append(url)

            stored_groups = [{"domain": d, "urls": u} for d, u in grouped.items()]
            parsing_storage.update_key_status(run_id, kid, "succeeded", stored_groups)
            key_statuses.append("succeeded")
        except Exception as e:
            err = str(e) if str(e) else f"{type(e).__name__}: (no message)"
            parsing_storage.update_key_status(run_id, kid, "failed", [], err)
            key_statuses.append("failed")

    overall = "failed" if "failed" in key_statuses else "succeeded"
    parsing_storage.update_run_status(run_id, overall)

    return StartParsingResponseDTO(
        requestId=requestId, runId=run_id, status=ParsingRunStatus(overall)
    )


@router.get(
    "/moderator/requests/{requestId}/parsing-status", response_model=ParsingStatusResponseDTO
)
async def get_parsing_status(requestId: int):
    latest = parsing_storage.get_latest_run_by_request(requestId)
    if not latest:
        raise HTTPException(status_code=404, detail="No parsing run found for this request")

    run_id, run_data = latest
    keys_status: list[ParsingKeyStatusDTO] = []
    for kid, kdata in run_data["keys"].items():
        # items stored as groups now -> itemsFound = number of domain groups
        keys_status.append(
            ParsingKeyStatusDTO(
                keyId=int(kid),
                status=ParsingRunStatus(kdata["status"]),
                itemsFound=len(kdata["items"]),
                error=kdata["error"],
            )
        )

    return ParsingStatusResponseDTO(
        requestId=requestId,
        runId=run_id,
        status=ParsingRunStatus(run_data["status"]),
        keys=keys_status,
    )


@router.get(
    "/moderator/requests/{requestId}/parsing-results", response_model=ParsingResultsResponseDTO
)
async def get_parsing_results(requestId: int):
    latest = parsing_storage.get_latest_run_by_request(requestId)
    if not latest:
        raise HTTPException(status_code=404, detail="No parsing run found for this request")

    run_id, run_data = latest

    results: list[ParsingResultsByKeyDTO] = []
    for kid, kdata in run_data["keys"].items():
        groups = [
            ParsingDomainGroupDTO(
                domain=g["domain"],
                urls=g["urls"],
                source=None,  # parser_service does not provide source yet
                title=None,
            )
            for g in kdata["items"]
        ]
        results.append(ParsingResultsByKeyDTO(keyId=int(kid), groups=groups))

    return ParsingResultsResponseDTO(requestId=requestId, runId=run_id, results=results)
