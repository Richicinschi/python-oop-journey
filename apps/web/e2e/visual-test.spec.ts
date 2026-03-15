import { test, expect } from '@playwright/test';

const BASE_URL = process.env.BASE_URL || 'https://python-oop-journey.onrender.com';

test.describe('Visual verification of key pages', () => {
  test('homepage screenshot', async ({ page }) => {
    await page.goto(BASE_URL);
    await page.screenshot({ path: 'test-results/homepage.png', fullPage: true });
    console.log('Homepage screenshot saved');
  });

  test('Start Learning button behavior', async ({ page }) => {
    await page.goto(BASE_URL);
    
    // Get href before clicking
    const button = page.getByRole('link', { name: /Start Learning/i });
    const href = await button.getAttribute('href');
    console.log('Start Learning href:', href);
    
    // Click and wait
    await button.click();
    await page.waitForLoadState('networkidle');
    
    // Screenshot
    await page.screenshot({ path: 'test-results/start-learning-result.png', fullPage: true });
    console.log('After Start Learning, URL:', page.url());
    
    // Check for 404 indicators
    const title = await page.title();
    console.log('Page title:', title);
    
    const hasNotFound = await page.locator('text=/404|not found|page could not be found/i').isVisible().catch(() => false);
    console.log('Has 404 text:', hasNotFound);
  });

  test('Week 0 page exists?', async ({ page }) => {
    await page.goto(`${BASE_URL}/weeks/0`);
    await page.screenshot({ path: 'test-results/weeks-0.png', fullPage: true });
    console.log('Weeks/0 URL:', page.url());
    console.log('Weeks/0 title:', await page.title());
  });

  test('Actual week slug page', async ({ page }) => {
    await page.goto(`${BASE_URL}/weeks/week00_getting_started`);
    await page.screenshot({ path: 'test-results/weeks-actual-slug.png', fullPage: true });
    console.log('Real week URL:', page.url());
    console.log('Real week title:', await page.title());
  });

  test('/problems page exists?', async ({ page }) => {
    await page.goto(`${BASE_URL}/problems`);
    await page.screenshot({ path: 'test-results/problems-index.png', fullPage: true });
    console.log('/problems URL:', page.url());
    console.log('/problems title:', await page.title());
  });

  test('First problem page', async ({ page }) => {
    // Navigate to a known problem
    await page.goto(`${BASE_URL}/problems/week00_getting_started_day00_welcome_problem_00_hello_world`);
    await page.screenshot({ path: 'test-results/problem-detail.png', fullPage: true });
    console.log('Problem URL:', page.url());
    console.log('Problem title:', await page.title());
    
    // Check if editor loads
    const hasEditor = await page.locator('.monaco-editor, [data-testid="code-editor"]').isVisible().catch(() => false);
    console.log('Has code editor:', hasEditor);
  });
});
