from unittest.mock import MagicMock, patch

import pytest
from httpx import Response


@pytest.mark.asyncio
async def test_login_google_success(client):
    # Mock Google token info response
    mock_google_data = {
        "sub": "google-id-123",
        "email": "test-google@example.com",
        "name": "Google User",
        "aud": "your-google-client-id",
    }

    with patch(
        "app.infrastructure.clients.google_auth.httpx.AsyncClient.get"
    ) as mock_get:
        mock_get.return_value = Response(200, json=mock_google_data)

        # Mock user_service functions to avoid DB issues in mock session
        with patch("app.api.v1.endpoints.auth.get_user_by_google_id") as mock_get_user:
            mock_get_user.return_value = None
            with patch("app.api.v1.endpoints.auth.get_user_by_email") as mock_get_email:
                mock_get_email.return_value = None
                with patch(
                    "app.api.v1.endpoints.auth.create_user_google"
                ) as mock_create:
                    mock_user = MagicMock()
                    mock_user.email = "test-google@example.com"
                    mock_user.is_active = True
                    mock_create.return_value = mock_user

                    from app.core.config import settings

                    with patch.object(
                        settings, "GOOGLE_CLIENT_ID", "your-google-client-id"
                    ):
                        response = await client.post(
                            "/api/v1/auth/login/google",
                            json={"id_token": "fake-google-token"},
                        )

                        assert response.status_code == 200
                        data = response.json()
                        assert "access_token" in data
                        assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_google_invalid_token(client):
    with patch(
        "app.infrastructure.clients.google_auth.httpx.AsyncClient.get"
    ) as mock_get:
        mock_get.return_value = Response(401, json={"error": "invalid_token"})

        response = await client.post(
            "/api/v1/auth/login/google", json={"id_token": "invalid-token"}
        )

        assert response.status_code == 401
        assert response.json()["detail"] == "Invalid Google token"
