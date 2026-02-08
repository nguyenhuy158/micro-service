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

    @staticmethod
    async def get_product(product_id: UUID) -> dict | None:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{settings.PRODUCT_SERVICE_URL}/api/v1/product/products/{product_id}",
                    timeout=5.0,
                )
                if response.status_code == 200:
                    return response.json()
                return None
            except Exception:
                return None

    @staticmethod
    async def get_api_keys(order_id: UUID) -> list[dict]:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{settings.INVENTORY_SERVICE_URL}/api/v1/inventory/keys/order/{order_id}",
                    timeout=5.0,
                )
                if response.status_code == 200:
                    return response.json()
                return []
            except Exception:
                return []

    @staticmethod
    async def generate_api_key(
        user_id: UUID, product_id: UUID, order_id: UUID, quota_limit: int = 1000
    ) -> bool:
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{settings.INVENTORY_SERVICE_URL}/api/v1/inventory/generate-key",
                    json={
                        "user_id": str(user_id),
                        "product_id": str(product_id),
                        "order_id": str(order_id),
                        "quota_limit": quota_limit,
                    },
                    timeout=5.0,
                )
                return response.status_code == 201
            except Exception:
                return False
