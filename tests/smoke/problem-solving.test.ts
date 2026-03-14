/**
 * Problem Solving Flow Smoke Tests
 * 
 * These tests verify the core problem-solving experience
 * in the production environment.
 */

import { test, expect } from '@playwright/test';

const BASE_URL = process.env.TEST_BASE_URL || 'https://oopjourney.com';
const API_URL = process.env.TEST_API_URL || 'https://api.oopjourney.com';

test.describe('Problem Solving Flow', () => {
  test('problem page should load with code editor', async ({ page }) => {
    await page.goto(`${BASE_URL}/weeks/week-01-fundamentals/day-01/problem-01`);
    
    // Should see problem title
    await expect(page.locator('h1')).toBeVisible();
    
    // Should see code editor or code block
    const codeElement = page.locator('.monaco-editor, pre code, .code-editor, [data-testid="code-editor"]').first();
    await expect(codeElement).toBeVisible();
  });

  test('problem should have instructions', async ({ page }) => {
    await page.goto(`${BASE_URL}/weeks/week-01-fundamentals/day-01/problem-01`);
    
    // Should see problem description
    const description = page.locator('article, .problem-description, .description, [data-testid="problem-description"]').first();
    await expect(description).toBeVisible();
    
    // Should have some text content
    const text = await description.textContent();
    expect(text?.length).toBeGreaterThan(50);
  });

  test('run code button should be present', async ({ page }) => {
    await page.goto(`${BASE_URL}/weeks/week-01-fundamentals/day-01/problem-01`);
    
    // Look for run button
    const runButton = page.locator('button:has-text("Run"), button:has-text("Execute"), [data-testid="run-button"]').first();
    await expect(runButton).toBeVisible();
  });

  test('hint button should be present', async ({ page }) => {
    await page.goto(`${BASE_URL}/weeks/week-01-fundamentals/day-01/problem-01`);
    
    // Look for hint button or section
    const hintElement = page.locator('button:has-text("Hint"), .hint-button, [data-testid="hint-button"], details summary:has-text("Hint"), #hints').first();
    await expect(hintElement).toBeVisible();
  });

  test('solution button should be present', async ({ page }) => {
    await page.goto(`${BASE_URL}/weeks/week-01-fundamentals/day-01/problem-01`);
    
    // Look for solution button or section
    const solutionElement = page.locator('button:has-text("Solution"), .solution-button, [data-testid="solution-button"], details summary:has-text("Solution"), #solution').first();
    await expect(solutionElement).toBeVisible();
  });

  test('progress should be tracked locally', async ({ page }) => {
    await page.goto(`${BASE_URL}/weeks/week-01-fundamentals/day-01/problem-01`);
    
    // Check localStorage for progress
    const progress = await page.evaluate(() => {
      return localStorage.getItem('oopjourney-progress');
    });
    
    // Progress might not exist yet, which is fine
    // If it exists, it should be valid JSON
    if (progress) {
      expect(() => JSON.parse(progress)).not.toThrow();
    }
  });

  test('AI hint API should be accessible', async ({ request }) => {
    const response = await request.post(`${API_URL}/api/v1/ai/hint`, {
      data: {
        weekId: 'week-01-fundamentals',
        dayId: 'day-01',
        problemId: 'problem-01',
        code: 'print("Hello")',
      },
    });
    
    // Should get a response (might be 401 if not authenticated, which is expected)
    expect([200, 401, 422]).toContain(response.status());
  });

  test('code execution API should be accessible', async ({ request }) => {
    const response = await request.post(`${API_URL}/api/v1/execute`, {
      data: {
        code: 'print("Hello, World!")',
        testCases: [],
      },
    });
    
    // Should get a response
    expect([200, 401, 422]).toContain(response.status());
  });

  test('navigation between problems should work', async ({ page }) => {
    await page.goto(`${BASE_URL}/weeks/week-01-fundamentals/day-01`);
    
    // Find and click on a problem link
    const problemLink = page.locator('a[href*="problem"], [data-testid="problem-link"]').first();
    
    if (await problemLink.isVisible().catch(() => false)) {
      await problemLink.click();
      
      // Should navigate to a problem page
      await page.waitForURL(/.*problem.*/, { timeout: 5000 });
      
      // Should see problem content
      await expect(page.locator('article, .problem-content, main')).toBeVisible();
    }
  });

  test('progress bar should be visible on week page', async ({ page }) => {
    await page.goto(`${BASE_URL}/weeks/week-01-fundamentals`);
    
    // Look for progress indicator
    const progressBar = page.locator('.progress-bar, [role="progressbar"], .progress, [data-testid="progress"]').first();
    
    // Progress bar should exist (even if at 0%)
    const hasProgressBar = await progressBar.isVisible().catch(() => false);
    expect(hasProgressBar).toBe(true);
  });
});

test.describe('Project Flow', () => {
  test('project page should be accessible', async ({ page }) => {
    await page.goto(`${BASE_URL}/weeks/week-01-fundamentals/project`);
    
    // Should see project content or coming soon message
    const content = await page.textContent('body');
    const hasContent = 
      content?.toLowerCase().includes('project') ||
      content?.toLowerCase().includes('coming soon');
    
    expect(hasContent).toBe(true);
  });

  test('projects list page should be accessible', async ({ page }) => {
    await page.goto(`${BASE_URL}/projects`);
    
    // Should see projects list
    await expect(page.locator('h1, h2').first()).toBeVisible();
  });
});
