from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_todo():
    response = client.post("/todos/", json={"title": "Test", "description": "Test description"})
    assert response.status_code == 200
    assert response.json()["title"] == "Test"

# More test cases here...
