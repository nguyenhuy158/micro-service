from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest
from app.api import deps
from app.models.user import User


@pytest.mark.asyncio
async def test_register_user(client, mock_db_session):
    user_data = {
        "email": "test@example.com",
        "password": "password123",
        "full_name": "Test User",
    }

    user_id = uuid4()

    # Mock behavior
    with patch(
        "app.api.v1.endpoints.auth.get_user_by_email", new_callable=AsyncMock
    ) as mock_get_user:
        mock_get_user.return_value = None
        with patch(
            "app.api.v1.endpoints.auth.create_user", new_callable=AsyncMock
        ) as mock_create_user:
            mock_create_user.return_value = User(
                id=user_id,
                email=user_data["email"],
                full_name=user_data["full_name"],
                is_active=True,
            )

            response = await client.post("/api/v1/auth/register", json=user_data)

            assert response.status_code == 200
            data = response.json()
            assert data["email"] == user_data["email"]
            assert "id" in data


@pytest.mark.asyncio
async def test_login_user(client, mock_db_session):
    login_data = {"username": "test@example.com", "password": "password123"}

    user_id = uuid4()

    mock_user = User(
        id=user_id,
        email=login_data["username"],
        is_active=True,
        hashed_password="hashed_password",
    )

    with patch(
        "app.api.v1.endpoints.auth.authenticate_user", new_callable=AsyncMock
    ) as mock_auth:
        mock_auth.return_value = mock_user

        response = await client.post("/api/v1/auth/login", data=login_data)

        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_read_users_me(client, mock_db_session):
    user_id = uuid4()
    mock_user = User(
        id=user_id, email="test@example.com", full_name="Test User", is_active=True
    )

    # Override dependency
    async def mock_get_current_active_user():
        return mock_user

    from app.main import app

    app.dependency_overrides[deps.get_current_active_user] = (
        mock_get_current_active_user
    )

    try:
        response = await client.get("/api/v1/users/me")

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == mock_user.email
        assert data["full_name"] == mock_user.full_name
    finally:
        del app.dependency_overrides[deps.get_current_active_user]
