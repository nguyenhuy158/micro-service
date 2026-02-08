import uuid
import pytest
from unittest.mock import MagicMock, AsyncMock
from app.models.inventory import Inventory


@pytest.mark.asyncio
async def test_create_inventory(client, mock_db_session):
    product_id = str(uuid.uuid4())
    inventory_data = {
        "product_id": product_id,
        "quantity": 100,
        "location": "Warehouse A",
    }

    # Mock that inventory doesn't exist
    mock_db_session.execute.return_value.scalar_one_or_none.return_value = None

    # We need to mock the service or make sure the service returns a valid object
    # Since we are using the real service with a mock DB, we need to ensure
    # the object created by the service has its attributes set.
    # In SQLAlchemy, defaults are not always set immediately.

    response = await client.post("/api/v1/inventory/", json=inventory_data)
    assert response.status_code == 201
    assert response.json()["product_id"] == product_id
    assert "id" in response.json()
    assert response.json()["reserved_quantity"] == 0


@pytest.mark.asyncio
async def test_reserve_stock(client, mock_db_session):
    product_id = str(uuid.uuid4())
    reservation_data = {"product_id": product_id, "quantity": 10}

    # Mock existing inventory
    mock_inventory = Inventory(
        id=uuid.uuid4(),
        product_id=uuid.UUID(product_id),
        quantity=100,
        reserved_quantity=0,
    )
    mock_db_session.execute.return_value.scalar_one_or_none.return_value = (
        mock_inventory
    )

    response = await client.post("/api/v1/inventory/reserve", json=reservation_data)
    assert response.status_code == 200
    assert response.json()["status"] == "success"
    assert mock_inventory.reserved_quantity == 10


@pytest.mark.asyncio
async def test_reserve_stock_insufficient(client, mock_db_session):
    product_id = str(uuid.uuid4())
    reservation_data = {"product_id": product_id, "quantity": 110}

    # Mock existing inventory
    mock_inventory = Inventory(
        id=uuid.uuid4(),
        product_id=uuid.UUID(product_id),
        quantity=100,
        reserved_quantity=0,
    )
    mock_db_session.execute.return_value.scalar_one_or_none.return_value = (
        mock_inventory
    )

    response = await client.post("/api/v1/inventory/reserve", json=reservation_data)
    assert response.status_code == 400
    assert "Insufficient stock" in response.json()["detail"]
