import uuid

from app.core.security import get_password_hash
from app.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from shared.enums.status import UserRole

# Fixed UUIDs for seeding to ensure consistent linking across services
TEST_USER_ID = uuid.UUID("550e8400-e29b-41d4-a716-446655440000")
TEST_ADMIN_ID = uuid.UUID("550e8400-e29b-41d4-a716-446655440001")


async def init_db(db: AsyncSession) -> None:
    # Check if we already have users
    result = await db.execute(select(User).limit(1))
    user = result.scalar_one_or_none()

    if not user:
        # Create a test customer
        test_user = User(
            id=TEST_USER_ID,
            email="user@example.com",
            hashed_password=get_password_hash("password123"),
            full_name="Test User",
            role=UserRole.CUSTOMER,
            is_active=True,
        )
        db.add(test_user)

        # Create a test admin
        test_admin = User(
            id=TEST_ADMIN_ID,
            email="admin@example.com",
            hashed_password=get_password_hash("admin123"),
            full_name="Test Admin",
            role=UserRole.ADMIN,
            is_active=True,
        )
        db.add(test_admin)

        await db.commit()
