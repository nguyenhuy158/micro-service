.PHONY: type-check lint format install-dev

install-dev:
	pip install -r dev-requirements.txt

type-check:
	mypy services/user-service/app services/product-service/app services/order-service/app services/inventory-service/app services/payment-service/app services/docs-service/app shared/app

lint:
	ruff check .

format:
	ruff format .
