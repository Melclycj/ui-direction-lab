---
name: anchor-prototype-wave-dark-mode
description: >
  Optional extension for anchor-prototype-wave. Adds light + dark mode to
  every surface via a 9-patch token-override, a small theme-toggle widget,
  and per-prototype localStorage persistence. Default theme is light; the
  validator's `dark-by-default` ban still applies. Trigger: include
  `dark-mode` in the parent wave's `extensions:` input.
allowed-tools: Read, Write, Edit, Grep, Glob
---

# anchor-prototype-wave-dark-mode

**Hook point**: woven into Stage 2 of `anchor-prototype-wave` (surface authoring). The parent passes this extension's rules to every surface subagent's prompt so dark-mode wiring is authored alongside the surface, not patched in afterwards.

## What it does

Every surface produced by the wave ships with:

1. A **theme-bootstrap script** in `<head>` that runs before stylesheet paint and prevents FOUC.
2. **Dual token blocks** — `:root { /* light tokens */ }` and `html[data-theme="dark"] { /* dark token overrides */ }` — covering at least the 9-patch set.
3. **A theme-toggle UI** wired to update `data-theme` on `<html>` and persist the choice per prototype.
4. **`<html lang="..." data-theme="light">`** as the default attribute on the root element.

The base skill's `dark-by-default` ban remains in force — surfaces default to light, users opt in.

## Inputs (passed from parent wave)

- `output_dir`: the wave's output directory.
- `wave_slug`: short slug used as the localStorage key prefix (e.g. `v2`, `2026-05-26-todo`). Each prototype keys its theme independently as `<wave-slug>-theme-<surface-slug>` so toggling one surface does not flip the others.

## The 9-patch token set

Both the `:root` block and the `html[data-theme="dark"]` block MUST define paired values for these tokens (token names identical, values shifted):

| Token | Role |
|---|---|
| `--page-bg` | outer page background |
| `--card-bg` | primary card / panel surface |
| `--sunken-bg` | inset / sunken surface (e.g. code blocks, secondary panels) |
| `--muted-bg` | hover / pressed / chip background |
| `--text-primary` | body text |
| `--text-secondary` | secondary / metadata text |
| `--text-tertiary` | tertiary / placeholder text |
| `--border-hairline` | hairline border value (rgba with the right alpha for each mode) |
| `--accent` | accent color (often unchanged across modes, but verify contrast) |

If the surface relies on additional semantic tokens (status colors, accent-fg, etc.), pair those too. The rule is: **every token used in light mode has a dark mode value, or it's left to inherit (rare and must be intentional)**.

## Required HTML/CSS/JS pattern

Canonical pattern: the inline snippets below (root attribute → FOUC-guard bootstrap → dual token blocks → toggle widget → wiring). Self-contained — no external file needed.

### 1. Root element

```html
<html lang="en" data-theme="light">
```

### 2. Bootstrap script (in `<head>`, before any stylesheet)

```html
<script>
  (function () {
    try {
      var saved = localStorage.getItem('<wave-slug>-theme-<surface-slug>');
      if (saved === 'dark' || saved === 'light') {
        document.documentElement.setAttribute('data-theme', saved);
      }
    } catch (_) {}
  })();
</script>
```

Runs synchronously before paint — no FOUC flash from light → dark on hard reload.

### 3. Dual token blocks (in the surface's `<style>`)

```css
:root {
  --page-bg: #fafaf9;
  --card-bg: #ffffff;
  --sunken-bg: #f5f5f4;
  --muted-bg: #e7e5e4;
  --text-primary: #0a0a0a;
  --text-secondary: #525252;
  --text-tertiary: #a3a3a3;
  --border-hairline: rgba(15, 23, 42, 0.08);
  --accent: #0f766e;
}

html[data-theme="dark"] {
  --page-bg: #0a0a0b;
  --card-bg: #15161a;
  --sunken-bg: #0f1014;
  --muted-bg: #1c1d22;
  --text-primary: #f5f5f4;
  --text-secondary: #a1a1aa;
  --text-tertiary: #71717a;
  --border-hairline: rgba(255, 255, 255, 0.08);
  --accent: #14b8a6;
}
```

Token names are identical; only values shift. Surface CSS never references raw colors — it references these tokens — so switching `data-theme` re-themes the whole page.

### 4. Toggle widget (placed in the chrome / header / footer)

```html
<div class="theme-toggle" role="group" aria-label="Theme (light / dark)">
  <button type="button" class="theme-choice" data-theme-value="light"
          aria-pressed="true" aria-label="Light theme" title="Light">☀</button>
  <button type="button" class="theme-choice" data-theme-value="dark"
          aria-pressed="false" aria-label="Dark theme" title="Dark">☾</button>
</div>
```

Both buttons MUST satisfy the universal Fitts 44px rule (wrap with padding or invisible hit-area). `aria-pressed` updates on selection, and both `aria-label` and the visible glyph reflect the choice.

### 5. Toggle wiring (in the surface's `<script>`)

```html
<script>
  (function setupThemeToggle() {
    var STORAGE_KEY = '<wave-slug>-theme-<surface-slug>';
    var buttons = document.querySelectorAll('.theme-choice');
    function reflect() {
      var current = document.documentElement.getAttribute('data-theme') || 'light';
      buttons.forEach(function (b) {
        b.setAttribute('aria-pressed', b.dataset.themeValue === current ? 'true' : 'false');
      });
    }
    reflect();
    buttons.forEach(function (b) {
      b.addEventListener('click', function () {
        var value = b.dataset.themeValue;
        document.documentElement.setAttribute('data-theme', value);
        try { localStorage.setItem(STORAGE_KEY, value); } catch (_) {}
        reflect();
      });
    });
  })();
</script>
```

## Workflow (parent-side, before spawning surface subagents)

1. Read this SKILL.md.
2. For each surface in Stage 2 subagent prompts, **append the four required pieces** above into the prompt as a section titled "Dark-mode wiring (required)". Inline the canonical snippets with the wave's actual token values substituted in.
3. Add a line to each subagent's success criteria: "Light + dark modes both render without missing tokens; the toggle persists across reload."
4. After Stage 6 (validator + scorer), spot-check by reading any surface's CSS and grep for `html[data-theme="dark"]` — every surface must match. If not, mark `FIX_NEEDED` with sub-cause `dark-mode-missing`.
5. After Stage 8, append to `<output_dir>/audits/manifest.json`:
   ```json
   {
     "extensions_applied": ["...existing...", "dark-mode"],
     "dark_mode": {
       "surfaces_themed": <N>,
       "storage_key_prefix": "<wave-slug>-theme-"
     }
   }
   ```

## Outputs

Per surface: an additional `html[data-theme="dark"] { … }` block in `<style>` + bootstrap script + toggle widget + wiring. No new files.

## Hard boundaries

- Default theme stays light. Surfaces that default to dark fail validation regardless of this extension.
- Token names MUST match between light and dark blocks. Asymmetric naming (e.g. `--card-bg` light + `--card-background` dark) is a defect.
- localStorage key is **per-surface, not per-wave**. Toggling one surface to dark must not affect siblings.
- The toggle MUST be keyboard-reachable and announce state via `aria-pressed`.

## When to stop and ask

1. Anchor lacks a defined dark palette and the user gave no instruction → ask for the dark-side 9-patch, or offer a contrast-shifted default and ask for sign-off.
2. Surface uses raw colors (not tokens) in places — you can't theme it without first refactoring to tokens. Stop and surface this to the user.

## Reference

The canonical pattern is the five inline snippets in §Required HTML/CSS/JS pattern above (root `data-theme` attribute → FOUC-guard bootstrap → dual `:root` / `html[data-theme="dark"]` token blocks → toggle widget → toggle wiring). They are self-contained — no external file or pattern-memory lookup needed.
