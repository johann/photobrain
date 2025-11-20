from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_health():
    response = client.get("/api/system/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_list_shoots():
    response = client.get("/api/shoots")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_photo_rating():
    response = client.patch("/api/photos/photo-1", params={"rating": 5})
    assert response.status_code == 200
    payload = response.json()
    assert payload["rating"] == 5
