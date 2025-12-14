from fastapi.testclient import TestClient
from app.main import app

def test_user_request_messages_not_implemented_yet():
    with TestClient(app) as client:
        r = client.get("/apiv1/user/requests/1/messages?limit=50&offset=0&includedeleted=false")
        assert r.status_code == 501

def test_update_recipients_not_implemented_yet():
    with TestClient(app) as client:
        r = client.put("/apiv1/user/requests/1/recipients", json={"recipients": [{"supplierid": 1, "selected": True}]})
        assert r.status_code == 501

def test_send_not_implemented_yet():
    with TestClient(app) as client:
        r = client.post("/apiv1/user/requests/1/send", json={"subject": "Hi", "body": "Test", "attachrequestfile": True, "attachmentids": []})
        assert r.status_code == 501

def test_send_new_not_implemented_yet():
    with TestClient(app) as client:
        r = client.post("/apiv1/user/requests/1/send-new", json={"subject": "Hi", "body": "Test", "attachrequestfile": True, "attachmentids": []})
        assert r.status_code == 501

def test_delete_message_not_implemented_yet():
    with TestClient(app) as client:
        r = client.delete("/apiv1/user/messages/1")
        assert r.status_code == 501