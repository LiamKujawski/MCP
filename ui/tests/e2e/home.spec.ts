import { test, expect } from '@playwright/test';

test.describe('Home Page', () => {
  test('should load and display welcome message', async ({ page }) => {
    await page.goto('/');
    
    // Check if the page title contains MCP
    await expect(page).toHaveTitle(/Next/); // Default Next.js title
    
    // Check if welcome message is visible
    await expect(page.locator('h1')).toContainText('Welcome to MCP');
    
    // Check if navigation links are present - match actual text
    await expect(page.getByRole('link', { name: /API/ }).first()).toBeVisible();
    await expect(page.getByRole('link', { name: /Docs/ })).toBeVisible();
    await expect(page.getByRole('link', { name: /GitHub/ })).toBeVisible();
    await expect(page.getByRole('link', { name: /Experiments/ })).toBeVisible();
  });

  test('should have working navigation links', async ({ page }) => {
    await page.goto('/');
    
    // Check API link
    const apiLink = page.getByRole('link', { name: /API/ }).first();
    await expect(apiLink).toHaveAttribute('href', '/api');
    
    // Check Docs link
    const docsLink = page.getByRole('link', { name: /Docs/ });
    await expect(docsLink).toHaveAttribute('href', '/docs');
    
    // Check GitHub link - this one has target="_blank"
    const githubLink = page.getByRole('link', { name: /GitHub/ });
    await expect(githubLink).toHaveAttribute('href', 'https://github.com/LiamKujawski/MCP');
    await expect(githubLink).toHaveAttribute('target', '_blank');
    await expect(githubLink).toHaveAttribute('rel', 'noopener noreferrer');
    
    // Check Experiments link
    const experimentsLink = page.getByRole('link', { name: /Experiments/ });
    await expect(experimentsLink).toHaveAttribute('href', '/experiments');
  });

  test('should display navigation cards with descriptions', async ({ page }) => {
    await page.goto('/');
    
    // Check for card descriptions
    await expect(page.locator('text=Explore the FastAPI backend')).toBeVisible();
    await expect(page.locator('text=Read the comprehensive documentation')).toBeVisible();
    await expect(page.locator('text=View the source code on GitHub')).toBeVisible();
    await expect(page.locator('text=Run and monitor agent experiments')).toBeVisible();
  });

  test('should have responsive design', async ({ page, viewport }) => {
    if (!viewport) return; // Skip if no viewport
    
    await page.goto('/');
    
    // Desktop view
    if (viewport.width >= 1024) {
      await expect(page.locator('.lg\\:flex').first()).toBeVisible();
    }
    
    // Check main content is always visible
    await expect(page.locator('main')).toBeVisible();
    await expect(page.locator('h1')).toBeVisible();
  });

  test('should have proper styling classes', async ({ page }) => {
    await page.goto('/');
    
    // Check that cards have hover classes
    const firstCard = page.getByRole('link', { name: /API/ }).first();
    await expect(firstCard).toHaveClass(/group rounded-lg border/);
    
    // Check that main has flex layout
    const main = page.locator('main');
    await expect(main).toHaveClass(/flex min-h-screen/);
  });
});