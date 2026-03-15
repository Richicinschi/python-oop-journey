import { defineConfig, devices } from '@playwright/test';

/**
 * Playwright configuration for Python OOP Journey E2E tests
 * 
 * Environment Variables:
 * - BASE_URL: Target URL for tests (default: https://python-oop-journey.onrender.com)
 * - CI: Set to 'true' for CI mode (more retries, screenshots on failure)
 */

const BASE_URL = process.env.BASE_URL || 'https://python-oop-journey.onrender.com';

export default defineConfig({
  testDir: './apps/web/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: process.env.CI ? [['list'], ['html', { outputFolder: 'playwright-report' }]] : 'list',
  
  // Global timeout for each test
  timeout: 30000,
  
  // Expect timeout for assertions
  expect: {
    timeout: 10000,
  },
  
  use: {
    // Base URL for all tests
    baseURL: BASE_URL,
    
    // Collect trace when retrying the failed test
    trace: 'on-first-retry',
    
    // Capture screenshot on failure
    screenshot: 'only-on-failure',
    
    // Record video on failure
    video: 'retain-on-failure',
    
    // Viewport size
    viewport: { width: 1280, height: 720 },
    
    // Action timeout
    actionTimeout: 15000,
    
    // Navigation timeout
    navigationTimeout: 30000,
  },
  
  // Output directory for test artifacts
  outputDir: 'test-results',
  
  projects: [
    {
      name: 'chromium',
      use: { 
        ...devices['Desktop Chrome'],
        // Launch options
        launchOptions: {
          slowMo: process.env.CI ? 0 : 50, // Slightly slower in local for visibility
        },
      },
    },
    // Uncomment to test on multiple browsers
    // {
    //   name: 'firefox',
    //   use: { ...devices['Desktop Firefox'] },
    // },
    // {
    //   name: 'webkit',
    //   use: { ...devices['Desktop Safari'] },
    // },
  ],
  
  // Run local dev server before starting tests (optional)
  // webServer: {
  //   command: 'npm run dev',
  //   url: 'http://localhost:3000',
  //   reuseExistingServer: !process.env.CI,
  // },
});
