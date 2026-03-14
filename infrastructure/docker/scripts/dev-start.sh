#!/bin/bash
# =============================================================================
# Development Stack Start Script
# =============================================================================
# Starts all services for local development with hot reload enabled.
# =============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOCKER_DIR="$(dirname "$SCRIPT_DIR")"
PROJECT_ROOT="$(dirname "$DOCKER_DIR")"

echo -e "${BLUE}==============================================${NC}"
echo -e "${BLUE}  OOP Journey - Development Stack${NC}"
echo -e "${BLUE}==============================================${NC}"
echo ""

# Check if .env exists
if [ ! -f "$PROJECT_ROOT/.env" ]; then
    echo -e "${YELLOW}⚠ .env file not found!${NC}"
    echo -e "${YELLOW}Creating from .env.example...${NC}"
    cp "$PROJECT_ROOT/.env.example" "$PROJECT_ROOT/.env"
    echo -e "${GREEN}✓ Created .env file. Please review and update as needed.${NC}"
    echo ""
fi

# Check Docker is running
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}✗ Docker is not running!${NC}"
    echo "Please start Docker and try again."
    exit 1
fi

echo -e "${BLUE}Checking Docker Compose...${NC}"

# Determine docker compose command
if docker compose version > /dev/null 2>&1; then
    COMPOSE_CMD="docker compose"
elif docker-compose version > /dev/null 2>&1; then
    COMPOSE_CMD="docker-compose"
else
    echo -e "${RED}✗ Docker Compose not found!${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Using: $COMPOSE_CMD${NC}"
echo ""

# Build images if needed
echo -e "${BLUE}Building images if needed...${NC}"
$COMPOSE_CMD -f "$DOCKER_DIR/docker-compose.yml" build

echo ""
echo -e "${BLUE}Starting development stack...${NC}"
echo -e "${YELLOW}This may take a few minutes on first run.${NC}"
echo ""

# Start services
$COMPOSE_CMD -f "$DOCKER_DIR/docker-compose.yml" up -d

echo ""
echo -e "${BLUE}Waiting for services to be healthy...${NC}"
echo ""

# Wait for services with timeout
timeout=120
elapsed=0
while [ $elapsed -lt $timeout ]; do
    web_healthy=$(docker inspect --format='{{.State.Health.Status}}' website-playground-web-1 2>/dev/null || echo "unhealthy")
    api_healthy=$(docker inspect --format='{{.State.Health.Status}}' website-playground-api-1 2>/dev/null || echo "unhealthy")
    db_healthy=$(docker inspect --format='{{.State.Health.Status}}' website-playground-db-1 2>/dev/null || echo "unhealthy")
    redis_healthy=$(docker inspect --format='{{.State.Health.Status}}' website-playground-redis-1 2>/dev/null || echo "unhealthy")
    
    if [ "$web_healthy" = "healthy" ] && [ "$api_healthy" = "healthy" ] && [ "$db_healthy" = "healthy" ] && [ "$redis_healthy" = "healthy" ]; then
        echo ""
        echo -e "${GREEN}==============================================${NC}"
        echo -e "${GREEN}  All services are healthy!${NC}"
        echo -e "${GREEN}==============================================${NC}"
        echo ""
        echo -e "${GREEN}🚀 Development stack is running!${NC}"
        echo ""
        echo -e "  ${BLUE}Web:${NC}     http://localhost:3000"
        echo -e "  ${BLUE}API:${NC}      http://localhost:8000"
        echo -e "  ${BLUE}API Docs:${NC} http://localhost:8000/docs"
        echo -e "  ${BLUE}DB:${NC}       localhost:5432"
        echo -e "  ${BLUE}Redis:${NC}    localhost:6379"
        echo ""
        echo -e "${YELLOW}Useful commands:${NC}"
        echo -e "  View logs:    ${BLUE}make logs${NC} or ${BLUE}$COMPOSE_CMD logs -f${NC}"
        echo -e "  Stop:         ${BLUE}make dev-stop${NC} or ${BLUE}$COMPOSE_CMD down${NC}"
        echo -e "  Run tests:    ${BLUE}make test${NC}"
        echo -e "  Database:     ${BLUE}make migrate${NC} or ${BLUE}make db-reset${NC}"
        echo ""
        exit 0
    fi
    
    sleep 2
    elapsed=$((elapsed + 2))
    
    # Show progress
    printf "\r⏳ Waiting... %d/%d seconds (Web: %s, API: %s, DB: %s, Redis: %s)" \
        $elapsed $timeout "$web_healthy" "$api_healthy" "$db_healthy" "$redis_healthy"
done

echo ""
echo ""
echo -e "${RED}✗ Timeout waiting for services to start!${NC}"
echo ""
echo -e "${YELLOW}Check logs with:${NC} $COMPOSE_CMD -f $DOCKER_DIR/docker-compose.yml logs"
echo ""
exit 1
