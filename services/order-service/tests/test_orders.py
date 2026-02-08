import uuid
import pytest
from unittest.mock import AsyncMock, patch
from app.models.order import Order
from shared.enums.status import OrderStatus


@pytest.mark.asyncio
async def test_create_order_success(client, mock_db_session):
    user_id = str(uuid.uuid4())
    product_id = str(uuid.uuid4())
    order_data = {
        "user_id": user_id,
        "shipping_address": "123 Street",
        "items": [{"product_id": product_id, "quantity": 2, "price": 50.0}],
    }

    # Mock InternalServiceClient
    with (
        patch(
            "app.services.order_service.InternalServiceClient.reserve_stock",
            new_callable=AsyncMock,
        ) as mock_reserve,
        patch(
            "app.services.order_service.InternalServiceClient.process_payment",
            new_callable=AsyncMock,
        ) as mock_payment,
    ):
        mock_reserve.return_value = True
        mock_payment.return_value = True

        # Mock session behavior
        mock_db_session.refresh = AsyncMock()

        response = await client.post("/api/v1/orders/", json=order_data)

        assert response.status_code == 201
        data = response.json()
        assert data["user_id"] == user_id
        assert data["status"] == OrderStatus.PAID
        assert data["total_amount"] == 100.0
        assert len(data["items"]) == 1
        assert data["items"][0]["product_id"] == product_id


@pytest.mark.asyncio
async def test_create_order_stock_failure(client, mock_db_session):
    user_id = str(uuid.uuid4())
    product_id = str(uuid.uuid4())
    order_data = {
        "user_id": user_id,
        "shipping_address": "123 Street",
        "items": [{"product_id": product_id, "quantity": 2, "price": 50.0}],
    }

    # Mock InternalServiceClient
    with (
        patch(
            "app.services.order_service.InternalServiceClient.reserve_stock",
            new_callable=AsyncMock,
        ) as mock_reserve,
        patch(
            "app.services.order_service.InternalServiceClient.release_stock",
            new_callable=AsyncMock,
        ) as mock_release,
    ):
        mock_reserve.return_value = False
        mock_release.return_value = True

        # Mock session behavior
        mock_db_session.refresh = AsyncMock()

        response = await client.post("/api/v1/orders/", json=order_data)

        assert response.status_code == 400
        assert "insufficient stock" in response.json()["detail"].lower()
