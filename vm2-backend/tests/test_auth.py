import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_login_success():
    """Test successful login with valid credentials"""
    response = client.post(
        "/api/auth/login",
        json={"user_id": 1, "company_id": 1}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_failure():
    """Test failed login with invalid credentials"""
    response = client.post(
        "/api/auth/login",
        json={"user_id": 999, "company_id": 999}
    )
    assert response.status_code == 401
    assert "detail" in response.json()

def test_login_missing_fields():
    """Test login with missing fields"""
    response = client.post(
        "/api/auth/login",
        json={"user_id": 1}  # Missing company_id
    )
    assert response.status_code == 422  # Validation error