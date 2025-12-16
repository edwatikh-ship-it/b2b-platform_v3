from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from app.transport.schemas.moderator_domain_decision import (
    DomainDecisionRequestDTO,
    DomainDecisionResponseDTO,
)

router = APIRouter(tags=["ModeratorDomainDecision"])


@router.get(
    "/moderator/domains/{domain}/decision",
    response_model=DomainDecisionResponseDTO,
    responses={404: {"description": "Domain not found or no decision made"}},
)
async def get_domain_decision(domain: str) -> DomainDecisionResponseDTO:
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")


@router.post(
    "/moderator/domains/{domain}/decision",
    response_model=DomainDecisionResponseDTO,
    responses={404: {"description": "Domain not found"}},
)
async def make_domain_decision(
    domain: str, body: DomainDecisionRequestDTO
) -> DomainDecisionResponseDTO:
    if body.status in ("supplier", "reseller") and body.carddata is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="carddata is required for status supplier/reseller",
        )

    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Not implemented")
