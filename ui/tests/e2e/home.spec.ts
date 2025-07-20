import { test, expect } from '@playwright/test';

test.describe('Home Page', () => {
  test('should load and display welcome message', async ({ page }) => {
    await page.goto('/');
    
    // Check if the page title contains MCP
    await expect(page).toHaveTitle(/MCP/);
    
    // Check if welcome message is visible
    await expect(page.locator('h1')).toContainText('Welcome to MCP');
    
    // Check if navigation links are present
    await expect(page.locator('text=API')).toBeVisible();
    await expect(page.locator('text=Docs')).toBeVisible();
    await expect(page.locator('text=GitHub')).toBeVisible();
    await expect(page.locator('text=Experiments')).toBeVisible();
  });

  test('should have working navigation links', async ({ page }) => {
    await page.goto('/');
    
    // Check API link
    const apiLink = page.locator('a[href="/api"]');
    await expect(apiLink).toBeVisible();
    
    // Check Docs link
    const docsLink = page.locator('a[href="/docs"]');
    await expect(docsLink).toBeVisible();
    
    // Check GitHub link opens in new tab
    const githubLink = page.locator('a[href="https://github.com/LiamKujawski/MCP"]');
    await expect(githubLink).toHaveAttribute('target', '_blank');
    await expect(githubLink).toHaveAttribute('rel', 'noopener noreferrer');
  });
});