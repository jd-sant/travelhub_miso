# Infrastructure – AWS

## Overview

This directory contains the **AWS deployment configuration** for TravelHub.

## What will be developed here

- **Amazon ECS (Fargate)** task definitions — one per microservice (auth, trips, users) and the Nuxt frontend
- **Amazon ECR** repository definitions — stores Docker images for each service
- **Application Load Balancer (ALB)** listener rules — routes traffic to the correct service by path prefix
- **Amazon RDS (PostgreSQL)** — managed database for each microservice
- **Amazon VPC** — network configuration with public and private subnets
- **AWS Secrets Manager** — stores secrets such as JWT signing keys and database passwords
- **Amazon CloudWatch** — centralised logging and monitoring dashboards

## Planned ALB path routing

| Path prefix | Target service | Port |
|-------------|---------------|------|
| `/auth/*`   | auth-service  | 8001 |
| `/trips/*`  | trips-service | 8002 |
| `/users/*`  | users-service | 8003 |
| `/*`        | frontend      | 3000 |

## Planned folder structure

```
infrastructure/
└── aws/
    ├── ecs-task-definitions/   # ECS task definition JSON files
    │   ├── auth-service.json
    │   ├── trips-service.json
    │   ├── users-service.json
    │   └── frontend.json
    ├── alb-rules.json          # ALB listener rules
    └── vpc.json                # VPC / subnet configuration
```

