from typing import Any

import httpx
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse

app = FastAPI(title="Unified E-commerce API", version="1.0.0")

# Service Map: Service Name -> Internal URL
SERVICES = {
    "user": "http://user-service:8000",
    "product": "http://product-service:8000",
    "order": "http://order-service:8000",
    "inventory": "http://inventory-service:8000",
    "payment": "http://payment-service:8000",
}


@app.get("/health")
async def health() -> Any:
    return {"status": "ok", "service": "docs-service"}


@app.get("/openapi.json")
async def get_unified_openapi() -> Any:
    # Base schema
    unified_schema = get_openapi(
        title="Unified E-commerce API",
        version="1.0.0",
        routes=app.routes,
    )

    # Initialize schema structure
    unified_schema.setdefault("paths", {})
    if "components" not in unified_schema:
        unified_schema["components"] = {}

    # Use httpx to fetch schemas
    async with httpx.AsyncClient() as client:
        for service_name, url in SERVICES.items():
            try:
                response = await client.get(f"{url}/openapi.json", timeout=5.0)
                if response.status_code == 200:
                    service_schema = response.json()

                    # Merge paths
                    # We prefix with /api/v1/{service_name} to match Kong routing
                    paths = service_schema.get("paths", {})
                    for path, path_item in paths.items():
                        # Construct public path
                        # Example: /api/v1/user/auth if internal is /api/v1/auth
                        internal_path = path
                        if internal_path.startswith("/api/v1"):
                            internal_path = internal_path.replace("/api/v1", "", 1)

                        if internal_path == "/" or internal_path == "":
                            public_path = f"/api/v1/{service_name}"
                        else:
                            public_path = f"/api/v1/{service_name}{internal_path}"

                        unified_schema["paths"][public_path] = path_item

                    # Merge components
                    components = service_schema.get("components", {})
                    for comp_type, comp_dict in components.items():
                        unified_schema["components"].setdefault(comp_type, {})
                        for name, component in comp_dict.items():
                            unified_schema["components"][comp_type][name] = component

            except Exception as e:
                # Log error but continue
                print(f"Failed to load schema for {service_name}: {e}")
                pass

    return JSONResponse(unified_schema)
