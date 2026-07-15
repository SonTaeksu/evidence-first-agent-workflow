import { mkdir, writeFile } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import AxeBuilder from '@axe-core/playwright';
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


interface ColorEvidence {
  selector: string;
  text: string;
  color: string;
  backgroundColor: string;
  borderColor: string;
  fontSize: string;
  fontWeight: string;
}

test('visible text passes the deterministic color-contrast gate', async ({
  page,
}, testInfo) => {
  await mockTaskApi(page);
  await page.goto(targetURL);
  await page.getByRole('heading', { name: 'TaskFlow' }).waitFor();

  const results = await new AxeBuilder({ page })
    .withRules(['color-contrast'])
    .analyze();

  await testInfo.attach('axe-color-contrast.json', {
    body: Buffer.from(JSON.stringify(results, null, 2)),
    contentType: 'application/json',
  });

  const summary = results.violations.map((violation) => ({
    id: violation.id,
    impact: violation.impact,
    help: violation.help,
    nodes: violation.nodes.map((node) => ({
      target: node.target,
      html: node.html,
      failureSummary: node.failureSummary,
    })),
  }));

  expect(summary, JSON.stringify(summary, null, 2)).toEqual([]);
});

test('exports computed color evidence for smaller models', async ({
  page,
}, testInfo) => {
  await mockTaskApi(page);
  await page.goto(targetURL);
  await page.getByRole('heading', { name: 'TaskFlow' }).waitFor();

  const evidence = await page.evaluate<ColorEvidence[]>(() => {
    const visible = (element: Element): element is HTMLElement => {
      if (!(element instanceof HTMLElement)) {
        return false;
      }

      const style = getComputedStyle(element);
      const rect = element.getBoundingClientRect();
      return (
        style.display !== 'none' &&
        style.visibility !== 'hidden' &&
        Number(style.opacity) > 0 &&
        rect.width > 0 &&
        rect.height > 0
      );
    };

    const selectorFor = (element: HTMLElement): string => {
      if (element.id) {
        return `#${CSS.escape(element.id)}`;
      }

      const className = [...element.classList]
        .map((name) => `.${CSS.escape(name)}`)
        .join('');

      return `${element.tagName.toLowerCase()}${className}`;
    };

    return [...document.querySelectorAll('body *')]
      .filter(visible)
      .filter((element) => Boolean(element.textContent?.trim()))
      .map((element) => {
        const style = getComputedStyle(element);
        return {
          selector: selectorFor(element),
          text: element.textContent?.trim().replace(/\s+/g, ' ').slice(0, 120) ?? '',
          color: style.color,
          backgroundColor: style.backgroundColor,
          borderColor: style.borderColor,
          fontSize: style.fontSize,
          fontWeight: style.fontWeight,
        };
      })
      .filter(
        (item, index, array) =>
          array.findIndex(
            (candidate) =>
              candidate.selector === item.selector &&
              candidate.color === item.color &&
              candidate.backgroundColor === item.backgroundColor &&
              candidate.borderColor === item.borderColor,
          ) === index,
      );
  });

  const payload = {
    schema: 'evidence-first/computed-color-evidence/v1',
    generatedAt: new Date().toISOString(),
    pageUrl: page.url(),
    items: evidence,
  };

  const serialized = JSON.stringify(payload, null, 2);

  await testInfo.attach('computed-color-evidence.json', {
    body: Buffer.from(serialized),
    contentType: 'application/json',
  });

  const outputPath = resolve(
    process.env.COLOR_EVIDENCE_OUTPUT ??
      '../docs/evidence/generated/computed-color-evidence.json',
  );
  await mkdir(dirname(outputPath), { recursive: true });
  await writeFile(outputPath, `${serialized}\n`, 'utf8');

  expect(evidence.length).toBeGreaterThan(0);
  expect(evidence.some((item) => item.color !== 'rgba(0, 0, 0, 0)')).toBe(
    true,
  );
});