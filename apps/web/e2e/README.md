# E2E Test Suite for Python OOP Journey

Comprehensive end-to-end tests for the Python OOP Journey website using Playwright.

## Test Files

### 1. `critical-paths.spec.ts`
Tests the most important user flows:
- ✅ Homepage loads successfully
- ✅ Navigation works (sidebar links)
- ✅ Week pages load
- ✅ Problem pages load
- ✅ Code execution works
- ✅ Theme toggle works
- ✅ Error handling (404 pages)
- ✅ Complete user journey: Homepage → Weeks → Week → Problem

### 2. `navigation.spec.ts`
Comprehensive navigation tests:
- ✅ Header navigation (logo, links, user menu, search)
- ✅ Sidebar navigation (all sections, active states)
- ✅ Footer links (privacy, terms, copyright)
- ✅ Mobile navigation (responsive menu)
- ✅ Breadcrumb navigation
- ✅ Keyboard navigation (Tab, Enter, Escape)
- ✅ Quick links & command palette
- ✅ Deep link navigation

### 3. `code-execution.spec.ts`
Code editor and execution tests:
- ✅ Simple code execution (print statements)
- ✅ Variable assignment and f-strings
- ✅ Arithmetic operations
- ✅ Syntax error handling
- ✅ Runtime error handling (NameError, ZeroDivisionError, IndexError, KeyError, TypeError)
- ✅ Timeout handling (infinite loops)
- ✅ Editor features (keyboard input, reset, save)
- ✅ Output panel functionality
- ✅ Test runner integration

### 4. Existing Tests
- `smoke-test.spec.ts` - Basic smoke tests
- `verify-routes.spec.ts` - Route verification
- `visual-test.spec.ts` - Visual screenshots
- `test-project-flow.spec.ts` - Project workflow

## Configuration

### Environment Variables
```bash
# Set base URL for tests
export BASE_URL=https://python-oop-journey.onrender.com
```

### Playwright Config
Located at `website-playground/playwright.config.ts`:
- Test directory: `./apps/web/e2e`
- Browser: Chromium
- Retries: 2 in CI, 0 locally
- Screenshots: On failure
- Video: Retain on failure

## Running Tests

### Quick Start
```bash
# Run all tests
npm run test:e2e

# Or using the test runner script
./e2e/run-tests.sh
```

### Test Runner Scripts

#### Bash (Linux/Mac/Git Bash)
```bash
# Run all tests
./e2e/run-tests.sh

# Run specific test suite
./e2e/run-tests.sh --critical    # Critical paths only
./e2e/run-tests.sh --nav         # Navigation only
./e2e/run-tests.sh --code        # Code execution only
./e2e/run-tests.sh --smoke       # Smoke tests only

# Additional options
./e2e/run-tests.sh --headed      # Visible browser
./e2e/run-tests.sh --debug       # Debug output
./e2e/run-tests.sh --ci          # CI mode
./e2e/run-tests.sh --url https://custom-url.com  # Custom URL
```

#### PowerShell (Windows)
```powershell
# Run all tests
.\e2e\run-tests.ps1

# Run specific test suite
.\e2e\run-tests.ps1 -Critical   # Critical paths only
.\e2e\run-tests.ps1 -Nav        # Navigation only
.\e2e\run-tests.ps1 -Code       # Code execution only

# Additional options
.\e2e\run-tests.ps1 -Headed     # Visible browser
.\e2e\run-tests.ps1 -Debug      # Debug output
.\e2e\run-tests.ps1 -Url "https://custom-url.com"  # Custom URL
```

### Direct Playwright Commands
```bash
# Run all tests
npx playwright test

# Run specific file
npx playwright test e2e/critical-paths.spec.ts

# Run with visible browser
npx playwright test --headed

# Run with debug
npx playwright test --debug

# Run specific test
npx playwright test -g "homepage loads"
```

## Test Results

Results are saved to `test-results/`:
- Screenshots (on failure)
- Videos (on failure)
- Traces (on first retry)

## CI/CD Integration

### GitHub Actions Example
```yaml
name: E2E Tests
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: 18
      - run: npm ci
      - run: npx playwright install
      - run: ./e2e/run-tests.sh --ci
        env:
          BASE_URL: ${{ vars.PRODUCTION_URL }}
      - uses: actions/upload-artifact@v3
        if: failure()
        with:
          name: test-results
          path: test-results/
```

## Test Reliability

### Anti-Flake Measures
1. **Wait for network idle** before assertions
2. **Retry logic** for finding elements
3. **Graceful fallbacks** for optional features
4. **Timeout handling** for code execution
5. **Screenshot capture** on failures

### Best Practices
- Tests run against production URL by default
- Tests are independent (no shared state)
- Tests clean up after themselves
- Tests use semantic selectors (role, text) when possible

## Troubleshooting

### Tests fail locally
1. Check BASE_URL is accessible
2. Ensure Playwright browsers are installed: `npx playwright install`
3. Run with `--headed` to see what's happening
4. Check `test-results/` for screenshots

### Tests fail in CI
1. Check production deployment is up
2. Verify BASE_URL environment variable
3. Increase timeouts if needed
4. Check artifacts for failure details

### Common Issues
- **Timeout errors**: Increase timeout in playwright.config.ts
- **404 errors**: Verify URLs match production routes
- **Element not found**: Check selectors match current UI

## Maintenance

When adding new features:
1. Add tests to appropriate spec file
2. Run full test suite before committing
3. Update this README with new test coverage
4. Tag tests appropriately (e.g., `@slow`, `@smoke`)

## Coverage Summary

| Feature | Coverage |
|---------|----------|
| Homepage | ✅ Full |
| Navigation | ✅ Full |
| Week Pages | ✅ Full |
| Problem Pages | ✅ Full |
| Code Editor | ✅ Full |
| Code Execution | ✅ Full |
| Error Handling | ✅ Full |
| Mobile/Responsive | ✅ Partial |
| Theme Toggle | ✅ Basic |
| User Auth | ⚠️ Partial (requires login) |
