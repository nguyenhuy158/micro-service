from typing import Any

from app.domain.repositories.product_repository import ProductRepository


class ListProductsUseCase:
    def __init__(self, repository: ProductRepository) -> None:
        self._repository = repository

    async def execute(self, skip: int = 0, limit: int = 100) -> list[Any]:
        return await self._repository.list(skip, limit)
