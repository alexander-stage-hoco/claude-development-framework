"""
Integration Tests for User API

Tests for user API endpoints (full HTTP request/response cycle).
"""

from fastapi import status


def test_create_user_endpoint(client):
    """Test POST /api/v1/users endpoint."""
    user_data = {
        "email": "newuser@example.com",
        "username": "newuser",
        "password": "SecurePass123!",
    }

    response = client.post("/api/v1/users/", json=user_data)

    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["username"] == user_data["username"]
    assert "id" in data
    assert "password" not in data  # Password should not be in response
    assert "hashed_password" not in data


def test_create_user_duplicate_email(client, created_user):
    """Test that duplicate email returns 400."""
    user_data = {
        "email": created_user.email,
        "username": "differentuser",
        "password": "SecurePass123!",
    }

    response = client.post("/api/v1/users/", json=user_data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "email" in response.json()["detail"].lower()


def test_create_user_invalid_email(client):
    """Test that invalid email returns 422 validation error."""
    user_data = {
        "email": "not-an-email",
        "username": "testuser",
        "password": "SecurePass123!",
    }

    response = client.post("/api/v1/users/", json=user_data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_user_weak_password(client):
    """Test that weak password returns 422 validation error."""
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "123",  # Too short
    }

    response = client.post("/api/v1/users/", json=user_data)

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_list_users_requires_auth(client):
    """Test that listing users requires authentication."""
    response = client.get("/api/v1/users/")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_list_users_with_auth(client, created_user, auth_headers):
    """Test listing users with authentication."""
    response = client.get("/api/v1/users/", headers=auth_headers)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert len(data["items"]) >= 1


def test_list_users_pagination(client, auth_headers):
    """Test user list pagination."""
    response = client.get("/api/v1/users/?skip=0&limit=5", headers=auth_headers)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["skip"] == 0
    assert data["limit"] == 5


def test_get_user_by_id(client, created_user, auth_headers):
    """Test GET /api/v1/users/{id} endpoint."""
    response = client.get(f"/api/v1/users/{created_user.id}", headers=auth_headers)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == str(created_user.id)
    assert data["email"] == created_user.email


def test_get_user_not_found(client, auth_headers):
    """Test GET /api/v1/users/{id} with non-existent ID."""
    fake_uuid = "00000000-0000-0000-0000-000000000000"
    response = client.get(f"/api/v1/users/{fake_uuid}", headers=auth_headers)

    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_update_user(client, created_user, auth_headers):
    """Test PUT /api/v1/users/{id} endpoint."""
    update_data = {
        "email": "updated@example.com",
        "username": "updateduser",
    }

    response = client.put(
        f"/api/v1/users/{created_user.id}",
        json=update_data,
        headers=auth_headers,
    )

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == update_data["email"]
    assert data["username"] == update_data["username"]


def test_update_user_unauthorized(client, created_user):
    """Test that updating user without auth returns 401."""
    update_data = {"email": "updated@example.com"}

    response = client.put(
        f"/api/v1/users/{created_user.id}",
        json=update_data,
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_delete_user(client, created_user, auth_headers):
    """Test DELETE /api/v1/users/{id} endpoint."""
    response = client.delete(f"/api/v1/users/{created_user.id}", headers=auth_headers)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    # Verify user is deleted
    response = client.get(f"/api/v1/users/{created_user.id}", headers=auth_headers)
    assert response.status_code == status.HTTP_404_NOT_FOUND
