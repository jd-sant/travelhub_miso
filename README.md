# travelhub_miso

TravelHub is the travel planning platform built for the MISO course at Universidad de los Andes.

## Architecture

TravelHub uses a **microservice architecture** split across four technology layers:

| Layer | Technology | Location |
|-------|-----------|----------|
| Frontend | Nuxt 3 (Vue.js) | [`frontend/`](frontend/) |
| Backend | Python + FastAPI | [`backend/services/`](backend/) |
| Mobile | Android (Kotlin + Jetpack Compose) | [`mobile/`](mobile/) |
| Infrastructure | AWS ECS / Fargate | [`infrastructure/aws/`](infrastructure/aws/) |

## Repository structure

```
travelhub_miso/
├── frontend/                        # Nuxt 3 web application
├── backend/
│   └── services/
│       ├── auth-service/            # FastAPI – authentication & JWT
│       ├── trips-service/           # FastAPI – trip management
│       └── users-service/           # FastAPI – user profiles
├── mobile/                          # Android Studio project (Kotlin + Compose)
└── infrastructure/
    └── aws/                         # AWS ECS task definitions & config
```

Each directory contains a `README.md` that describes what will be developed there.

