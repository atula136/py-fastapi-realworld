import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.db.models import User
from app.schemas.user import UserCreate
from app.core.security.jwt import create_access_token, get_password_hash, verify_password
from app.crud.user import create_user

@pytest.fixture()
def test_user(db_session: Session):
    """
    Fixture to create a test user.
    """
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    }
    user_data = UserCreate(**user_data)
    user_data.password = get_password_hash(user_data.password)
    user = create_user(db_session, user_data)
    return user

# @pytest.fixture
# def test_user(db_session):
#     print(f"Session ID in create test user: {id(db_session)}")
#     hashed_password = get_password_hash("password123")
#     user = User(
#         username="testuser",
#         email="test@example.com",
#         password=hashed_password
#     )
#     db_session.add(user)
#     db_session.commit()
#     db_session.refresh(user)
#     return user

def test_login(test_client, db_session, test_user: User):

    url = "/api/users/login/"
    response = test_client.post(url, json={
        "user": {
            "email": test_user.email,
            "password": "password123",
        }
    })
    
    assert response.status_code == 200


def test_follow_user(test_client: TestClient, db_session: Session, test_user: User):
    """
    Test following a user.
    """
    # Authenticate the user and obtain a token
    response = test_client.post("/api/users/login", json={
        "user": {
            "email": test_user.email,
            "password": "password123",
        }
    })
    # Check if the response is successful
    assert response.status_code == 200, f"Login failed: {response.json()}"
    token = response.json()["user"]["token"]

    # Follow another user
    follow_username = "otheruser"
    db_session.add(User(username=follow_username, email="other@example.com", password="password456"))
    db_session.commit()

    # Query the newly added user to ensure they exist
    followed_user = db_session.query(User).filter_by(username=follow_username).first()
    assert followed_user is not None, "The user to follow was not found in the database."

    # Follow the new user
    response = test_client.post(f"/api/profiles/{follow_username}/follow", headers={
        "Authorization": f"Token {token}"
    })

    # Assert the follow was successful
    assert response.status_code == 200, f"Following user failed: {response.json()}"
    assert response.json()["profile"]["username"] == follow_username
    assert response.json()["profile"]["following"] is True

def test_unfollow_user(test_client: TestClient, db_session: Session, test_user: User):
    """
    Test unfollowing a user.
    """
    # Authenticate the user and obtain a token
    response = test_client.post("/api/users/login", json={
        "user": {
            "email": test_user.email,
            "password": "password123",
        }
    })
    token = response.json()["user"]["token"]

    # Follow and then unfollow another user
    follow_username = "otheruser"
    db_session.add(User(username=follow_username, email="other@example.com", password="password456"))
    db_session.commit()

    test_client.post(f"/api/profiles/{follow_username}/follow", headers={
        "Authorization": f"Token {token}"
    })

    response = test_client.delete(f"/api/profiles/{follow_username}/follow", headers={
        "Authorization": f"Token {token}"
    })

    assert response.status_code == 200
    assert response.json()["profile"]["username"] == follow_username
    assert response.json()["profile"]["following"] is False

""" """
@pytest.fixture
def create_test_user(db_session: Session):
    user_data = {
        "username": "user1",
        "email": "user1@example.com",
        "password": "password"
    }
    user = User(**user_data)
    user.password = "password_hashed"
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture
def create_second_user(db_session: Session):
    user_data = {
        "username": "user2",
        "email": "user2@example.com",
        "password": "password"
    }
    user = User(**user_data)
    user.password = "password_hashed"
    db_session.add(user)
    db_session.commit()
    return user

def get_auth_headers(user: User):
    token = create_access_token({"sub": user.id})
    return {"Authorization": f"Token {token}"}

def test_follow_user_2(test_client: TestClient, db_session: Session, create_test_user, create_second_user):
    auth_headers = get_auth_headers(create_test_user)
    
    response = test_client.post(
        f"/api/profiles/{create_second_user.username}/follow",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json() == {
        "profile": {
            "username": create_second_user.username,
            "bio": None,
            "image": None,
            "following": True
        }
    }

def test_unfollow_user_2(test_client: TestClient, db_session: Session, create_test_user, create_second_user):
    auth_headers = get_auth_headers(create_test_user)

    response = test_client.delete(
        f"/api/profiles/{create_second_user.username}/follow",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json() == {
        "profile": {
            "username": create_second_user.username,
            "bio": None,
            "image": None,
            "following": False
        }
    }

def test_prevent_duplicate_follow(test_client: TestClient, db_session: Session, create_test_user, create_second_user):
    auth_headers = get_auth_headers(create_test_user)

    # Follow once
    test_client.post(
        f"/api/profiles/{create_second_user.username}/follow",
        headers=auth_headers
    )

    # Follow again
    response = test_client.post(
        f"/api/profiles/{create_second_user.username}/follow",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json() == {
        "profile": {
            "username": create_second_user.username,
            "bio": None,
            "image": None,
            "following": True
        }
    }

def test_follow_non_existent_user(test_client: TestClient, db_session: Session, create_test_user):
    auth_headers = get_auth_headers(create_test_user)

    response = test_client.post(
        "/api/profiles/nonexistentuser/follow",
        headers=auth_headers
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}

def test_unfollow_non_existent_user(test_client: TestClient, db_session: Session, create_test_user):
    auth_headers = get_auth_headers(create_test_user)

    response = test_client.delete(
        "/api/profiles/nonexistentuser/follow",
        headers=auth_headers
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "User not found"}