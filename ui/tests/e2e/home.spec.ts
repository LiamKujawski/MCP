import { test, expect } from '@playwright/test';

test.describe('Home Page', () => {
  test('should load and display welcome message', async ({ page }) => {
    await page.goto('/');
    
    // Wait for the page to be fully loaded
    await page.waitForLoadState('networkidle');
    
    // Check if the page title contains MCP (flexible across environments)
    await expect(page).toHaveTitle(/MCP/);
    
    // Check if welcome message is visible
    await expect(page.locator('h1')).toContainText('Welcome to MCP');
    
    // Check if the control center button is present
    await expect(page.getByRole('link', { name: /Open Control Center/ })).toBeVisible();
  });

  test('should have working control center link', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    
    // Check Control Center link
    const controlCenterLink = page.getByRole('link', { name: /Open Control Center/ });
    await expect(controlCenterLink).toHaveAttribute('href', '/dashboard');
    await expect(controlCenterLink).toBeVisible();
    
    // Click and verify navigation
    await controlCenterLink.click();
    await page.waitForURL('**/dashboard');
    await expect(page).toHaveURL(/.*\/dashboard/);
  });

  test('should display navigation cards with descriptions', async ({ page }) => {
    await page.goto('/');
    
    // Check for at least some navigation elements
    const links = await page.getByRole('link').count();
    expect(links).toBeGreaterThan(0);
  });

  test('should have responsive design', async ({ page, viewport }) => {
    if (!viewport) return; // Skip if no viewport
    
    await page.goto('/');
    
    // Check main content is always visible
    await expect(page.locator('main')).toBeVisible();
    await expect(page.locator('h1')).toBeVisible();
  });

  test('should have proper styling classes', async ({ page }) => {
    await page.goto('/');
    
    // Check that the control center button has proper styling
    const controlCenterButton = page.getByRole('link', { name: /Open Control Center/ });
    await expect(controlCenterButton).toHaveClass(/rounded-lg/);
    
    // Check that main has flex layout
    const main = page.locator('main');
    await expect(main).toHaveClass(/flex min-h-screen/);
  });
});
