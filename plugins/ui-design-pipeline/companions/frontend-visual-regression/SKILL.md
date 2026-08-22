---
name: frontend-visual-regression
description: >
  Set up and run Playwright visual regression for any directory of HTML files — installs the
  tooling, scaffolds the harness, captures baselines, and diffs against them on later runs.
  Works on pipeline output, a standalone static site, or any directory with one index.html per
  subfolder. Triggers: "set up visual regression", "capture visual baselines", "regression
  check the frontend", "配置视觉回归", "给这些页面拍基线".
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# frontend-visual-regression

Standalone skill. Sets up Playwright visual regression on any frontend directory.

## What it does

1. Verifies Node + npm are on PATH.
2. Installs `@playwright/test` + Chromium browser into the target's `verify/` subdir (idempotent).
3. Scaffolds `playwright.config.ts`, `package.json`, a runner spec, and per-surface `verify.spec.json` files.
4. Captures visual baselines OR runs regression against existing baselines.

Generic — no coupling to anchor-prototype-wave or any specific generator.

## Inputs (ask once, never invent)

1. **Target dir**: directory containing surfaces. Convention: each surface is at `<target>/<slug>/index.html` (subfolder-per-surface) OR `<target>/<file>.html` (flat). Skill auto-detects.
2. **Mode**: `capture` (write fresh baselines) | `run` (check against existing) | `update` (overwrite baselines).
3. **Viewport** (optional, default `[1440, 900]`).
4. **Per-surface states** (optional): each surface can declare hover/scroll/click setup steps; default is single `default` state.

## Prerequisites

- Node 18+ on PATH.
- npm on PATH.
- If absent, stop and report which is missing.

## Workflow

### 1. Pre-flight checks
```bash
node --version    # expect ≥ v18
npm --version
```
If either fails → stop and report to user.

### 2. Bootstrap verify/ in target dir (idempotent)
```bash
cd <target>
mkdir -p verify/specs verify/__baselines__ verify/__output__
cd verify
[ ! -f package.json ] && cp ${CLAUDE_PLUGIN_ROOT}/companions/frontend-visual-regression/verify-template/package.json .
[ ! -f playwright.config.ts ] && cp ${CLAUDE_PLUGIN_ROOT}/companions/frontend-visual-regression/verify-template/playwright.config.ts .
[ ! -f specs/runner.spec.ts ] && cp ${CLAUDE_PLUGIN_ROOT}/companions/frontend-visual-regression/verify-template/specs/runner.spec.ts specs/
npm install
npx playwright install --with-deps chromium
```

The template files are bundled with this skill at `${CLAUDE_PLUGIN_ROOT}/companions/frontend-visual-regression/verify-template/`.

### 3. Write per-surface verify.spec.json
Discover surfaces under `<target>` via Glob: `**/index.html` (subfolder-per-surface) or `*.html` (flat). For each, if `<surface-dir>/verify.spec.json` doesn't exist, write:

```json
{
  "viewport": [1440, 900],
  "states": [
    {"name": "default", "setup": null}
  ]
}
```

If the user supplied per-surface states inputs, use those instead. The `setup` field can be a JS expression string to `eval` on the page before screenshot (e.g., to trigger hover or open a panel).

### 4. Run Playwright
**Mode `capture`** (first-time baselines):
```bash
cd <target>/verify
npx playwright test --update-snapshots
```
Baselines land in `<target>/verify/__baselines__/`.

**Mode `run`** (regression check):
```bash
cd <target>/verify
npx playwright test
```
Exit non-zero if any diff exceeds `maxDiffPixelRatio: 0.01`. Diffs land in `<target>/verify/__output__/`.

**Mode `update`** (refresh after intentional changes):
```bash
cd <target>/verify
npx playwright test --update-snapshots
```

### 5. Report
Single message:
- Mode used (capture/run/update).
- Number of surfaces tested.
- Number of regressions (mode `run`): one line per failed surface with diff magnitude.
- Path to HTML report: `<target>/verify/__output__/report/index.html` (if generated).
- Baseline count + dir.

## File layout produced

```
<target>/
└── verify/
    ├── package.json           ← scaffolded
    ├── playwright.config.ts   ← scaffolded
    ├── specs/
    │   └── runner.spec.ts     ← scaffolded
    ├── __baselines__/         ← canonical screenshots (kept under VCS)
    └── __output__/            ← diffs from `run` mode (gitignore)
```

Per surface (idempotent):
```
<target>/<slug>/
├── index.html
└── verify.spec.json           ← scaffolded if missing
```

Recommend adding `verify/__output__/` to `.gitignore`.

## Hard boundaries

- Do NOT modify the surface HTML files themselves.
- Install Playwright LOCAL to `<target>/verify/` only — never global.
- Default to Chromium only (`--with-deps chromium`). User adds Firefox/WebKit manually if needed.
- Don't silently skip a surface missing `index.html` — list it in the report.
- Don't auto-commit baselines — that's the user's decision.

## When to stop and ask

1. Node or npm missing → install instructions, then stop.
2. Target dir doesn't exist or has no HTML files.
3. Mode `run` but no baselines yet → ask if user meant `capture`.
4. Playwright install fails (network, permissions) → report the actual error.

## Pairs well with

- `anchor-prototype-wave` (run after wave completes to capture baselines).
- `frontend-audit-polish` (capture before polish, run after to confirm no unintended visual regressions).
- `anchor-prototype-wave-versions` (snapshots and visual baselines are orthogonal — versions preserve HTML, baselines preserve pixels; using both gives full history).

## Reference

The scaffolded infrastructure is fully described in §File layout produced above and bundled in this skill's `verify-template/` — no external example needed.
