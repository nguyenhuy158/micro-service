from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Adjust URL for asyncpg
SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL
if SQLALCHEMY_DATABASE_URL.startswith("postgresql://"):
    SQLALCHEMY_DATABASE_URL = SQLALCHEMY_DATABASE_URL.replace(
        "postgresql://", "postgresql+asyncpg://", 1
    )

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True,  # Set to False in production
    future=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
