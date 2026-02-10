import uuid
from typing import Any

from app.domain.repositories.product_repository import ProductRepository


class GetProductUseCase:
    def __init__(self, repository: ProductRepository) -> None:
        self._repository = repository

    async def execute(self, product_id: uuid.UUID) -> Any | None:
        return await self._repository.get_by_id(product_id)
