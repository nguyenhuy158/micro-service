import secrets
import uuid
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.repositories.api_key_repository import ApiKeyRepository
from app.infrastructure.persistence.models.inventory import ApiKey


class SqlAlchemyApiKeyRepository(ApiKeyRepository):
    async def get_by_order_id(self, db: AsyncSession, order_id: UUID) -> list[ApiKey]:
        result = await db.execute(select(ApiKey).where(ApiKey.order_id == order_id))
        return list(result.scalars().all())

    async def get_by_user_id(self, db: AsyncSession, user_id: UUID) -> list[ApiKey]:
        result = await db.execute(select(ApiKey).where(ApiKey.user_id == user_id))
        return list(result.scalars().all())

    async def create(self, db: AsyncSession, api_key: ApiKey) -> ApiKey:
        if not api_key.key:
            api_key.key = f"sk_{secrets.token_urlsafe(32)}"
        if not api_key.id:
            api_key.id = uuid.uuid4()
        db.add(api_key)
        await db.commit()
        await db.refresh(api_key)
        return api_key
