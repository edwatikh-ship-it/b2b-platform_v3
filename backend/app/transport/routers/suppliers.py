from fastapi import APIRouter, HTTPException, Query

router = APIRouter(tags=["Suppliers"])


@router.get("/suppliers/search")
async def suppliers_search(
    q: str = Query(..., min_length=1),
    limit: int = Query(20, ge=1, le=200),
):
    raise HTTPException(status_code=501, detail="Not Implemented")
