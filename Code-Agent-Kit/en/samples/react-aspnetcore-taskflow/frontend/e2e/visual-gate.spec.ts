import { expect, test } from '@playwright/test';

const targetURL = process.env.PLAYWRIGHT_TARGET_URL ?? '/';

const mockTasks = [
  {
    id: '11111111-1111-1111-1111-111111111111',
    title: 'Create public workflow sample',
    description: 'Prepare the first stack-neutral sample repository.',
    assignee: 'Taeksu',
    status: 'InProgress',
    createdAt: '2026-07-12T00:00:00Z',
    updatedAt: '2026-07-13T00:00:00Z',
  },
  {
    id: '22222222-2222-2222-2222-222222222222',
    title: 'Review deterministic gates',
    description: 'Verify build, API, UI, and color validation evidence.',
    assignee: 'Reviewer',
    status: 'ReadyForApproval',
    createdAt: '2026-07-12T08:00:00Z',
    updatedAt: '2026-07-13T01:00:00Z',
  },
];

async function mockTaskApi(page: import('@playwright/test').Page) {
  await page.route('**/api/tasks', async (route) => {
    if (route.request().method() === 'GET') {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(mockTasks),
      });
      return;
    }

    await route.fulfill({
      status: 405,
      contentType: 'application/json',
      body: JSON.stringify({ title: 'Method not allowed in UI gate.' }),
    });
  });
}


test('matches the approved desktop visual baseline', async ({ page }) => {
  await mockTaskApi(page);
  await page.goto(targetURL);
  await page.getByRole('heading', { name: 'TaskFlow' }).waitFor();

  await expect(page).toHaveScreenshot('taskflow-desktop.png', {
    animations: 'disabled',
    fullPage: true,
    mask: [page.locator('.task-footer > span')],
    maxDiffPixelRatio: 0.01,
  });
});

test('matches the approved narrow visual baseline', async ({ page }) => {
  await page.setViewportSize({ width: 390, height: 844 });
  await mockTaskApi(page);
  await page.goto(targetURL);
  await page.getByRole('heading', { name: 'TaskFlow' }).waitFor();

  await expect(page).toHaveScreenshot('taskflow-narrow.png', {
    animations: 'disabled',
    fullPage: true,
    mask: [page.locator('.task-footer > span')],
    maxDiffPixelRatio: 0.01,
  });
});