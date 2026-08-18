import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './specs',
  outputDir: './__output__',
  snapshotDir: './__baselines__',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: [
    ['list'],
    ['html', { outputFolder: '__output__/report', open: 'never' }],
  ],
  use: {
    baseURL: 'http://127.0.0.1:8765',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
  },
  webServer: {
    command: 'python -m http.server 8765 --bind 127.0.0.1 --directory ..',
    url: 'http://127.0.0.1:8765',
    reuseExistingServer: true,
    timeout: 10_000,
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'], viewport: { width: 1440, height: 900 } },
    },
  ],
});
