from fastapi.testclient import TestClient
from ..app import app
import pytest

client = TestClient(app)

def test_register():
    # Registro Test
    response = client.post(
        "/auth/register",
        auth=("testuser", "testpass")
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    

def test_login():
    # Login Tests
    response = client.post(
        "/auth/login",
        auth=("testuser", "testpass")
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    
def test_login_wrong_password():
    client.post("/auth/register", auth=("user2", "pass2"))
    response = client.post("/auth/login", auth=("user2", "wrongpass"))
    assert response.status_code == 401
