#!/bin/bash
# =============================================================================
# Database Backup Script for OOP Journey Production
# =============================================================================
# This script creates a PostgreSQL backup and optionally uploads to S3
# Run as: ./scripts/backup.sh
# =============================================================================

set -e

# Configuration
BACKUP_DIR="/opt/oopjourney/backups"
DB_CONTAINER="oopjourney-db"
DB_NAME="${POSTGRES_DB:-oopjourney_production}"
DB_USER="${POSTGRES_USER:-oopjourney}"
RETENTION_DAYS="${BACKUP_RETENTION_DAYS:-30}"
S3_BUCKET="${AWS_S3_BUCKET:-}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="oopjourney_backup_${TIMESTAMP}.sql.gz"

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

# Create backup directory if it doesn't exist
mkdir -p "$BACKUP_DIR"

log_info "Starting database backup..."
log_info "Backup file: $BACKUP_FILE"

# Create backup
docker exec "$DB_CONTAINER" pg_dump -U "$DB_USER" -d "$DB_NAME" | gzip > "$BACKUP_DIR/$BACKUP_FILE"

if [ $? -eq 0 ]; then
    log_info "Backup created successfully: $BACKUP_DIR/$BACKUP_FILE"
    
    # Get file size
    FILE_SIZE=$(du -h "$BACKUP_DIR/$BACKUP_FILE" | cut -f1)
    log_info "Backup size: $FILE_SIZE"
else
    log_error "Backup failed!"
    exit 1
fi

# Upload to S3 if configured
if [ -n "$S3_BUCKET" ]; then
    log_info "Uploading backup to S3..."
    
    if command -v aws &> /dev/null; then
        aws s3 cp "$BACKUP_DIR/$BACKUP_FILE" "s3://$S3_BUCKET/database/$BACKUP_FILE"
        
        if [ $? -eq 0 ]; then
            log_info "Backup uploaded to S3 successfully"
        else
            log_error "Failed to upload backup to S3"
        fi
    else
        log_warn "AWS CLI not found, skipping S3 upload"
    fi
fi

# Clean up old backups
log_info "Cleaning up backups older than $RETENTION_DAYS days..."

# Local cleanup
find "$BACKUP_DIR" -name "oopjourney_backup_*.sql.gz" -mtime +$RETENTION_DAYS -delete

# S3 cleanup (if configured)
if [ -n "$S3_BUCKET" ] && command -v aws &> /dev/null; then
    aws s3 ls "s3://$S3_BUCKET/database/" | while read -r line; do
        file_date=$(echo "$line" | awk '{print $1}')
        file_name=$(echo "$line" | awk '{print $4}')
        
        # Calculate days difference
        file_epoch=$(date -d "$file_date" +%s 2>/dev/null || echo 0)
        current_epoch=$(date +%s)
        days_diff=$(( (current_epoch - file_epoch) / 86400 ))
        
        if [ $days_diff -gt $RETENTION_DAYS ]; then
            log_info "Deleting old backup from S3: $file_name"
            aws s3 rm "s3://$S3_BUCKET/database/$file_name"
        fi
    done
fi

log_info "Backup process completed!"

# Verify backup integrity
log_info "Verifying backup integrity..."
if gunzip -t "$BACKUP_DIR/$BACKUP_FILE" 2>/dev/null; then
    log_info "Backup integrity verified"
else
    log_error "Backup file is corrupted!"
    exit 1
fi

exit 0
