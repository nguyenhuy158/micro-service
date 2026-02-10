import httpx
from fastapi import HTTPException, status

from app.domain.ports.google_auth_port import GoogleAuthPort
from app.infrastructure.config import settings


class HttpxGoogleAuthClient(GoogleAuthPort):
    async def verify_token(self, token: str) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://oauth2.googleapis.com/tokeninfo?id_token={token}"
            )
            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid Google token",
                )

            data = response.json()

            if (
                settings.GOOGLE_CLIENT_ID
                and data.get("aud") != settings.GOOGLE_CLIENT_ID
            ):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid Google token audience",
                )

            return data
