from typing import Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.domain.repositories.user_repository import UserRepositoryInterface
from app.infrastructure.persistence.models.user import User


class SqlAlchemyUserRepository(UserRepositoryInterface):
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def get_by_id(self, user_id: UUID) -> User | None:
        result = await self._db.execute(select(User).filter(User.id == user_id))
        return result.scalars().first()

    async def get_by_email(self, email: str) -> User | None:
        result = await self._db.execute(select(User).filter(User.email == email))
        return result.scalars().first()

    async def get_by_google_id(self, google_id: str) -> User | None:
        result = await self._db.execute(
            select(User).filter(User.google_id == google_id)
        )
        return result.scalars().first()

    async def create(
        self,
        email: str,
        hashed_password: str | None,
        full_name: str | None,
        role: Any,
        is_active: bool,
        google_id: str | None = None,
    ) -> User:
        db_user = User(
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
            role=role,
            is_active=is_active,
            google_id=google_id,
        )
        self._db.add(db_user)
        await self._db.commit()
        await self._db.refresh(db_user)
        return db_user

    async def update(self, user: Any, **kwargs: Any) -> User:
        for field, value in kwargs.items():
            setattr(user, field, value)
        self._db.add(user)
        await self._db.commit()
        await self._db.refresh(user)
        return user

    async def has_any_user(self) -> bool:
        result = await self._db.execute(select(User).limit(1))
        return result.scalar_one_or_none() is not None
