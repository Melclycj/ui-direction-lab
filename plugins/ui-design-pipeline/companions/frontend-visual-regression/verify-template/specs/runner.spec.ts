import { test, expect } from '@playwright/test';
import { readFileSync } from 'node:fs';
import { join } from 'node:path';
import { globSync } from 'glob';

// Discover all surfaces (each has its own verify.spec.json sitting next to its index.html).
// Convention: subfolder-per-surface (<slug>/index.html + <slug>/verify.spec.json)
// or flat (<file>.html + <file>.verify.spec.json — not yet supported).
const targetRoot = '..';
const surfaceSpecs = globSync('**/verify.spec.json', { cwd: targetRoot, ignore: ['verify/**', 'node_modules/**'] });

for (const rawSpecPath of surfaceSpecs) {
  // Windows globSync returns backslash-separated paths; normalize to forward slashes
  // so URL paths + snapshot names work cross-platform.
  const specPath = rawSpecPath.replace(/\\/g, '/');
  const slug = specPath.replace('/verify.spec.json', '');
  let spec: { viewport?: [number, number]; states?: { name: string; setup: string | null }[] };
  try {
    spec = JSON.parse(readFileSync(join(targetRoot, specPath), 'utf-8'));
  } catch (e) {
    test(`${slug} :: parse-error`, () => {
      throw new Error(`Cannot parse ${specPath}: ${(e as Error).message}`);
    });
    continue;
  }

  const viewport = spec.viewport ?? [1440, 900];
  const states = spec.states ?? [{ name: 'default', setup: null }];

  for (const state of states) {
    test(`${slug} :: ${state.name}`, async ({ page }) => {
      await page.setViewportSize({ width: viewport[0], height: viewport[1] });
      await page.goto(`/${slug}/index.html`);
      await page.waitForLoadState('networkidle');
      if (state.setup) {
        // state.setup is a string of JS to evaluate in the page context
        await page.evaluate(state.setup);
        await page.waitForTimeout(100);
      }
      const snapshotName = `${slug.replace(/\//g, '-')}-${state.name}.png`;
      await expect(page).toHaveScreenshot(snapshotName, {
        fullPage: true,
        maxDiffPixelRatio: 0.01,
      });
    });
  }
}
