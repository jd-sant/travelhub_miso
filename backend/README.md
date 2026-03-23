# Backend (Python / FastAPI)

## Overview

This module contains the backend API for TravelHub built with **Python** and **FastAPI**.

## Active API modules

| Module | Responsibility |
|--------|----------------|
| [app/api/v1/endpoints/users.py](app/api/v1/endpoints/users.py) | User profile endpoints |

## Common conventions

- **FastAPI** as the web framework
- **Pydantic v2** for request / response schema validation
- **SQLAlchemy + Alembic** for database access and migrations (PostgreSQL on AWS RDS)
- **Docker** containerisation
- **pytest** for unit and integration tests
- **CORS** configured to allow requests from the Nuxt frontend

## Current folder structure

```
backend/
├── app/
│   ├── api/v1/
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   └── services/
├── tests/
├── main.py
├── requirements.txt
└── services/
    ├── auth-service/
    └── trips-service/
```
