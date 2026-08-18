---
name: anchor-prototype-wave-versions
description: >
  Optional extension for anchor-prototype-wave. Snapshots each surface to
  <slug>/versions/<date>-<label>/, injects a version-switcher widget into
  each surface so users can toggle between current and frozen snapshots,
  and adds row-level update badges to the master gallery for surfaces
  that gained a new version this wave. Trigger: include `versions` in
  the parent wave's `extensions:` input.
allowed-tools: Read, Write, Edit, Bash, Glob
---

# anchor-prototype-wave-versions

**Hook point**: after Stage 8 of `anchor-prototype-wave` (master gallery + manifest written).

## What it does

1. Snapshot every surface into a dated `versions/` subfolder per surface.
2. Inject a version-switcher widget into each surface so a user can flip between current and frozen versions in-browser.
3. Inject update badges into the master gallery tiles.

## Inputs (passed from parent wave)

- `output_dir`: the wave's output directory.
- `wave_date`: e.g. `2026-05-25`.
- `label` (optional, default = `wave-slug` from `manifest.json`): suffix appended to the version folder name.

## Workflow

### 1. Snapshot each surface
For each `<output_dir>/<slug>/index.html` (excluding `elements/` — those are handled by `anchor-prototype-wave-elements`):

```bash
mkdir -p <output_dir>/<slug>/versions/<wave_date>-<label>
cp <output_dir>/<slug>/index.html <output_dir>/<slug>/versions/<wave_date>-<label>/index.html
```

Skip surfaces where the current `index.html` is byte-identical to the most-recent prior snapshot (idempotent fast-path).

### 2. Enumerate prior versions
For each surface, list `versions/*/` to build the version index that the switcher widget will reference.

### 3. Record per-version reason + inject the switcher as a sticky TOP BAR

**3a. Maintain `<output_dir>/<slug>/versions/versions.json`** — one entry per version, newest first, each
carrying the **reason it exists / what changed**. Version control is a *changelog*, not just snapshots:
the reason is mandatory, supplied from whatever produced the version (a §6 retry instruction, a
polish-round closeout, the user's edit note).

```json
{
  "versions": [
    { "label": "fixed", "date": "2026-06-28", "current": true,
      "href": "./index.html", "verdict": "PASS", "score": "9.10",
      "reason": "§6 fix-loop: oversized outlined editorial numerals — lifted innovation 7→8" },
    { "label": "2026-06-28-pre-fix", "short": "pre-fix", "date": "2026-06-28", "current": false,
      "href": "versions/2026-06-28-pre-fix/index.html", "verdict": "FIX", "score": "8.80",
      "reason": "initial wave output — under the old flat bar" }
  ]
}
```

**3b. Inject a full-width sticky TOP BAR** at the start of `<body>` in the live `<slug>/index.html` —
**not** a floating dropdown. The switcher must be a visible selector where every item shows
`label · date · verdict/score · the change reason`; current is marked active; clicking a prior version
navigates to its snapshot. Idempotent — replace `.vbar` if present. Adapt colors to the surface's
chassis tokens (fall back via CSS custom-property defaults). Pattern:

```html
<nav class="vbar" aria-label="Page versions">
  <span class="vbar__lbl">VERSIONS</span>
  <a class="vitem is-current" href="./index.html" aria-current="true">
    <b>fixed</b><span class="vmeta">2026-06-28 · PASS 9.10</span>
    <span class="vreason">§6 fix-loop: editorial outlined numerals (innovation 7→8)</span>
  </a>
  <a class="vitem" href="versions/2026-06-28-pre-fix/index.html">
    <b>pre-fix</b><span class="vmeta">2026-06-28 · FIX 8.80</span>
    <span class="vreason">initial wave output — under the old flat bar</span>
  </a>
  <!-- one <a> per version, newest first; build from versions.json -->
</nav>
<style>
  .vbar{position:sticky;top:0;z-index:1000;display:flex;align-items:stretch;overflow-x:auto;
        background:var(--c-surface,#1e2016);border-bottom:2px solid var(--c-border,#f1efe2);
        font-family:var(--font-mono,ui-monospace,monospace);font-size:11px;}
  .vbar__lbl{display:flex;align-items:center;padding:0 12px;color:var(--c-accent,#bfe800);
             letter-spacing:.12em;border-right:1px solid var(--c-border,#f1efe2);white-space:nowrap;}
  .vitem{display:flex;flex-direction:column;justify-content:center;gap:2px;padding:8px 14px;
         min-width:240px;text-decoration:none;color:var(--c-ink-2,#b7b5a4);
         border-right:1px solid rgba(241,239,226,.18);}
  .vitem:hover{background:rgba(241,239,226,.06);color:var(--c-ink,#f1efe2);}
  .vitem.is-current{background:var(--c-bg,#14150f);color:var(--c-ink,#f1efe2);}
  .vitem .vmeta{color:var(--c-accent,#bfe800);}
  .vitem .vreason{color:var(--c-ink-3,#82806f);white-space:normal;line-height:1.3;}
</style>
```

**3c. Bidirectional — the bar goes on EVERY version, not just the live page.** Inject the same `.vbar`
into each prior snapshot too, with hrefs recomputed relative to *that* snapshot's location
(`current` → `../../index.html`, a sibling version → `../<label>/index.html`, itself → `./index.html`)
and the viewed version marked `.is-current`. This gives **older ↔ newer** switching from any version.
Do NOT use a one-way "back to current" strip — it can't move forward.

### 4. Inject update badges in master gallery
For each surface that gained a new version this wave (all surfaces in the manifest), add a `data-updated="<wave_date>"` attribute to its tile in `<output_dir>/index.html`. Append CSS rule:

```css
[data-updated]::after {
  content: "updated " attr(data-updated);
  display: inline-block;
  margin-left: 8px;
  font-size: 10px;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: var(--status-active, #15803d);
  padding: 2px 6px;
  border-radius: 999px;
  background: var(--status-active-bg, rgba(21,128,61,0.07));
}
```

### 5. Update manifest
Append to `<output_dir>/audits/manifest.json`:

```json
{
  "extensions_applied": ["...existing...", "versions"],
  "versions_snapshot": {
    "wave_date": "<wave_date>",
    "label": "<label>",
    "surfaces_snapshotted": <N>
  }
}
```

## Outputs

Per surface:
- `<output_dir>/<slug>/versions/<wave_date>-<label>/index.html` — frozen snapshot (+ a "back to current" strip).
- `<output_dir>/<slug>/versions/versions.json` — version list with a **change reason** per version.

Modified files:
- `<output_dir>/<slug>/index.html` — sticky **TOP-BAR** version switcher injected (idempotent).
- `<output_dir>/index.html` — update badges added to tiles.
- `<output_dir>/audits/manifest.json` — extension recorded.

## Hard boundaries

- Modify nothing outside `<output_dir>/`.
- Append-only on `versions/` — never delete prior snapshots.
- Idempotent on the widget injection — check for existing `.vsw` first.
- Skip the no-op snapshot if current matches most-recent prior.

## When to stop and ask

1. `<output_dir>` is not a wave output (no `audits/manifest.json`).
2. Snapshot collision: `<wave_date>-<label>` already exists with different content → ask user for a new label.

## Reference — expected snapshot structure

`<output_dir>/<slug>/versions/<wave_date>-<label>/index.html`, one dated folder per wave (e.g. `2026-05-15-polish`, `2026-05-19-pre-usability`).
