from uuid import UUID

from app.infrastructure.persistence.models.inventory import ApiKey, Inventory
from app.infrastructure.persistence.repositories.api_key_repository import (
    SqlAlchemyApiKeyRepository,
)
from app.infrastructure.persistence.repositories.inventory_repository import (
    SqlAlchemyInventoryRepository,
)
from app.presentation.schemas.inventory import InventoryCreate
from sqlalchemy.ext.asyncio import AsyncSession

_inventory_repo = SqlAlchemyInventoryRepository()
_api_key_repo = SqlAlchemyApiKeyRepository()


class InventoryService:
    @staticmethod
    async def get_inventory_by_product(
        db: AsyncSession, product_id: UUID
    ) -> Inventory | None:
        return await _inventory_repo.get_by_product_id(db, product_id)

    @staticmethod
    async def create_inventory(
        db: AsyncSession, inventory_in: InventoryCreate
    ) -> Inventory:
        db_inventory = Inventory(**inventory_in.model_dump())
        return await _inventory_repo.create(db, db_inventory)

    @staticmethod
    async def update_stock(
        db: AsyncSession, product_id: UUID, quantity: int
    ) -> Inventory | None:
        db_inventory = await _inventory_repo.get_by_product_id(db, product_id)
        if db_inventory:
            db_inventory.quantity = quantity
            await _inventory_repo.save(db, db_inventory)
        return db_inventory

    @staticmethod
    async def reserve_stock(db: AsyncSession, product_id: UUID, quantity: int) -> bool:
        db_inventory = await _inventory_repo.get_by_product_id(db, product_id)
        if not db_inventory:
            return False
        if db_inventory.available_quantity >= quantity:
            db_inventory.reserved_quantity += quantity
            await _inventory_repo.save(db, db_inventory)
            return True
        return False

    @staticmethod
    async def release_stock(db: AsyncSession, product_id: UUID, quantity: int) -> bool:
        db_inventory = await _inventory_repo.get_by_product_id(db, product_id)
        if not db_inventory:
            return False
        db_inventory.reserved_quantity = max(
            0, db_inventory.reserved_quantity - quantity
        )
        await _inventory_repo.save(db, db_inventory)
        return True

    @staticmethod
    async def confirm_stock_deduction(
        db: AsyncSession, product_id: UUID, quantity: int
    ) -> bool:
        db_inventory = await _inventory_repo.get_by_product_id(db, product_id)
        if not db_inventory:
            return False
        if db_inventory.reserved_quantity >= quantity:
            db_inventory.reserved_quantity -= quantity
            db_inventory.quantity -= quantity
            await _inventory_repo.save(db, db_inventory)
            return True
        return False

    @staticmethod
    async def get_api_keys_by_order(db: AsyncSession, order_id: UUID) -> list[ApiKey]:
        return await _api_key_repo.get_by_order_id(db, order_id)

    @staticmethod
    async def get_api_keys_by_user(db: AsyncSession, user_id: UUID) -> list[ApiKey]:
        return await _api_key_repo.get_by_user_id(db, user_id)

    @staticmethod
    async def generate_api_key(
        db: AsyncSession,
        user_id: UUID,
        product_id: UUID,
        order_id: UUID,
        quota_limit: int,
        rate_limit: int,
    ) -> ApiKey:
        import secrets
        import uuid

        api_key_value = f"sk_{secrets.token_urlsafe(32)}"
        db_key = ApiKey(
            id=uuid.uuid4(),
            user_id=user_id,
            product_id=product_id,
            order_id=order_id,
            key=api_key_value,
            quota_limit=quota_limit,
            quota_used=0,
            rate_limit=rate_limit,
            is_active=True,
        )
        return await _api_key_repo.create(db, db_key)
