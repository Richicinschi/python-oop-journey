import { test, expect } from '@playwright/test';

const BASE_URL = process.env.BASE_URL || 'https://python-oop-journey.onrender.com';

test.describe('Verify all main routes', () => {
  const routes = [
    // Working routes
    { path: '/', shouldWork: true, name: 'Homepage' },
    { path: '/weeks', shouldWork: true, name: 'Weeks list' },
    { path: '/weeks/week00_getting_started', shouldWork: true, name: 'Week 0 detail' },
    { path: '/weeks/week01_fundamentals', shouldWork: true, name: 'Week 1 detail' },
    { path: '/search', shouldWork: true, name: 'Search page' },
    { path: '/bookmarks', shouldWork: true, name: 'Bookmarks' },
    { path: '/recent', shouldWork: true, name: 'Recent' },
    
    // Broken routes  
    { path: '/problems', shouldWork: false, name: 'Problems index (BROKEN)' },
    { path: '/weeks/0', shouldWork: false, name: 'Week by number (BROKEN)' },
    { path: '/weeks/1', shouldWork: false, name: 'Week 1 by number (BROKEN)' },
    
    // Problem pages - need correct slugs
    { path: '/problems/problem_01_assign_and_print', shouldWork: true, name: 'Problem 1' },
    { path: '/problems/problem_02_swap_values', shouldWork: true, name: 'Problem 2' },
  ];

  for (const route of routes) {
    test(`${route.name}: ${route.path}`, async ({ page }) => {
      await page.goto(`${BASE_URL}${route.path}`);
      await page.waitForLoadState('networkidle');
      
      const title = await page.title();
      const has404 = title.includes('404') || title.includes('not found');
      const url = page.url();
      
      console.log(`${route.path}: ${has404 ? '❌ 404' : '✅ OK'} | Title: ${title.substring(0, 50)}`);
      
      if (route.shouldWork) {
        expect(has404, `Expected ${route.path} to work but got 404`).toBe(false);
      } else {
        // For known broken routes, just log
        if (!has404) {
          console.log(`  ⚠️ ${route.path} unexpectedly worked!`);
        }
      }
    });
  }
});

test.describe('Day pages', () => {
  test('Week 0 Day 4 (has problems)', async ({ page }) => {
    await page.goto(`${BASE_URL}/weeks/week00_getting_started/days/day04_variables`);
    const title = await page.title();
    console.log('Day page title:', title);
    
    // Should show problems list
    const hasProblems = await page.locator('text=problem').count() > 0;
    console.log('Has problems listed:', hasProblems);
  });
});

test.describe('Problem solving flow', () => {
  test('Open problem -> see editor', async ({ page }) => {
    await page.goto(`${BASE_URL}/problems/problem_01_assign_and_print`);
    
    const title = await page.title();
    console.log('Problem page title:', title);
    
    // Check for editor
    const hasMonaco = await page.locator('.monaco-editor').isVisible().catch(() => false);
    const hasInstructions = await page.locator('text=Instructions').isVisible().catch(() => false);
    const hasRunButton = await page.locator('text=Run').isVisible().catch(() => false);
    
    console.log('Has Monaco editor:', hasMonaco);
    console.log('Has Instructions:', hasInstructions);
    console.log('Has Run button:', hasRunButton);
    
    await page.screenshot({ path: 'test-results/problem-page.png' });
  });
});
