import pytest
import pytest_asyncio
from app.main import app
from httpx import AsyncClient, ASGITransport


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
