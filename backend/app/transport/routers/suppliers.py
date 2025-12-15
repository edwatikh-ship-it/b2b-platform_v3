from typing import Any

from fastapi import APIRouter, Query

router = APIRouter(tags=["Suppliers"])


@router.get("/suppliers/search", summary="Suppliers Search")
async def suppliers_search(
    q: str = Query(..., min_length=1, title="Q"),
    limit: int = Query(20, ge=1, le=200, title="Limit"),
) -> dict[str, Any]:
    # Minimal stable response matching api-contracts.yaml.
    # TODO: replace with real search by DB/index.
    return {
        "items": [],
        "q": q,
        "limit": limit,
    }
