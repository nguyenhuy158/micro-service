.PHONY: type-check lint format install-dev up down restart logs ps

install-dev:
	pip install -r dev-requirements.txt

test:
	pytest services/product-service/tests services/user-service/tests services/order-service/tests services/inventory-service/tests services/payment-service/tests

type-check:
	mypy services/user-service/app services/product-service/app services/order-service/app services/inventory-service/app services/payment-service/app services/docs-service/app shared/app

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
