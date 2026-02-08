from uuid import UUID

import httpx
from app.core.config import settings


class InternalServiceClient:
    @staticmethod
    async def reserve_stock(product_id: UUID, quantity: int) -> bool:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{settings.INVENTORY_SERVICE_URL}/api/v1/inventory/reserve",
                    json={"product_id": str(product_id), "quantity": quantity},
                    timeout=5.0,
                )
                return response.status_code == 200
            except Exception:
                return False

    @staticmethod
    async def release_stock(product_id: UUID, quantity: int) -> bool:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{settings.INVENTORY_SERVICE_URL}/api/v1/inventory/release",
                    json={"product_id": str(product_id), "quantity": quantity},
                    timeout=5.0,
                )
                return response.status_code == 200
            except Exception:
                return False

    @staticmethod
    async def process_payment(order_id: UUID, amount: float) -> bool:
        # Mock payment for now or call payment-service
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{settings.PAYMENT_SERVICE_URL}/api/v1/payments/process",
                    json={"order_id": str(order_id), "amount": amount},
                    timeout=5.0,
                )
                return response.status_code == 200
            except Exception:
                # If payment service is not yet ready, we might want to return True
                # for testing but for core logic we should probably return False.
                # However, during development of Order logic, we might need a way
                # to bypass.
                return False
