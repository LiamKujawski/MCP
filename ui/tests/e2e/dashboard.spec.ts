import { test, expect } from '@playwright/test';

test.describe('Dashboard Page', () => {
  test('should load dashboard', async ({ page }) => {
    await page.goto('/dashboard');
    
    // Wait for the page to be fully loaded
    await page.waitForLoadState('networkidle');
    
    // Check if the dashboard loads
    await expect(page.locator('h1')).toContainText('MCP Control Center');
    
    // Check if tabs are present
    await expect(page.getByRole('tab', { name: /Overview/i })).toBeVisible();
    await expect(page.getByRole('tab', { name: /Research/i })).toBeVisible();
  });

  test('should show workflow status', async ({ page }) => {
    await page.goto('/dashboard');
    await page.waitForLoadState('networkidle');
    
    // Check if workflow status section is present
    await expect(page.locator('text=/Current Workflow/i')).toBeVisible();
  });
});
