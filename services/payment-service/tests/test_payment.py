import uuid
from unittest.mock import AsyncMock

import pytest

from shared.enums.status import PaymentStatus


@pytest.mark.asyncio
async def test_process_payment_success(client, mock_db_session):
    order_id = str(uuid.uuid4())
    payment_data = {"order_id": order_id, "amount": 100.0}

    # Mock session behavior
    mock_db_session.refresh = AsyncMock()

    response = await client.post("/api/v1/payments/process", json=payment_data)

    assert response.status_code == 200

    data = response.json()
    assert data["order_id"] == order_id
    assert data["status"] == PaymentStatus.SUCCESS
    assert data["transaction_id"] is not None


@pytest.mark.asyncio
async def test_process_payment_failure(client, mock_db_session):
    order_id = str(uuid.uuid4())
    payment_data = {
        "order_id": order_id,
        "amount": 20000.0,  # Large amount triggers failure in our mock logic
    }

    # Mock session behavior
    mock_db_session.refresh = AsyncMock()

    response = await client.post("/api/v1/payments/process", json=payment_data)

    assert response.status_code == 400

    assert "Payment failed" in response.json()["detail"]
