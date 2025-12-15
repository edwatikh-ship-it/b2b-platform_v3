from typing import Any

from fastapi import APIRouter, Query

router = APIRouter(tags=["Suppliers"])


@router.get("/suppliers/search", summary="Suppliers Search")
async def suppliers_search(
    q: str = Query(..., min_length=1, title="Q"),
    limit: int = Query(20, ge=1, le=200, title="Limit"),
) -> Any:
    # Минимальная реализация: контракт на 200 не фиксирует schema, поэтому отдаём стабильный JSON.
    # Дальше заменим на реальный поиск по базе/индексу.
    return []
