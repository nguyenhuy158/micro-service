from pydantic import ConfigDict
from pydantic_settings import BaseSettings

from shared.version import VERSION


class Settings(BaseSettings):
    model_config = ConfigDict(case_sensitive=True)
    PROJECT_NAME: str = "Product Service"
    API_V1_STR: str = "/api/v1"
    VERSION: str = VERSION

    DATABASE_URL: str

    RABBITMQ_URL: str

    MEILISEARCH_URL: str
    MEILISEARCH_KEY: str


settings = Settings()
