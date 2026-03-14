#!/bin/bash
# =============================================================================
# SSL Certificate Setup Script for OOP Journey
# =============================================================================
# This script sets up SSL certificates using Let's Encrypt
# Usage: ./scripts/setup-ssl.sh <domain>
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

# Check arguments
if [ $# -eq 0 ]; then
    echo "Usage: $0 <domain> [staging]"
    echo "Example: $0 oopjourney.com"
    echo "Example: $0 staging.oopjourney.com staging"
    exit 1
fi

DOMAIN="$1"
ENVIRONMENT="${2:-production}"
EMAIL="admin@$DOMAIN"

log_info "Setting up SSL certificate for: $DOMAIN"
log_info "Environment: $ENVIRONMENT"

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    log_error "Docker is not running"
    exit 1
fi

# Start nginx temporarily for certbot validation
log_info "Starting nginx..."
docker-compose -f docker-compose.prod.yml up -d nginx

# Wait for nginx to be ready
sleep 5

# Determine certbot flags
CERTBOT_FLAGS=""
if [ "$ENVIRONMENT" == "staging" ]; then
    log_warn "Using Let's Encrypt staging environment"
    CERTBOT_FLAGS="--staging"
fi

# Obtain certificate
log_info "Obtaining SSL certificate from Let's Encrypt..."
docker run -it --rm \
    -v oopjourney_certbot_data:/etc/letsencrypt \
    -v ./certbot/www:/var/www/certbot \
    certbot/certbot certonly \
    $CERTBOT_FLAGS \
    --webroot \
    --webroot-path=/var/www/certbot \
    --email "$EMAIL" \
    --agree-tos \
    --no-eff-email \
    -d "$DOMAIN" \
    -d "www.$DOMAIN" 2>/dev/null || true

# Check if certificate was obtained
if docker run --rm -v oopjourney_certbot_data:/etc/letsencrypt busybox test -f "/etc/letsencrypt/live/$DOMAIN/fullchain.pem"; then
    log_info "SSL certificate obtained successfully!"
    
    # Display certificate info
    log_info "Certificate details:"
    docker run --rm -v oopjourney_certbot_data:/etc/letsencrypt busybox ls -la "/etc/letsencrypt/live/$DOMAIN/"
else
    log_error "Failed to obtain SSL certificate"
    log_warn "Check that DNS is properly configured for $DOMAIN"
    exit 1
fi

# Restart nginx with SSL configuration
log_info "Restarting nginx with SSL..."
docker-compose -f docker-compose.prod.yml restart nginx

log_info "SSL setup completed!"
log_info "Your site should now be accessible at: https://$DOMAIN"

# Display renewal information
log_info "Certificate will auto-renew. To test renewal:"
echo "  docker-compose -f docker-compose.prod.yml run --rm certbot renew --dry-run"

exit 0
