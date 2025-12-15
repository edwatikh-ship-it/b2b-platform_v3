from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.db.repositories import DomainBlacklistRepository
from app.adapters.db.session import getdbsession
from app.transport.schemas.blacklist import (
    AddBlacklistDomainRequestDTO,
    BlacklistDomainsListResponseDTO,
)

router = APIRouter(tags=["Blacklist"])


@router.post("/moderator/blacklist/domains")
async def add_blacklist_domain(
    payload: AddBlacklistDomainRequestDTO,
    session: AsyncSession = Depends(getdbsession),
):
    repo = DomainBlacklistRepository(session)
    try:
        await repo.add_root_domain(payload.domain)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
    return {}


@router.get("/moderator/blacklist/domains", response_model=BlacklistDomainsListResponseDTO)
async def list_blacklist_domains(
    limit: int = 200,
    session: AsyncSession = Depends(getdbsession),
):
    repo = DomainBlacklistRepository(session)
    items = await repo.list_root_domains(limit=limit)
    return {"items": items, "limit": int(limit), "total": len(items)}


@router.delete("/moderator/blacklist/domains/{domain}")
async def delete_blacklist_domain(
    domain: str,
    session: AsyncSession = Depends(getdbsession),
):
    repo = DomainBlacklistRepository(session)
    await repo.remove_root_domain(domain)
    return {}
