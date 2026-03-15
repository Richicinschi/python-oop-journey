# Python OOP Journey - E2E Test Runner (PowerShell)
# Usage: .\run-tests.ps1 [options]
#
# Options:
#   -Critical    Run only critical path tests
#   -Nav         Run only navigation tests
#   -Code        Run only code execution tests
#   -Smoke       Run only smoke tests
#   -All         Run all tests (default)
#   -Headed      Run tests in headed mode (visible browser)
#   -Debug       Run with debug output
#   -CI          Run in CI mode
#   -Url         Set base URL

param(
    [switch]$Critical,
    [switch]$Nav,
    [switch]$Code,
    [switch]$Smoke,
    [switch]$All = $true,
    [switch]$Headed,
    [switch]$Debug,
    [switch]$CI,
    [string]$Url = "https://python-oop-journey.onrender.com"
)

# Show help
if ($args -contains "-h" -or $args -contains "--help") {
    Write-Host "Python OOP Journey - E2E Test Runner" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Usage: .\run-tests.ps1 [options]" -ForegroundColor White
    Write-Host ""
    Write-Host "Options:" -ForegroundColor Yellow
    Write-Host "  -Critical    Run only critical path tests"
    Write-Host "  -Nav         Run only navigation tests"
    Write-Host "  -Code        Run only code execution tests"
    Write-Host "  -Smoke       Run only smoke tests"
    Write-Host "  -All         Run all tests (default)"
    Write-Host "  -Headed      Run tests in headed mode (visible browser)"
    Write-Host "  -Debug       Run with debug output"
    Write-Host "  -CI          Run in CI mode"
    Write-Host "  -Url URL     Set base URL"
    Write-Host "  -h, --help   Show this help message"
    Write-Host ""
    exit 0
}

# Determine which test suite to run
$TestSuite = "all"
if ($Critical) { $TestSuite = "critical"; $All = $false }
if ($Nav) { $TestSuite = "nav"; $All = $false }
if ($Code) { $TestSuite = "code"; $All = $false }
if ($Smoke) { $TestSuite = "smoke"; $All = $false }

# Build arguments
$PlaywrightArgs = @()
if ($Headed) { $PlaywrightArgs += "--headed" }
if ($Debug) { $PlaywrightArgs += "--debug" }
if ($CI) { $PlaywrightArgs += "--reporter=list" }

# Export base URL
$env:BASE_URL = $Url

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Python OOP Journey - E2E Tests" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "Base URL: $Url" -ForegroundColor White
Write-Host "Test Suite: $TestSuite" -ForegroundColor White
Write-Host ""

# Create test results directory
New-Item -ItemType Directory -Force -Path "test-results" | Out-Null

# Run tests based on suite
switch ($TestSuite) {
    "critical" {
        Write-Host "Running critical path tests..." -ForegroundColor Yellow
        npx playwright test e2e/critical-paths.spec.ts @PlaywrightArgs
    }
    "nav" {
        Write-Host "Running navigation tests..." -ForegroundColor Yellow
        npx playwright test e2e/navigation.spec.ts @PlaywrightArgs
    }
    "code" {
        Write-Host "Running code execution tests..." -ForegroundColor Yellow
        npx playwright test e2e/code-execution.spec.ts @PlaywrightArgs
    }
    "smoke" {
        Write-Host "Running smoke tests..." -ForegroundColor Yellow
        npx playwright test e2e/smoke-test.spec.ts @PlaywrightArgs
    }
    default {
        Write-Host "Running all tests..." -ForegroundColor Yellow
        npx playwright test @PlaywrightArgs
    }
}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Green
Write-Host "Test run complete!" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Green
Write-Host "Screenshots saved to: test-results/" -ForegroundColor White
