# Trips Service

## Overview

The **Trips Service** manages the full lifecycle of travel trips in TravelHub.

## What will be developed here

- **List trips** — `GET /trips`
- **Get trip detail** — `GET /trips/{id}`
- **Create trip** — `POST /trips`
- **Update trip** — `PUT /trips/{id}`
- **Delete trip** — `DELETE /trips/{id}`
- **Search / filter trips** — by destination, date range, price, etc.

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
trips-service/
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
