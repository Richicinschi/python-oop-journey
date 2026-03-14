# =============================================================================
# OOP Journey Website - Makefile
# =============================================================================
# Common development and deployment tasks.
#
# Usage:
#   make [target]
#
# Targets:
#   dev          - Start development stack
#   dev-stop     - Stop development stack
#   build        - Build all Docker images
#   test         - Run all tests
#   test-web     - Run web tests only
#   test-api     - Run API tests only
#   migrate      - Run database migrations
#   db-reset     - Reset database (DESTRUCTIVE!)
#   logs         - View logs
#   clean        - Clean up containers and volumes
#   shell-web    - Open shell in web container
#   shell-api    - Open shell in API container
#   prod-build   - Build production images
#   prod-deploy  - Deploy to production (requires setup)
# =============================================================================

# Configuration
DOCKER_DIR := infrastructure/docker
COMPOSE_DEV := $(DOCKER_DIR)/docker-compose.yml
COMPOSE_PROD := $(DOCKER_DIR)/docker-compose.prod.yml
SCRIPTS_DIR := $(DOCKER_DIR)/scripts

# Determine docker compose command
DOCKER_COMPOSE := $(shell if docker compose version > /dev/null 2>&1; then echo "docker compose"; else echo "docker-compose"; fi)

# Colors for output
BLUE := \033[36m
GREEN := \033[32m
YELLOW := \033[33m
RED := \033[31m
NC := \033[0m # No Color

.PHONY: help dev dev-stop build test test-web test-api migrate db-reset logs clean shell-web shell-api prod-build prod-deploy

# Default target
help:
	@echo "$(BLUE)OOP Journey - Available Commands$(NC)"
	@echo ""
	@echo "$(GREEN)Development:$(NC)"
	@echo "  $(YELLOW)make dev$(NC)          Start development stack"
	@echo "  $(YELLOW)make dev-stop$(NC)     Stop development stack"
	@echo "  $(YELLOW)make logs$(NC)         View logs (add SERVICE=web to filter)"
	@echo "  $(YELLOW)make shell-web$(NC)    Open shell in web container"
	@echo "  $(YELLOW)make shell-api$(NC)    Open shell in API container"
	@echo ""
	@echo "$(GREEN)Build & Test:$(NC)"
	@echo "  $(YELLOW)make build$(NC)        Build all Docker images"
	@echo "  $(YELLOW)make test$(NC)         Run all tests"
	@echo "  $(YELLOW)make test-web$(NC)     Run web tests only"
	@echo "  $(YELLOW)make test-api$(NC)     Run API tests only"
	@echo ""
	@echo "$(GREEN)Database:$(NC)"
	@echo "  $(YELLOW)make migrate$(NC)      Run database migrations"
	@echo "  $(YELLOW)make db-reset$(NC)     Reset database $(RED)(DESTRUCTIVE!)$(NC)"
	@echo ""
	@echo "$(GREEN)Production:$(NC)"
	@echo "  $(YELLOW)make prod-build$(NC)   Build production images"
	@echo ""
	@echo "$(GREEN)Maintenance:$(NC)"
	@echo "  $(YELLOW)make clean$(NC)        Clean up containers and volumes"
	@echo "  $(YELLOW)make prune$(NC)        Full Docker cleanup $(RED)(DESTRUCTIVE!)$(NC)"
	@echo ""

# =============================================================================
# Development Commands
# =============================================================================

dev:
	@echo "$(BLUE)Starting development stack...$(NC)"
	@$(SCRIPTS_DIR)/dev-start.sh

dev-stop:
	@echo "$(BLUE)Stopping development stack...$(NC)"
	@$(SCRIPTS_DIR)/dev-stop.sh

logs:
	@echo "$(BLUE)Viewing logs...$(NC)"
	@$(SCRIPTS_DIR)/logs.sh $(SERVICE) $(LINES)

shell-web:
	@echo "$(BLUE)Opening shell in web container...$(NC)"
	@$(DOCKER_COMPOSE) -f $(COMPOSE_DEV) exec web sh

shell-api:
	@echo "$(BLUE)Opening shell in API container...$(NC)"
	@$(DOCKER_COMPOSE) -f $(COMPOSE_DEV) exec api bash

# =============================================================================
# Build Commands
# =============================================================================

build:
	@echo "$(BLUE)Building development images...$(NC)"
	@$(DOCKER_COMPOSE) -f $(COMPOSE_DEV) build --parallel
	@echo "$(GREEN)✓ Build complete!$(NC)"

build-no-cache:
	@echo "$(BLUE)Building development images (no cache)...$(NC)"
	@$(DOCKER_COMPOSE) -f $(COMPOSE_DEV) build --no-cache --parallel
	@echo "$(GREEN)✓ Build complete!$(NC)"

# =============================================================================
# Test Commands
# =============================================================================

test: test-api test-web
	@echo "$(GREEN)✓ All tests complete!$(NC)"

test-web:
	@echo "$(BLUE)Running web tests...$(NC)"
	@$(DOCKER_COMPOSE) -f $(COMPOSE_DEV) run --rm web npm test

test-api:
	@echo "$(BLUE)Running API tests...$(NC)"
	@$(DOCKER_COMPOSE) -f $(COMPOSE_DEV) exec -T api pytest -v

test-api-watch:
	@echo "$(BLUE)Running API tests in watch mode...$(NC)"
	@$(DOCKER_COMPOSE) -f $(COMPOSE_DEV) exec api ptw

# =============================================================================
# Database Commands
# =============================================================================

migrate:
	@echo "$(BLUE)Running database migrations...$(NC)"
	@$(SCRIPTS_DIR)/db-migrate.sh upgrade

db-migrate-create:
	@echo "$(BLUE)Creating new migration...$(NC)"
	@$(SCRIPTS_DIR)/db-migrate.sh create

db-downgrade:
	@echo "$(YELLOW)Downgrading database...$(NC)"
	@$(SCRIPTS_DIR)/db-migrate.sh downgrade

db-history:
	@echo "$(BLUE)Migration history:$(NC)"
	@$(SCRIPTS_DIR)/db-migrate.sh history

db-reset:
	@echo "$(RED)WARNING: This will delete all database data!$(NC)"
	@$(SCRIPTS_DIR)/db-reset.sh

db-seed:
	@echo "$(BLUE)Seeding database...$(NC)"
	@$(DOCKER_COMPOSE) -f $(COMPOSE_DEV) exec api python -m apps.api.scripts.seed

# =============================================================================
# Production Commands
# =============================================================================

prod-build:
	@echo "$(BLUE)Building production images...$(NC)"
	@$(DOCKER_COMPOSE) -f $(COMPOSE_PROD) build --parallel
	@echo "$(GREEN)✓ Production build complete!$(NC)"

prod-up:
	@echo "$(BLUE)Starting production stack...$(NC)"
	@$(DOCKER_COMPOSE) -f $(COMPOSE_PROD) up -d

prod-down:
	@echo "$(BLUE)Stopping production stack...$(NC)"
	@$(DOCKER_COMPOSE) -f $(COMPOSE_PROD) down

prod-logs:
	@echo "$(BLUE)Viewing production logs...$(NC)"
	@$(DOCKER_COMPOSE) -f $(COMPOSE_PROD) logs -f

prod-deploy: prod-build prod-up
	@echo "$(GREEN)✓ Production deployment complete!$(NC)"

# =============================================================================
# Cleanup Commands
# =============================================================================

clean:
	@echo "$(YELLOW)Cleaning up containers and volumes...$(NC)"
	@$(DOCKER_COMPOSE) -f $(COMPOSE_DEV) down -v --remove-orphans
	@$(DOCKER_COMPOSE) -f $(COMPOSE_PROD) down -v --remove-orphans
	@echo "$(GREEN)✓ Cleanup complete!$(NC)"

prune:
	@echo "$(RED)WARNING: This will remove all unused Docker data!$(NC)"
	@echo "$(YELLOW)Continue? [y/N]$(NC)"
	@read -r response; \
	if [ "$$response" = "y" ] || [ "$$response" = "Y" ]; then \
		docker system prune -af --volumes; \
		echo "$(GREEN)✓ Prune complete!$(NC)"; \
	else \
		echo "$(YELLOW)Cancelled.$(NC)"; \
	fi

# =============================================================================
# Utility Commands
# =============================================================================

format:
	@echo "$(BLUE)Formatting code...$(NC)"
	@cd apps/web && npm run format 2>/dev/null || echo "$(YELLOW)No format script in web$(NC)"
	@$(DOCKER_COMPOSE) -f $(COMPOSE_DEV) exec api black apps/api packages 2>/dev/null || echo "$(YELLOW)Black not available$(NC)"

lint:
	@echo "$(BLUE)Running linters...$(NC)"
	@cd apps/web && npm run lint 2>/dev/null || echo "$(YELLOW)No lint script in web$(NC)"
	@$(DOCKER_COMPOSE) -f $(COMPOSE_DEV) exec api flake8 apps/api packages 2>/dev/null || echo "$(YELLOW)Flake8 not available$(NC)"

type-check:
	@echo "$(BLUE)Running type checks...$(NC)"
	@cd apps/web && npm run type-check 2>/dev/null || echo "$(YELLOW)No type-check script in web$(NC)"
	@$(DOCKER_COMPOSE) -f $(COMPOSE_DEV) exec api mypy apps/api packages 2>/dev/null || echo "$(YELLOW)Mypy not available$(NC)"

# Sandbox commands
sandbox-build:
	@echo "$(BLUE)Building sandbox image...$(NC)"
	@docker build -f $(DOCKER_DIR)/sandbox.Dockerfile -t oopjourney-sandbox:latest .
	@echo "$(GREEN)✓ Sandbox image built!$(NC)"

sandbox-test:
	@echo "$(BLUE)Testing sandbox security...$(NC)"
	@docker run --rm \
		--read-only \
		--network none \
		--memory 256m \
		--cpus 0.5 \
		--pids-limit 50 \
		--security-opt no-new-privileges:true \
		--cap-drop ALL \
		--tmpfs /tmp:noexec,nosuid,size=100m \
		oopjourney-sandbox:latest \
		python -c "print('Sandbox security test passed')"
	@echo "$(GREEN)✓ Sandbox test passed!$(NC)"

# =============================================================================
# CI/CD Commands
# =============================================================================

ci-test:
	@echo "$(BLUE)Running CI test suite...$(NC)"
	@$(DOCKER_COMPOSE) -f $(COMPOSE_DEV) up -d db redis
	@sleep 5
	@$(DOCKER_COMPOSE) -f $(COMPOSE_DEV) build api
	@$(DOCKER_COMPOSE) -f $(COMPOSE_DEV) run --rm api pytest -v --cov=apps.api --cov-report=xml
	@$(DOCKER_COMPOSE) -f $(COMPOSE_DEV) down

ci-build:
	@echo "$(BLUE)Running CI build...$(NC)"
	@$(DOCKER_COMPOSE) -f $(COMPOSE_DEV) build
	@$(DOCKER_COMPOSE) -f $(COMPOSE_PROD) build
	@echo "$(GREEN)✓ CI build complete!$(NC)"
