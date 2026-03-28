.PHONY: help docker-up docker-down docker-build docker-logs clean users-test users-build users-logs

help:
	@echo "=== TravelHub Monorepo ==="
	@echo ""
	@echo "Global:"
	@echo "  make docker-up      - Start all services"
	@echo "  make docker-down    - Stop all services"
	@echo "  make docker-build   - Build all images"
	@echo "  make docker-logs    - Tail all logs"
	@echo "  make clean          - Remove __pycache__ files"
	@echo ""
	@echo "Users service:"
	@echo "  make users-test     - Run users tests"
	@echo "  make users-build    - Build users image"
	@echo "  make users-logs     - Tail users logs"

# Global commands
docker-up:
	docker compose up -d

docker-down:
	docker compose down

docker-build:
	docker compose build

docker-logs:
	docker compose logs -f

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Users service
users-test:
	cd services/users && PYTHONPATH=src pytest tests/ -v

users-build:
	docker compose build users

users-logs:
	docker compose logs -f users
