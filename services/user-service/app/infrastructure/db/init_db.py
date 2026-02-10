import uuid

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.infrastructure.persistence.models.user import User
from app.infrastructure.security.password_hasher import BcryptPasswordHasher
from shared.enums.status import UserRole

TEST_USER_ID = uuid.UUID("550e8400-e29b-41d4-a716-446655440000")
TEST_ADMIN_ID = uuid.UUID("550e8400-e29b-41d4-a716-446655440001")

_hasher = BcryptPasswordHasher()


async def init_db(db: AsyncSession) -> None:
    result = await db.execute(select(User).limit(1))
    user = result.scalar_one_or_none()

    if not user:
        test_user = User(
            id=TEST_USER_ID,
            email="user@example.com",
            hashed_password=_hasher.hash("password123"),
            full_name="Test User",
            role=UserRole.CUSTOMER,
            is_active=True,
        )
        db.add(test_user)

        test_admin = User(
            id=TEST_ADMIN_ID,
            email="admin@example.com",
            hashed_password=_hasher.hash("admin123"),
            full_name="Test Admin",
            role=UserRole.ADMIN,
            is_active=True,
        )
        db.add(test_admin)

        await db.commit()
