import { defineConfig, devices } from '@playwright/test';

const executablePath = process.env.PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH;
const baseURL = process.env.PLAYWRIGHT_BASE_URL ?? 'http://127.0.0.1:5173';
const targetURL = process.env.PLAYWRIGHT_TARGET_URL;
const fileMode = Boolean(targetURL?.startsWith('file:'));

export default defineConfig({
  testDir: './e2e',
  fullyParallel: false,
  reporter: [['list'], ['html', { open: 'never', outputFolder: 'playwright-color-report' }]],
  outputDir: 'test-results/color',
  use: {
    baseURL,
    trace: 'retain-on-failure',
  },
  snapshotPathTemplate:
    '{testDir}/{testFilePath}-snapshots/{arg}-{projectName}-linux{ext}',
  projects: [
    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome'],
        launchOptions: executablePath
          ? { executablePath, args: ['--no-sandbox', '--disable-dev-shm-usage', '--allow-file-access-from-files'] }
          : undefined,
      },
    },
  ],
  webServer: fileMode
    ? undefined
    : {
        command: 'npm run dev -- --host 0.0.0.0',
        url: baseURL,
        reuseExistingServer: true,
        timeout: 120_000,
      },
});
