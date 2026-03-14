#!/bin/bash
# =============================================================================
# Development Stack Stop Script
# =============================================================================
# Stops all development services cleanly.
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

echo -e "${BLUE}==============================================${NC}"
echo -e "${BLUE}  OOP Journey - Stopping Development Stack${NC}"
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

echo -e "${YELLOW}Stopping services...${NC}"
$COMPOSE_CMD -f "$DOCKER_DIR/docker-compose.yml" down

echo ""
echo -e "${GREEN}✓ Development stack stopped.${NC}"
echo ""

# Show stopped containers count
stopped=$(docker ps -q | wc -l)
if [ "$stopped" -eq "0" ]; then
    echo -e "${GREEN}No containers running.${NC}"
else
    echo -e "${YELLOW}$stopped containers still running (may be from other projects).${NC}"
fi
echo ""
