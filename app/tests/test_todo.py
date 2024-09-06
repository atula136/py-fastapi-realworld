from fastapi.testclient import TestClient

def test_create_todo(test_client: TestClient):
    response = test_client.post("/todos/", json={"title": "Test", "description": "Test description"})
    assert response.status_code == 200
    assert response.json()["title"] == "Test"
