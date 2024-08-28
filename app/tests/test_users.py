from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user():
    response = client.post(
        "/api/users/",
        json={
            "user": {
                "username": "testuser",
                "email": "test@example.com",
                "password": "password123"
            }
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "user" in data
    assert data["user"]["username"] == "testuser"
    assert data["user"]["email"] == "test@example.com"
    