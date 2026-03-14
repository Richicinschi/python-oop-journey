/**
 * Critical Path Smoke Tests
 * 
 * These tests verify the most important user flows are working
 * in the production environment.
 */

import { test, expect } from '@playwright/test';

const BASE_URL = process.env.TEST_BASE_URL || 'https://oopjourney.com';

test.describe('Critical User Flows', () => {
  test('user can view homepage', async ({ page }) => {
    await page.goto(BASE_URL);
    
    // Should see the main heading
    await expect(page.locator('h1')).toContainText(/Python|OOP|Journey/i);
    
    // Should see navigation
    await expect(page.locator('nav, header')).toBeVisible();
  });

  test('user can browse curriculum weeks', async ({ page }) => {
    await page.goto(`${BASE_URL}/weeks`);
    
    // Should see week cards
    const weekCards = page.locator('[data-testid="week-card"], .week-card, article').first();
    await expect(weekCards).toBeVisible();
  });

  test('user can view a specific week', async ({ page }) => {
    await page.goto(`${BASE_URL}/weeks/week-01-fundamentals`);
    
    // Should see week content
    await expect(page.locator('h1, h2')).toContainText(/Week|Fundamentals/i);
    
    // Should see day sections
    await expect(page.locator('[data-testid="day-section"], section').first()).toBeVisible();
  });

  test('user can view a problem', async ({ page }) => {
    await page.goto(`${BASE_URL}/weeks/week-01-fundamentals/day-01`);
    
    // Should see problem content
    await expect(page.locator('article, .problem-content, main')).toBeVisible();
  });

  test('user can access login page', async ({ page }) => {
    await page.goto(`${BASE_URL}/login`);
    
    // Should see login form
    await expect(page.locator('input[type="email"], input[name="email"]').first()).toBeVisible();
  });

  test('user can access signup page', async ({ page }) => {
    await page.goto(`${BASE_URL}/signup`);
    
    // Should see signup form
    await expect(page.locator('input[type="email"], input[name="email"]').first()).toBeVisible();
  });

  test('404 page works for unknown routes', async ({ page }) => {
    await page.goto(`${BASE_URL}/this-page-does-not-exist`);
    
    // Should show 404 or not found message
    const body = await page.textContent('body');
    const is404 = body?.toLowerCase().includes('404') || 
                  body?.toLowerCase().includes('not found') ||
                  body?.toLowerCase().includes('page not found');
    expect(is404).toBe(true);
  });

  test('site is responsive on mobile', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto(BASE_URL);
    
    // Should not have horizontal scroll
    const body = await page.locator('body');
    const bodyWidth = await body.evaluate(el => el.scrollWidth);
    const viewportWidth = 375;
    
    expect(bodyWidth).toBeLessThanOrEqual(viewportWidth + 20); // Allow small tolerance
  });
});

test.describe('Performance Checks', () => {
  test('homepage should load within 3 seconds', async ({ page }) => {
    const start = Date.now();
    await page.goto(BASE_URL);
    await page.waitForLoadState('networkidle');
    const loadTime = Date.now() - start;
    
    expect(loadTime).toBeLessThan(3000);
  });

  test('should not have any console errors', async ({ page }) => {
    const errors: string[] = [];
    
    page.on('console', msg => {
      if (msg.type() === 'error') {
        errors.push(msg.text());
      }
    });
    
    await page.goto(BASE_URL);
    await page.waitForLoadState('networkidle');
    
    // Filter out non-critical errors
    const criticalErrors = errors.filter(e => 
      !e.includes('favicon') && 
      !e.includes('google-analytics')
    );
    
    expect(criticalErrors).toHaveLength(0);
  });
});
