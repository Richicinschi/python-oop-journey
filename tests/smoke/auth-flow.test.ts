/**
 * Authentication Flow Smoke Tests
 * 
 * These tests verify the authentication system is working
 * in the production environment.
 */

import { test, expect } from '@playwright/test';

const BASE_URL = process.env.TEST_BASE_URL || 'https://oopjourney.com';
const TEST_EMAIL = process.env.TEST_USER_EMAIL || 'test@example.com';

test.describe('Authentication Flow', () => {
  test('login page should be accessible', async ({ page }) => {
    await page.goto(`${BASE_URL}/login`);
    
    // Should see email input
    const emailInput = page.locator('input[type="email"]').first();
    await expect(emailInput).toBeVisible();
    await expect(emailInput).toBeEnabled();
  });

  test('magic link form should submit', async ({ page }) => {
    await page.goto(`${BASE_URL}/login`);
    
    // Fill in email
    await page.locator('input[type="email"]').first().fill(TEST_EMAIL);
    
    // Submit form
    await page.locator('button[type="submit"]').first().click();
    
    // Should show success message or redirect
    await page.waitForTimeout(2000);
    
    const bodyText = await page.textContent('body');
    const hasSuccessMessage = 
      bodyText?.toLowerCase().includes('check your email') ||
      bodyText?.toLowerCase().includes('magic link sent') ||
      bodyText?.toLowerCase().includes('email sent') ||
      page.url().includes('check-email');
    
    expect(hasSuccessMessage).toBe(true);
  });

  test('should handle invalid email', async ({ page }) => {
    await page.goto(`${BASE_URL}/login`);
    
    // Fill in invalid email
    await page.locator('input[type="email"]').first().fill('not-an-email');
    
    // Submit form
    await page.locator('button[type="submit"]').first().click();
    
    // Should show validation error
    await page.waitForTimeout(500);
    
    const bodyText = await page.textContent('body');
    const hasError = 
      bodyText?.toLowerCase().includes('invalid') ||
      bodyText?.toLowerCase().includes('valid email');
    
    expect(hasError).toBe(true);
  });

  test('protected routes should redirect to login', async ({ page }) => {
    // Try to access a protected route
    await page.goto(`${BASE_URL}/dashboard`);
    
    // Should redirect to login
    await page.waitForURL(/.*login.*/, { timeout: 5000 });
    
    expect(page.url()).toContain('login');
  });

  test('signup page should be accessible', async ({ page }) => {
    await page.goto(`${BASE_URL}/signup`);
    
    // Should see signup form elements
    const emailInput = page.locator('input[type="email"]').first();
    await expect(emailInput).toBeVisible();
    await expect(emailInput).toBeEnabled();
  });

  test('passwordless auth flow (complete)', async ({ page, context }) => {
    // This test requires a valid magic link token
    // It's skipped if no token is provided
    test.skip(!process.env.TEST_MAGIC_LINK_TOKEN, 'No magic link token provided');
    
    const token = process.env.TEST_MAGIC_LINK_TOKEN!;
    
    // Visit magic link
    await page.goto(`${BASE_URL}/auth/callback?token=${token}`);
    
    // Should redirect to dashboard or home
    await page.waitForURL(/dashboard|home/, { timeout: 10000 });
    
    // Verify user is logged in (check for user menu, profile, etc.)
    const userMenu = page.locator('[data-testid="user-menu"], .user-menu, button[aria-label*="user"]').first();
    await expect(userMenu).toBeVisible();
  });

  test('logout should work', async ({ page, context }) => {
    // This test requires an authenticated session
    test.skip(!process.env.TEST_AUTH_TOKEN, 'No auth token provided');
    
    // Set auth token
    await context.addCookies([{
      name: 'auth_token',
      value: process.env.TEST_AUTH_TOKEN!,
      domain: new URL(BASE_URL).hostname,
      path: '/',
    }]);
    
    // Go to dashboard
    await page.goto(`${BASE_URL}/dashboard`);
    
    // Find and click logout
    const logoutButton = page.locator('button:has-text("Logout"), a:has-text("Logout"), [data-testid="logout"]').first();
    await logoutButton.click();
    
    // Should redirect to home or login
    await page.waitForURL(/.*(login|home|\\/)$/, { timeout: 5000 });
    
    // Verify we're logged out by trying to access dashboard
    await page.goto(`${BASE_URL}/dashboard`);
    await page.waitForURL(/.*login.*/, { timeout: 5000 });
  });
});
