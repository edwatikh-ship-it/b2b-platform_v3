from fastapi.testclient import TestClient
from app.main import app

def test_suppliers_search_not_implemented_yet():
    with TestClient(app) as client:
        r = client.get("/apiv1/suppliers/search?q=bolt&limit=20")
        # Пока нет реализации — должен быть 501 (явно), а не 404
        assert r.status_code == 501