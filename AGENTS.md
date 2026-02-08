# AGENTS.md - Developer & Agent Guidelines

This document provides essential guidelines for AI agents and developers working on the Microservices Ecosystem project. Adhere strictly to these rules to maintain code quality, consistency, and architecture integrity.

## 1. Build, Test, and Lint Commands

The project uses `make` for common tasks and `uv` (implied via `requirements.txt`) for dependency management.

### Setup & Installation
```bash
# Install development dependencies
make install-dev
```

### Type Checking & Linting
Run these commands before submitting any changes.
```bash
# Run static type checking (mypy) across all services
make type-check

# Run linter (ruff) to check for style issues
make lint

# Auto-format code (ruff)
make format
```

### Testing
Tests are located in `tests/` directories within each service or in a global `tests/` folder (verify per service).
Use `pytest` for running tests.

```bash
# Run all tests
pytest

# Run tests for a specific service (example)
pytest services/user-service/tests

# Run a single test file
pytest services/user-service/tests/test_api.py

# Run a specific test case by name
pytest -k "test_create_user"

# Run with verbose output to see test execution details
pytest -vv
```

## 2. Code Style & Architecture Guidelines

### Architecture: Clean Architecture & Saga Pattern
-   **Layers:**
    1.  **API (`app/api`):** Handles HTTP requests/responses. Validation via Pydantic. Calls Service layer. **NO business logic here.**
    2.  **Service (`app/services`):** Contains business logic. Calls DB/Repository layer.
    3.  **Schemas (`app/schemas`):** Pydantic models for Data Transfer Objects (DTOs).
    4.  **Models (`app/models`):** SQLAlchemy ORM models for Database entities.
    5.  **DB (`app/db`):** Database connection and session management.
-   **Dependency Injection:** Use FastAPI's `Depends` for injecting dependencies (e.g., DB sessions, services).
-   **Saga Pattern:** Use events defined in `shared/app/schemas/events.py` for inter-service communication via RabbitMQ.

### Python Coding Standards

#### Imports
-   **Order:**
    1.  Standard Library (e.g., `typing`, `datetime`, `os`)
    2.  Third-Party (e.g., `fastapi`, `sqlalchemy`, `pydantic`)
    3.  Local Application (Absolute imports: `from app.core import ...`)
-   **Style:** Avoid `from module import *`. Be explicit.
-   **Grouping:** Group imports logically with blank lines between groups.

#### Typing (Strict)
-   **Enforcement:** Code must pass `mypy` strict mode.
-   **Type Hints:** explicit type hints for ALL function arguments and return values.
    ```python
    # Good
    async def get_user(db: AsyncSession, user_id: int) -> Optional[User]: ...
    
    # Bad
    async def get_user(db, user_id): ...
    ```
-   **Pydantic:** Use Pydantic models for all API inputs and outputs. Do NOT return ORM models directly from API endpoints.

#### Formatting
-   **Tool:** `ruff` (compatible with Black).
-   **Line Length:** 88 characters.
-   **Quotes:** Double quotes `"` for strings.
-   **Trailing Commas:** Use trailing commas in multi-line lists/dicts/calls.

#### Naming Conventions
-   **Variables/Functions:** `snake_case` (e.g., `get_user_by_email`).
-   **Classes/Types:** `PascalCase` (e.g., `UserCreate`, `ProductService`).
-   **Constants:** `UPPER_CASE` (e.g., `ACCESS_TOKEN_EXPIRE_MINUTES`).
-   **Private Members:** `_prefixed` (e.g., `_verify_password`).

#### Error Handling
-   **API Layer:** Use `fastapi.HTTPException` with appropriate status codes (4xx, 5xx).
-   **Service Layer:** Raise custom exceptions (if needed) or let DB exceptions propagate to be caught by API layer or global exception handlers.
-   **Validation:** Rely on Pydantic for request validation.

#### Asynchronous Programming
-   **Async/Await:** Use `async def` for all API endpoints and DB operations.
-   **DB:** Use `await` for all SQLAlchemy async calls (`await db.execute(...)`, `await db.commit()`).

### Documentation
-   **Docstrings:** Required for complex functions, classes, and modules. Use Google or NumPy style.
-   **API Docs:** FastAPI auto-generates Swagger UI. Ensure Pydantic models have `description` fields where helpful.

### Shared Library (`shared/`)
-   Reusable code (schemas, enums, utils) goes here.
-   **Do not duplicate** logic across services if it belongs in `shared`.
-   Modifying `shared` requires rebuilding/checking all dependent services.

## 3. Tool Configuration
-   **`pyproject.toml`:** Master configuration for `mypy` and `ruff`. Do not modify unless adding global tool settings.
-   **`Makefile`:** Use for standardizing commands.

---
*Generated for Cursor/Windsurf/Copilot Agents - Version 1.0*
