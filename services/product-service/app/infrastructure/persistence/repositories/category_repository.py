from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.domain.repositories.category_repository import (
    CategoryRepository as CategoryRepositoryABC,
)
from app.infrastructure.persistence.models.product import Category


class SqlAlchemyCategoryRepository(CategoryRepositoryABC):
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def create(self, data: dict[str, Any]) -> Category:
        db_category = Category(**data)
        self._db.add(db_category)
        await self._db.commit()
        await self._db.refresh(db_category)
        return db_category

    async def list(self, skip: int = 0, limit: int = 100) -> list[Category]:
        query = select(Category).offset(skip).limit(limit)
        result = await self._db.execute(query)
        return list(result.scalars().all())
