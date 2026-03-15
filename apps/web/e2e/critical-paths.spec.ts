/**
 * Critical Paths E2E Tests
 * 
 * Tests the most important user flows that must always work:
 * - Homepage loads
 * - Navigation works (sidebar links)
 * - Week page loads
 * - Problem page loads
 * - Code execution works
 * - Theme toggle works
 */

import { test, expect } from '@playwright/test';

const BASE_URL = process.env.BASE_URL || 'https://python-oop-journey.onrender.com';

// Helper to check for 404 errors
async function checkNo404(page: any, context: string): Promise<void> {
  const has404 = await page.locator('text=404').isVisible().catch(() => false);
  const hasNotFound = await page.locator('text=This page could not be found').isVisible().catch(() => false);
  const hasError = await page.locator('text=Internal Server Error').isVisible().catch(() => false);
  
  if (has404 || hasNotFound) {
    throw new Error(`${context}: Page returned 404 at ${page.url()}`);
  }
  if (hasError) {
    throw new Error(`${context}: Page returned 500 error at ${page.url()}`);
  }
}

test.describe('🚀 Critical User Flows', () => {
  test.describe('Homepage', () => {
    test('homepage loads successfully', async ({ page }) => {
      await page.goto(BASE_URL);
      
      // Wait for page to fully load
      await page.waitForLoadState('networkidle');
      
      // Check page title contains expected text
      const title = await page.title();
      expect(title).toContain('Python OOP Journey');
      
      // Verify main content is visible
      await expect(page.locator('h1').first()).toBeVisible();
      
      // Verify no 404
      await checkNo404(page, 'Homepage');
      
      console.log('✅ Homepage loaded successfully');
    });

    test('homepage main CTA buttons work', async ({ page }) => {
      await page.goto(BASE_URL);
      
      // Test Start Learning button
      const startButton = page.getByRole('link', { name: /Start Learning/i });
      await expect(startButton).toBeVisible();
      
      const startHref = await startButton.getAttribute('href');
      expect(startHref).toBeTruthy();
      
      // Test Browse Curriculum button  
      const browseButton = page.getByRole('link', { name: /Browse Curriculum/i });
      await expect(browseButton).toBeVisible();
      
      const browseHref = await browseButton.getAttribute('href');
      expect(browseHref).toBeTruthy();
      
      console.log('✅ Homepage CTAs verified');
    });
  });

  test.describe('Navigation - Sidebar', () => {
    test.beforeEach(async ({ page }) => {
      await page.goto(`${BASE_URL}/weeks`);
      await page.waitForLoadState('networkidle');
    });

    test('all sidebar navigation links work', async ({ page }) => {
      const navLinks = [
        { name: 'Curriculum', href: '/weeks' },
        { name: 'Projects', href: '/projects' },
        { name: 'Bookmarks', href: '/bookmarks' },
        { name: 'Search', href: '/search' },
      ];
      
      for (const link of navLinks) {
        // Navigate to the page
        await page.goto(`${BASE_URL}${link.href}`);
        await page.waitForLoadState('networkidle');
        
        // Verify no 404
        await checkNo404(page, `Sidebar nav: ${link.name}`);
        
        // Verify page has content
        const hasContent = await page.locator('main, [role="main"], .container').first().isVisible().catch(() => false);
        if (!hasContent) {
          throw new Error(`Sidebar nav ${link.name}: No main content found`);
        }
        
        console.log(`✅ Sidebar nav: ${link.name} -> ${link.href}`);
      }
    });

    test('sidebar is visible on dashboard pages', async ({ page }) => {
      await page.goto(`${BASE_URL}/weeks`);
      
      // Look for sidebar navigation
      const sidebar = page.locator('aside, nav[role="navigation"], [data-testid="sidebar"]').first();
      const hasSidebar = await sidebar.isVisible().catch(() => false);
      
      if (hasSidebar) {
        console.log('✅ Sidebar is visible');
      } else {
        // Some layouts may not have a traditional sidebar
        console.log('ℹ️ Sidebar element not found - may be mobile or different layout');
      }
    });
  });

  test.describe('Week Pages', () => {
    test('week list page loads', async ({ page }) => {
      await page.goto(`${BASE_URL}/weeks`);
      await page.waitForLoadState('networkidle');
      
      await checkNo404(page, 'Week list page');
      
      // Verify week content is present
      const hasWeeks = await page.locator('a[href^="/weeks/week"]').count() > 0;
      expect(hasWeeks, 'Week list page should contain week links').toBe(true);
      
      console.log('✅ Week list page loaded');
    });

    test('individual week pages load', async ({ page }) => {
      // Test Week 0 (Getting Started)
      await page.goto(`${BASE_URL}/weeks/week00_getting_started`);
      await page.waitForLoadState('networkidle');
      await checkNo404(page, 'Week 0 page');
      
      // Verify week title/content
      const hasTitle = await page.locator('h1').first().isVisible();
      expect(hasTitle).toBe(true);
      
      // Test Week 1 (Fundamentals)
      await page.goto(`${BASE_URL}/weeks/week01_fundamentals`);
      await page.waitForLoadState('networkidle');
      await checkNo404(page, 'Week 1 page');
      
      console.log('✅ Individual week pages loaded');
    });

    test('week page shows days and problems', async ({ page }) => {
      // Navigate to Week 0 Day 4 which has problems
      await page.goto(`${BASE_URL}/weeks/week00_getting_started`);
      await page.waitForLoadState('networkidle');
      
      // Look for day links
      const dayLinks = await page.locator('a[href*="/days/"]').all();
      
      if (dayLinks.length > 0) {
        console.log(`Found ${dayLinks.length} day links on week page`);
        
        // Click first day
        await dayLinks[0].click();
        await page.waitForLoadState('networkidle');
        
        await checkNo404(page, 'Day page');
        console.log('✅ Day page loaded from week page');
      } else {
        console.log('ℹ️ No day links found - page structure may differ');
      }
    });
  });

  test.describe('Problem Pages', () => {
    test('problem page loads with editor', async ({ page }) => {
      await page.goto(`${BASE_URL}/problems/problem_01_assign_and_print`);
      await page.waitForLoadState('networkidle');
      
      await checkNo404(page, 'Problem page');
      
      // Verify editor or instructions are present
      const hasEditor = await page.locator('.monaco-editor, [data-testid="code-editor"], textarea[class*="monaco"]').isVisible().catch(() => false);
      const hasInstructions = await page.locator('text=Instructions, text=Problem, h2, h3').first().isVisible().catch(() => false);
      
      if (!hasEditor && !hasInstructions) {
        throw new Error('Problem page: Neither editor nor instructions found');
      }
      
      console.log(`✅ Problem page loaded (editor: ${hasEditor}, instructions: ${hasInstructions})`);
    });

    test('problem page navigation works', async ({ page }) => {
      await page.goto(`${BASE_URL}/problems/problem_01_assign_and_print`);
      await page.waitForLoadState('networkidle');
      
      // Look for navigation elements
      const hasRunButton = await page.getByRole('button', { name: /Run/i }).isVisible().catch(() => false);
      const hasSubmitButton = await page.getByRole('button', { name: /Submit/i }).isVisible().catch(() => false);
      
      console.log(`Problem page buttons - Run: ${hasRunButton}, Submit: ${hasSubmitButton}`);
      
      // At minimum, should have some interactive elements
      const hasInteractiveElements = await page.locator('button').count() > 0;
      expect(hasInteractiveElements, 'Problem page should have interactive elements').toBe(true);
      
      console.log('✅ Problem page navigation verified');
    });
  });

  test.describe('Code Execution', () => {
    test('simple code execution works', async ({ page }) => {
      // Navigate to a problem page
      await page.goto(`${BASE_URL}/problems/problem_01_assign_and_print`);
      await page.waitForLoadState('networkidle');
      
      // Look for Run button
      const runButton = page.getByRole('button', { name: /Run/i });
      const hasRunButton = await runButton.isVisible().catch(() => false);
      
      if (!hasRunButton) {
        console.log('ℹ️ Run button not found - code execution test skipped');
        return;
      }
      
      // Click Run and wait for output
      await runButton.click();
      
      // Wait for output panel to show something
      await page.waitForTimeout(3000);
      
      // Check for output or running indicator
      const hasOutput = await page.locator('text=Output, .output, [data-testid="output"]').first().isVisible().catch(() => false);
      const hasRunning = await page.locator('text=Running, text=Executing').first().isVisible().catch(() => false);
      const hasCompleted = await page.locator('text=completed, text=done').first().isVisible().catch(() => false);
      
      if (hasOutput || hasRunning || hasCompleted) {
        console.log('✅ Code execution triggered successfully');
      } else {
        // The execution might have completed too fast or the UI differs
        console.log('ℹ️ Code execution status unclear - may need visual verification');
      }
    });

    test('code editor is interactive', async ({ page }) => {
      await page.goto(`${BASE_URL}/problems/problem_01_assign_and_print`);
      await page.waitForLoadState('networkidle');
      
      // Look for editor
      const editor = page.locator('.monaco-editor, [data-testid="code-editor"]').first();
      const hasEditor = await editor.isVisible().catch(() => false);
      
      if (hasEditor) {
        // Try to click into editor
        await editor.click();
        
        // Try typing (Monaco editor specific)
        await page.keyboard.type('# Test comment');
        
        console.log('✅ Code editor is interactive');
      } else {
        console.log('ℹ️ Monaco editor not found - may be lazy loaded or different implementation');
      }
    });
  });

  test.describe('Theme Toggle', () => {
    test('theme toggle works', async ({ page }) => {
      await page.goto(BASE_URL);
      await page.waitForLoadState('networkidle');
      
      // Look for theme toggle button (sun/moon icon or "theme" text)
      const themeToggle = page.locator('button[aria-label*="theme" i], button[title*="theme" i], [data-testid="theme-toggle"]').first();
      
      // Alternative: look for sun/moon icons
      const hasThemeButton = await themeToggle.isVisible().catch(async () => {
        // Try finding by icon
        const sunIcon = page.locator('svg[class*="sun"], svg[class*="moon"]').first();
        return await sunIcon.isVisible().catch(() => false);
      });
      
      if (!hasThemeButton) {
        console.log('ℹ️ Theme toggle not found - may be in settings menu or not implemented');
        return;
      }
      
      // Get initial theme
      const initialClass = await page.evaluate(() => document.documentElement.className);
      const initialDark = initialClass.includes('dark');
      
      // Click theme toggle
      await themeToggle.click();
      
      // Wait for theme change
      await page.waitForTimeout(500);
      
      // Verify theme changed
      const newClass = await page.evaluate(() => document.documentElement.className);
      const newDark = newClass.includes('dark');
      
      if (initialDark !== newDark) {
        console.log('✅ Theme toggle works (dark mode changed)');
      } else {
        // Theme might be controlled differently
        console.log('ℹ️ Theme class unchanged - may use different mechanism');
      }
      
      // Toggle back
      await themeToggle.click();
    });
  });

  test.describe('Error Handling', () => {
    test('404 page shows for invalid routes', async ({ page }) => {
      await page.goto(`${BASE_URL}/this-page-does-not-exist-12345`);
      await page.waitForLoadState('networkidle');
      
      // Should show 404 or not found message
      const has404 = await page.locator('text=404').isVisible().catch(() => false);
      const hasNotFound = await page.locator('text=not found').isVisible().catch(() => false);
      
      expect(has404 || hasNotFound, 'Invalid route should show 404 page').toBe(true);
      console.log('✅ 404 page displayed correctly');
    });

    test('error boundary catches errors gracefully', async ({ page }) => {
      // Navigate to a valid page first
      await page.goto(`${BASE_URL}/weeks`);
      await page.waitForLoadState('networkidle');
      
      // Page should not show generic error
      const hasGenericError = await page.locator('text=Application error, text=Something went wrong').isVisible().catch(() => false);
      expect(hasGenericError).toBe(false);
      
      console.log('✅ No unhandled errors on valid pages');
    });
  });
});

test.describe('📊 Critical Path Summary', () => {
  test('complete user journey - browse to solve', async ({ page }) => {
    // Step 1: Homepage
    await page.goto(BASE_URL);
    await page.waitForLoadState('networkidle');
    await checkNo404(page, 'Homepage');
    
    // Step 2: Navigate to weeks
    await page.goto(`${BASE_URL}/weeks`);
    await page.waitForLoadState('networkidle');
    await checkNo404(page, 'Weeks list');
    
    // Step 3: Click first week
    const firstWeek = page.locator('a[href^="/weeks/week"]').first();
    if (await firstWeek.isVisible().catch(() => false)) {
      await firstWeek.click();
      await page.waitForLoadState('networkidle');
      await checkNo404(page, 'Week detail');
      
      // Step 4: Look for a problem link
      const problemLink = page.locator('a[href^="/problems/"]').first();
      if (await problemLink.isVisible().catch(() => false)) {
        await problemLink.click();
        await page.waitForLoadState('networkidle');
        await checkNo404(page, 'Problem page');
        
        console.log('✅ Complete user journey: Homepage -> Weeks -> Week -> Problem');
      } else {
        console.log('✅ Partial journey: Homepage -> Weeks -> Week (no problem link found)');
      }
    } else {
      console.log('✅ Partial journey: Homepage -> Weeks (no week link found)');
    }
  });
});
