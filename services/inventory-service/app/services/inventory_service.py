import uuid
from uuid import UUID

from app.models.inventory import Inventory
from app.schemas.inventory import InventoryCreate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class InventoryService:
    @staticmethod
    async def get_inventory_by_product(
        db: AsyncSession, product_id: UUID
    ) -> Inventory | None:
        result = await db.execute(
            select(Inventory).where(Inventory.product_id == product_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def create_inventory(
        db: AsyncSession, inventory_in: InventoryCreate
    ) -> Inventory:
        db_inventory = Inventory(**inventory_in.model_dump())
        if not db_inventory.id:
            db_inventory.id = uuid.uuid4()
        if db_inventory.reserved_quantity is None:
            db_inventory.reserved_quantity = 0
        db.add(db_inventory)
        await db.commit()
        await db.refresh(db_inventory)
        return db_inventory

    @staticmethod
    async def update_stock(
        db: AsyncSession, product_id: UUID, quantity: int
    ) -> Inventory | None:
        db_inventory = await InventoryService.get_inventory_by_product(db, product_id)
        if db_inventory:
            db_inventory.quantity = quantity
            await db.commit()
            await db.refresh(db_inventory)
        return db_inventory

    @staticmethod
    async def reserve_stock(db: AsyncSession, product_id: UUID, quantity: int) -> bool:
        db_inventory = await InventoryService.get_inventory_by_product(db, product_id)
        if not db_inventory:
            return False

        if db_inventory.available_quantity >= quantity:
            db_inventory.reserved_quantity += quantity
            await db.commit()
            return True
        return False

    @staticmethod
    async def release_stock(db: AsyncSession, product_id: UUID, quantity: int) -> bool:
        db_inventory = await InventoryService.get_inventory_by_product(db, product_id)
        if not db_inventory:
            return False

        db_inventory.reserved_quantity = max(
            0, db_inventory.reserved_quantity - quantity
        )
        await db.commit()
        return True

    @staticmethod
    async def confirm_stock_deduction(
        db: AsyncSession, product_id: UUID, quantity: int
    ) -> bool:
        db_inventory = await InventoryService.get_inventory_by_product(db, product_id)
        if not db_inventory:
            return False

        if db_inventory.reserved_quantity >= quantity:
            db_inventory.reserved_quantity -= quantity
            db_inventory.quantity -= quantity
            await db.commit()
            return True
        return False
