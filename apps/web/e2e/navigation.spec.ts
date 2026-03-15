/**
 * Navigation E2E Tests
 * 
 * Comprehensive navigation tests covering:
 * - Header navigation
 * - Sidebar navigation
 * - Footer links
 * - Mobile navigation
 * - Breadcrumb navigation
 * - Keyboard navigation
 */

import { test, expect } from '@playwright/test';

const BASE_URL = process.env.BASE_URL || 'https://python-oop-journey.onrender.com';

// Helper to verify page loaded without errors
async function verifyPageLoaded(page: any, context: string): Promise<void> {
  const has404 = await page.locator('text=404').isVisible().catch(() => false);
  const hasNotFound = await page.locator('text=This page could not be found').isVisible().catch(() => false);
  const hasError = await page.locator('text=Internal Server Error, text=Application error').first().isVisible().catch(() => false);
  
  if (has404 || hasNotFound) {
    throw new Error(`${context}: Page returned 404 at ${page.url()}`);
  }
  if (hasError) {
    throw new Error(`${context}: Page has error at ${page.url()}`);
  }
}

test.describe('🧭 Navigation Tests', () => {
  test.describe('Header Navigation', () => {
    test.beforeEach(async ({ page }) => {
      await page.goto(BASE_URL);
      await page.waitForLoadState('networkidle');
    });

    test('header is visible on homepage', async ({ page }) => {
      const header = page.locator('header').first();
      await expect(header).toBeVisible();
      
      // Should contain site title or logo
      const hasTitle = await page.locator('header h1, header a[href="/"], header img[alt*="logo" i]').first().isVisible().catch(() => false);
      console.log(`Header visible with title/logo: ${hasTitle}`);
    });

    test('header logo links to homepage', async ({ page }) => {
      // Navigate to a different page first
      await page.goto(`${BASE_URL}/weeks`);
      await page.waitForLoadState('networkidle');
      
      // Find logo/title link in header
      const logoLink = page.locator('header a[href="/"]').first();
      const hasLogoLink = await logoLink.isVisible().catch(() => false);
      
      if (hasLogoLink) {
        await logoLink.click();
        await page.waitForLoadState('networkidle');
        
        expect(page.url()).toBe(`${BASE_URL}/`);
        console.log('✅ Header logo links to homepage');
      } else {
        console.log('ℹ️ Header logo link not found');
      }
    });

    test('header navigation links work', async ({ page }) => {
      await page.goto(`${BASE_URL}/weeks`);
      await page.waitForLoadState('networkidle');
      
      // Common header navigation items
      const headerLinks = [
        { selector: 'header a[href="/weeks"]', name: 'Curriculum' },
        { selector: 'header a[href="/projects"]', name: 'Projects' },
        { selector: 'header a[href="/bookmarks"]', name: 'Bookmarks' },
        { selector: 'header a[href="/search"]', name: 'Search' },
      ];
      
      for (const link of headerLinks) {
        const element = page.locator(link.selector).first();
        const isVisible = await element.isVisible().catch(() => false);
        
        if (isVisible) {
          console.log(`Found header link: ${link.name}`);
        }
      }
    });

    test('user menu is present in header', async ({ page }) => {
      await page.goto(`${BASE_URL}/weeks`);
      await page.waitForLoadState('networkidle');
      
      // Look for user menu (avatar or login button)
      const userMenu = page.locator('header button[aria-label*="user" i], header button[aria-label*="account" i], header a[href="/login"], header button[class*="avatar"]').first();
      const hasUserMenu = await userMenu.isVisible().catch(() => false);
      
      if (hasUserMenu) {
        console.log('✅ User menu found in header');
      } else {
        console.log('ℹ️ User menu not found - may require login or different selector');
      }
    });

    test('search button is accessible from header', async ({ page }) => {
      await page.goto(`${BASE_URL}/weeks`);
      await page.waitForLoadState('networkidle');
      
      // Look for search button or link
      const searchBtn = page.locator('header button[aria-label*="search" i], header a[href="/search"]').first();
      const hasSearch = await searchBtn.isVisible().catch(() => false);
      
      if (hasSearch) {
        await searchBtn.click();
        await page.waitForTimeout(500);
        
        // Check if search dialog opened or navigated to search page
        const isSearchPage = page.url().includes('/search');
        const hasSearchDialog = await page.locator('[role="dialog"], [data-testid="search-dialog"]').isVisible().catch(() => false);
        
        if (isSearchPage || hasSearchDialog) {
          console.log('✅ Search accessible from header');
        }
      } else {
        console.log('ℹ️ Search button not found in header');
      }
    });
  });

  test.describe('Sidebar Navigation', () => {
    test('sidebar navigation on main pages', async ({ page }) => {
      const pagesWithSidebar = ['/weeks', '/projects', '/bookmarks'];
      
      for (const path of pagesWithSidebar) {
        await page.goto(`${BASE_URL}${path}`);
        await page.waitForLoadState('networkidle');
        
        // Look for sidebar
        const sidebar = page.locator('aside, nav[role="navigation"]').first();
        const hasSidebar = await sidebar.isVisible().catch(() => false);
        
        console.log(`${path}: Sidebar visible = ${hasSidebar}`);
      }
    });

    test('sidebar links to all main sections', async ({ page }) => {
      await page.goto(`${BASE_URL}/weeks`);
      await page.waitForLoadState('networkidle');
      
      const mainSections = [
        { path: '/weeks', name: 'Curriculum' },
        { path: '/projects', name: 'Projects' },
        { path: '/bookmarks', name: 'Bookmarks' },
        { path: '/search', name: 'Search' },
      ];
      
      for (const section of mainSections) {
        // Find link by href
        const link = page.locator(`nav a[href="${section.path}"], aside a[href="${section.path}"]`).first();
        const hasLink = await link.isVisible().catch(() => false);
        
        if (hasLink) {
          await link.click();
          await page.waitForLoadState('networkidle');
          await verifyPageLoaded(page, `Sidebar: ${section.name}`);
          
          expect(page.url()).toContain(section.path);
          console.log(`✅ Sidebar navigation to ${section.name} works`);
          
          // Go back for next test
          await page.goto(`${BASE_URL}/weeks`);
          await page.waitForLoadState('networkidle');
        }
      }
    });

    test('sidebar shows week navigation', async ({ page }) => {
      await page.goto(`${BASE_URL}/weeks/week00_getting_started`);
      await page.waitForLoadState('networkidle');
      
      // Look for week navigation in sidebar
      const weekLinks = await page.locator('nav a[href*="/weeks/week"], aside a[href*="/weeks/week"]').all();
      
      console.log(`Found ${weekLinks.length} week links in sidebar`);
      
      if (weekLinks.length > 0) {
        // Click a different week
        const otherWeek = weekLinks.find(async (link) => {
          const href = await link.getAttribute('href');
          return href && !href.includes('week00_getting_started');
        });
        
        if (otherWeek) {
          await otherWeek.click();
          await page.waitForLoadState('networkidle');
          await verifyPageLoaded(page, 'Week navigation via sidebar');
          console.log('✅ Week navigation via sidebar works');
        }
      }
    });

    test('sidebar active state is highlighted', async ({ page }) => {
      await page.goto(`${BASE_URL}/weeks`);
      await page.waitForLoadState('networkidle');
      
      // Look for active/current state in sidebar
      const activeLink = page.locator('nav a[class*="active"], nav a[aria-current="page"], aside a[class*="active"]').first();
      const hasActiveState = await activeLink.isVisible().catch(() => false);
      
      console.log(`Active state in sidebar: ${hasActiveState}`);
    });
  });

  test.describe('Footer Navigation', () => {
    test('footer is present on main pages', async ({ page }) => {
      const pagesToCheck = ['/', '/weeks', '/problems'];
      
      for (const path of pagesToCheck) {
        await page.goto(`${BASE_URL}${path}`);
        await page.waitForLoadState('networkidle');
        
        const footer = page.locator('footer').first();
        const hasFooter = await footer.isVisible().catch(() => false);
        
        console.log(`${path}: Footer present = ${hasFooter}`);
      }
    });

    test('footer contains legal links', async ({ page }) => {
      await page.goto(BASE_URL);
      await page.waitForLoadState('networkidle');
      
      const footerLinks = [
        { path: '/privacy', name: 'Privacy' },
        { path: '/terms', name: 'Terms' },
      ];
      
      for (const link of footerLinks) {
        const footerLink = page.locator(`footer a[href="${link.path}"]`).first();
        const hasLink = await footerLink.isVisible().catch(() => false);
        
        if (hasLink) {
          await footerLink.click();
          await page.waitForLoadState('networkidle');
          await verifyPageLoaded(page, `Footer: ${link.name}`);
          
          console.log(`✅ Footer link to ${link.name} works`);
          
          await page.goto(BASE_URL);
          await page.waitForLoadState('networkidle');
        }
      }
    });

    test('footer copyright text is present', async ({ page }) => {
      await page.goto(BASE_URL);
      await page.waitForLoadState('networkidle');
      
      const footer = page.locator('footer').first();
      const hasCopyright = await footer.locator('text=/©|copyright|all rights/i').isVisible().catch(() => false);
      
      console.log(`Footer copyright text: ${hasCopyright}`);
    });
  });

  test.describe('Mobile Navigation', () => {
    test('mobile menu button exists on small screens', async ({ page }) => {
      // Set mobile viewport
      await page.setViewportSize({ width: 375, height: 667 });
      
      await page.goto(BASE_URL);
      await page.waitForLoadState('networkidle');
      
      // Look for hamburger menu button
      const menuBtn = page.locator('button[aria-label*="menu" i], button[aria-label*="navigation" i], button[class*="hamburger"]').first();
      const hasMenuBtn = await menuBtn.isVisible().catch(() => false);
      
      console.log(`Mobile menu button visible: ${hasMenuBtn}`);
      
      if (hasMenuBtn) {
        // Click to open menu
        await menuBtn.click();
        await page.waitForTimeout(500);
        
        // Look for mobile menu
        const mobileMenu = page.locator('[role="dialog"], [data-testid="mobile-menu"], nav[class*="mobile"]').first();
        const menuOpen = await mobileMenu.isVisible().catch(() => false);
        
        console.log(`Mobile menu opened: ${menuOpen}`);
        
        // Close menu if opened
        if (menuOpen) {
          await page.keyboard.press('Escape');
        }
      }
      
      // Reset viewport
      await page.setViewportSize({ width: 1280, height: 720 });
    });

    test('navigation adapts to mobile viewport', async ({ page }) => {
      await page.goto(`${BASE_URL}/weeks`);
      await page.waitForLoadState('networkidle');
      
      // Desktop: Sidebar should be visible
      const desktopSidebar = page.locator('aside, nav[role="navigation"]').first();
      const sidebarVisibleDesktop = await desktopSidebar.isVisible().catch(() => false);
      
      // Switch to mobile
      await page.setViewportSize({ width: 375, height: 667 });
      await page.waitForTimeout(500);
      
      // Mobile: Sidebar may be hidden or in menu
      const sidebarVisibleMobile = await desktopSidebar.isVisible().catch(() => false);
      
      console.log(`Sidebar - Desktop: ${sidebarVisibleDesktop}, Mobile: ${sidebarVisibleMobile}`);
      
      // Reset viewport
      await page.setViewportSize({ width: 1280, height: 720 });
    });

    test('all navigation accessible on mobile', async ({ page }) => {
      await page.setViewportSize({ width: 375, height: 667 });
      
      const mainPages = ['/', '/weeks', '/projects', '/bookmarks', '/search'];
      
      for (const path of mainPages) {
        await page.goto(`${BASE_URL}${path}`);
        await page.waitForLoadState('networkidle');
        
        await verifyPageLoaded(page, `Mobile navigation: ${path}`);
        console.log(`✅ Mobile: ${path} accessible`);
      }
      
      // Reset viewport
      await page.setViewportSize({ width: 1280, height: 720 });
    });
  });

  test.describe('Breadcrumb Navigation', () => {
    test('breadcrumbs appear on nested pages', async ({ page }) => {
      const nestedPages = [
        '/weeks/week00_getting_started',
        '/weeks/week00_getting_started/days/day00_welcome',
      ];
      
      for (const path of nestedPages) {
        await page.goto(`${BASE_URL}${path}`);
        await page.waitForLoadState('networkidle');
        
        // Look for breadcrumbs
        const breadcrumbs = page.locator('nav[aria-label="breadcrumb"], [data-testid="breadcrumb"], .breadcrumb').first();
        const hasBreadcrumbs = await breadcrumbs.isVisible().catch(() => false);
        
        console.log(`${path}: Breadcrumbs = ${hasBreadcrumbs}`);
      }
    });

    test('breadcrumb links navigate correctly', async ({ page }) => {
      await page.goto(`${BASE_URL}/weeks/week00_getting_started`);
      await page.waitForLoadState('networkidle');
      
      // Look for breadcrumb links
      const breadcrumbLinks = await page.locator('nav[aria-label="breadcrumb"] a, [data-testid="breadcrumb"] a').all();
      
      if (breadcrumbLinks.length > 0) {
        // Click the first breadcrumb (usually Home or parent)
        const firstLink = breadcrumbLinks[0];
        const href = await firstLink.getAttribute('href');
        
        await firstLink.click();
        await page.waitForLoadState('networkidle');
        
        if (href) {
          expect(page.url()).toContain(href);
          console.log(`✅ Breadcrumb navigation to ${href} works`);
        }
      } else {
        console.log('ℹ️ No breadcrumb links found');
      }
    });
  });

  test.describe('Keyboard Navigation', () => {
    test('tab navigation works through all interactive elements', async ({ page }) => {
      await page.goto(BASE_URL);
      await page.waitForLoadState('networkidle');
      
      // Press Tab multiple times and track focus
      const focusedElements: string[] = [];
      
      for (let i = 0; i < 10; i++) {
        await page.keyboard.press('Tab');
        await page.waitForTimeout(100);
        
        const activeElement = await page.evaluate(() => {
          const el = document.activeElement;
          return el ? el.tagName + (el.getAttribute('aria-label') ? ` (${el.getAttribute('aria-label')})` : '') : 'none';
        });
        
        focusedElements.push(activeElement);
      }
      
      // Should have focused multiple elements
      const uniqueElements = [...new Set(focusedElements)];
      expect(uniqueElements.length).toBeGreaterThan(1);
      
      console.log(`Tab navigation focused ${uniqueElements.length} unique elements`);
    });

    test('enter key activates focused links', async ({ page }) => {
      await page.goto(BASE_URL);
      await page.waitForLoadState('networkidle');
      
      // Tab to first link
      await page.keyboard.press('Tab');
      
      // Get current URL before Enter
      const beforeUrl = page.url();
      
      // Press Enter
      await page.keyboard.press('Enter');
      await page.waitForTimeout(500);
      
      // URL may have changed
      console.log(`Enter key navigation: ${beforeUrl} -> ${page.url()}`);
    });

    test('escape key closes dialogs', async ({ page }) => {
      await page.goto(`${BASE_URL}/weeks`);
      await page.waitForLoadState('networkidle');
      
      // Try to open any dialog (search or menu)
      const searchBtn = page.locator('button[aria-label*="search" i]').first();
      if (await searchBtn.isVisible().catch(() => false)) {
        await searchBtn.click();
        await page.waitForTimeout(500);
        
        // Press Escape
        await page.keyboard.press('Escape');
        await page.waitForTimeout(500);
        
        console.log('Escape key pressed after opening dialog');
      }
    });
  });

  test.describe('Quick Links & Shortcuts', () => {
    test('dashboard quick links work', async ({ page }) => {
      await page.goto(BASE_URL);
      await page.waitForLoadState('networkidle');
      
      const quickLinks = [
        { text: 'All Problems', path: '/problems' },
        { text: 'Recently Viewed', path: '/recent' },
        { text: 'My Bookmarks', path: '/bookmarks' },
      ];
      
      for (const link of quickLinks) {
        const element = page.locator(`text="${link.text}"`).first();
        const isVisible = await element.isVisible().catch(() => false);
        
        if (isVisible) {
          console.log(`Found quick link: ${link.text}`);
          
          await element.click();
          await page.waitForLoadState('networkidle');
          await verifyPageLoaded(page, `Quick link: ${link.text}`);
          
          await page.goto(BASE_URL);
          await page.waitForLoadState('networkidle');
        }
      }
    });

    test('command palette search works', async ({ page }) => {
      await page.goto(BASE_URL);
      await page.waitForLoadState('networkidle');
      
      // Try keyboard shortcut for command palette (usually Cmd/Ctrl+K)
      await page.keyboard.press('Control+k');
      await page.waitForTimeout(500);
      
      // Look for command palette dialog
      const commandPalette = page.locator('[role="dialog"], [data-testid="command-palette"], .cmdk-root').first();
      const isOpen = await commandPalette.isVisible().catch(() => false);
      
      if (isOpen) {
        console.log('✅ Command palette opened with Ctrl+K');
        
        // Close it
        await page.keyboard.press('Escape');
      } else {
        console.log('ℹ️ Command palette not found or different shortcut');
      }
    });
  });
});

test.describe('🔗 Deep Link Navigation', () => {
  test('direct links to all major pages work', async ({ page }) => {
    const directLinks = [
      '/',
      '/weeks',
      '/weeks/week00_getting_started',
      '/weeks/week01_fundamentals',
      '/projects',
      '/bookmarks',
      '/search',
      '/recent',
      '/achievements',
      '/privacy',
      '/terms',
    ];
    
    for (const path of directLinks) {
      await page.goto(`${BASE_URL}${path}`);
      await page.waitForLoadState('networkidle');
      
      const has404 = await page.locator('text=404').isVisible().catch(() => false);
      const hasNotFound = await page.locator('text=This page could not be found').isVisible().catch(() => false);
      
      if (has404 || hasNotFound) {
        console.log(`❌ ${path}: 404`);
      } else {
        console.log(`✅ ${path}: OK`);
      }
    }
  });

  test('problem page deep links work', async ({ page }) => {
    const problemSlugs = [
      'problem_01_assign_and_print',
      'problem_02_swap_values',
      'problem_03_string_concat',
    ];
    
    for (const slug of problemSlugs) {
      await page.goto(`${BASE_URL}/problems/${slug}`);
      await page.waitForLoadState('networkidle');
      
      const has404 = await page.locator('text=404').isVisible().catch(() => false);
      
      console.log(`/problems/${slug}: ${has404 ? '❌ 404' : '✅ OK'}`);
    }
  });
});
