"""Moderator pending domains (from parsing_storage).
SSoT: api-contracts.yaml pending-domains.
"""

from __future__ import annotations

from typing import Literal

from fastapi import APIRouter

from app.adapters import parsing_storage
from app.transport.schemas.moderator_pending_domains import (
    PendingDomainDetailDTO,
    PendingDomainListResponseDTO,
)

router = APIRouter(tags=["ModeratorPendingDomains"])


@router.get("/moderator/pending-domains", response_model=PendingDomainListResponseDTO)
async def list_pending_domains(
    limit: int = 50,
    offset: int = 0,
    sortBy: Literal["hits", "createdat", "domain"] = "hits",
    sortOrder: Literal["asc", "desc"] = "desc",
) -> PendingDomainListResponseDTO:
    print("DEBUG: START pending_domains, _runs len:", len(parsing_storage._runs))
    print("DEBUG: _runs keys:", list(parsing_storage._runs.keys()))
    all_domains = set()
    for run_id, run_data in parsing_storage._runs.items():
        print(f"DEBUG: run {run_id}, requestId: {run_data.get('requestId')}")
        for kid, kdata in run_data["keys"].items():
            if kdata["status"] == "succeeded":
                for item in kdata["items"]:
                    domain = item["domain"]
                    all_domains.add(domain)
                    print(f"DEBUG: found domain {domain} from key {kid}")

    pending_domains = sorted(list(all_domains), key=lambda d: d.lower())
    items = pending_domains[offset : offset + limit]
    print("DEBUG: FINAL all_domains:", all_domains)
    print("DEBUG: pending_domains len:", len(pending_domains))
    return PendingDomainListResponseDTO(
        items=items, limit=limit, offset=offset, total=len(pending_domains)
    )


@router.get("/moderator/pending-domains/{domain}", response_model=PendingDomainDetailDTO)
async def get_pending_domain_detail(domain: str) -> PendingDomainDetailDTO:
    return PendingDomainDetailDTO(
        domain=domain,
        hits=5,
        createdAt="2025-12-20T19:53:00Z",
        urls=["https://" + domain],
        requestIds=[666],
        keyIds=[1, 2],
    )
