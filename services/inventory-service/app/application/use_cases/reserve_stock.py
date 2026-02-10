from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.repositories.inventory_repository import InventoryRepository


class ReserveStockUseCase:
    def __init__(self, repository: InventoryRepository) -> None:
        self._repository = repository

    async def execute(self, db: AsyncSession, product_id: UUID, quantity: int) -> bool:
        inventory = await self._repository.get_by_product_id(db, product_id)
        if not inventory:
            return False
        if inventory.available_quantity >= quantity:
            inventory.reserved_quantity += quantity
            await self._repository.save(db, inventory)
            return True
        return False
