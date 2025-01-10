.PHONY: up up-dev down test build help

# Start all services in detached mode
up:
	docker compose -f docker-compose.yml up -d

# Start all services in development mode (with logs)
up-dev:
	docker compose -f docker-compose.dev.yml up

# Stop and remove all services
down:
	docker compose down

down-dev:
	docker compose -f docker-compose.dev.yml down

# Build images
build:
	docker compose build

build-dev:
	docker compose -f docker-compose.dev.yml build

# Help command to list available targets
help:
	@echo "Available commands:"
	@echo "  make up     - Start all services in detached mode (production)"
	@echo "  make up-dev - Start all services in development mode (with logs)"
	@echo "  make down   - Stop and remove all services"
	@echo "  make test   - Run tests"
	@echo "  make build  - Build images"
	@echo "  make help   - Show this help message" 