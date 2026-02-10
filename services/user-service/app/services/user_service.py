from typing import Any

import pyotp
from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


async def get_user(db: AsyncSession, user_id: Any) -> User | None:
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalars().first()


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()


async def get_user_by_google_id(db: AsyncSession, google_id: str) -> User | None:
    result = await db.execute(select(User).filter(User.google_id == google_id))
    return result.scalars().first()


async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    hashed_password = get_password_hash(user_in.password)
    db_user = User(
        email=user_in.email,
        hashed_password=hashed_password,
        full_name=user_in.full_name,
        role=user_in.role,
        is_active=True,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def create_user_google(
    db: AsyncSession, email: str, google_id: str, full_name: str | None = None
) -> User:
    db_user = User(
        email=email,
        google_id=google_id,
        full_name=full_name,
        is_active=True,
        hashed_password=None,  # No password for Google users
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def authenticate_user(db: AsyncSession, email: str, password: str) -> User | None:
    user = await get_user_by_email(db, email)
    if not user or not user.hashed_password:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


async def update_user(db: AsyncSession, db_user: User, user_in: UserUpdate) -> User:
    update_data = user_in.model_dump(exclude_unset=True)
    if update_data.get("password"):
        hashed_password = get_password_hash(update_data["password"])
        db_user.hashed_password = hashed_password
        del update_data["password"]

    for field, value in update_data.items():
        setattr(db_user, field, value)

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def update_user_password(
    db: AsyncSession, db_user: User, new_password: str
) -> User:
    db_user.hashed_password = get_password_hash(new_password)
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


def generate_totp_secret() -> str:
    return pyotp.random_base32()


def get_totp_uri(email: str, secret: str, issuer_name: str = "MicroShop") -> str:
    return pyotp.totp.TOTP(secret).provisioning_uri(name=email, issuer_name=issuer_name)


def verify_totp_code(secret: str, code: str) -> bool:
    totp = pyotp.totp.TOTP(secret)
    return totp.verify(code)


async def enable_totp(db: AsyncSession, db_user: User, secret: str) -> User:
    db_user.totp_secret = secret
    db_user.is_totp_enabled = True
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def disable_totp(db: AsyncSession, db_user: User) -> User:
    db_user.totp_secret = None
    db_user.is_totp_enabled = False
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user
