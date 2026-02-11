from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.persistence.repositories.user_repository import (
    SqlAlchemyUserRepository,
)
from app.infrastructure.security.password_hasher import BcryptPasswordHasher
from app.infrastructure.security.totp_service import PyotpTotpService

_hasher = BcryptPasswordHasher()
_totp = PyotpTotpService()


async def get_user(db: AsyncSession, user_id: Any) -> Any | None:
    repo = SqlAlchemyUserRepository(db)
    return await repo.get_by_id(user_id)


async def get_user_by_email(db: AsyncSession, email: str) -> Any | None:
    repo = SqlAlchemyUserRepository(db)
    return await repo.get_by_email(email)


async def get_user_by_google_id(db: AsyncSession, google_id: str) -> Any | None:
    repo = SqlAlchemyUserRepository(db)
    return await repo.get_by_google_id(google_id)


async def create_user(db: AsyncSession, user_in: Any) -> Any:
    repo = SqlAlchemyUserRepository(db)
    hashed_password = _hasher.hash(user_in.password)
    return await repo.create(
        email=user_in.email,
        hashed_password=hashed_password,
        full_name=user_in.full_name,
        role=user_in.role,
        is_active=True,
    )


async def create_user_google(
    db: AsyncSession, email: str, google_id: str, full_name: str | None = None
) -> Any:
    repo = SqlAlchemyUserRepository(db)
    return await repo.create(
        email=email,
        google_id=google_id,
        full_name=full_name,
        hashed_password=None,
        role=None,
        is_active=True,
    )


async def authenticate_user(db: AsyncSession, email: str, password: str) -> Any | None:
    repo = SqlAlchemyUserRepository(db)
    user = await repo.get_by_email(email)
    if not user or not user.hashed_password:
        return None
    if not _hasher.verify(password, user.hashed_password):
        return None
    return user


async def update_user(db: AsyncSession, db_user: Any, user_in: Any) -> Any:
    repo = SqlAlchemyUserRepository(db)
    update_data = user_in.model_dump(exclude_unset=True)
    if update_data.get("password"):
        update_data["hashed_password"] = _hasher.hash(update_data["password"])
        del update_data["password"]
    return await repo.update(db_user, **update_data)


async def update_user_password(
    db: AsyncSession, db_user: Any, new_password: str
) -> Any:
    repo = SqlAlchemyUserRepository(db)
    hashed = _hasher.hash(new_password)
    return await repo.update(db_user, hashed_password=hashed)


def generate_totp_secret() -> str:
    return _totp.generate_secret()


def get_totp_uri(email: str, secret: str, issuer_name: str = "MicroShop") -> str:
    return _totp.get_uri(email, secret, issuer_name)


def verify_totp_code(secret: str, code: str) -> bool:
    return _totp.verify_code(secret, code)


async def enable_totp(db: AsyncSession, db_user: Any, secret: str) -> Any:
    repo = SqlAlchemyUserRepository(db)
    return await repo.update(db_user, totp_secret=secret, is_totp_enabled=True)


async def disable_totp(db: AsyncSession, db_user: Any) -> Any:
    repo = SqlAlchemyUserRepository(db)
    return await repo.update(db_user, totp_secret=None, is_totp_enabled=False)
