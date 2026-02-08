import os
from unittest.mock import AsyncMock, MagicMock

import pytest
import pytest_asyncio

# Set environment variables for testing
os.environ["DATABASE_URL"] = "postgresql+asyncpg://user:password@localhost/test_db"
os.environ["RABBITMQ_URL"] = "amqp://guest:guest@localhost/"
os.environ["SECRET_KEY"] = "test_secret_key"

from app.db.session import get_db
from app.main import app
from httpx import ASGITransport, AsyncClient


@pytest.fixture
def mock_db_session():
    session = AsyncMock()
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = []
    mock_result.scalars.return_value.first.return_value = None
    session.execute.return_value = mock_result
    return session


@pytest.fixture
def override_get_db(mock_db_session):
    async def _get_db():
        yield mock_db_session

    return _get_db


@pytest_asyncio.fixture
async def client(override_get_db):
    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
