from fastapi import APIRouter, HTTPException

router = APIRouter(tags=["Suppliers"])


@router.get("/suppliers/search")
async def suppliers_search(q: str, limit: int = 20):
    # Implemented later (DB + search logic). For now: explicit 501 per project rules.
    raise HTTPException(status_code=501, detail="Not Implemented")