from fastapi.testclient import TestClient

from app.main import app


class _FakeChecko:
    async def search_companies(self, *, q: str, limit: int):
        return [
            {
                "ИНН": "7735560386",
                "НаимСокр": 'ООО "1С-СТАРТ"',
                "Контакты": {"Емэйл": ["contact@1c-start.biz"], "ВебСайт": "https://1c-start.biz"},
            }
        ]


def test_suppliers_search_returns_items(monkeypatch):
    from app.transport.routers import suppliers as suppliers_router

    monkeypatch.setattr(suppliers_router, "get_checko_client", lambda: _FakeChecko())

    with TestClient(app) as client:
        r = client.get("/apiv1/suppliers/search?q=1c&limit=20")
        assert r.status_code == 200, r.text
        data = r.json()
        assert "items" in data
        assert data["limit"] == 20
        assert len(data["items"]) == 1
        assert data["items"][0]["inn"] == "7735560386"
        assert data["items"][0]["suppliername"]
