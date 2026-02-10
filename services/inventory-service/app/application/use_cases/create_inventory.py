from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.repositories.inventory_repository import InventoryRepository
from app.infrastructure.persistence.models.inventory import Inventory
from app.presentation.schemas.inventory import InventoryCreate


class CreateInventoryUseCase:
    def __init__(self, repository: InventoryRepository) -> None:
        self._repository = repository

    async def execute(
        self, db: AsyncSession, inventory_in: InventoryCreate
    ) -> Inventory:
        existing = await self._repository.get_by_product_id(db, inventory_in.product_id)
        if existing:
            raise ValueError("Inventory for this product already exists")

        db_inventory = Inventory(**inventory_in.model_dump())
        return await self._repository.create(db, db_inventory)
