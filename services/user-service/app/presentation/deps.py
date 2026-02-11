from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.clients.google_auth import HttpxGoogleAuthClient
from app.infrastructure.config import settings
from app.infrastructure.db.session import get_db
from app.infrastructure.persistence.models.user import User
from app.infrastructure.persistence.repositories.user_repository import (
    SqlAlchemyUserRepository,
)
from app.infrastructure.security.jwt_service import JoseJwtService
from app.infrastructure.security.password_hasher import BcryptPasswordHasher
from app.infrastructure.security.totp_service import PyotpTotpService
from app.presentation.schemas.user import TokenPayload

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")


def get_user_repo(
    db: AsyncSession = Depends(get_db),
) -> SqlAlchemyUserRepository:
    return SqlAlchemyUserRepository(db)


def get_password_hasher() -> BcryptPasswordHasher:
    return BcryptPasswordHasher()


def get_jwt_service() -> JoseJwtService:
    return JoseJwtService()


def get_totp_service() -> PyotpTotpService:
    return PyotpTotpService()


def get_google_auth_client() -> HttpxGoogleAuthClient:
    return HttpxGoogleAuthClient()


async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(reusable_oauth2),
) -> User:
    try:
        jwt_service = JoseJwtService()
        payload = jwt_service.decode_token(token)
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        ) from None
    if token_data.sub is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    repo = SqlAlchemyUserRepository(db)
    user = await repo.get_by_email(token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
