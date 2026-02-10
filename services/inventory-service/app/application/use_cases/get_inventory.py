from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.repositories.inventory_repository import InventoryRepository
from app.infrastructure.persistence.models.inventory import Inventory


class GetInventoryUseCase:
    def __init__(self, repository: InventoryRepository) -> None:
        self._repository = repository

    async def execute(self, db: AsyncSession, product_id: UUID) -> Inventory | None:
        return await self._repository.get_by_product_id(db, product_id)
