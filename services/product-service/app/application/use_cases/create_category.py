from typing import Any

from app.domain.repositories.category_repository import CategoryRepository


class CreateCategoryUseCase:
    def __init__(self, repository: CategoryRepository) -> None:
        self._repository = repository

    async def execute(self, data: dict[str, Any]) -> Any:
        return await self._repository.create(data)
