from fastapi.testclient import TestClient

from app.main import app


def test_moderator_tasks_list_not_implemented_yet():
    with TestClient(app) as client:
        r = client.get("/moderator/tasks?status=pending&limit=50")
        assert r.status_code == 501


def test_moderator_task_detail_not_implemented_yet():
    with TestClient(app) as client:
        r = client.get("/moderator/tasks/1")
        assert r.status_code == 501


def test_moderator_start_parsing_not_implemented_yet():
    with TestClient(app) as client:
        r = client.post("/moderator/requests/1/start-parsing")
        # start-parsing уже реализован, так что тут не 501
        assert r.status_code in (200, 404, 422)
