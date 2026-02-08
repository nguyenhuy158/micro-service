# Microservice E-commerce Platform Blueprint

## 1. Project Overview
**Name:** Microservice E-commerce Platform
**Description:** A scalable, event-driven e-commerce backend built with Python (FastAPI), Kong Gateway, and RabbitMQ.
**Architecture Style:** Microservices with Saga Pattern (Orchestration) and Clean Architecture.

## 2. Technology Stack
- **Language:** Python 3.11+
- **Web Framework:** FastAPI
- **API Gateway:** Kong (DB-less mode)
- **Message Broker:** RabbitMQ
- **Database:** PostgreSQL (Per-service isolation)
- **Caching:** Redis
- **Search Engine:** Meilisearch
- **Containerization:** Docker & Docker Compose
- **Observability:** Prometheus, Grafana, Jaeger

## 3. System Architecture

### 3.1. Core Services
| Service | Port | Database | Responsibilities |
|---------|------|----------|------------------|
| **User Service** | 8001 | `user_db` | Authentication (JWT), User Profile Management |
| **Product Service** | 8002 | `product_db` | Product Catalog, Categories, Meilisearch Sync |
| **Order Service** | 8003 | `order_db` | Order Placement, **Saga Orchestrator** |
| **Inventory Service** | 8004 | `inventory_db` | Stock Management, Reservations |
| **Payment Service** | 8005 | `payment_db` | Payment Processing (Mock/Stripe) |

### 3.2. Infrastructure Components
- **Kong Gateway (Port 8000):** Single entry point. Handles Routing, Rate Limiting, CORS, and Auth Validation.
- **RabbitMQ (Port 5672/15672):** Handles asynchronous events (e.g., `OrderCreated`, `PaymentSuccess`) for the Saga pattern.
- **Redis (Port 6379):** Caching for frequently accessed data (e.g., product details, user sessions).
- **Meilisearch (Port 7700):** Fast, typo-tolerant search for products.

### 3.3. Observability Stack
- **Prometheus (Port 9090):** Scrapes metrics from services (via `/metrics` endpoint).
- **Grafana (Port 3001):** Visualizes metrics (Dashboards).
- **Jaeger (Port 16686):** Distributed tracing to track requests across services.

## 4. Directory Structure
```
/micro-service
├── deployment/              # K8s or other deployment configs (future)
├── docker-compose.yml       # Defines all 14 containers
├── .env                     # Centralized configuration (secrets)
├── gateway/
│   └── kong/
│       └── kong.yml         # Declarative Gateway Configuration
├── monitoring/
│   ├── grafana/             # Dashboards
│   └── prometheus/          # Scrape configs
├── services/
│   ├── user-service/
│   ├── product-service/
│   ├── order-service/
│   ├── inventory-service/
│   └── payment-service/
│       ├── app/
│       │   ├── domain/      # Entities, Interfaces (Clean Arch)
│       │   ├── application/ # Use Cases, DTOs
│       │   ├── infrastructure/ # DB, Adapters
│       │   └── presentation/   # API Routes
│       ├── Dockerfile
│       ├── requirements.txt
│       └── main.py
└── shared/
    └── app/
        ├── enums/           # Shared constants (UserRole, OrderStatus)
        └── schemas/         # Shared Pydantic models (Events)
```

## 5. Key Workflows

### 5.1. Order Placement (Saga Pattern)
1. **Client** sends `POST /orders` to **Kong**.
2. **Kong** routes to **Order Service**.
3. **Order Service** creates "PENDING" order and publishes `OrderCreatedEvent` to **RabbitMQ**.
4. **Inventory Service** consumes event -> Reserves Stock -> Publishes `StockReservedEvent`.
5. **Payment Service** consumes event -> Processes Payment -> Publishes `PaymentProcessedEvent`.
6. **Order Service** consumes events -> Updates Order Status to "CONFIRMED".
   - *Failure Scenario:* If Stock/Payment fails, **Order Service** triggers specific compensation events (e.g., `ReleaseStock`) to roll back changes.

## 6. Development & Deployment

### Prerequisites
- Docker & Docker Compose
- Python 3.11+

### Running the System
```bash
# 1. Setup Environment
cp .env.example .env

# 2. Start all services
docker-compose up -d --build

# 3. Access Points
# API Gateway: http://localhost:8000
# Kong Admin: http://localhost:8001
# RabbitMQ UI: http://localhost:15672 (guest/guest)
# Grafana: http://localhost:3000
```
