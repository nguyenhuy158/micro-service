from fastapi import FastAPI
from starlette_prometheus import metrics, PrometheusMiddleware

app = FastAPI(title="Order Service", version="1.0.0")

app.add_middleware(PrometheusMiddleware)
app.add_route("/metrics", metrics)


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "order-service"}


@app.get("/")
def root():
    return {"message": "Welcome to Order Service"}
