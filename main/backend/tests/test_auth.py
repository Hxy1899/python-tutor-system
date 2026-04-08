def test_register(client):
    response = client.post(
        "/api/v1/auth/register",
        json={"username": "testuser", "password": "testpassword", "name": "Test Student", "role": "student"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["role"] == "student"

def test_login(client):
    # Register first
    client.post(
        "/api/v1/auth/register",
        json={"username": "loginuser", "password": "loginpassword", "name": "Login Test", "role": "student"},
    )
    
    # Login
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "loginuser", "password": "loginpassword"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password(client):
    response = client.post(
        "/api/v1/auth/login",
        json={"username": "loginuser", "password": "wrongpassword"},
    )
    assert response.status_code == 401
