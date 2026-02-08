# Microservice Ecosystem

![Version](https://img.shields.io/badge/version-1.1.0-blue.svg)

A modular microservice architecture built with FastAPI, Kong Gateway, and RabbitMQ.

## 🏗️ System Architecture

```mermaid
graph TD
    Client[Client] -->|HTTP:8000| Kong[Kong API Gateway]

    subgraph "Microservices (FastAPI)"
        Kong --> US[User Service]
        Kong --> PS[Product Service]
        Kong --> OS[Order Service]
        Kong --> IS[Inventory Service]
        Kong --> PY[Payment Service]
    end

    subgraph "Event Bus & Storage"
        RabbitMQ[RabbitMQ]
        Redis[Redis]
        Meilisearch[Meilisearch]
    end

    subgraph "Databases"
        US --- USDB[(User DB)]
        PS --- PSDB[(Product DB)]
        OS --- OSDB[(Order DB)]
        IS --- ISDB[(Inventory DB)]
        PY --- PYDB[(Payment DB)]
    end

    subgraph "Observability"
        Prometheus[Prometheus]
        Grafana[Grafana]
        Jaeger[Jaeger]
    end

    OS -->|Internal API| IS
    OS -->|Internal API| PY
    OS -->|Internal API| PS
    OS --- Redis
    PS --- Meilisearch

    US & PS & OS & IS & PY --- RabbitMQ
    US & PS & OS & IS & PY --- Prometheus
    US & PS & OS & IS & PY --- Jaeger
```

## 🚀 Order Workflow

```mermaid
sequenceDiagram
    autonumber
    participant C as Client
    participant K as Kong Gateway
    participant O as Order Service
    participant I as Inventory Service
    participant P as Payment Service
    participant R as RabbitMQ

    C->>K: POST /orders
    K->>O: Forward Request
    Note over O,I: Synchronous Validation
    O->>I: Reserve Stock
    I-->>O: OK
    O->>P: Process Payment
    P-->>O: Success
    O-->>K: 201 Created
    K-->>C: Response
    Note over O,R: Asynchronous Events
    O->>R: Publish 'Order.Placed'
    R-->>PS: Notify Product (Update Stats)
    R-->>US: Notify User (Email)
```

## 📂 Project Structure

```mermaid
mindmap
  root((Project))
    gateway
      Kong Config
    services
      User Service
      Product Service
      Order Service
      Inventory Service
      Payment Service
    shared
      Enums
      Schemas
    monitoring
      Prometheus
      Grafana
```

## 🛠️ Tech Stack

| Category | Technology |
| :--- | :--- |
| **Framework** | FastAPI (Python 3.11+) |
| **Gateway** | Kong (DB-less) |
| **Message Broker** | RabbitMQ |
| **Caching** | Redis |
| **Search Engine** | Meilisearch |
| **Database** | PostgreSQL (Per-service) |
| **Tracing** | Jaeger (OpenTelemetry) |
| **Monitoring** | Prometheus & Grafana |

## 🏁 Quick Start

```bash
# 1. Setup environment
cp .env.example .env

# 2. Spin up the cluster
docker-compose up -d --build

# 3. Access Services
# - Gateway: http://localhost:8000
# - Grafana: http://localhost:3001
# - Jaeger: http://localhost:16686
# - Prometheus: http://localhost:9090
```

## 💻 Development

### Setup

Install development dependencies:

```bash
make install-dev
```

### Type Checking

Run static type checking with `mypy`:

```bash
make type-check
```

### Linting

Run linting with `ruff`:

```bash
make lint
```

### Formatting

Format code with `ruff`:

```bash
make format
```
