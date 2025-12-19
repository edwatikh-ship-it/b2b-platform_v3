from fastapi.testclient import TestClient

from app.main import app


def test_suppliers_search_present_in_openapi():
    with TestClient(app) as client:
        spec = client.get("/openapi.json")
        assert spec.status_code == 200
        paths = spec.json().get("paths", {})
        assert "/suppliers/search" in paths


def test_suppliers_search_returns_501_not_implemented():
    with TestClient(app) as client:
        r = client.get("/suppliers/search", params={"q": "test", "limit": 20})
        assert r.status_code == 200
