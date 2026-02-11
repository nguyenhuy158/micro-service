from pydantic import ConfigDict
from pydantic_settings import BaseSettings

from shared.version import VERSION


class Settings(BaseSettings):
    model_config = ConfigDict(case_sensitive=True)
    PROJECT_NAME: str = "Order Service"
    API_V1_STR: str = "/api/v1"
    VERSION: str = VERSION

    DATABASE_URL: str

    RABBITMQ_URL: str

    INVENTORY_SERVICE_URL: str = "http://inventory-service:8000"
    PAYMENT_SERVICE_URL: str = "http://payment-service:8000"
    PRODUCT_SERVICE_URL: str = "http://product-service:8000"


settings = Settings()
