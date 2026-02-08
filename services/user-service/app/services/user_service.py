from app.core.security import get_password_hash, verify_password
from app.models.user import User
from app.schemas.user import UserCreate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


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
