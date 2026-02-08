import uuid
from unittest.mock import AsyncMock, MagicMock

import pytest
from app.models.product import Category, Product


@pytest.mark.asyncio
async def test_create_product(client, mock_db_session):
    # Setup mock behavior
    mock_db_session.add = MagicMock()
    mock_db_session.commit = AsyncMock()

    test_id = uuid.uuid4()
    test_cat_id = uuid.uuid4()

    async def mock_refresh(obj):
        obj.id = test_id

    mock_db_session.refresh = AsyncMock(side_effect=mock_refresh)

    product_data = {
        "name": "Test Product",
        "description": "A test product",
        "price": 10.0,
        "stock": 100,
        "category_id": str(test_cat_id),
        "api_url": "http://test.com",
        "quota_limit": 1000,
        "rate_limit": 60,
    }

    response = await client.post("/api/v1/products", json=product_data)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == product_data["name"]
    assert data["price"] == product_data["price"]
    assert data["id"] == str(test_id)

    # Verify DB interactions
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once()


@pytest.mark.asyncio
async def test_get_products(client, mock_db_session):
    # Setup mock return value
    test_id = uuid.uuid4()
    mock_product = Product(
        id=test_id,
        name="Test Product",
        price=10.0,
        stock=100,
        quota_limit=1000,
        rate_limit=60,
    )
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [mock_product]
    mock_db_session.execute.return_value = mock_result

    response = await client.get("/api/v1/products")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Test Product"
    assert data[0]["id"] == str(test_id)


@pytest.mark.asyncio
async def test_get_product_found(client, mock_db_session):
    # Setup mock return value
    test_id = uuid.uuid4()
    mock_product = Product(
        id=test_id,
        name="Test Product",
        price=10.0,
        stock=100,
        quota_limit=1000,
        rate_limit=60,
    )
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = mock_product
    mock_db_session.execute.return_value = mock_result

    response = await client.get(f"/api/v1/products/{test_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(test_id)
    assert data["name"] == "Test Product"


@pytest.mark.asyncio
async def test_get_product_not_found(client, mock_db_session):
    # Setup mock return value
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = None
    mock_db_session.execute.return_value = mock_result

    test_id = uuid.uuid4()
    response = await client.get(f"/api/v1/products/{test_id}")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_category(client, mock_db_session):
    # Setup mock behavior
    mock_db_session.add = MagicMock()
    mock_db_session.commit = AsyncMock()

    test_id = uuid.uuid4()

    async def mock_refresh(obj):
        obj.id = test_id

    mock_db_session.refresh = AsyncMock(side_effect=mock_refresh)

    category_data = {"name": "Test Category", "description": "A test category"}

    response = await client.post("/api/v1/categories", json=category_data)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == category_data["name"]
    assert data["id"] == str(test_id)

    # Verify DB interactions
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once()


@pytest.mark.asyncio
async def test_get_categories(client, mock_db_session):
    # Setup mock return value
    test_id = uuid.uuid4()
    mock_category = Category(id=test_id, name="Test Category")
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [mock_category]
    mock_db_session.execute.return_value = mock_result

    response = await client.get("/api/v1/categories")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Test Category"
    assert data[0]["id"] == str(test_id)
