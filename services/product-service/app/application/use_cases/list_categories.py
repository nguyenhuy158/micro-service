from typing import Any

from app.domain.repositories.category_repository import CategoryRepository


class ListCategoriesUseCase:
    def __init__(self, repository: CategoryRepository) -> None:
        self._repository = repository

    async def execute(self, skip: int = 0, limit: int = 100) -> list[Any]:
        return await self._repository.list(skip, limit)
