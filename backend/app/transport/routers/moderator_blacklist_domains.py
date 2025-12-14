from fastapi import APIRouter, HTTPException

router = APIRouter(tags=["Blacklist"])

@router.post("/moderator/blacklist/domains")
async def add_blacklist_domain(payload: dict):
    raise HTTPException(status_code=501, detail="Not Implemented")

@router.get("/moderator/blacklist/domains")
async def list_blacklist_domains(limit: int = 200):
    raise HTTPException(status_code=501, detail="Not Implemented")

@router.delete("/moderator/blacklist/domains/{domain}")
async def delete_blacklist_domain(domain: str):
    raise HTTPException(status_code=501, detail="Not Implemented")