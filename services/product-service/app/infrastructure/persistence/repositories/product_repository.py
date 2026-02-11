from __future__ import annotations

import uuid
from typing import Any

from sqlalchemy import asc, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.domain.repositories.product_repository import (
    ProductRepository as ProductRepositoryABC,
)
from app.infrastructure.persistence.models.product import Product

SORT_OPTIONS: dict[str, Any] = {
    "price_asc": asc(Product.price),
    "price_desc": desc(Product.price),
    "name_asc": asc(Product.name),
    "name_desc": desc(Product.name),
    "newest": desc(Product.id),
}


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

    async def list(
        self,
        skip: int = 0,
        limit: int = 100,
        category_id: uuid.UUID | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        in_stock: bool | None = None,
        sort_by: str | None = None,
    ) -> list[Product]:
        query = select(Product).options(selectinload(Product.category))

        if category_id is not None:
            query = query.where(Product.category_id == category_id)
        if min_price is not None:
            query = query.where(Product.price >= min_price)
        if max_price is not None:
            query = query.where(Product.price <= max_price)
        if in_stock is not None:
            if in_stock:
                query = query.where(Product.stock > 0)
            else:
                query = query.where(Product.stock == 0)

        if sort_by and sort_by in SORT_OPTIONS:
            query = query.order_by(SORT_OPTIONS[sort_by])

        query = query.offset(skip).limit(limit)
        result = await self._db.execute(query)
        return list(result.scalars().all())
