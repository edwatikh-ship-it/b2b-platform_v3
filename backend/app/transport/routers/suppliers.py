import httpx
from fastapi import APIRouter, HTTPException, Query

from app.adapters.checko.client import CheckoClient
from app.config import settings
from app.transport.schemas.suppliers import SupplierSearchItemDTO, SuppliersSearchResponseDTO
from app.usecases.search_suppliers import SearchSuppliersUseCase

router = APIRouter(prefix="/suppliers", tags=["Suppliers"])


def get_checko_client() -> CheckoClient:
    api_key = getattr(settings, "CHECKO_API_KEY", None)
    if not api_key:
        raise RuntimeError("checko_api_key_missing")
    return CheckoClient(api_key=api_key)


@router.get("/search", response_model=SuppliersSearchResponseDTO)
async def suppliers_search(
    q: str = Query(..., min_length=2),
    limit: int = Query(20, ge=1, le=200),
) -> SuppliersSearchResponseDTO:
    try:
        checko = get_checko_client()
    except RuntimeError:
        raise HTTPException(status_code=501, detail="Not Implemented")

    uc = SearchSuppliersUseCase(checko)

    try:
        items = await uc.execute(q=q, limit=limit)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except httpx.HTTPStatusError:
        # Внешний сервис вернул 4xx/5xx — это не "ошибка сервера", это upstream.
        raise HTTPException(status_code=502, detail="Upstream service error")

    return SuppliersSearchResponseDTO(
        items=[SupplierSearchItemDTO(**i.__dict__) for i in items],
        limit=int(limit),
    )
