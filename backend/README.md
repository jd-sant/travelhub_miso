# Backend – Microservices (Python / FastAPI)

## Overview

This module contains all **backend microservices** for TravelHub, each built with **Python** and **FastAPI**.

## Services

| Service | Port | Responsibility |
|---------|------|----------------|
| [auth-service](services/auth-service/) | 8001 | Authentication & JWT token management |
| [trips-service](services/trips-service/) | 8002 | Trip creation, listing, and management |
| [users-service](services/users-service/) | 8003 | User profiles |

## Common conventions across all services

- **FastAPI** as the web framework
- **Pydantic v2** for request / response schema validation
- **SQLAlchemy + Alembic** for database access and migrations (PostgreSQL on AWS RDS)
- **Docker** containerisation — each service ships its own `Dockerfile`
- **pytest** for unit and integration tests
- **CORS** configured to allow requests from the Nuxt frontend

## Planned folder structure

```
backend/
└── services/
    ├── auth-service/
    ├── trips-service/
    └── users-service/
```
