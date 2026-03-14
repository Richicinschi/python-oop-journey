#!/bin/bash
# =============================================================================
# Smoke Test Script for OOP Journey Production
# =============================================================================
# This script runs basic smoke tests against the production environment
# Usage: ./scripts/smoke-test.sh [BASE_URL]
# =============================================================================

set -e

# Configuration
BASE_URL="${1:-https://oopjourney.com}"
API_URL="${2:-https://api.oopjourney.com}"
TIMEOUT=30

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Counters
TESTS_PASSED=0
TESTS_FAILED=0

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

# Test function
run_test() {
    local name="$1"
    local command="$2"
    
    echo -n "Testing $name... "
    
    if eval "$command" > /dev/null 2>&1; then
        echo -e "${GREEN}✓${NC}"
        ((TESTS_PASSED++))
        return 0
    else
        echo -e "${RED}✗${NC}"
        ((TESTS_FAILED++))
        return 1
    fi
}

echo "========================================"
echo "OOP Journey Smoke Tests"
echo "========================================"
echo "Base URL: $BASE_URL"
echo "API URL: $API_URL"
echo "========================================"
echo ""

# Health checks
echo "--- Health Checks ---"
run_test "Web server is accessible" "curl -f -s --max-time $TIMEOUT $BASE_URL"
run_test "API health endpoint" "curl -f -s --max-time $TIMEOUT $API_URL/health"
run_test "Nginx health endpoint" "curl -f -s --max-time $TIMEOUT $BASE_URL/nginx-health"
run_test "API readiness endpoint" "curl -f -s --max-time $TIMEOUT $API_URL/ready"

echo ""
echo "--- SSL/TLS Checks ---"
run_test "HTTPS is enforced" "curl -f -s --max-time $TIMEOUT -I $BASE_URL 2>&1 | grep -q 'https'"
run_test "SSL certificate is valid" "curl -f -s --max-time $TIMEOUT -v $BASE_URL 2>&1 | grep -q 'SSL certificate verify ok'"

echo ""
echo "--- API Endpoints ---"
run_test "Curriculum weeks endpoint" "curl -f -s --max-time $TIMEOUT $API_URL/api/v1/curriculum/weeks"
run_test "Static assets are served" "curl -f -s --max-time $TIMEOUT $BASE_URL/favicon.ico"

echo ""
echo "--- Security Headers ---"
run_test "X-Frame-Options header" "curl -f -s --max-time $TIMEOUT -I $BASE_URL 2>&1 | grep -qi 'x-frame-options'"
run_test "X-Content-Type-Options header" "curl -f -s --max-time $TIMEOUT -I $BASE_URL 2>&1 | grep -qi 'nosniff'"

echo ""
echo "--- Content Checks ---"
run_test "Homepage has content" "curl -f -s --max-time $TIMEOUT $BASE_URL | grep -qi 'python\|oop\|journey'"
run_test "Weeks page is accessible" "curl -f -s --max-time $TIMEOUT $BASE_URL/weeks | grep -qi 'week'"

echo ""
echo "========================================"
echo "Test Results"
echo "========================================"
echo -e "Tests Passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests Failed: ${RED}$TESTS_FAILED${NC}"
echo "========================================"

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}All smoke tests passed!${NC}"
    exit 0
else
    echo -e "${RED}Some smoke tests failed!${NC}"
    exit 1
fi
