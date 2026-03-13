/**
 * Integration Test: Project Flow
 * 
 * This test verifies the complete project workflow:
 * 1. Navigate to Week 1
 * 2. Start project
 * 3. Create new file
 * 4. Edit file
 * 5. Run project
 * 6. Run tests
 * 7. Submit project
 * 8. Verify status updated
 * 
 * Note: This is a test specification. Implement with your preferred testing framework (Playwright, Cypress, etc.)
 */

import { test, expect } from '@playwright/test'; // or your testing framework

test.describe('Project Flow Integration Test', () => {
  test.beforeEach(async ({ page }) => {
    // Clear localStorage to start fresh
    await page.goto('/');
    await page.evaluate(() => localStorage.clear());
  });

  test('complete project workflow', async ({ page }) => {
    // Step 1: Navigate to Week 1
    await test.step('Navigate to Week 1', async () => {
      await page.goto('/weeks');
      await page.waitForSelector('text=Week 1');
      
      // Click on Week 1
      await page.click('text=Week 1');
      await page.waitForURL('**/weeks/week*');
      
      // Verify we're on a week page
      await expect(page.locator('h1')).toContainText('Week');
      
      // Verify Weekly Project section exists
      await expect(page.locator('text=Weekly Project')).toBeVisible();
    });

    // Step 2: Start project
    await test.step('Start project', async () => {
      // Click Start Project button
      await page.click('text=Start Project');
      
      // Verify we're on the project page
      await page.waitForURL('**/weeks/**/project');
      
      // Verify project editor loads
      await expect(page.locator('[data-tour="editor"]')).toBeVisible();
      
      // Verify file tree is present
      await expect(page.locator('[data-tour="file-tree"]')).toBeVisible();
      
      // Verify tour modal appears (first time)
      await expect(page.locator('text=Welcome to Project Mode!')).toBeVisible();
      
      // Close tour
      await page.click('text=Get Started');
    });

    // Step 3: Create new file
    await test.step('Create new file', async () => {
      // Click new file button in file tree
      await page.click('[title="New File"]');
      
      // Type filename
      await page.fill('input[placeholder="filename.py"]', 'test_module.py');
      await page.press('input[placeholder="filename.py"]', 'Enter');
      
      // Verify file appears in tree
      await expect(page.locator('text=test_module.py')).toBeVisible();
      
      // Verify tab opens
      await expect(page.locator('text=test_module.py').first()).toBeVisible();
    });

    // Step 4: Edit file
    await test.step('Edit file', async () => {
      // Wait for editor to be ready
      await page.waitForSelector('.monaco-editor');
      
      // Type code into editor
      // Note: Monaco editor interaction may require specific handling
      await page.click('.monaco-editor');
      await page.keyboard.type(`def hello_world():
    return "Hello, World!"
`);
      
      // Verify modified indicator appears
      await expect(page.locator('text=test_module.py •')).toBeVisible();
    });

    // Step 5: Save file
    await test.step('Save file', async () => {
      // Press Ctrl+S
      await page.keyboard.press('Control+s');
      
      // Wait for save to complete
      await page.waitForTimeout(500);
      
      // Verify modified indicator is gone
      await expect(page.locator('text=test_module.py •')).not.toBeVisible();
    });

    // Step 6: Run project
    await test.step('Run project', async () => {
      // Click Run button or use keyboard shortcut
      await page.click('text=Run');
      
      // Wait for output
      await page.waitForSelector('text=Running...', { timeout: 5000 });
      
      // Verify output panel shows results
      await expect(page.locator('text=Process completed')).toBeVisible({ timeout: 10000 });
    });

    // Step 7: Run tests
    await test.step('Run tests', async () => {
      // Click on Tests tab
      await page.click('text=Tests');
      
      // Run tests with keyboard shortcut
      await page.keyboard.press('Control+t');
      
      // Wait for test results
      await page.waitForSelector('text=Running tests...', { timeout: 5000 });
      
      // Verify test output
      await expect(page.locator('text=test session')).toBeVisible({ timeout: 10000 });
    });

    // Step 8: Submit project
    await test.step('Submit project', async () => {
      // Click Submit button
      await page.click('text=Submit');
      
      // Verify success state
      await expect(page.locator('text=Submitted')).toBeVisible();
    });

    // Step 9: Verify status updated
    await test.step('Verify status updated', async () => {
      // Navigate back to week page
      await page.click('text=Back to Week');
      
      // Verify project shows as submitted
      await expect(page.locator('text=Submitted')).toBeVisible();
      
      // Navigate to projects page
      await page.goto('/projects');
      
      // Verify project appears in completed tab
      await page.click('text=Completed');
      await expect(page.locator('text=CLI Calculator')).toBeVisible();
    });
  });

  test('keyboard shortcuts work correctly', async ({ page }) => {
    await page.goto('/weeks/week-01-foundations/project');
    
    // Test Ctrl+? opens shortcuts dialog
    await page.keyboard.press('?');
    await expect(page.locator('text=Keyboard Shortcuts')).toBeVisible();
    
    // Close dialog
    await page.keyboard.press('Escape');
    
    // Test Ctrl+B toggles file tree
    await page.keyboard.press('Control+b');
    // File tree visibility would change
    
    // Test file creation and save
    await page.click('[title="New File"]');
    await page.fill('input[placeholder="filename.py"]', 'shortcut_test.py');
    await page.press('input[placeholder="filename.py"]', 'Enter');
    
    // Edit and save with Ctrl+S
    await page.click('.monaco-editor');
    await page.keyboard.type('# Test content');
    await page.keyboard.press('Control+s');
    
    // Verify save indicator removed
    await expect(page.locator('text=shortcut_test.py •')).not.toBeVisible();
  });

  test('file tree navigation with keyboard', async ({ page }) => {
    await page.goto('/weeks/week-01-foundations/project');
    
    // Focus file tree
    await page.click('[data-tour="file-tree"]');
    
    // Test arrow key navigation
    await page.keyboard.press('ArrowDown');
    await page.keyboard.press('ArrowRight');
    await page.keyboard.press('Enter');
    
    // Verify file opened
    await expect(page.locator('[data-tour="editor"]')).toBeVisible();
  });

  test('error handling displays gracefully', async ({ page }) => {
    // Block execution API to simulate error
    await page.route('**/api/execute', route => route.abort());
    
    await page.goto('/weeks/week-01-foundations/project');
    
    // Try to run code
    await page.click('text=Run');
    
    // Verify error state is handled
    await expect(page.locator('text=Failed to execute')).toBeVisible({ timeout: 10000 });
  });

  test('tour can be skipped and completed', async ({ page }) => {
    await page.goto('/weeks/week-01-foundations/project');
    
    // Verify tour appears
    await expect(page.locator('text=Welcome to Project Mode!')).toBeVisible();
    
    // Click Next to go through tour
    await page.click('text=Next');
    await expect(page.locator('text=File Explorer')).toBeVisible();
    
    // Continue through tour
    await page.click('text=Next');
    await expect(page.locator('text=Code Editor')).toBeVisible();
    
    // Skip tour
    await page.click('[aria-label="Close"]');
    
    // Verify tour closed
    await expect(page.locator('text=Welcome to Project Mode!')).not.toBeVisible();
    
    // Refresh page - tour should not appear again (stored in localStorage)
    await page.reload();
    await expect(page.locator('text=Welcome to Project Mode!')).not.toBeVisible();
  });

  test('mobile responsive layout', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });
    
    await page.goto('/weeks/week-01-foundations/project');
    
    // Verify mobile menu button exists
    await expect(page.locator('[aria-label="Toggle menu"]')).toBeVisible();
    
    // Verify file tree is hidden by default or accessible via menu
    // Layout should adapt to smaller screen
    
    // Test navigation still works
    await page.click('text=Week 1');
    await page.waitForURL('**/weeks/**');
  });
});

/**
 * Test Data Requirements:
 * 
 * 1. Test user account (optional for localStorage-based tests)
 * 2. Week 1 project data available
 * 3. API endpoints mocked or available:
 *    - GET /api/execute
 *    - GET /api/verify
 * 
 * Environment Setup:
 * 
 * ```bash
 * # Install dependencies
 * npm install -D @playwright/test
 * 
 * # Install browsers
 * npx playwright install
 * 
 * # Run tests
 * npx playwright test
 * ```
 */

/**
 * Expected Test Results:
 * 
 * ✓ Navigate to Week 1 - Page loads with project section
 * ✓ Start project - Redirects to project page, tour shows
 * ✓ Create new file - File appears in tree and as tab
 * ✓ Edit file - Content changes, modified indicator shows
 * ✓ Save file - Modified indicator removed, data persisted
 * ✓ Run project - Output shows in panel
 * ✓ Run tests - Test results display
 * ✓ Submit project - Status updates to submitted
 * ✓ Verify status - Week page and projects list show correct status
 * ✓ Keyboard shortcuts - All shortcuts work as expected
 * ✓ Error handling - Errors display gracefully
 * ✓ Tour flow - Can navigate and skip tour
 * ✓ Mobile layout - Responsive on small screens
 */
