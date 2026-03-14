#!/bin/bash
# =============================================================================
# Database Migration Script
# =============================================================================
# Runs database migrations using Alembic.
#
# Usage:
#   db-migrate.sh              # Run pending migrations
#   db-migrate.sh create       # Create new migration (interactive)
#   db-migrate.sh downgrade    # Downgrade one revision
#   db-migrate.sh reset        # Reset to baseline
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

# Determine docker compose command
if docker compose version > /dev/null 2>&1; then
    COMPOSE_CMD="docker compose"
elif docker-compose version > /dev/null 2>&1; then
    COMPOSE_CMD="docker-compose"
else
    echo -e "${RED}✗ Docker Compose not found!${NC}"
    exit 1
fi

# Check if API container is running
if ! $COMPOSE_CMD -f "$DOCKER_DIR/docker-compose.yml" ps | grep -q "api.*running"; then
    echo -e "${RED}✗ API service is not running!${NC}"
    echo -e "${YELLOW}Start the development stack first:${NC} make dev"
    exit 1
fi

COMMAND="${1:-upgrade}"

echo -e "${BLUE}==============================================${NC}"
echo -e "${BLUE}  Database Migration${NC}"
echo -e "${BLUE}==============================================${NC}"
echo ""

case "$COMMAND" in
    upgrade|migrate|up)
        echo -e "${YELLOW}Running pending migrations...${NC}"
        $COMPOSE_CMD -f "$DOCKER_DIR/docker-compose.yml" exec api alembic upgrade head
        echo ""
        echo -e "${GREEN}✓ Migrations complete!${NC}"
        ;;
    
    downgrade|down)
        echo -e "${YELLOW}Downgrading one revision...${NC}"
        $COMPOSE_CMD -f "$DOCKER_DIR/docker-compose.yml" exec api alembic downgrade -1
        echo ""
        echo -e "${GREEN}✓ Downgrade complete!${NC}"
        ;;
    
    create|revision|new)
        echo -e "${YELLOW}Creating new migration...${NC}"
        echo -e "${BLUE}Enter migration message:${NC} "
        read -r message
        if [ -z "$message" ]; then
            echo -e "${RED}✗ Migration message is required!${NC}"
            exit 1
        fi
        $COMPOSE_CMD -f "$DOCKER_DIR/docker-compose.yml" exec api alembic revision --autogenerate -m "$message"
        echo ""
        echo -e "${GREEN}✓ Migration created!${NC}"
        ;;
    
    history)
        echo -e "${YELLOW}Migration history:${NC}"
        $COMPOSE_CMD -f "$DOCKER_DIR/docker-compose.yml" exec api alembic history --verbose
        ;;
    
    current)
        echo -e "${YELLOW}Current revision:${NC}"
        $COMPOSE_CMD -f "$DOCKER_DIR/docker-compose.yml" exec api alembic current
        ;;
    
    reset)
        echo -e "${RED}WARNING: This will reset the database to baseline!${NC}"
        echo -e "${YELLOW}All data will be lost. Are you sure? (yes/no)${NC}"
        read -r confirm
        if [ "$confirm" = "yes" ]; then
            $COMPOSE_CMD -f "$DOCKER_DIR/docker-compose.yml" exec api alembic downgrade base
            $COMPOSE_CMD -f "$DOCKER_DIR/docker-compose.yml" exec api alembic upgrade head
            echo -e "${GREEN}✓ Database reset complete!${NC}"
        else
            echo -e "${YELLOW}Cancelled.${NC}"
        fi
        ;;
    
    stamp)
        echo -e "${YELLOW}Stamping database with head revision...${NC}"
        $COMPOSE_CMD -f "$DOCKER_DIR/docker-compose.yml" exec api alembic stamp head
        echo -e "${GREEN}✓ Database stamped!${NC}"
        ;;
    
    *)
        echo -e "${RED}Unknown command: $COMMAND${NC}"
        echo ""
        echo "Usage: db-migrate.sh [command]"
        echo ""
        echo "Commands:"
        echo "  upgrade|migrate|up  - Run pending migrations (default)"
        echo "  downgrade|down      - Downgrade one revision"
        echo "  create|revision     - Create new migration"
        echo "  history             - Show migration history"
        echo "  current             - Show current revision"
        echo "  reset               - Reset to baseline (DESTRUCTIVE!)"
        echo "  stamp               - Stamp database without running migrations"
        echo ""
        exit 1
        ;;
esac

echo ""
