#!/bin/bash
# =============================================================================
# Deployment Script for OOP Journey
# =============================================================================
# Usage: ./scripts/deploy.sh [environment]
#   environment: production (default) or staging
# =============================================================================

set -e

# Configuration
ENVIRONMENT="${1:-production}"
COMPOSE_FILE="docker-compose.prod.yml"

if [ "$ENVIRONMENT" == "staging" ]; then
    COMPOSE_FILE="docker-compose.staging.yml"
fi

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Logging
log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_step() { echo -e "${BLUE}[STEP]${NC} $1"; }

echo "========================================"
echo "OOP Journey Deployment"
echo "========================================"
echo "Environment: $ENVIRONMENT"
echo "Compose file: $COMPOSE_FILE"
echo "========================================"

# Pre-deployment checks
log_step "Running pre-deployment checks..."

# Check if running from project root
if [ ! -f "$COMPOSE_FILE" ]; then
    log_error "$COMPOSE_FILE not found. Are you in the project root?"
    exit 1
fi

# Check environment file
if [ ! -f ".env.production" ] && [ "$ENVIRONMENT" == "production" ]; then
    log_error ".env.production file not found!"
    exit 1
fi

log_info "Pre-deployment checks passed"

# Create backup (production only)
if [ "$ENVIRONMENT" == "production" ]; then
    log_step "Creating database backup..."
    if [ -f "scripts/backup.sh" ]; then
        ./scripts/backup.sh || log_warn "Backup failed, continuing anyway..."
    else
        log_warn "Backup script not found, skipping..."
    fi
fi

# Pull latest images
log_step "Pulling latest Docker images..."
docker-compose -f "$COMPOSE_FILE" pull

# Build if needed
log_step "Building images..."
docker-compose -f "$COMPOSE_FILE" build --no-cache

# Run database migrations
log_step "Running database migrations..."
docker-compose -f "$COMPOSE_FILE" run --rm api alembic upgrade head

# Deploy services
log_step "Deploying services..."
docker-compose -f "$COMPOSE_FILE" up -d

# Wait for services to be healthy
log_step "Waiting for services to be healthy..."
sleep 10

# Health check
log_step "Running health checks..."
MAX_RETRIES=10
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if curl -sf http://localhost/api/health > /dev/null 2>&1; then
        log_info "API is healthy"
        break
    fi
    
    RETRY_COUNT=$((RETRY_COUNT + 1))
    log_warn "Health check failed, retrying ($RETRY_COUNT/$MAX_RETRIES)..."
    sleep 5
done

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
    log_error "Health checks failed after $MAX_RETRIES attempts"
    log_warn "Rolling back..."
    docker-compose -f "$COMPOSE_FILE" down
    exit 1
fi

# Smoke tests
log_step "Running smoke tests..."
if [ -f "scripts/smoke-test.sh" ]; then
    ./scripts/smoke-test.sh || {
        log_error "Smoke tests failed!"
        exit 1
    }
else
    log_warn "Smoke test script not found, skipping..."
fi

# Cleanup
log_step "Cleaning up..."
docker system prune -f
docker volume prune -f

# Deployment summary
log_info "========================================"
log_info "Deployment Complete!"
log_info "========================================"
log_info "Environment: $ENVIRONMENT"
log_info "Services deployed:"
docker-compose -f "$COMPOSE_FILE" ps --services
log_info "========================================"

exit 0
