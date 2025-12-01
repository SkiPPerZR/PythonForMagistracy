from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Тестовые данные
test_user = {
    "username": "testuser",
    "password": "testpass123"
}

# /register

def test_register_success():
    response = client.post("/register", json=test_user)
    assert response.status_code == 201 or response.status_code == 200
    assert "id" in response.json() or "username" in response.json()


def test_register_user_already_exists():
    client.post("/register", json=test_user)
    response = client.post("/register", json=test_user)
    assert response.status_code == 400 or response.status_code == 409


# /login

def test_login_success():
    client.post("/register", json=test_user)
    response = client.post("/login", json=test_user)
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_wrong_password():
    client.post("/register", json=test_user)
    response = client.post("/login", json={"username": "testuser", "password": "wrong"})
    assert response.status_code == 401

# /me

def get_token():
    client.post("/register", json=test_user)
    response = client.post("/login", json=test_user)
    return response.json()["access_token"]


def test_me_success():
    token = get_token()
    response = client.get("/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["username"] == "testuser"


def test_me_unauthorized():
    response = client.get("/me")
    assert response.status_code == 401

# /refresh

def test_refresh_success():
    token = get_token()
    response = client.post("/refresh", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_refresh_no_token():
    response = client.post("/refresh")
    assert response.status_code == 401

# /logout

def test_logout_success():
    token = get_token()
    response = client.post("/logout", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code in (200, 204)


def test_logout_unauthorized():
    response = client.post("/logout")
    assert response.status_code == 401
