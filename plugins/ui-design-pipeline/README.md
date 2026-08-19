# ui-design-pipeline

A create pipeline for UI work, as Claude Code skills: **one-line idea → N direction
prototypes → you pick → locked design chassis → parallel hi-fi surface wave**, with
deterministic validators and an explicit human approval gate at every lock.

It is built around one opinion: **taste is not automatable, but everything around it is.**
Scripts check that the code is correct and obeys the locked chassis; *which direction is
good* stays your call, at named decision points.

## Install

```
/plugin marketplace add Melclycj/ui-direction-lab
/plugin install ui-design-pipeline@ui-direction-lab
```

Then just say **"give me a few UI directions"** (or "做几版 dashboard 方向给我评审").
You only need a one-line description of the product — the pipeline asks for the rest in order.

Prerequisite: **Python ≥ 3.9** on PATH (the validators). No pip packages — standard library only.

## What's inside (21 skills)

| Group | Skills | Role |
|---|---|---|
| `core/` | `prototyping-ui-directions`, `anchor-prototype-wave` | The pipeline: divergence engine, then production engine |
| `companions/` | `information-architecture`, `taste-skill`, `design-system`, `frontend-audit-polish`, `frontend-visual-regression` | Optional quality companions, invoked at named seams |
| `extensions/` | `anchor-prototype-wave-{dark-mode,elements,versions}` | Opt-in add-ons to the production wave |
| `three/` | 11 Three.js / WebGL skills | The canvas/3D HOW layer (see `three/README.md`) |

Skills are namespaced: `/ui-design-pipeline:prototyping-ui-directions`.

## The nine decision points

You are asked, in this order — everything else runs unattended:

1. Intent (4 questions, all defaultable) · 2. **Do you have a reference, or is this exploration?**
· 3. Confirm the reference list · 4. **Pick the LEAD variant** · 5. Contrast-gate failures: fix or
knowingly accept · 6. Pick the motion stance · 7. **Approve lock → wave** (a hook hard-blocks the
fan-out until you say an explicit approval word) · 8. Escalations only, when a surface fails 3 times
· 9. Accept the gallery.

Two more appear once the motion architecture is engaged — a Sectional Score pick and an Atomic Pass
budget approval — and two more if the information-architecture companion runs: approving the
information structure before any visual work exists, and walking the round-2 wireframes at the
Stage-F gate before the wave colours them.

## Not shipped — nominated

Some skills this pipeline calls are **deliberately not redistributed here**. Third-party work is
better installed from its own source: you get the current version, and its author stays its
publisher. Each call site says how to install it, and what happens if you don't.

| Skill | Install | Without it |
|---|---|---|
| `gsap-*` (8, GreenSock, MIT) | `/plugin marketplace add greensock/gsap-skills` | Motion is still authored with GSAP, from `taste-skill` §8 engine rules; recorded as `companion_skipped` |
| `frontend-design` (Anthropic, Apache-2.0) | `/plugin install frontend-design@claude-plugins-official` | Authoring falls back to `taste-skill`'s anti-slop rules |
| `grill-with-docs` | user-installed | Idea refinement runs inline |
| `competitive-teardown` | user-installed (⚠ upstream is the full business-intelligence skill; only its Design-Reference Visual Mode is wanted here) | Falls back to model prior |
| `codex-dispatch` | user-installed | The cross-AI review pass is skipped — never silently replaced by a self-review |
| `shadcn-registry` | user-installed | Component install is done by hand |

**A missing nominated skill is a normal state, not a failure.** It is recorded as
`companion_skipped: <name>` on the stage output, never silently dropped.

## Path conventions

- `${CLAUDE_PLUGIN_ROOT}/…` — files inside this plugin. Always resolve.
- `testbed/…` — the **lab corpus**, which lives only in the private lab checkout, not here.
  **not with this plugin** (~20MB of reference material, three quarters of it demo imagery). Reference docs point into it for
  provenance; scripts that touch it detect its absence and say so out loud rather than failing —
  e.g. `check_registry_sync.py` prints `material paths SKIPPED (lab-only check)`.
- `vendor/…` — nominated third-party copies kept in the lab checkout only.

## Honest boundaries

- **Whether it looks good is always your judgment.** Scorers and validators only guarantee "written
  correctly, obeys the chassis".
- **3D / canvas surfaces can only be machine-checked for console errors, leaks and API misuse** —
  a validator cannot see inside a `<canvas>`. You must look at those with your own eyes.
- One run serves one register. A marketing site and an app console are two runs, two chassis.
- Variants are review prototypes, not production code. Cross-page links are mocked and labelled.

## License

MIT — see `LICENSE`. Two components are vendored verbatim from other MIT projects, each
carrying its upstream attribution in place rather than a restated summary:

- **`three/`** (10 of its 11 skills) from
  [CloudAI-X/threejs-skills](https://github.com/CloudAI-X/threejs-skills) — MIT is declared in
  that project's README; it ships no LICENSE file, and this package does not invent one. See
  `three/LICENSE-UPSTREAM.md`. `three/threejs-scroll-stage` is original to this lab.
- **`core/prototyping-ui-directions/references/_vendor/hallmark-slop-test.md`** from
  [Nutlope/hallmark](https://github.com/Nutlope/hallmark) @ `627f5d2` — MIT
  (Hassan El Mghari). The file's own header carries the source, commit and licence.

Everything else here is original work.
