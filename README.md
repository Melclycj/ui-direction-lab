# UI Skills Lab

**A design pipeline that turns one line of product intent into a locked design system and a full set of production-grade pages** — built as Claude Code skills, with a deterministic gate and a named human decision at every step.

The premise: taste is not automatable, but everything around it is. Machines check that the code is correct, that it obeys the locked design chassis, and that nothing drifted since it was last verified. *Which direction is good* stays a human call — at nine explicit decision points, not implicitly buried in a prompt.

![Vernata home — WebGL skyline hero, built by this pipeline](docs/media/vernata-home.png)

---

## What has been built with it

### Vernata — marketing site for an AI delivery studio

Three pages produced end-to-end by the pipeline: a home page with a WebGL systems gallery, a delivered-work page, and a booking page wired to a Cloudflare Pages Function and a transactional email backend. Design tokens are a single locked chassis shared across all three.

Production-ready; awaiting a domain. Repo: `Melclycj/landing_page` (private).

![Vernata delivered-work page](docs/media/vernata-work.png)

Same pipeline, a deliberately different register from the hero above: a warm editorial archive instead of a dark WebGL stage. Neither look is a template — each direction was picked from generated variants, then frozen into a chassis every page inherits.

### Averonel — enterprise AI integration, marketing register

A complete marketing site built as the pipeline's end-to-end evaluation run: information architecture round 1 → visual direction exploration → chassis lock → motion architecture → surface wave, with the evaluation findings recorded against each stage rather than asserted.

![Averonel variant review gallery](docs/media/averonel-variants.png)

**This is the review surface, and it is where the method lives.** The top bar switches between the five generated directions — `Anchor`, `Ledger`, `Control`, `Journal`, `Civic Control` — so they are judged against each other rather than in isolation. The bottom bar carries each variant's rationale and palette as data, not prose: *cream paper / Fraunces serif / single warm coral / centered hero / motion: null*. You pick one. That choice becomes the chassis, and every page produced afterwards is validated against it.

### The material library — 55 verified front-end modules

Scroll-driven WebGL scenes, shader transitions, physics slideshows, layout-FLIP choreography, pointer-reactive grids. Each one is a single applyable module plus a demo that consumes that same module — **never a second implementation** — with a machine-checked receipt proving the shipped code is byte-identical to what was verified.

Seven of them are in production use on the Vernata site.

| | |
|---|---|
| ![Shard vessel — 84 shards, one draw call](docs/media/piece-shard-vessel.png) | ![Real-time dither shader](docs/media/piece-dithered-vessel.png) |
| ![Perlin landscape](docs/media/piece-perlin-landscape.png) | ![Letter bulge shader](docs/media/piece-letter-bulge-shader.png) |
| ![Cloth physics slideshow](docs/media/piece-cloth-slideshow.png) | ![SVG mask blinds transition](docs/media/piece-svg-mask-blinds.png) |

*Six of fifty-five. Every frame above was captured by running the module's own demo — the same file a consuming page imports.*

---

## How the pipeline works

```
[one-line idea]
     ▼
  intent Q&A ──► ● do you have a reference, or is this exploration?
     ▼
  batch 1: 3-4 visual directions  ──► ● pick the LEAD
     ▼
  contrast gate (WCAG, computed) ──► ● fix, or accept knowingly (debt is recorded)
     ▼
  batch 2: 2-3 motion stances (visual frozen) ──► ● pick one
     ▼
  LOCK the chassis  ──► ● explicit approval required; a hook hard-blocks the next step without it
     ▼
  surface wave: N pages in parallel, each validated and scored ──► ● accept the gallery
```

● = a human decides. Everything else runs unattended.

**One axis per batch.** Visuals change, then freeze; then motion changes. This is deliberate — it is what stops the review turning into a combinatorial mess where you cannot tell which change you are reacting to.

An optional information-architecture companion wraps the pipeline at both ends: it settles *what information is on each screen and what dominates* before any visual work, and after the chassis locks it generalises the approved composition to the remaining screens.

---

## What actually makes it work: the verification layer

Most of the engineering here is not in generating pages. It is in making sure the generated thing is what it claims to be.

| Mechanism | What it stops |
|---|---|
| **Hash receipts on every module** | Verify a module, then quietly edit it — the static gate turns red on the next run. Proven by test: add one newline, gate fails; revert, gate passes. |
| **A hook on the lock→wave transition** | The model may *propose* skipping a step. It cannot *act* on that until the user answers with an explicit approval word. Instruction alone was measured to be insufficient, so this became deterministic code. |
| **Two-way verbatim assertions** | When a mechanism is extracted from a demo into a reusable module, the load-bearing constants, shaders and timings must survive character-for-character. Upstream quirks are preserved on purpose — they are the regression baseline. |
| **`companion_skipped`, never silent** | When an optional companion skill is unavailable, the run records that it was skipped. It never proceeds as though the stage ran in full. |
| **Scoped absence, said out loud** | Scripts that need the lab-only material corpus detect its absence and report `SKIPPED (lab-only check)` rather than passing quietly. |

**129 automated checks**: 97 pipeline assertions, 16 wave test functions, 16 information-architecture fixtures. All green from a clean install with none of the lab's own data present.

### Honest boundaries

Stated up front, because a tool that overstates itself is worse than one that does less:

- **Whether it looks good is always a human call.** Scorers guarantee "written correctly, obeys the chassis" — nothing more.
- **A validator cannot see inside a `<canvas>`.** WebGL surfaces are machine-checked for console errors, leaks and API misuse; how they *feel* must be watched with human eyes.
- **Variants are review prototypes, not production code.** Cross-page links are mocked and labelled as such.
- One run serves one register. A marketing site and an app console are two runs and two chassis.

---

## Install

```
/plugin marketplace add Melclycj/ui-direction-lab
/plugin install ui-design-pipeline@ui-direction-lab
```

21 skills, 1.4 MB, ~3.2k tokens of always-on context. Requires Python ≥ 3.9 — standard library only, no pip packages.

Then say *"give me a few UI directions"*. You need one line describing the product; the pipeline asks for the rest in order.

Third-party skills this pipeline calls — GreenSock's GSAP set, Anthropic's `frontend-design`, and four others — are **nominated rather than redistributed**: each call site names how to install it from its own source, and what degrades if you don't. Details in [`plugins/ui-design-pipeline/README.md`](plugins/ui-design-pipeline/README.md).

---

## Repository map

| Path | What it is |
|---|---|
| `plugins/ui-design-pipeline/` | The distributable plugin — 21 skills, the approval hook, its own README |
| ├ `core/` | The two engines: direction exploration, then chassis-locked production |
| ├ `companions/` | Information architecture, an anti-slop taste red-team, a ~165-system design-system catalog, audit and visual-regression companions |
| ├ `extensions/` | Opt-in add-ons to the production wave: dark mode, atom pages, version snapshots |
| └ `three/` | 11 Three.js / WebGL skills (10 vendored MIT + 1 original) |
| `docs/media/` | The screenshots above — captured by running each thing, not mocked up |

Only `plugins/` is installed. The showcase assets sit outside it on purpose: a plugin
install copies the whole plugin directory and ignores `.gitignore`, so 1.8MB of
screenshots would otherwise land on every installer's disk.

### Where this comes from

This repository is the published face of a working lab that stays private. The lab holds
what a published package should not: the 55-piece material corpus with its demos and
verification receipts, third-party skills kept for local use and deliberately not
redistributed, and a work ledger that quotes its author and names clients.

That split is also why the pipeline you install has no material library attached — the
scripts that would read it detect its absence and say so out loud rather than passing
quietly. Everything here is generated from the lab by a one-way sync; nothing is edited
here directly.

---

## Status

Actively developed. The pipeline and the material library are in daily use; the plugin packaging landed in August 2026. The two sites above are complete and awaiting deployment.

Licensed MIT — see [`LICENSE`](LICENSE). Third-party provenance is recorded per piece; vendored groups carry their upstream terms verbatim rather than a restated summary.
