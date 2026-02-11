import secrets
import uuid
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.repositories.api_key_repository import ApiKeyRepository
from app.infrastructure.persistence.models.inventory import ApiKey


class GenerateApiKeyUseCase:
    def __init__(self, repository: ApiKeyRepository) -> None:
        self._repository = repository

    async def execute(
        self,
        db: AsyncSession,
        user_id: UUID,
        product_id: UUID,
        order_id: UUID,
        quota_limit: int,
        rate_limit: int,
    ) -> ApiKey:
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
        return await self._repository.create(db, db_key)
