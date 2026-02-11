from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.repositories.api_key_repository import ApiKeyRepository
from app.infrastructure.persistence.models.inventory import ApiKey


class GetApiKeysUseCase:
    def __init__(self, repository: ApiKeyRepository) -> None:
        self._repository = repository

    async def get_by_order(self, db: AsyncSession, order_id: UUID) -> list[ApiKey]:
        return await self._repository.get_by_order_id(db, order_id)

    async def get_by_user(self, db: AsyncSession, user_id: UUID) -> list[ApiKey]:
        return await self._repository.get_by_user_id(db, user_id)
