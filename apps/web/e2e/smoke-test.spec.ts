import { test, expect } from '@playwright/test';

const BASE_URL = process.env.BASE_URL || 'https://python-oop-journey.onrender.com';

test.describe('Smoke Tests - Click all navigation', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(BASE_URL);
  });

  test('homepage - Start Learning button should not 404', async ({ page }) => {
    // Find and click Start Learning
    const startButton = page.getByRole('link', { name: /Start Learning/i });
    await expect(startButton).toBeVisible();
    
    const href = await startButton.getAttribute('href');
    console.log('Start Learning links to:', href);
    
    await startButton.click();
    
    // Check we didn't get 404
    await expect(page.locator('text=404')).not.toBeVisible();
    await expect(page.locator('text=This page could not be found')).not.toBeVisible();
    
    // Log current URL
    console.log('After Start Learning, URL is:', page.url());
  });

  test('homepage - Browse Curriculum button should work', async ({ page }) => {
    const browseButton = page.getByRole('link', { name: /Browse Curriculum/i });
    await browseButton.click();
    
    await expect(page.locator('text=404')).not.toBeVisible();
    console.log('Browse Curriculum URL:', page.url());
  });

  test('homepage - all week cards should link to valid pages', async ({ page }) => {
    // Get all week card links
    const weekLinks = await page.locator('a[href^="/weeks/"]').all();
    console.log(`Found ${weekLinks.length} week links`);
    
    for (const link of weekLinks.slice(0, 3)) { // Test first 3
      const href = await link.getAttribute('href');
      console.log('Testing week link:', href);
      
      await link.click();
      
      // Check for 404
      const has404 = await page.locator('text=404').isVisible().catch(() => false);
      const hasNotFound = await page.locator('text=This page could not be found').isVisible().catch(() => false);
      
      if (has404 || hasNotFound) {
        throw new Error(`Week link ${href} returned 404`);
      }
      
      console.log(`✓ ${href} is valid`);
      
      // Go back for next test
      await page.goto(BASE_URL);
    }
  });

  test('navigation - sidebar links', async ({ page }) => {
    // Go to dashboard first
    await page.goto(`${BASE_URL}/weeks`);
    
    const navLinks = [
      { name: 'Curriculum', href: '/weeks' },
      { name: 'Projects', href: '/projects' },
      { name: 'Bookmarks', href: '/bookmarks' },
      { name: 'Search', href: '/search' },
    ];
    
    for (const link of navLinks) {
      console.log(`Testing nav: ${link.name} -> ${link.href}`);
      await page.goto(`${BASE_URL}${link.href}`);
      
      const has404 = await page.locator('text=404').isVisible().catch(() => false);
      const hasNotFound = await page.locator('text=This page could not be found').isVisible().catch(() => false);
      
      if (has404 || hasNotFound) {
        console.error(`✗ ${link.href} returned 404`);
      } else {
        console.log(`✓ ${link.href} is valid`);
      }
    }
  });

  test('quick links - All Problems, Recent, Bookmarks', async ({ page }) => {
    await page.goto(BASE_URL);
    
    const quickLinks = [
      { name: 'All Problems', selector: 'text=All Problems' },
      { name: 'Recently Viewed', selector: 'text=Recently Viewed' },
      { name: 'My Bookmarks', selector: 'text=My Bookmarks' },
    ];
    
    for (const link of quickLinks) {
      const element = page.locator(link.selector).first();
      if (await element.isVisible().catch(() => false)) {
        await element.click();
        
        const has404 = await page.locator('text=404').isVisible().catch(() => false);
        console.log(`${link.name}: ${has404 ? '✗ 404' : '✓ OK'} - ${page.url()}`);
        
        await page.goto(BASE_URL);
      }
    }
  });
});

test.describe('Critical User Flows', () => {
  test('week detail page - Start Week button', async ({ page }) => {
    await page.goto(`${BASE_URL}/weeks`);
    
    // Click first week
    const firstWeek = page.locator('a[href^="/weeks/"]').first();
    await firstWeek.click();
    
    // Look for Start/Continue Week button
    const startWeekBtn = page.getByRole('button', { name: /Start Week|Continue Week/i });
    if (await startWeekBtn.isVisible().catch(() => false)) {
      await startWeekBtn.click();
      
      const has404 = await page.locator('text=404').isVisible().catch(() => false);
      console.log('Start Week button result:', has404 ? '404' : 'OK', page.url());
    }
  });

  test('day page - solve first problem flow', async ({ page }) => {
    // Navigate to first week's first day
    await page.goto(`${BASE_URL}/weeks/week00_getting_started`);
    
    // Click first day
    const firstDay = page.locator('a[href*="/days/"]').first();
    if (await firstDay.isVisible().catch(() => false)) {
      await firstDay.click();
      console.log('Day page URL:', page.url());
      
      // Look for first problem
      const firstProblem = page.locator('a[href^="/problems/"]').first();
      if (await firstProblem.isVisible().catch(() => false)) {
        await firstProblem.click();
        console.log('Problem page URL:', page.url());
        
        const has404 = await page.locator('text=404').isVisible().catch(() => false);
        if (has404) {
          throw new Error('Problem page returned 404');
        }
      }
    }
  });
});
