from fastapi.testclient import TestClient

from app.main import app


def test_moderator_tasks_list_not_implemented_yet():
    with TestClient(app) as client:
        r = client.get("/apiv1/moderator/tasks?status=pending&limit=50")
        assert r.status_code == 501


def test_moderator_task_detail_not_implemented_yet():
    with TestClient(app) as client:
        r = client.get("/apiv1/moderator/tasks/1")
        assert r.status_code == 501


def test_moderator_start_parsing_not_implemented_yet():
    with TestClient(app) as client:
        r = client.post("/apiv1/moderator/requests/1/start-parsing")
        assert r.status_code == 501
