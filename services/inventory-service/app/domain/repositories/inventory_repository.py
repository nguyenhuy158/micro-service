from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.persistence.models.inventory import Inventory


class InventoryRepository(ABC):
    @abstractmethod
    async def get_by_product_id(
        self, db: AsyncSession, product_id: UUID
    ) -> Inventory | None: ...

    @abstractmethod
    async def get_all(
        self, db: AsyncSession, skip: int = 0, limit: int = 100
    ) -> list[Inventory]: ...

    @abstractmethod
    async def create(self, db: AsyncSession, inventory: Inventory) -> Inventory: ...

    @abstractmethod
    async def save(self, db: AsyncSession, inventory: Inventory) -> None: ...
