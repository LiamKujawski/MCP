import { test, expect } from '@playwright/test';

test.describe('Home Page', () => {
  test('should load and display welcome message', async ({ page }) => {
    await page.goto('/');
    
    // Check if the page title contains MCP
    await expect(page).toHaveTitle(/MCP/);
    
    // Check if welcome message is visible
    await expect(page.locator('h1')).toContainText('Welcome to MCP');
    
    // Check if navigation links are present - use more specific selectors
    await expect(page.getByRole('link', { name: /API.*Explore/ })).toBeVisible();
    await expect(page.getByRole('link', { name: /Docs.*Documentation/ })).toBeVisible();
    await expect(page.getByRole('link', { name: /GitHub.*View/ })).toBeVisible();
    await expect(page.getByRole('link', { name: /Experiments.*Research/ })).toBeVisible();
  });

  test('should have working navigation links', async ({ page }) => {
    await page.goto('/');
    
    // Check API link
    const apiLink = page.getByRole('link', { name: /API.*Explore/ });
    await expect(apiLink).toHaveAttribute('href', '/api');
    await expect(apiLink).toHaveAttribute('target', '_blank');
    
    // Check Docs link
    const docsLink = page.getByRole('link', { name: /Docs.*Documentation/ });
    await expect(docsLink).toHaveAttribute('href', 'http://localhost:9000');
    await expect(docsLink).toHaveAttribute('target', '_blank');
    
    // Check GitHub link
    const githubLink = page.getByRole('link', { name: /GitHub.*View/ });
    await expect(githubLink).toHaveAttribute('href', 'https://github.com/your-repo/mcp');
    await expect(githubLink).toHaveAttribute('target', '_blank');
  });

  test('should display feature cards', async ({ page }) => {
    await page.goto('/');
    
    // Check for main features
    await expect(page.locator('text=Multi-Agent Architecture')).toBeVisible();
    await expect(page.locator('text=Real-time Monitoring')).toBeVisible();
    await expect(page.locator('text=Scalable Infrastructure')).toBeVisible();
  });

  test('should have responsive design', async ({ page, viewport }) => {
    if (!viewport) return; // Skip if no viewport
    
    await page.goto('/');
    
    // Desktop view
    if (viewport.width >= 1024) {
      await expect(page.locator('.lg\\:flex')).toBeVisible();
    }
    
    // Check main content is always visible
    await expect(page.locator('main')).toBeVisible();
    await expect(page.locator('h1')).toBeVisible();
  });

  test('should have proper meta tags', async ({ page }) => {
    await page.goto('/');
    
    // Check viewport meta
    const viewport = await page.locator('meta[name="viewport"]').getAttribute('content');
    expect(viewport).toContain('width=device-width');
    
    // Check description meta
    const description = await page.locator('meta[name="description"]').getAttribute('content');
    expect(description).toBeTruthy();
  });
});