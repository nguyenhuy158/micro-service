# AGENTS.md - Developer & Agent Guidelines

This document provides essential guidelines for AI agents and developers working on the Microservices Ecosystem project. Adhere strictly to these rules to maintain code quality, consistency, and architecture integrity.

## 🚨 CRITICAL RULE: Verification Loop

**AFTER every significant code change, you MUST run the following commands in order:**

1.  **Format Code:** `make format` (Fixes style automatically)
2.  **Lint Code:** `make lint` (Checks for style/quality issues)
3.  **Run Tests:** `make test` (Ensures no regressions)

Do **NOT** submit or finalize your task until all three commands pass successfully.

---

## 1. Build, Test, and Lint Commands

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
pytest services/product-service/tests

# Run a single test file
pytest services/product-service/tests/test_products.py

# Run a specific test case by name (substring match)
pytest -k "test_create_product"

# Run with verbose output to see test execution details
pytest -vv

# Run failed tests from the last run
pytest --lf
```

---

## 2. Code Style & Architecture Guidelines

### Architecture: Clean Architecture & Saga Pattern
-   **Structure:** `services/<service-name>/app/`
    1.  **API (`api/`):** Handles HTTP requests/responses. Validation via Pydantic. Calls Service layer. **NO business logic here.**
    2.  **Service (`services/`):** Contains business logic. Calls DB/Repository layer.
    3.  **Schemas (`schemas/`):** Pydantic models for Data Transfer Objects (DTOs).
    4.  **Models (`models/`):** SQLAlchemy ORM models for Database entities.
    5.  **DB (`db/`):** Database connection and session management.
    6.  **Core (`core/`):** Configuration and security settings.
-   **Dependency Injection:** Use FastAPI's `Depends` for injecting dependencies (e.g., DB sessions, settings).
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
-   **Type Hints:** Explicit type hints for **ALL** function arguments and return values.
    ```python
    # Good
    async def get_user(db: AsyncSession, user_id: int) -> Optional[User]: ...
    
    # Bad
    async def get_user(db, user_id): ...
    ```
-   **Pydantic:** Use Pydantic models for all API inputs and outputs. **Do NOT** return ORM models directly from API endpoints; convert them to Pydantic schemas first.

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
-   **Tests:** `test_` prefix for files and functions (e.g., `test_products.py`, `test_create_product`).

#### Error Handling
-   **API Layer:** Use `fastapi.HTTPException` with appropriate status codes (400, 401, 403, 404, 500).
-   **Service Layer:** Raise custom exceptions (if needed) or let DB exceptions propagate to be caught by API layer or global exception handlers.
-   **Validation:** Rely on Pydantic for request validation.

#### Asynchronous Programming
-   **Async/Await:** Use `async def` for all API endpoints and DB operations.
-   **DB:** Use `await` for all SQLAlchemy async calls (`await db.execute(...)`, `await db.commit()`, `await db.refresh()`).

### Documentation
-   **Docstrings:** Required for complex functions, classes, and modules. Use Google or NumPy style.
-   **API Docs:** FastAPI auto-generates Swagger UI. Ensure Pydantic models have `description` fields where helpful.

### Shared Library (`shared/`)
-   Reusable code (schemas, enums, utils) goes here.
-   **Do not duplicate** logic across services if it belongs in `shared`.
-   Modifying `shared` requires rebuilding/checking all dependent services.

---

## 3. Tool Configuration
-   **`pyproject.toml`:** Master configuration for `mypy` and `ruff`. Do not modify unless adding global tool settings.
-   **`Makefile`:** Use for standardizing commands.

---
*Generated for Cursor/Windsurf/Copilot Agents*
