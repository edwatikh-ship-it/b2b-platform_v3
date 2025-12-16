from datetime import UTC, datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.db.repositories import DomainBlacklistRepository
from app.adapters.db.session import getdbsession
from app.transport.schemas.moderator_blacklist_domains import (
    AddModeratorBlacklistDomainRequestDTO,
    ModeratorBlacklistDomainDTO,
    ModeratorBlacklistDomainListResponseDTO,
)

router = APIRouter(tags=["Blacklist"])


def _iso(dt: object) -> str:
    if isinstance(dt, datetime):
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=UTC)
        return dt.isoformat()
    return str(dt)


@router.post("/moderator/blacklist/domains", response_model=ModeratorBlacklistDomainDTO)
async def add_blacklist_domain(
    payload: AddModeratorBlacklistDomainRequestDTO,
    session: AsyncSession = Depends(getdbsession),
) -> ModeratorBlacklistDomainDTO:
    repo = DomainBlacklistRepository(session)
    try:
        await repo.add_root_domain(payload.domain)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e

    # MVP: url-level blacklist isn't stored yet; keep urls empty.
    # createdat ideally should come from DB, but without a SELECT here we return "now".
    return ModeratorBlacklistDomainDTO(
        domain=payload.domain.strip().lower(),
        createdat=_iso(datetime.now(tz=UTC)),
        comment=payload.comment,
        urls=[],
    )


@router.get("/moderator/blacklist/domains", response_model=ModeratorBlacklistDomainListResponseDTO)
async def list_blacklist_domains(
    limit: int = 200,
    offset: int = 0,
    session: AsyncSession = Depends(getdbsession),
) -> ModeratorBlacklistDomainListResponseDTO:
    repo = DomainBlacklistRepository(session)

    if hasattr(repo, "list_domains") and hasattr(repo, "count_domains"):
        total = await repo.count_domains()
        rows = await repo.list_domains(limit=limit, offset=offset)
        items = [
            ModeratorBlacklistDomainDTO(domain=d, createdat=_iso(ca), comment=None, urls=[])
            for (d, ca) in rows
        ]
        return ModeratorBlacklistDomainListResponseDTO(
            items=items, limit=limit, offset=offset, total=total
        )

    # Fallback (legacy)
    domains = await repo.list_root_domains(limit=limit)
    items = [
        ModeratorBlacklistDomainDTO(
            domain=d, createdat=_iso(datetime.now(tz=UTC)), comment=None, urls=[]
        )
        for d in domains
    ]
    return ModeratorBlacklistDomainListResponseDTO(
        items=items, limit=limit, offset=0, total=len(items)
    )


@router.delete("/moderator/blacklist/domains/{domain}")
async def delete_blacklist_domain(
    domain: str,
    session: AsyncSession = Depends(getdbsession),
) -> None:
    repo = DomainBlacklistRepository(session)
    await repo.remove_root_domain(domain)
    return None
