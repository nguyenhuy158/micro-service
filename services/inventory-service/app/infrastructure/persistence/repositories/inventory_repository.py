import uuid
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.repositories.inventory_repository import InventoryRepository
from app.infrastructure.persistence.models.inventory import Inventory


class SqlAlchemyInventoryRepository(InventoryRepository):
    async def get_by_product_id(
        self, db: AsyncSession, product_id: UUID
    ) -> Inventory | None:
        result = await db.execute(
            select(Inventory).where(Inventory.product_id == product_id)
        )
        return result.scalar_one_or_none()

    async def create(self, db: AsyncSession, inventory: Inventory) -> Inventory:
        if not inventory.id:
            inventory.id = uuid.uuid4()
        if inventory.reserved_quantity is None:
            inventory.reserved_quantity = 0
        db.add(inventory)
        await db.commit()
        await db.refresh(inventory)
        return inventory

    async def save(self, db: AsyncSession, inventory: Inventory) -> None:
        await db.commit()
