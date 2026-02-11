from pydantic import ConfigDict
from pydantic_settings import BaseSettings

from shared.version import VERSION


class Settings(BaseSettings):
    model_config = ConfigDict(case_sensitive=True)
    PROJECT_NAME: str = "Inventory Service"
    API_V1_STR: str = "/api/v1"
    VERSION: str = VERSION

    SECRET_KEY: str = "your-secret-key-change-me"
    ALGORITHM: str = "HS256"

    USER_SERVICE_URL: str = "http://user-service:8000"

    DATABASE_URL: str
    RABBITMQ_URL: str


settings = Settings()
