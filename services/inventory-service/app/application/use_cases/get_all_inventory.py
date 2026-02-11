from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.repositories.inventory_repository import InventoryRepository
from app.infrastructure.persistence.models.inventory import Inventory


class GetAllInventoryUseCase:
    def __init__(self, repository: InventoryRepository) -> None:
        self._repository = repository

    async def execute(
        self, db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> list[Inventory]:
        return await self._repository.get_all(db, skip=skip, limit=limit)
