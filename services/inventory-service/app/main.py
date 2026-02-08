from fastapi import FastAPI
from starlette_prometheus import metrics, PrometheusMiddleware

app = FastAPI(
    title="Inventory Service",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", metrics)


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "inventory-service"}


@app.get("/")
def root():
    return {"message": "Welcome to Inventory Service"}
