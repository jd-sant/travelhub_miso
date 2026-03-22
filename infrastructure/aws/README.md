# TravelHub AWS Infrastructure

This directory contains the AWS deployment configuration for the TravelHub platform.

## Architecture

TravelHub is deployed on AWS using the following services:

- **Amazon ECS (Fargate)** — runs the containerised microservices (auth, trips, users) and the Nuxt frontend
- **Amazon ECR** — stores Docker images for each service
- **Application Load Balancer (ALB)** — routes traffic to the appropriate service by path prefix
- **Amazon RDS (PostgreSQL)** — managed relational database for each microservice
- **Amazon VPC** — private network with public/private subnets
- **AWS Secrets Manager** — stores secrets (DB passwords, JWT secret keys)
- **Amazon CloudWatch** — centralised logging and monitoring

## Path Routing (ALB)

| Path Prefix    | Target Service  | Port |
|---------------|-----------------|------|
| `/auth/*`     | auth-service    | 8001 |
| `/trips/*`    | trips-service   | 8002 |
| `/users/*`    | users-service   | 8003 |
| `/*`          | frontend        | 3000 |

## Directory Structure

```
infrastructure/
└── aws/
    ├── ecs-task-definitions/   # ECS task definition JSON files
    │   ├── auth-service.json
    │   ├── trips-service.json
    │   ├── users-service.json
    │   └── frontend.json
    └── alb-rules.json          # ALB listener rules
```

## Deployment

1. Build and push Docker images to ECR:
   ```bash
   # Authenticate to ECR
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account_id>.dkr.ecr.us-east-1.amazonaws.com

   # Build and push each service
   docker build -t travelhub/auth-service ./backend/services/auth-service
   docker tag travelhub/auth-service:latest <account_id>.dkr.ecr.us-east-1.amazonaws.com/travelhub/auth-service:latest
   docker push <account_id>.dkr.ecr.us-east-1.amazonaws.com/travelhub/auth-service:latest
   ```

2. Register ECS task definitions:
   ```bash
   aws ecs register-task-definition --cli-input-json file://infrastructure/aws/ecs-task-definitions/auth-service.json
   ```

3. Update ECS services to deploy the new task revision:
   ```bash
   aws ecs update-service --cluster travelhub --service auth-service --force-new-deployment
   ```
