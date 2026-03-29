# Accommodations Service

Microservicio para gestión de detalles de hospedajes en TravelHub.

## Descripción

Este servicio proporciona funcionalidad para obtener los detalles de un hospedaje específico, incluyendo información como nombre, descripción, ubicación, precio, rating y disponibilidad.

## Stack

- Python 3.11+
- FastAPI
- SQLModel / SQLAlchemy
- Pydantic v2
- PostgreSQL 15
- Docker

## Estructura

```
src/
├── adapters/
│   ├── models/
│   │   └── accommodation.py
│   └── repositories/
│       └── accommodation_repository.py
├── core/
│   └── config.py
├── db/
│   └── session.py
├── domain/
│   ├── ports/
│   │   └── accommodation_repository.py
│   ├── schemas/
│   │   └── accommodation.py
│   └── use_cases/
│       ├── base.py
│       └── get_accommodation_detail.py
├── entrypoints/
│   └── api/
│       ├── main.py
│       └── routers/
│           └── accommodations.py
├── assembly.py
└── errors.py
```

## API Endpoints

### GET /api/v1/accommodations/{id}

Obtiene el detalle de un hospedaje específico.

**Parámetros:**
- `id` (UUID): ID del hospedaje

**Respuesta:**
```json
{
  "id": "uuid",
  "name": "Hotel XYZ",
  "description": "Descripción del hotel",
  "location": "Ciudad, País",
  "price_per_night": 150.00,
  "rating": 4.5,
  "available_rooms": 10,
  "status": 1
}
```

## Ejecución local

```bash
# Con Docker
docker build -t accommodations .
docker run -p 8002:8002 accommodations

# O con uvicorn
PYTHONPATH=src uvicorn entrypoints.api.main:app --reload --port 8002
```

## Tests

```bash
PYTHONPATH=src pytest tests/ -v
```

## Health Check

```bash
GET /health
```
