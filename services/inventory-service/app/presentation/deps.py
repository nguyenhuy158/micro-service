from uuid import UUID

import httpx
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.infrastructure.config import settings

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


async def get_current_user_id(
    token: str = Depends(reusable_oauth2),
) -> UUID:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{settings.USER_SERVICE_URL}/api/v1/users/me",
                headers={"Authorization": f"Bearer {token}"},
            )
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Could not validate credentials",
            )
        user_data = response.json()
        return UUID(user_data["id"])
    except httpx.HTTPError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        ) from None
