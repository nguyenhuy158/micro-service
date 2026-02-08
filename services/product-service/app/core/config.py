from pydantic_settings import BaseSettings

from shared.version import VERSION


class Settings(BaseSettings):
    PROJECT_NAME: str = "Product Service"
    API_V1_STR: str = "/api/v1"
    VERSION: str = VERSION

    # DATABASE
    DATABASE_URL: str

    # RABBITMQ
    RABBITMQ_URL: str

    # MEILISEARCH
    MEILISEARCH_URL: str
    MEILISEARCH_KEY: str

    class Config:
        case_sensitive = True


settings = Settings()
