from fastapi.testclient import TestClient

def test_create_user(test_client: TestClient):
    response = test_client.post(
        "/api/users",
        json={
            "user": {
                "username": "testuser",
                "email": "testuser@example.com",
                "password": "testpassword"
            }
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["user"]["username"] == "testuser"
    assert data["user"]["email"] == "testuser@example.com"