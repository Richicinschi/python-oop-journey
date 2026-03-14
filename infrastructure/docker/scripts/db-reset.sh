#!/bin/bash
# =============================================================================
# Database Reset Script
# =============================================================================
# WARNING: Destructive operation! Resets the database to a clean state.
#
# This will:
# 1. Stop all services
# 2. Remove the database volume
# 3. Recreate the database
# 4. Run migrations
# 5. (Optional) Seed with test data
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

echo -e "${RED}==============================================${NC}"
echo -e "${RED}  ⚠ WARNING: DATABASE RESET${NC}"
echo -e "${RED}==============================================${NC}"
echo ""
echo -e "${RED}This will:${NC}"
echo "  • Stop all services"
echo "  • DELETE ALL DATABASE DATA"
echo "  • Recreate the database"
echo "  • Run migrations"
echo ""
echo -e "${YELLOW}Type 'RESET' to continue:${NC}"
read -r confirm

if [ "$confirm" != "RESET" ]; then
    echo -e "${YELLOW}Cancelled. No changes made.${NC}"
    exit 0
fi

echo ""
echo -e "${BLUE}==============================================${NC}"
echo -e "${BLUE}  Database Reset${NC}"
echo -e "${BLUE}==============================================${NC}"
echo ""

# Determine docker compose command
if docker compose version > /dev/null 2>&1; then
    COMPOSE_CMD="docker compose"
elif docker-compose version > /dev/null 2>&1; then
    COMPOSE_CMD="docker-compose"
else
    echo -e "${RED}✗ Docker Compose not found!${NC}"
    exit 1
fi

# Step 1: Stop services
echo -e "${YELLOW}Step 1/5: Stopping services...${NC}"
$COMPOSE_CMD -f "$DOCKER_DIR/docker-compose.yml" down
echo -e "${GREEN}✓ Services stopped${NC}"
echo ""

# Step 2: Remove database volume
echo -e "${YELLOW}Step 2/5: Removing database volume...${NC}"
docker volume rm website-playground_postgres_data 2>/dev/null || true
docker volume rm oopjourney_postgres_data 2>/dev/null || true
echo -e "${GREEN}✓ Database volume removed${NC}"
echo ""

# Step 3: Start database only
echo -e "${YELLOW}Step 3/5: Starting database...${NC}"
$COMPOSE_CMD -f "$DOCKER_DIR/docker-compose.yml" up -d db redis

# Wait for database to be ready
echo -e "${YELLOW}Waiting for database to be ready...${NC}"
sleep 5
for i in {1..30}; do
    if $COMPOSE_CMD -f "$DOCKER_DIR/docker-compose.yml" exec -T db pg_isready -U postgres > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Database is ready${NC}"
        break
    fi
    sleep 1
done
echo ""

# Step 4: Start API and run migrations
echo -e "${YELLOW}Step 4/5: Running migrations...${NC}"
$COMPOSE_CMD -f "$DOCKER_DIR/docker-compose.yml" up -d api

# Wait for API to be healthy
sleep 5
for i in {1..30}; do
    if $COMPOSE_CMD -f "$DOCKER_DIR/docker-compose.yml" exec -T api python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" > /dev/null 2>&1; then
        break
    fi
    sleep 1
done

$COMPOSE_CMD -f "$DOCKER_DIR/docker-compose.yml" exec api alembic upgrade head
echo -e "${GREEN}✓ Migrations complete${NC}"
echo ""

# Step 5: Start all services
echo -e "${YELLOW}Step 5/5: Starting all services...${NC}"
$COMPOSE_CMD -f "$DOCKER_DIR/docker-compose.yml" up -d
echo -e "${GREEN}✓ All services started${NC}"
echo ""

echo -e "${GREEN}==============================================${NC}"
echo -e "${GREEN}  ✓ Database Reset Complete!${NC}"
echo -e "${GREEN}==============================================${NC}"
echo ""
echo -e "Your database has been reset to a clean state with all migrations applied."
echo ""
echo -e "Services are available at:"
echo -e "  ${BLUE}Web:${NC} http://localhost:3000"
echo -e "  ${BLUE}API:${NC}  http://localhost:8000"
echo ""
