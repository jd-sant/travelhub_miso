# travelhub_miso

TravelHub is the travel planning platform built for the MISO course at Universidad de los Andes.

## Architecture

TravelHub uses a **microservice architecture** split across four technology layers:

| Layer | Technology | Location |
|-------|-----------|----------|
| Frontend | Nuxt 3 (Vue.js) | `frontend/` |
| Backend | Python + FastAPI | `backend/services/` |
| Mobile | Android (Kotlin + Jetpack Compose) | `mobile/` |
| Infra | AWS ECS / Fargate | `infrastructure/aws/` |

```
travelhub_miso/
├── frontend/                   # Nuxt 3 web application
│   ├── pages/
│   ├── components/
│   ├── layouts/
│   ├── nuxt.config.ts
│   └── Dockerfile
├── backend/
│   └── services/
│       ├── auth-service/       # FastAPI – authentication & JWT
│       ├── trips-service/      # FastAPI – trip management
│       └── users-service/      # FastAPI – user profiles
├── mobile/                     # Android Studio project
│   └── app/src/main/
│       ├── java/com/travelhub/app/
│       └── res/
├── infrastructure/
│   └── aws/
│       └── ecs-task-definitions/
└── docker-compose.yml          # Local development
```

## Quick Start (Local)

### Prerequisites

- Docker & Docker Compose
- Node.js 22+
- Python 3.12+
- Android Studio (for mobile)

### Run with Docker Compose

```bash
docker-compose up --build
```

Services will be available at:

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Auth Service | http://localhost:8001 |
| Trips Service | http://localhost:8002 |
| Users Service | http://localhost:8003 |

### Run services individually

**Frontend**

```bash
cd frontend
npm install
npm run dev
```

**Backend services** (example for trips-service)

```bash
cd backend/services/trips-service
pip install -r requirements.txt
uvicorn main:app --reload --port 8002
```

## Testing

**Backend (pytest)**

```bash
cd backend/services/auth-service && pip install -r requirements.txt && pytest
cd backend/services/trips-service && pip install -r requirements.txt && pytest
cd backend/services/users-service && pip install -r requirements.txt && pytest
```

**Frontend (vitest)**

```bash
cd frontend && npm install && npm test
```

**Mobile**

Run unit tests from Android Studio or:

```bash
cd mobile && ./gradlew test
```

## Deployment (AWS)

See [`infrastructure/aws/README.md`](infrastructure/aws/README.md) for instructions on deploying to AWS ECS Fargate.
