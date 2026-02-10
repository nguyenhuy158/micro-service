from abc import ABC, abstractmethod
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.persistence.models.inventory import ApiKey


class ApiKeyRepository(ABC):
    @abstractmethod
    async def get_by_order_id(
        self, db: AsyncSession, order_id: UUID
    ) -> list[ApiKey]: ...

    @abstractmethod
    async def get_by_user_id(self, db: AsyncSession, user_id: UUID) -> list[ApiKey]: ...

    @abstractmethod
    async def create(self, db: AsyncSession, api_key: ApiKey) -> ApiKey: ...
