#!/bin/bash

# Python OOP Journey - E2E Test Runner
# Usage: ./run-tests.sh [options]
#
# Options:
#   --critical    Run only critical path tests
#   --nav         Run only navigation tests
#   --code        Run only code execution tests
#   --smoke       Run only smoke tests
#   --all         Run all tests (default)
#   --headed      Run tests in headed mode (visible browser)
#   --debug       Run with debug output
#   --ci          Run in CI mode (more retries, screenshots on failure)

set -e

# Default configuration
BASE_URL="${BASE_URL:-https://python-oop-journey.onrender.com}"
TEST_SUITE="all"
HEADED=""
DEBUG=""
CI=""

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --critical)
      TEST_SUITE="critical"
      shift
      ;;
    --nav)
      TEST_SUITE="nav"
      shift
      ;;
    --code)
      TEST_SUITE="code"
      shift
      ;;
    --smoke)
      TEST_SUITE="smoke"
      shift
      ;;
    --all)
      TEST_SUITE="all"
      shift
      ;;
    --headed)
      HEADED="--headed"
      shift
      ;;
    --debug)
      DEBUG="--debug"
      shift
      ;;
    --ci)
      CI="true"
      shift
      ;;
    --url)
      BASE_URL="$2"
      shift 2
      ;;
    -h|--help)
      echo "Python OOP Journey - E2E Test Runner"
      echo ""
      echo "Usage: ./run-tests.sh [options]"
      echo ""
      echo "Options:"
      echo "  --critical    Run only critical path tests"
      echo "  --nav         Run only navigation tests"
      echo "  --code        Run only code execution tests"
      echo "  --smoke       Run only smoke tests"
      echo "  --all         Run all tests (default)"
      echo "  --headed      Run tests in headed mode (visible browser)"
      echo "  --debug       Run with debug output"
      echo "  --ci          Run in CI mode"
      echo "  --url URL     Set base URL (default: https://python-oop-journey.onrender.com)"
      echo "  -h, --help    Show this help message"
      echo ""
      echo "Environment Variables:"
      echo "  BASE_URL      Set the base URL for tests"
      echo ""
      exit 0
      ;;
    *)
      echo "Unknown option: $1"
      echo "Run with --help for usage information"
      exit 1
      ;;
  esac
done

echo "========================================="
echo "Python OOP Journey - E2E Tests"
echo "========================================="
echo "Base URL: $BASE_URL"
echo "Test Suite: $TEST_SUITE"
echo ""

# Export base URL for tests
export BASE_URL

# Create test results directory
mkdir -p test-results

# Determine which tests to run
case $TEST_SUITE in
  critical)
    echo "Running critical path tests..."
    npx playwright test e2e/critical-paths.spec.ts $HEADED $DEBUG
    ;;
  nav)
    echo "Running navigation tests..."
    npx playwright test e2e/navigation.spec.ts $HEADED $DEBUG
    ;;
  code)
    echo "Running code execution tests..."
    npx playwright test e2e/code-execution.spec.ts $HEADED $DEBUG
    ;;
  smoke)
    echo "Running smoke tests..."
    npx playwright test e2e/smoke-test.spec.ts $HEADED $DEBUG
    ;;
  all)
    echo "Running all tests..."
    if [ "$CI" = "true" ]; then
      npx playwright test --reporter=list $HEADED $DEBUG
    else
      npx playwright test $HEADED $DEBUG
    fi
    ;;
esac

echo ""
echo "========================================="
echo "Test run complete!"
echo "========================================="
echo "Screenshots saved to: test-results/"
