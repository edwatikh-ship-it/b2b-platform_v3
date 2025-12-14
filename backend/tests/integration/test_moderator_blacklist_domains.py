from fastapi.testclient import TestClient

from app.main import app


def test_moderator_blacklist_domains_add_not_implemented_yet():
    with TestClient(app) as client:
        r = client.post(
            "/apiv1/moderator/blacklist/domains",
            json={"domaincanonical": "example.com", "reason": "pytest"},
        )
        assert r.status_code == 501


def test_moderator_blacklist_domains_list_not_implemented_yet():
    with TestClient(app) as client:
        r = client.get("/apiv1/moderator/blacklist/domains?limit=200")
        assert r.status_code == 501


def test_moderator_blacklist_domains_delete_not_implemented_yet():
    with TestClient(app) as client:
        r = client.delete("/apiv1/moderator/blacklist/domains/example.com")
        assert r.status_code == 501
