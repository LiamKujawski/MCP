import { test, expect } from '@playwright/test';

test('homepage has title', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveTitle(/MCP/);
});

test('dashboard link is visible', async ({ page }) => {
  await page.goto('/');
  const dashboardLink = page.getByRole('link', { name: /control center/i });
  await expect(dashboardLink).toBeVisible();
});
