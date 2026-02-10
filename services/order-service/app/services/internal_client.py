from uuid import UUID

from app.infrastructure.clients.internal_service_client import (
    HttpxInventoryClient,
    HttpxPaymentClient,
    HttpxProductClient,
)


class InternalServiceClient:
    _inventory = HttpxInventoryClient()
    _payment = HttpxPaymentClient()
    _product = HttpxProductClient()

    @staticmethod
    async def reserve_stock(product_id: UUID, quantity: int) -> bool:
        return await InternalServiceClient._inventory.reserve_stock(
            product_id, quantity
        )

    @staticmethod
    async def release_stock(product_id: UUID, quantity: int) -> bool:
        return await InternalServiceClient._inventory.release_stock(
            product_id, quantity
        )

    @staticmethod
    async def process_payment(order_id: UUID, amount: float) -> bool:
        return await InternalServiceClient._payment.process_payment(order_id, amount)

    @staticmethod
    async def get_product(product_id: UUID) -> dict | None:
        return await InternalServiceClient._product.get_product(product_id)

    @staticmethod
    async def get_api_keys(order_id: UUID) -> list[dict]:
        return await InternalServiceClient._inventory.get_api_keys(order_id)

    @staticmethod
    async def generate_api_key(
        user_id: UUID,
        product_id: UUID,
        order_id: UUID,
        quota_limit: int = 1000,
        rate_limit: int = 60,
    ) -> bool:
        return await InternalServiceClient._inventory.generate_api_key(
            user_id, product_id, order_id, quota_limit, rate_limit
        )
