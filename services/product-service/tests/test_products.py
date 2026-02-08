import pytest
from unittest.mock import MagicMock
from app.models.product import Product, Category


@pytest.mark.asyncio
async def test_create_product(client, mock_db_session):
    # Setup mock behavior
    mock_db_session.add = MagicMock()
    mock_db_session.commit = MagicMock()
    mock_db_session.refresh = MagicMock()

    product_data = {
        "name": "Test Product",
        "description": "A test product",
        "price": 10.0,
        "stock": 100,
        "category_id": 1,
    }

    response = await client.post("/api/v1/products", json=product_data)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == product_data["name"]
    assert data["price"] == product_data["price"]

    # Verify DB interactions
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once()


@pytest.mark.asyncio
async def test_get_products(client, mock_db_session):
    # Setup mock return value
    mock_product = Product(id=1, name="Test Product", price=10.0, stock=100)
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [mock_product]
    mock_db_session.execute.return_value = mock_result

    response = await client.get("/api/v1/products")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Test Product"


@pytest.mark.asyncio
async def test_get_product_found(client, mock_db_session):
    # Setup mock return value
    mock_product = Product(id=1, name="Test Product", price=10.0, stock=100)
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = mock_product
    mock_db_session.execute.return_value = mock_result

    response = await client.get("/api/v1/products/1")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Test Product"


@pytest.mark.asyncio
async def test_get_product_not_found(client, mock_db_session):
    # Setup mock return value
    mock_result = MagicMock()
    mock_result.scalars.return_value.first.return_value = None
    mock_db_session.execute.return_value = mock_result

    response = await client.get("/api/v1/products/999")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_category(client, mock_db_session):
    # Setup mock behavior
    mock_db_session.add = MagicMock()
    mock_db_session.commit = MagicMock()
    mock_db_session.refresh = MagicMock()

    category_data = {"name": "Test Category", "description": "A test category"}

    response = await client.post("/api/v1/categories", json=category_data)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == category_data["name"]

    # Verify DB interactions
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    mock_db_session.refresh.assert_called_once()


@pytest.mark.asyncio
async def test_get_categories(client, mock_db_session):
    # Setup mock return value
    mock_category = Category(id=1, name="Test Category")
    mock_result = MagicMock()
    mock_result.scalars.return_value.all.return_value = [mock_category]
    mock_db_session.execute.return_value = mock_result

    response = await client.get("/api/v1/categories")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Test Category"
