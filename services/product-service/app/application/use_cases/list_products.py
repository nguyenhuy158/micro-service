from __future__ import annotations

import uuid
from typing import Any

from app.domain.repositories.product_repository import ProductRepository


class ListProductsUseCase:
    def __init__(self, repository: ProductRepository) -> None:
        self._repository = repository

    async def execute(
        self,
        skip: int = 0,
        limit: int = 100,
        category_id: uuid.UUID | None = None,
        min_price: float | None = None,
        max_price: float | None = None,
        in_stock: bool | None = None,
        sort_by: str | None = None,
    ) -> list[Any]:
        return await self._repository.list(
            skip=skip,
            limit=limit,
            category_id=category_id,
            min_price=min_price,
            max_price=max_price,
            in_stock=in_stock,
            sort_by=sort_by,
        )
