"""Moderator tasks router (includes parsing endpoints).
SSoT: api-contracts.yaml:
- POST /moderator/requests/{requestId}/start-parsing
- GET  /moderator/requests/{requestId}/parsing-status
- GET  /moderator/requests/{requestId}/parsing-results
"""

from __future__ import annotations

import uuid

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters import parsing_storage
from app.adapters.db.session import getdbsession
from app.transport.parsing import parse_query
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


@router.get("/moderator/tasks")
async def list_moderator_tasks(status: str | None = None, limit: int = 50):
    return {}


@router.get("/moderator/tasks/{taskId}")
async def get_moderator_task(taskId: int):
    return {}


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
    depth = payload.depth if payload and payload.depth is not None else 10

    key_ids = [1, 2]
    keys_data = {1: {"text": "металлургия"}, 2: {"text": "сталь"}}

    run_id = str(uuid.uuid4())
    parsing_storage.create_run(requestId, key_ids)
    parsing_storage._runs[run_id] = parsing_storage._runs.pop(
        list(parsing_storage._runs.keys())[-1]
    )
    parsing_storage._runs[run_id]["requestId"] = requestId
    parsing_storage.update_run_status(run_id, "running")

    key_statuses = []
    for kid in key_ids:
        query = keys_data[kid]["text"]
        try:
            groups = await parse_query(query, depth, session)
            stored_groups = [{"domain": g.domain, "urls": g.urls} for g in groups]
            parsing_storage.update_key_status(run_id, kid, "succeeded", stored_groups)
            key_statuses.append("succeeded")
        except Exception as e:
            err = str(e)
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
    keys_status = [
        ParsingKeyStatusDTO(
            keyId=int(kid),
            status=ParsingRunStatus(kdata["status"]),
            itemsFound=len(kdata["items"]),
            error=kdata["error"],
        )
        for kid, kdata in run_data["keys"].items()
    ]

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
    results = []
    for kid, kdata in run_data["keys"].items():
        groups = [
            ParsingDomainGroupDTO(
                domain=g["domain"],
                urls=g["urls"],
                source=None,
                title=None,
            )
            for g in kdata["items"]
        ]
        results.append(ParsingResultsByKeyDTO(keyId=int(kid), groups=groups))

    return ParsingResultsResponseDTO(requestId=requestId, runId=run_id, results=results)
