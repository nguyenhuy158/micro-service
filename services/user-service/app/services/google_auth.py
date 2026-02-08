import httpx
from app.core.config import settings
from fastapi import HTTPException, status


async def verify_google_token(token: str) -> dict:
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

        # Verify audience
        if settings.GOOGLE_CLIENT_ID and data.get("aud") != settings.GOOGLE_CLIENT_ID:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Google token audience",
            )

        return data
