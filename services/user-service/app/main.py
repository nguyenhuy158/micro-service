from fastapi import FastAPI
from starlette_prometheus import metrics, PrometheusMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api.api import api_router
from app.db.session import engine
from app.db.base import Base

# Import models to ensure they are registered with Base.metadata
from app.models import user


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create tables (In production, use Alembic!)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Shutdown
    await engine.dispose()


app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
)

app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", metrics)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "user-service"}


@app.get("/")
def root():
    return {"message": "Welcome to User Service"}
