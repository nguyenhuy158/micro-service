import os
from unittest.mock import AsyncMock, MagicMock

import pytest
import pytest_asyncio

os.environ["DATABASE_URL"] = "postgresql+asyncpg://user:password@localhost/test_db"
os.environ["RABBITMQ_URL"] = "amqp://guest:guest@localhost/"
os.environ["MEILISEARCH_URL"] = "http://localhost:7700"
os.environ["MEILISEARCH_KEY"] = "test_key"

from app.db.session import get_db
from app.infrastructure.search.meili_client import get_meili_client
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


@pytest.fixture
def mock_meili_client():
    client = MagicMock()
    client.index_product.return_value = {"taskUid": 1}
    client.delete_product.return_value = {"taskUid": 2}
    client.search.return_value = {
        "hits": [],
        "estimatedTotalHits": 0,
        "offset": 0,
        "limit": 20,
        "processingTimeMs": 0,
        "query": "",
    }
    return client


@pytest_asyncio.fixture
async def client(override_get_db, mock_meili_client):
    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_meili_client] = lambda: mock_meili_client
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
