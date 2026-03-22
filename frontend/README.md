# Frontend – Nuxt 3

## Overview

This module contains the **web frontend** for TravelHub, built with **Nuxt 3** (Vue.js).

## What will be developed here

- **Nuxt 3** application with server-side rendering (SSR) support
- **Pages**
  - `/` — Home / landing page
  - `/trips` — Trip listing
  - `/trips/:id` — Trip detail
  - `/login` and `/register` — Authentication screens
  - `/profile` — User profile
- **Layouts** — Default layout with navigation header and footer
- **Components** — Reusable UI components (TripCard, NavBar, AuthForm, etc.)
- **State management** — Pinia stores for authentication and trip data
- **API integration** — Composables that communicate with the FastAPI microservices
- **Styling** — CSS / Tailwind CSS (TBD)
- **Dockerisation** — `Dockerfile` for containerised deployment on AWS ECS

## Technology stack

| Tool | Purpose |
|------|---------|
| Nuxt 3 | Framework (SSR + SPA) |
| Vue 3 | UI library |
| Pinia | State management |
| Nuxt fetch / useFetch | HTTP calls to backend services |
| Vitest | Unit testing |

## Planned folder structure

```
frontend/
├── assets/
├── components/
├── layouts/
│   └── default.vue
├── pages/
│   ├── index.vue
│   ├── trips/
│   │   ├── index.vue
│   │   └── [id].vue
│   ├── login.vue
│   └── register.vue
├── stores/
│   ├── auth.ts
│   └── trips.ts
├── composables/
│   └── useApi.ts
├── public/
├── nuxt.config.ts
└── package.json
```
