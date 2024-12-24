from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create():
    response = client.post("/create")
    assert response.status_code == 200


def test_start():
    response = client.post("/start", json={"task_id": 1})
    assert response.status_code == 200


def test_get_task_state():
    response = client.get("/get_task_state", params={"task_id": 1})
    assert response.status_code == 200


def test_get_state():
    response = client.get("/get_state")
    assert response.status_code == 200
