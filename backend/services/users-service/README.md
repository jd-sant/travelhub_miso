# Users Service

## Overview

The **Users Service** manages user profiles in TravelHub.

## What will be developed here

- **List users** — `GET /users`
- **Get user profile** — `GET /users/{id}`
- **Create user** — `POST /users`
- **Update user** — `PUT /users/{id}`
- **Delete user** — `DELETE /users/{id}`

## Technology stack

| Tool | Purpose |
|------|---------|
| FastAPI | Web framework |
| Pydantic v2 | Schema validation |
| SQLAlchemy | ORM |
| Alembic | Database migrations |
| pytest | Testing |

## Planned folder structure

```
users-service/
├── main.py            # FastAPI app & route definitions
├── models.py          # SQLAlchemy database models
├── schemas.py         # Pydantic request/response schemas
├── database.py        # Database session setup
├── requirements.txt   # Python dependencies
├── Dockerfile
└── test_main.py       # pytest test suite
```

## Environment variables

| Variable | Description |
|----------|-------------|
| `DATABASE_URL` | PostgreSQL connection string |
| `CORS_ORIGINS` | JSON list of allowed origins |
