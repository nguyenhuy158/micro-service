from typing import Any

from app.domain.repositories.product_repository import ProductRepository


class CreateProductUseCase:
    def __init__(self, repository: ProductRepository) -> None:
        self._repository = repository

    async def execute(self, data: dict[str, Any]) -> Any:
        return await self._repository.create(data)
