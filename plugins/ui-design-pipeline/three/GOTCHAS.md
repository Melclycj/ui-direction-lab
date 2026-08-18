# three/ — Gotchas & verification discipline (cross-cutting)

> Cross-cutting traps and verification lessons for **any** three.js / canvas / single-file WebGL
> demo in this lab — vendored `threejs-*` skills, `threejs-scroll-stage`, or ad-hoc demos alike.
> Split out of `threejs-scroll-stage` (2026-07-09) so that skill stays focused on *how to build a
> scroll-driven 3D stage*; this file holds the "traps you hit writing any three+GSAP+GLSL demo"
> and "how to verify 3D work" concerns that are not specific to any one pattern.
>
> Read this before authoring a non-trivial single-file three.js demo, and before setting up a
> verification loop for one. Pattern-specific anti-patterns (particle stage, scroll bridge,
> parallax, cleanup, reduced-motion, token derive, shard object) live in
> [`threejs-scroll-stage`](threejs-scroll-stage/SKILL.md) `## Anti-patterns`.

## Authoring gotchas (three + GSAP + GLSL, single-file demos)

Each row is provenance-tagged to the wave-2 rebuild batch demo that surfaced it
(`testbed/material/*` + `testbed/runs/2026-07-08-rebuild-wave2/`).

| ❌ | Why it's wrong / the fix |
|---|---|
| Expecting a 3D Y-rotation flip (card / page turn) under a **perspective** camera to keep its center line fixed | The half swinging toward the camera is magnified by perspective, so the page appears to drift sideways even though the pivot IS on the center line. To keep the center line visually fixed: remove the depth swing (horizontal squash `scaleX = cos(π·t)`, Z unchanged) or rotate AND counter-translate to cancel the projected drift (wave-2 C-05, user-diagnosed) |
| `gsap.killTweensOf(target)` to stop a **staggered** tween | GSAP 3.13's `killTweensOf` does NOT kill a stagger tween (multi-target + stagger) — it keeps running, so enter/exit animations coexist and fight the same property (visible flicker once durations are long enough to see). Keep a persistent handle and `.kill()` it by reference (wave-2 C-22, minimal repro confirmed). Also noted from `animation/README`. |
| A backtick inside a GLSL **comment** in a template-literal shader string | The backtick closes the JS template literal early → the rest of the GLSL leaks into JS context → `SyntaxError`, whole module dead (blank canvas). Line-by-line shader review misses it: the GLSL is correct, the bug lives at the JS/GLSL embedding seam. Use plain quotes in shader comments (wave-2 C-05 fatal; `node --check` on the extracted module catches it) |
| Mutating a `ShaderPass`/`EffectComposer` pass's uniforms via the object you passed to its constructor | `ShaderPass` clones the uniforms at construction (`UniformsUtils.cloneUniforms`); your live setter then mutates a dead copy = silent no-op, no error thrown. Mutate `pass.uniforms.*` instead. Screenshots can't catch it — verify with `gl.readPixels` (wave-2 C-10) |
| `img.decode()` as a boot gate | data-URL images can hang `decode()` indefinitely in headless Chromium → boot never completes. Don't gate init on decode; let layout come from CSS `aspect-ratio` (wave-2 C-07) |
| Equal resting Z on overlapping `transparent: true` planes | three sorts transparent objects by depth; on a depth **tie** the draw order is arbitrary, so a neighbor can paint over the one meant to be on top. Give the top layer an explicit small Z nudge from frame one (wave-2 C-18) |
| Deriving a "which item is centered/active" index from an in-flight eased `progress` with a bare `floor()` | Float round-trip + GSAP tween end-truncation land `progress` a hair below the integer target → `floor()` returns index−1 → intermittent off-by-one (drifted highlight, incomplete zoom coverage). Add an epsilon (`floor(raw + 1e-4)`), snap the tween's end value exactly, and derive identity from the clicked object — never re-derive from `progress` (wave-2 C-18) |

## Verification discipline (from the wave-2 consumption batch, 2026-07-08)

- **Headless can't judge motion feel.** Headless Chromium defaults to `prefers-reduced-motion: reduce`, which zeroes animation durations → the effect completes instantly and you can never screenshot a mid-animation frame. Headless verification proves API correctness, cleanup (leak-flat `renderer.info`), and structural perf — NOT whether motion looks or feels right. "Does it look good / is it smooth / is the pivot right" is a **human, real-time** judgment; don't spend rounds trying to verify it headlessly (wave-2 C-05 burned 5+ rounds before this was named — the loop, not any single fix, was the problem).
- **Prefer minimal targeted verification; only script long when it's actually justified.** Before writing a big verification harness, ask whether a few spot-checks would settle the question — they usually do. If a long run genuinely IS warranted (e.g. an N-case coverage matrix), chunk it into short separate invocations (fresh browser per chunk, foreground with an explicit timeout ≤~240 s), wrap every step in a hard per-check timeout (`Promise.race`), and print progress per check — a monolithic long script silently hangs when the page crashes and swallows the error (wave-2 C-18 hung ~30 min this way).
- **The MCP browser is a single-point resource under fan-out.** Concurrent verifying agents contend for the one shared MCP browser; have each spawn its own isolated headless Chromium (`playwright-core` + the locally cached binary) instead. A zombie Chromium can hold the profile lock after an agent dies — kill the PID tree to recover.
