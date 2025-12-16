from __future__ import annotations

from typing import Literal

from fastapi import APIRouter, HTTPException

from app.transport.schemas.moderator_pending_domains import (
    PendingDomainDetailDTO,
    PendingDomainListResponseDTO,
)

router = APIRouter(tags=["ModeratorPendingDomains"])


@router.get(
    "/moderator/pending-domains",
    response_model=PendingDomainListResponseDTO,
)
async def list_pending_domains(
    limit: int = 50,
    offset: int = 0,
    sortBy: Literal["hits", "createdat", "domain"] = "hits",
    sortOrder: Literal["asc", "desc"] = "desc",
) -> PendingDomainListResponseDTO:
    _ = (sortBy, sortOrder)
    return PendingDomainListResponseDTO(items=[], limit=limit, offset=offset, total=0)


@router.get(
    "/moderator/pending-domains/{domain}",
    response_model=PendingDomainDetailDTO,
)
async def get_pending_domain_detail(domain: str) -> PendingDomainDetailDTO:
    raise HTTPException(status_code=404, detail="Domain not found")
