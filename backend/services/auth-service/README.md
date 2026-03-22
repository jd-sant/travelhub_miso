# Auth Service

## Overview

The **Auth Service** is responsible for all authentication and authorisation logic in TravelHub.

## What will be developed here

- **User registration** — `POST /auth/register`
- **User login** — `POST /auth/token` (OAuth2 password flow, returns JWT)
- **Token verification** — middleware / dependency used by other services to validate Bearer tokens
- **Password hashing** — using `passlib[bcrypt]`
- **JWT management** — using `python-jose`

## Technology stack

| Tool | Purpose |
|------|---------|
| FastAPI | Web framework |
| Pydantic v2 | Schema validation |
| python-jose | JWT encoding / decoding |
| passlib[bcrypt] | Password hashing |
| SQLAlchemy | ORM |
| Alembic | Database migrations |
| pytest | Testing |

## Planned folder structure

```
auth-service/
├── main.py            # FastAPI app & route definitions
├── models.py          # SQLAlchemy database models
├── schemas.py         # Pydantic request/response schemas
├── dependencies.py    # Shared FastAPI dependencies (e.g. get_current_user)
├── database.py        # Database session setup
├── requirements.txt   # Python dependencies
├── Dockerfile
└── test_main.py       # pytest test suite
```

## Environment variables

| Variable | Description |
|----------|-------------|
| `SECRET_KEY` | Secret used to sign JWTs |
| `ALGORITHM` | JWT algorithm (default: `HS256`) |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token TTL in minutes |
| `DATABASE_URL` | PostgreSQL connection string |
| `CORS_ORIGINS` | JSON list of allowed origins |
