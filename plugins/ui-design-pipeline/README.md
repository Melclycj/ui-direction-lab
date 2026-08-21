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

## What's inside (22 skills, 6 registered)

| Group | Skills | Registered? | Role |
|---|---|---|---|
| `core/` | `ui-pipeline`, `prototyping-ui-directions`, `anchor-prototype-wave` | **yes** | The front door, then the divergence engine, then the production engine |
| `companions/` | `information-architecture`, `frontend-audit-polish`, `frontend-visual-regression` | **yes** | Invoked on their own: IA is the multi-screen entry, the other two run before or after a wave on any frontend directory |
| `authoring/` | `taste-skill`, `design-system` | no | Rulebooks the parent reads while authoring — anti-slop red-team, ~165-system catalog |
| `extensions/` | `anchor-prototype-wave-{dark-mode,elements,versions}` | no | Opt-in add-ons, switched on by the wave's `extensions:` input |
| `three/` | 11 Three.js / WebGL skills | no | The canvas/3D HOW layer (see `three/README.md`) |

Registered skills are namespaced: `/ui-design-pipeline:prototyping-ui-directions`.

**Start at `ui-pipeline`** — or just describe the product. It establishes the run root, routes by
screen count (one screen → directions; two or more → IA round 1 first), and owns `RUN.md`, the
resume pointer that lets a cleared session pick the run back up.

**Why only 6 of 22 are registered.** The other 16 ship with the plugin and resolve at their normal
paths, but they are deliberately kept out of the manifest's `skills` array: nothing ever
auto-invokes them — the parent reads them by path (`Read ${CLAUDE_PLUGIN_ROOT}/three/…`,
`${CLAUDE_PLUGIN_ROOT}/authoring/…`, `${CLAUDE_PLUGIN_ROOT}/extensions/…`) — so registering their
descriptions would buy always-on context for discovery that never happens. That is ~1,010 tokens
of every session instead of ~2,020 — the entry skill pays for itself twice over. The trade-off is that the 16 cannot be called by name.

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
| `ui-material-library` (54 built pieces) | `/plugin marketplace add Melclycj/ui-material-library` | The reference pools still describe every mechanism; what you lose is the built, human-reviewed implementation behind the `material/<slug>` pointers. `check_registry_sync.py` prints `material paths SKIPPED` instead of pretending to verify them |

**A missing nominated skill is a normal state, not a failure.** It is recorded as
`companion_skipped: <name>` on the stage output, never silently dropped.

`ui-material-library` is the one row here that is ours rather than someone else's. It is separate for
a reason of release rhythm, not of licence: the pieces grow in batches while the instruction layer
above them stays still, and folding them together would let a material batch drive the version number
of a package most of whose users never asked for one. Installed alongside this one, it is found automatically: the two land as siblings under the
plugin cache, so the sync gate resolves the corpus without being told where it is, and says which
route found it. `--material-root <path>` or `UI_MATERIAL_ROOT` still wins when given, and is the
guaranteed answer — auto-discovery reads an install layout that is internal rather than promised,
so it is a convenience that degrades to SKIP, never something a result depends on being there.

The `gsap-*` row above is the licence of those eight **skills**, which is not the licence of the
**library** the motion they describe runs on. GSAP itself is free for commercial use — including
the plugins that used to require a paid Club membership, such as SplitText and ScrollSmoother —
under the [Standard "No Charge" GSAP License](https://gsap.com/community/standard-license/),
effective 2025-04-30 under Webflow. It is proprietary, not MIT: read it rather than assuming
open-source terms. Its one prohibited use is building a no-code visual animation builder that
competes with Webflow — which is not what this pipeline is, but is worth re-reading if what you
build with it ever becomes one. Verified 2026-08-20; generated code loads GSAP from a CDN, so
nothing here redistributes it.

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
