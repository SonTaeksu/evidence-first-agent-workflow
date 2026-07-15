import { expect, test } from '@playwright/test';

test('creates a task and moves it to in progress', async ({ page }) => {
  await page.goto('/');

  await expect(page.getByRole('heading', { name: 'TaskFlow' })).toBeVisible();

  const title = `E2E task ${Date.now()}`;

  await page.getByLabel('Title').fill(title);
  await page
    .getByLabel('Description')
    .fill('Created by the deterministic Playwright check.');
  await page.getByLabel('Assignee').fill('Playwright');
  await page.getByRole('button', { name: 'Create task' }).click();

  const card = page.locator('article').filter({ hasText: title });
  await expect(card).toBeVisible();
  await card.getByRole('button', { name: 'Start' }).click();
  await expect(card.getByText('In progress')).toBeVisible();
});

test('does not introduce horizontal page scrolling on a narrow viewport', async ({
  page,
}) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await page.goto('/');

  const dimensions = await page.evaluate(() => ({
    scrollWidth: document.documentElement.scrollWidth,
    clientWidth: document.documentElement.clientWidth,
  }));

  expect(dimensions.scrollWidth).toBeLessThanOrEqual(
    dimensions.clientWidth,
  );
});
