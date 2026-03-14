#!/bin/bash
# =============================================================================
# Logs Viewer Script
# =============================================================================
# View logs from development services.
#
# Usage:
#   logs.sh [service] [lines]
#
# Examples:
#   logs.sh              # Show all logs (follow mode)
#   logs.sh web          # Show web logs
#   logs.sh api 100      # Show last 100 lines of api logs
# =============================================================================

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOCKER_DIR="$(dirname "$SCRIPT_DIR")"

# Determine docker compose command
if docker compose version > /dev/null 2>&1; then
    COMPOSE_CMD="docker compose"
elif docker-compose version > /dev/null 2>&1; then
    COMPOSE_CMD="docker-compose"
else
    echo -e "${RED}✗ Docker Compose not found!${NC}"
    exit 1
fi

# Parse arguments
SERVICE="${1:-}"
LINES="${2:-100}"

# Show help
if [ "$SERVICE" = "-h" ] || [ "$SERVICE" = "--help" ]; then
    echo -e "${BLUE}OOP Journey - Logs Viewer${NC}"
    echo ""
    echo "Usage: logs.sh [service] [lines]"
    echo ""
    echo "Services: web, api, db, redis, sandbox"
    echo ""
    echo "Examples:"
    echo "  logs.sh              # Follow all logs"
    echo "  logs.sh web          # Follow web logs"
    echo "  logs.sh api 50       # Show last 50 lines of api logs"
    echo "  logs.sh db 20 -f     # Follow db logs from last 20 lines"
    echo ""
    exit 0
fi

# Execute logs command
if [ -z "$SERVICE" ]; then
    # No service specified - show all in follow mode
    echo -e "${BLUE}Showing all logs (Ctrl+C to exit)...${NC}"
    $COMPOSE_CMD -f "$DOCKER_DIR/docker-compose.yml" logs -f --tail="$LINES"
else
    # Service specified
    echo -e "${BLUE}Showing logs for: ${YELLOW}$SERVICE${NC}"
    $COMPOSE_CMD -f "$DOCKER_DIR/docker-compose.yml" logs -f --tail="$LINES" "$SERVICE"
fi
