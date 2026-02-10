import uuid
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.domain.repositories.product_repository import (
    ProductRepository as ProductRepositoryABC,
)
from app.infrastructure.persistence.models.product import Product


class SqlAlchemyProductRepository(ProductRepositoryABC):
    def __init__(self, db: AsyncSession) -> None:
        self._db = db

    async def create(self, data: dict[str, Any]) -> Product:
        db_product = Product(**data)
        self._db.add(db_product)
        await self._db.commit()
        await self._db.refresh(db_product)
        return db_product

    async def get_by_id(self, product_id: uuid.UUID) -> Product | None:
        query = (
            select(Product)
            .options(selectinload(Product.category))
            .where(Product.id == product_id)
        )
        result = await self._db.execute(query)
        return result.scalar_one_or_none()

    async def list(self, skip: int = 0, limit: int = 100) -> list[Product]:
        query = (
            select(Product)
            .options(selectinload(Product.category))
            .offset(skip)
            .limit(limit)
        )
        result = await self._db.execute(query)
        return list(result.scalars().all())
