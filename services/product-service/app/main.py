from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI

from app.api.v1.endpoints import products
from app.core.config import settings
from app.db.base import Base
from app.db.init_db import init_db
from app.db.session import SessionLocal, engine


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # Startup: Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Seed data
    async with SessionLocal() as db:
        await init_db(db)

    yield
    # Shutdown
    await engine.dispose()


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url="/openapi.json",
    lifespan=lifespan,
)


app.include_router(products.router, prefix=settings.API_V1_STR, tags=["products"])


@app.get("/health")
def health_check() -> Any:
    return {"status": "ok"}
