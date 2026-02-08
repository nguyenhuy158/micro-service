# AGENTS.md - Developer & Agent Guidelines

This document provides essential guidelines for AI agents and developers working on the Microservices Ecosystem project. Adhere strictly to these rules to maintain code quality, consistency, and architecture integrity.

## 🚨 CRITICAL RULE: Verification Loop

**AFTER every significant code change, you MUST run the following commands in order:**

1.  **Format Code:** `make format` (Fixes style automatically using Ruff)
2.  **Lint Code:** `make lint` (Checks for style/quality issues using Ruff)
3.  **Run Tests:** `make test` (Ensures no regressions)
4.  **Update Version:** Based on changes, run `make patch`, `make minor`, or `make major`.
5.  **Update OpenAPI:** If endpoints changed, ensure `docs-service` can generate the unified `openapi.json`.

Do **NOT** submit or finalize your task until all relevant commands pass successfully.

---

## 2. Versioning (Semantic Versioning)

The project strictly follows [Semantic Versioning 2.0.0](https://semver.org/).

- **Format:** `MAJOR.MINOR.PATCH` (x.y.z)
- **Rules:**
    - **MAJOR:** Increment for breaking changes (backwards incompatible).
    - **MINOR:** Increment for new backward-compatible features.
    - **PATCH:** Increment for bug fixes and minor improvements.
- **Global Version:** Defined in the root `pyproject.toml` under `[project].version`.
- **Shared Version:** Defined in `shared/version.py`. This is the source of truth for all services.
- **Service Versioning:** All microservices import their version from `shared.version.VERSION`.
- **API Documentation:** The OpenAPI version for each service and the unified documentation always reflects the `VERSION`.

**Updating Version:**
Agents MUST automatically suggest the next version number and apply it using the provided `make` commands:
- `make patch`: Bumps the patch version (e.g., 1.0.0 -> 1.0.1)
- `make minor`: Bumps the minor version (e.g., 1.0.0 -> 1.1.0)
- `make major`: Bumps the major version (e.g., 1.0.0 -> 2.0.0)

Alternatively, manually update `shared/version.py` and run `make format` to sync or use the script directly.

---

## 3. Build, Test, and Lint Commands

The project uses `make` for common tasks and `pip` (via `requirements.txt`) for dependency management.

### Setup & Installation
```bash
# Install development dependencies (including pytest, ruff, mypy)
make install-dev

# Start infrastructure (Postgres, RabbitMQ, Kong, etc.)
make up
```

### Type Checking & Linting
Run these commands to ensure code quality.
```bash
# Run static type checking (mypy) across all services
make type-check

# Run linter (ruff) to check for style issues
make lint

# Auto-format code (ruff) - ALWAYS RUN THIS
make format
```

### Testing
Tests are located in `services/<service-name>/tests/`. The `make test` command runs all tests.

**Running All Tests:**
```bash
make test
```

**Running Specific Tests (Directly with `pytest`):**
Use `pytest` directly for granular testing to save time during development.

```bash
# Run tests for a specific service
PYTHONPATH=services/product-service:. pytest services/product-service/tests

# Run a single test file
PYTHONPATH=services/order-service:. pytest services/order-service/tests/test_orders.py

# Run a specific test case by name (substring match)
pytest -k "test_create_order_success"

# Run with verbose output and no capture (shows print statements)
pytest -vv -s
```

---

## 2. Code Style & Architecture Guidelines

### Architecture: Clean Architecture & Saga Pattern
-   **Structure:** `services/<service-name>/app/`
    1.  **API (`api/`):** Handles HTTP requests/responses. Validation via Pydantic. Calls Service layer. **NO business logic here.**
    2.  **Service (`services/`):** Contains business logic (Domain logic). Calls DB/Repository layer.
    3.  **Schemas (`schemas/`):** Pydantic models for Data Transfer Objects (DTOs).
    4.  **Models (`models/`):** SQLAlchemy ORM models for Database entities.
    5.  **DB (`db/`):** Database connection and session management (AsyncSession).
    6.  **Core (`core/`):** Configuration (Pydantic Settings) and security.
-   **Dependency Injection:** Use FastAPI's `Depends` for injecting `db` and `settings`.
-   **Saga Pattern:** Use events defined in `shared/schemas/events.py` for inter-service communication via RabbitMQ.

### Python Coding Standards

#### Imports
-   **Order:**
    1.  Standard Library (`typing`, `uuid`, `os`)
    2.  Third-Party (`fastapi`, `sqlalchemy`, `pydantic`, `httpx`)
    3.  Local Application (Absolute imports: `from app.core import ...`)
    4.  Shared Library (`from shared.enums.status import ...`)
-   **Style:** Avoid `from module import *`. Be explicit.

#### Typing (Strict)
-   **Enforcement:** Code must pass `mypy` strict mode.
-   **Type Hints:** Explicit type hints for **ALL** function arguments and return values.
-   **Pydantic:** Use Pydantic models for all API inputs and outputs. **Do NOT** return ORM models directly; convert them to Pydantic schemas using `from_attributes = True` (Pydantic v2).

#### Naming Conventions
-   **Variables/Functions:** `snake_case`.
-   **Classes/Types:** `PascalCase`.
-   **Constants:** `UPPER_CASE`.
-   **Tests:** `test_` prefix for files and functions.

#### Error Handling
-   **API Layer:** Use `fastapi.HTTPException` with appropriate status codes (400, 401, 404, 500).
-   **Service Layer:** Raise custom domain exceptions or let DB exceptions propagate.
-   **Database:** Always use `AsyncSession` and `await` for `commit()`, `refresh()`, and `execute()`.

### API Documentation (OpenAPI)
-   **Update Rule:** Always verify that changes to endpoints are reflected in the auto-generated Swagger UI (`/docs`).
-   **Unified Schema:** The `docs-service` aggregates schemas from all services. Ensure new services are added to `SERVICES` in `services/docs-service/app/main.py`.
-   **Pydantic V2:** Use `ConfigDict` or `model_config` for Pydantic v2 configuration (e.g., `from_attributes = True`).

---

## 3. Shared Library (`shared/`)
-   Located at `/shared` (mirrored from `shared/` in root).
-   Contains `enums/` and `schemas/` used by multiple services.
-   **Do not duplicate** logic across services if it belongs in `shared`.
-   When adding new event types, update `shared/schemas/events.py`.

---

## 4. Inter-service Communication
-   **Synchronous:** Use `httpx.AsyncClient` for critical paths (e.g., Order -> Inventory reservation).
-   **Asynchronous:** Use RabbitMQ for non-blocking updates (e.g., Order Placed -> Email Notification).

---

## 5. Tool Configuration
-   **`pyproject.toml`:** Master configuration for `mypy` and `ruff`.
-   **`Makefile`:** Use for standardizing commands. Always set `PYTHONPATH` when running tests locally.

---
*Updated for Microservices Ecosystem - 2026*
