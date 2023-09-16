# Desc: Tests for the user routes
from fastapi.testclient import TestClient

from api.db import SessionLocal
from main import app  # Import your FastAPI app instance
from api.crud.core.user import User

# Create a test client
client = TestClient(app)

# Define a test user data for registration
test_user_data = {
    "bio": "hello I am there",
    "birthdate": "2023-04-24T22:01:32.904Z",
    "email": "user@example.com",
    "faculty": "engineering",
    "faculty_department": "electrical",
    "first_name": "John",
    "graduation_year": "2025",
    "last_name": "Jacky",
    "password": "stringst",
    "phone_number": "01234567891",
    "university": "zagmansoura",
    "username": "j3uvaobz"
}


# Create a test database engine and session


def test_signup():
    # Test user registration
    response = client.post("/users/signup", json=test_user_data)
    assert response.status_code == 201
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_duplicate_signup():
    # Test duplicate user registration
    response = client.post("/users/signup", json=test_user_data)
    assert response.status_code == 409
    assert response.json()["detail"] == "Email already exists"


def test_signin():
    # Test user login
    response = client.post("/users/signin", data={"username": test_user_data["username"], "password": "stringst"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


def test_invalid_signin():
    # Test invalid user login
    response = client.post("/users/signin", data={"username": test_user_data["username"], "password": "wrongpassword"})
    assert response.status_code == 401
    assert response.json()["detail"] == "incorrect password"


def test_check_username():
    # Test username availability
    response = client.post("/users/check-username", json={"username": "newusername"})
    assert response.status_code == 200
    assert response.json()["message"] == "username is available"


def test_taken_username():
    # Test taken username
    response = client.post("/users/check-username", json={"username": test_user_data["username"]})
    assert response.status_code == 409
    assert "username is taken" in response.json()["detail"]


def test_delete_user():
    with SessionLocal() as db:
        # Get the user's ID
        user = User.get_db_username_or_email(db, test_user_data["username"])
        assert user is not None

        # Test user deletion
        response = client.delete(f"/users/delete/{user.id}")
        assert response.status_code == 200
        assert response.json()["msg"] == "user deleted"
