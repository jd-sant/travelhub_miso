# Mobile – Android App

## Overview

This module contains the **Android mobile application** for TravelHub, built with **Android Studio**, **Kotlin**, and **Jetpack Compose**.

## What will be developed here

- **Screens**
  - Home / Welcome screen
  - Trip listing screen
  - Trip detail screen
  - Login / Registration screen
  - User profile screen
- **Navigation** — Jetpack Navigation Compose with a bottom navigation bar
- **UI** — Material 3 design system with light / dark theme support
- **Networking** — Retrofit + OkHttp for REST API calls to the FastAPI backend
- **State management** — ViewModel + StateFlow
- **Dependency injection** — Hilt
- **Testing** — JUnit 4 unit tests and Espresso UI tests

## Technology stack

| Tool | Purpose |
|------|---------|
| Kotlin | Primary language |
| Jetpack Compose | Declarative UI toolkit |
| Material 3 | Design system |
| Retrofit | HTTP client |
| OkHttp | Networking layer / logging |
| Gson | JSON serialisation |
| Navigation Compose | In-app navigation |
| Hilt | Dependency injection |
| JUnit 4 | Unit testing |
| Espresso | UI testing |

## Planned folder structure

```
mobile/
├── app/
│   └── src/
│       ├── main/
│       │   ├── java/com/travelhub/app/
│       │   │   ├── MainActivity.kt
│       │   │   ├── navigation/
│       │   │   ├── ui/
│       │   │   │   ├── screens/
│       │   │   │   └── theme/
│       │   │   ├── data/
│       │   │   │   ├── model/
│       │   │   │   ├── network/
│       │   │   │   └── repository/
│       │   │   └── di/
│       │   ├── AndroidManifest.xml
│       │   └── res/
│       ├── test/
│       └── androidTest/
├── build.gradle.kts
├── settings.gradle.kts
└── gradle/
    └── libs.versions.toml
```
