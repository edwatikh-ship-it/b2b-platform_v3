from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.adapters.db.session import getdbsession
from app.adapters.db.repositories import UserRepository
from app.transport.schemas.auth import UpdateEmailPolicyRequestDTO
from app.usecases.update_email_policy import UpdateEmailPolicyUseCase

router = APIRouter(tags=["Auth"])


def require_userid(authorization: str | None) -> int:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing Bearer token")
    # MVP dev auth
    return 1


@router.get("/auth/oauth/google/start")
async def auth_oauth_google_start():
    raise HTTPException(status_code=501, detail="Not Implemented")


@router.get("/auth/oauth/google/callback")
async def auth_oauth_google_callback(code: str):
    raise HTTPException(status_code=501, detail="Not Implemented")


@router.get("/auth/me")
async def auth_me(
    authorization: str | None = Header(default=None),
    db: AsyncSession = Depends(getdbsession),
) -> dict:
    userid = require_userid(authorization)
    repo = UserRepository(db)
    user = await repo.get_or_create(userid=userid, email="dev@example.com")
    return {
        "id": int(user.id),
        "email": str(user.email),
        "emailpolicy": str(user.emailpolicy),
        "createdat": user.createdat.isoformat() if getattr(user, "createdat", None) else None,
    }


@router.put("/auth/policy")
async def update_auth_policy(
    payload: UpdateEmailPolicyRequestDTO,
    authorization: str | None = Header(default=None),
    db: AsyncSession = Depends(getdbsession),
) -> dict:
    userid = require_userid(authorization)
    repo = UserRepository(db)
    try:
        user = await UpdateEmailPolicyUseCase(repo).execute(userid=userid, emailpolicy=payload.emailpolicy)
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid emailpolicy")
    return {
        "id": int(user.id),
        "email": str(user.email),
        "emailpolicy": str(user.emailpolicy),
        "createdat": user.createdat.isoformat() if getattr(user, "createdat", None) else None,
    }