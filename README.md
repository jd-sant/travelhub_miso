# TravelHub MISO - Backend API

Este repositorio contiene la API de TravelHub construida con Python y FastAPI.

## Resumen

El proyecto expone endpoints REST para la gestion de usuarios y esta organizado por capas:

- API: rutas y endpoints HTTP
- Core: configuracion y seguridad
- DB: conexion y sesion de base de datos
- Models: entidades persistidas
- Schemas: contratos de entrada y salida
- Repositories: acceso a datos
- Services: logica de negocio

## Stack

- Python 3.11+
- FastAPI
- SQLModel
- Pydantic v2
- Pytest

## Estructura actual

```text
travelhub_miso/
├── app/
│   ├── api/
│   │   └── v1/
│   │       └── endpoints/
│   │           └── users.py
│   ├── core/
│   ├── db/
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   └── services/
├── tests/
├── main.py
├── requirements.txt
└── README.md
```

## Endpoints disponibles

- GET /: verificacion basica del servicio
- POST /api/v1/users: crea un usuario
- GET /api/v1/users: lista usuarios

## Ejecucion local

1. Crear y activar entorno virtual.
2. Instalar dependencias:

```bash
pip install -r requirements.txt
```

3. Levantar la API:

```bash
uvicorn app.main:app --reload
```

La API queda disponible en http://127.0.0.1:8000.

## Pruebas

```bash
pytest -q
```

Las pruebas de usuarios estan en tests/test_users_api.py.


