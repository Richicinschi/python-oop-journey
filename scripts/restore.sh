#!/bin/bash
# =============================================================================
# Database Restore Script for OOP Journey Production
# =============================================================================
# This script restores a PostgreSQL backup
# Usage: ./scripts/restore.sh <backup_file>
# =============================================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Configuration
BACKUP_DIR="/opt/oopjourney/backups"
DB_CONTAINER="oopjourney-db"
DB_NAME="${POSTGRES_DB:-oopjourney_production}"
DB_USER="${POSTGRES_USER:-oopjourney}"

# Check arguments
if [ $# -eq 0 ]; then
    echo "Usage: $0 <backup_file>"
    echo ""
    echo "Available backups:"
    ls -1t "$BACKUP_DIR"/oopjourney_backup_*.sql.gz 2>/dev/null | head -10 || echo "  No backups found"
    exit 1
fi

BACKUP_FILE="$1"

# Check if backup file exists
if [ ! -f "$BACKUP_FILE" ]; then
    # Try with backup directory prefix
    if [ -f "$BACKUP_DIR/$BACKUP_FILE" ]; then
        BACKUP_FILE="$BACKUP_DIR/$BACKUP_FILE"
    else
        log_error "Backup file not found: $BACKUP_FILE"
        exit 1
    fi
fi

log_warn "=============================================="
log_warn "WARNING: This will REPLACE the current database!"
log_warn "Database: $DB_NAME"
log_warn "Backup: $BACKUP_FILE"
log_warn "=============================================="
echo ""
read -p "Are you sure you want to continue? (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    log_info "Restore cancelled"
    exit 0
fi

log_info "Starting database restore..."

# Create pre-restore backup
log_info "Creating pre-restore backup..."
PRE_RESTORE_FILE="oopjourney_pre_restore_$(date +%Y%m%d_%H%M%S).sql.gz"
docker exec "$DB_CONTAINER" pg_dump -U "$DB_USER" -d "$DB_NAME" | gzip > "$BACKUP_DIR/$PRE_RESTORE_FILE"
log_info "Pre-restore backup created: $PRE_RESTORE_FILE"

# Stop application services
log_info "Stopping application services..."
docker-compose -f /opt/oopjourney/docker-compose.prod.yml stop web api worker scheduler

# Restore database
log_info "Restoring database from backup..."
gunzip < "$BACKUP_FILE" | docker exec -i "$DB_CONTAINER" psql -U "$DB_USER" -d "$DB_NAME"

if [ $? -eq 0 ]; then
    log_info "Database restored successfully"
else
    log_error "Database restore failed!"
    log_warn "You may need to restore from the pre-restore backup: $PRE_RESTORE_FILE"
    exit 1
fi

# Restart application services
log_info "Restarting application services..."
docker-compose -f /opt/oopjourney/docker-compose.prod.yml start web api worker scheduler

# Verify restore
log_info "Verifying database connectivity..."
sleep 5
if docker exec "$DB_CONTAINER" pg_isready -U "$DB_USER" -d "$DB_NAME"; then
    log_info "Database is online and accepting connections"
else
    log_error "Database verification failed!"
    exit 1
fi

log_info "Restore process completed!"
log_info "Pre-restore backup saved as: $PRE_RESTORE_FILE"

exit 0
