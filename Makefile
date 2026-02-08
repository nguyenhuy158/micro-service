.PHONY: type-check lint format install-dev up down restart logs ps major minor patch

install-dev:
	pip install -r dev-requirements.txt

major:
	python3 scripts/bump_version.py major

minor:
	python3 scripts/bump_version.py minor

patch:
	python3 scripts/bump_version.py patch

test:
	PYTHONPATH=services/product-service:. pytest services/product-service/tests
	PYTHONPATH=services/user-service:. pytest services/user-service/tests
	PYTHONPATH=services/order-service:. pytest services/order-service/tests
	PYTHONPATH=services/inventory-service:. pytest services/inventory-service/tests
	PYTHONPATH=services/payment-service:. pytest services/payment-service/tests

type-check:
	PYTHONPATH=services/user-service:shared mypy services/user-service/app
	PYTHONPATH=services/product-service:shared mypy services/product-service/app
	PYTHONPATH=services/order-service:shared mypy services/order-service/app
	PYTHONPATH=services/inventory-service:shared mypy services/inventory-service/app
	PYTHONPATH=services/payment-service:shared mypy services/payment-service/app
	PYTHONPATH=services/docs-service:shared mypy services/docs-service/app
	mypy shared

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
