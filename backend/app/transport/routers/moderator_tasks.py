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
from fastapi import APIRouter, Body, Depends, HTTPException
from publicsuffix2 import get_sld
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters import parsing_storage
from app.adapters.db.repositories import DomainBlacklistRepository
from app.adapters.db.session import getdbsession
from app.transport.schemas.moderator_parsing import (
    ParsingDomainGroupDTO,
    ParsingKeyStatusDTO,
    ParsingResultsByKeyDTO,
    ParsingResultsResponseDTO,
    ParsingRunStatus,
    ParsingStatusResponseDTO,
    StartParsingRequestDTO,
    StartParsingResponseDTO,
)

router = APIRouter(tags=["ModeratorTasks"])

PARSER_SERVICE_URL = "http://127.0.0.1:9001"


def extract_root_domain(domain: str) -> str:
    d = str(domain).strip().lower().strip(".")
    if not d:
        return ""
    # PSL-based: returns registrable domain e.g. bbc.co.uk, pulscen.ru
    sld = get_sld(d)
    return str(sld or d)


def is_blacklisted(domain: str, root_blacklist: set[str]) -> bool:
    root = extract_root_domain(domain)
    return root in root_blacklist


async def fetch_blacklist_domains_db(session: AsyncSession) -> set[str]:
    repo = DomainBlacklistRepository(session)
    items = await repo.list_root_domains(limit=1000)
    return {str(x).strip().lower() for x in items if str(x).strip()}


@router.get("/moderator/tasks")
async def list_moderator_tasks(status: str | None = None, limit: int = 50):
    raise HTTPException(status_code=501, detail="Not Implemented")


@router.get("/moderator/tasks/{taskId}")
async def get_moderator_task(taskId: int):
    raise HTTPException(status_code=501, detail="Not Implemented")


@router.get("/moderator/parsing-runs")
async def list_parsing_runs(status: str | None = None, limit: int = 50, offset: int = 0):
    raise HTTPException(status_code=501, detail="Not Implemented")


@router.get("/moderator/parsing-runs/{runId}")
async def get_parsing_run_detail(runId: str):
    raise HTTPException(status_code=501, detail="Not Implemented")


@router.get("/moderator/resolved-domains")
async def list_resolved_domains(status: str | None = None, limit: int = 50, offset: int = 0):
    raise HTTPException(status_code=501, detail="Not Implemented")


@router.get("/moderator/domains/{domain}/hits")
async def get_domain_hits(domain: str, limit: int = 100, offset: int = 0):
    raise HTTPException(status_code=501, detail="Not Implemented")


@router.get("/moderator/urls/hits")
async def get_url_hits(url: str, limit: int = 100, offset: int = 0):
    raise HTTPException(status_code=501, detail="Not Implemented")


@router.post(
    "/moderator/requests/{requestId}/start-parsing", response_model=StartParsingResponseDTO
)
async def start_parsing(
    requestId: int,
    payload: StartParsingRequestDTO | None = Body(None),
    session: AsyncSession = Depends(getdbsession),
):
    """
    Starts parsing for a request.
    MVP: request keys are mocked (later: fetch real keys from DB).
    """
    depth = payload.depth if payload and payload.depth is not None else 10
    source = payload.source.value if payload and payload.source is not None else "both"
    key_ids = [1, 2]
    keys_data = {
        1: {
            "text": "Р С—Р С•РЎРѓРЎвЂљР В°Р Р†РЎвЂ°Р С‘Р С” Р СР ВµРЎвЂљР В°Р В»Р В»Р С•Р С—РЎР‚Р С•Р С”Р В°РЎвЂљР В°"
        },
        2: {"text": "Р С•Р С—РЎвЂљР С•Р Р†РЎвЂ№Р в„– Р С—Р С•РЎРѓРЎвЂљР В°Р Р†РЎвЂ°Р С‘Р С”"},
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
    blacklist = await fetch_blacklist_domains_db(session)

    key_statuses: list[str] = []

    for kid in key_ids:
        query = keys_data[kid]["text"]
        try:
            async with httpx.AsyncClient(timeout=1800.0) as client:
                resp = await client.post(
                    f"{PARSER_SERVICE_URL}/parse",
                    json={"query": query, "depth": depth, "source": source},
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
