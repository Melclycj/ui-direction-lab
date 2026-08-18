---
name: anchor-prototype-wave-elements
description: >
  Optional extension for anchor-prototype-wave. Authors atom foundation
  pages (buttons, surface-card-drawer, forms, nav-structural) that
  consume the same anchor chassis as the wave's product surfaces. Useful
  for validating the chassis is internally consistent across atom-level
  and surface-level usage. Trigger: include `elements` in the parent
  wave's `extensions:` input.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# anchor-prototype-wave-elements

**Hook point**: Stage 2b of `anchor-prototype-wave` (parallel to product-surface authoring).

## What it does

Authors a small set of **atom foundation pages** that exhaustively demonstrate every element type the chassis supports. Element pages run through the same validator + grader + scorer as product surfaces, but their content brief is "show all variants of this element type using the locked chassis tokens" rather than "build a working product surface."

## Inputs (from parent wave)

- `output_dir`: wave output directory.
- `anchor`: locked chassis spec (for the subagent's prompt).
- `categories` (optional, default = all four below): which atom pages to author.

## Default categories

| Slug | Title | Content brief |
|---|---|---|
| `elements/01-atoms-buttons` | Atoms · Buttons | All button variants: primary / secondary / ghost / destructive × size sm/md/lg × state default/hover/active/disabled/loading. Plus icon buttons, button groups, toggle buttons. |
| `elements/02-surface-card-drawer` | Surface · Cards & Drawers | All card variants: hero card, list card, stat card, empty-state card. Plus drawer (right-side, bottom), modal, popover. |
| `elements/03-forms` | Forms | Inputs (text/email/number/select/textarea/checkbox/radio/toggle/date), helper text, error states, label patterns, button groups, form layouts (stacked, inline). |
| `elements/04-nav-structural` | Nav · Structural | Top nav, side nav, breadcrumb, tabs, pagination, footer. |

## Workflow

### 1. Write contracts for element pages
Same shape as product surfaces, but `claimed_surface_type` is always `audit-view` (a static display page) and `surface_innovation_target` is `mature`:

```json
{
  "surface_slug": "elements/01-atoms-buttons",
  "claimed_surface_type": "audit-view",
  "surface_innovation_target": "mature",
  "production_source": null,
  "research_only_reason": "atom-level foundation page; no product surface to mirror",
  "intent": "Demonstrate all button variants using the locked chassis tokens",
  "must_have": ["primary/secondary/ghost/destructive", "sm/md/lg sizes", "default/hover/active/disabled/loading states", "icon buttons", "button groups"],
  "must_not_have": ["product navigation", "real task data", "scaffold leak patterns"]
}
```

Write contracts to `<output_dir>/audits/contracts/elements__<slug>.contract.json` (double-underscore replaces the slash so filenames stay flat).

### 2. Spawn element subagents in parallel
One sonnet subagent per category. Each subagent's prompt includes:
- The anchor doc (same as product subagents).
- The contract (above).
- The "demonstrate exhaustively" brief: a labeled grid of every variant × size × state with section headers.
- **Hard write-scope**: ONLY `<output_dir>/elements/<slug>.html` (flat file convention to match v2's `elements/01-atoms-buttons.html` pattern).
- Dark mode requirement from base skill §Authoring still applies.

### 3. Validate + grade + score
Same Stage 3/4/5 pipeline as product surfaces. Element pages with the `audit-view` morphology have a permissive validator (no overlay/drawer/canvas requirements), but maturity-aware floor still applies and scaffold-leak checks remain.

### 4. Update manifest
Append element pages to `<output_dir>/audits/manifest.json` under a separate `elements:` key (parallel to `surfaces:`):

```json
{
  "elements": [
    {"slug": "elements/01-atoms-buttons", "verdict": "PASS_9PLUS", "score": 9.15},
    ...
  ]
}
```

### 5. Master gallery integration
The wave's gallery (Stage 8) should add an "Elements" section listing the atom pages alongside the product surfaces. If the gallery has already been written by Stage 8 before this extension runs, patch the gallery to add the Elements section.

## Outputs

For each enabled category:
- `<output_dir>/elements/<slug>.html` — atom foundation page.
- `<output_dir>/audits/<slug>.audit.json` — same audit format as product surfaces.
- `<output_dir>/audits/contracts/elements__<slug>.contract.json` — contract.

## Hard boundaries

- Element pages MUST use the same anchor tokens — no chassis drift.
- Element pages MUST NOT contain real product navigation or real task data — they are a token/component demo, not a product surface.
- If anchor tokens lack a value an element page needs (e.g., button shadow), record this as a chassis gap in `audits/cross-cutting.md` (base skill writes this), not a silent invention in the element page.

## When to stop and ask

1. `<output_dir>` is not a wave output (no `audits/contracts/` dir).
2. A category fails to PASS after 3 retries — same ESCALATE_HUMAN path as product surfaces (don't auto-promote).

## Reference — expected output structure

One flat file per category under `<output_dir>/elements/`: `01-atoms-buttons.html`, `02-surface-card-drawer.html`, `03-forms.html`, `04-nav-structural.html` (plus `versions/` subdirs if the `versions` extension also runs).
