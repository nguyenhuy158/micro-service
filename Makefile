.PHONY: type-check lint format install-dev up down restart logs ps

install-dev:
	pip install -r dev-requirements.txt

test:
	PYTHONPATH=services/product-service:. pytest services/product-service/tests
	PYTHONPATH=services/user-service:. pytest services/user-service/tests
	PYTHONPATH=services/order-service:. pytest services/order-service/tests
	PYTHONPATH=services/inventory-service:. pytest services/inventory-service/tests
	PYTHONPATH=services/payment-service:. pytest services/payment-service/tests

type-check:
	mypy services/user-service/app services/product-service/app services/order-service/app services/inventory-service/app services/payment-service/app services/docs-service/app shared

lint:
	ruff check .

format:
	ruff format .

up:
	docker-compose up -d --build

down:
	docker-compose down

restart: down up

logs:
	docker-compose logs -f

ps:
	docker-compose ps
