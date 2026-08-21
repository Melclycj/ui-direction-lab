---
name: prototyping-ui-directions
version: 1.1.0
description: >
  Turn a vague product idea into N variant UI direction prototypes for
  decision review (not for production). Walks through idea intake →
  reference selection → research → per-variant prototype package (HTML
  mocks + palette.json + token-candidates + readme + comparison report).
  Pairs downstream with `anchor-prototype-wave` — once the user picks a
  winning variant, that variant's token-candidates become the chassis
  for the anchor-wave run. NORMALLY ENTERED VIA `ui-pipeline`, which routes
  here directly only for a SINGLE-screen product; with a second screen
  `information-architecture` round 1 runs first and its approved hero spec
  becomes this skill's intake. Trigger: "explore N UI directions",
  "generate variant prototypes for review", "from idea to prototype package".
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, WebFetch
---

# prototyping-ui-directions

4-stage pipeline for vague-idea → review-ready prototype packages. Optional companion skills (taste-skill, design-system, etc.) enhance specific stages when present; degrades to main-thread fallback otherwise.

**Downstream**: `anchor-prototype-wave` (lock the winning variant's tokens as a chassis, then mass-produce hi-fi surfaces from a page list).

## Intent

- **What it does**: explore N UI/UX direction variants from a fuzzy idea.
- **Not for**: production code, component libraries, design-token
  pipelines, QA, deployment.

## Topology — parent runs inline; companions invoked via Read, not Skill

This skill MUST run in the **parent context**, and companions
(`taste-skill`, `design-system`, `grill-with-docs`, `frontend-design`,
`competitive-teardown`, `codex-dispatch`) must be invoked by **reading
their `SKILL.md` as files** and applying the rules. Two path shapes,
try in this order:

1. **shipped with this plugin** — `${CLAUDE_PLUGIN_ROOT}/companions/<name>/SKILL.md`
   (taste-skill, design-system, information-architecture,
   frontend-audit-polish, frontend-visual-regression). These always resolve.
2. **NOT shipped — nominated** (grill-with-docs, competitive-teardown,
   codex-dispatch, shadcn-registry, frontend-design, gsap-*): third-party
   skills this plugin deliberately does not redistribute. Each call site
   below names how to install it. Until the user installs one, it is
   **absent by design** — that is a normal state, not a failure.
3. **in the lab checkout only** — `vendor/<name>/SKILL.md` at the repo root,
   outside the plugin directory. Available when working inside the
   private lab checkout; never present in an install.

Every companion below carries an explicit "if it does not resolve" line.
A companion that cannot be read must be **recorded as skipped**, never
silently dropped.
The `Skill` tool does NOT auto-route project-local skills from any
context (this is a harness behavior, not a skill bug — the `Skill` tool
won't fire on project-local skills, so companions are invoked by reading
their SKILL.md).

**Default — run all four stages inline in the parent.** 3-4 variants of
~10 files each is small enough that inline is simpler than fan-out, and
inline keeps full Read access to companion SKILL.md files at each stage.

**Per-stage companion invocation**:
- Stage 0: `Read` **`grill-with-docs`** — NOT shipped (nominated). In the lab
  checkout it is at `vendor/grill-with-docs/SKILL.md`; elsewhere it must be
  installed into `~/.claude/skills/grill-with-docs/` by the user. Apply its
  questioning method to refine the idea brief.
  **If it does not resolve**: run the refinement inline with the parent's
  own questioning and record `companion_skipped: grill-with-docs` on the
  stage output. Do NOT silently proceed as though Stage 0 ran fully.
- Stage 1: `Read` **`competitive-teardown`** — NOT shipped (nominated; lab
  checkout has it at `vendor/competitive-teardown/SKILL.md`)
  for **design-reference extraction** — it emits a visual-pattern extract
  card (palette / typography / layout & spacing / motion / exemplar anchors)
  from a live product, which is what grounds the "I have a specific
  reference" branch of gate #0.
  ⚠ The lab copy is **trimmed to that mode only** (56KB → 8KB; trim record in
  `vendor/competitive-teardown/UPSTREAM.md`). Upstream is a business
  competitive-intelligence skill (12-dimension scorecard, pricing, SWOT,
  positioning, stakeholder deck) and that half is deliberately not carried:
  Stage 1 acquires **visual** references, not market intelligence. **So the
  nomination is not equivalent** — installing the upstream skill gets you the
  full business version, of which only its Design-Reference Visual Mode
  section is wanted here; read that section only.
  **If it does not resolve**: fall back to model-prior and record
  `companion_skipped: competitive-teardown` on the stage output.
- Stage 2: `Read ${CLAUDE_PLUGIN_ROOT}/authoring/design-system/SKILL.md` to shortlist 3-5
  reference systems from its catalog matching the brief's stance.
- Stage 3 authoring: `Read` **`frontend-design`** — NOT shipped (nominated).
  It is Anthropic's own skill, Apache-2.0, kept current upstream; install with
  `/plugin install frontend-design@claude-plugins-official`. Read it before
  writing HTML to absorb its anti-slop authoring rules.
  **Scope boundary** (this was the only lab-authored note on the old vendored
  copy, kept here): use `frontend-design` for single-file / one-off
  distinctive generation with no orchestration. Multi-variant direction
  exploration is THIS skill's job; chassis-locked multi-surface production is
  `anchor-prototype-wave`'s. When the task is pipeline-shaped, `frontend-design`
  supplies only the anti-slop authoring instinct — it does not take over.
  **If it does not resolve**: author from `${CLAUDE_PLUGIN_ROOT}/authoring/taste-skill/SKILL.md`
  alone (it carries the anti-slop rules that gate this lab) and record
  `companion_skipped: frontend-design`.
- Stage 3 authoring (motion): when a variant's **Motion** dimension weight
  is ≥ 3 (or the brief asks for animation), `Read` the `gsap-*` skills — NOT
  shipped (nominated). They are GreenSock's own MIT skills, kept current
  upstream; install with `/plugin marketplace add greensock/gsap-skills`
  (the lab checkout also has a copy at `gsap-*`).
  **If they do not resolve**: still author with GSAP from the engine rules in
  `${CLAUDE_PLUGIN_ROOT}/authoring/taste-skill/SKILL.md` §8, and record
  `companion_skipped: gsap-*`. Author motion with **GSAP** — that is the engine the Motion
  dimension compiles to. For HTML output GSAP is the default (Framer Motion
  is React-only and won't run in plain HTML). Start with `gsap-core` +
  `gsap-scrolltrigger`; add `gsap-timeline` / `gsap-plugins` (SplitText…) as
  the direction needs. Drive motion from the variant's `token-candidates`
  motion tokens (duration/easing), not raw values. Engine-choice +
  reduced-motion policy live in `taste-skill` §8.
- Stage 3 authoring (3D/canvas — conditional): if the brief or a variant
  direction calls for a 3D / particle canvas stage (signature hero, scroll-
  driven 3D scene), `Read` the `three/*` skills (`three/threejs-fundamentals`
  + `three/threejs-scroll-stage`; more as needed — vendored + lab-authored,
  see `three/README.md`). 3D obeys the 2D pipeline: page choreography stays
  with GSAP ScrollTrigger (the canvas only receives progress via
  `setProgress(p)`), one `gsap.ticker` loop (never a second RAF), colors
  derive from the variant's tokens, full disposal on teardown, reduced-motion
  static frame — and never Framer Motion in the same tree. Honest boundary:
  deterministic validators cannot see inside a `<canvas>`; a 3D variant's
  look is judged by human eyes in the gallery.
- Stage 3 red-team: `Read ${CLAUDE_PLUGIN_ROOT}/authoring/taste-skill/SKILL.md` and apply
  its full ruleset (Inter ban, anti-emoji policy, hardware acceleration,
  card-overuse, tactile feedback, brand naming) to each variant. This
  catches ~6 findings main-thread audit typically misses.
- Stage 3 parallelism (optional, if ≥4 variants): `Read`
  **`vendor/codex-dispatch/SKILL.md`** (same dual path) for the dispatch
  decision tree. Note it routes execution through the official
  `codex@openai-codex` plugin commands and does NOT shell out to
  `codex exec` itself. If it does not resolve, author the variants in the
  parent instead — do not invent a dispatch pattern.

**Optional fan-out (Stage 3 only)**: if generating ≥4 variants, parent
may spawn one subagent per variant. The parent must extract the
relevant companion guidance (e.g., taste-skill's findings on a draft)
and inline that guidance into each subagent's prompt. Subagents will
also need to be told the companion's absolute path
(`${CLAUDE_PLUGIN_ROOT}/companions/<name>/SKILL.md` for shipped ones) and
told to `Read` it directly if they must consult one themselves.

Do NOT spawn a single "run this skill for me" orchestrator subagent —
the cross-stage decisions need parent-level coordination, and the spawn
overhead exceeds the work for a 3-4 variant run.

## Inputs (ask once, never invent)

1. **Product idea**: one sentence + who/when/why.
2. **Vibe references**: 2-4 names / vibe descriptors; user picks, you
   don't. (A specific target — product/site/brand — is locked later at the Stage-1 gate #0.)
3. **Dimension weights**: 1-5 per dim (default 3) across the six dims
   below.
4. **Variant count**: default 3; cap at 5.
5. **Output type**: HTML (default; browser-direct) or React/TSX (needs
   `package.json` + `npm run dev`). Not both in one variant.
6. **Output dir**: default `output/<date>-<nickname>/`.
7. **IA info-spec (optional)**: if an `information-architecture` round-1 run exists, intake =
   the **hero screen's entry only** from its `info-spec.json` (+ `register`, `product`, and the
   hero's `link_map` rows for mocked-link context) — never the whole product (other screens
   stay dormant until IA round-2). The spec is a **hard constraint, not inspiration**: its
   blocks / tiers / scan_path / within_page_flow are FIXED across all variants; what varies is
   composition (arrangement, panes, widget choices) + visual. Provenance: the spec passed
   `validate_infospec.py` and its human board gate before arriving here.

8. **Performance budget (算力档)**: the run's device/audience ceiling —
   `light | medium | heavy` (default **heavy** — no perf filtering unless the
   user tightens it; user says "weak-machine-first / 弱机优先" → light). This is
   the resolver's `perf_budget` for chassis-phase
   candidates, becomes `performance_ceiling` in the Motion Architecture block at
   lock, and the sectional/atomic budgets downstream inherit from it. Over-budget
   candidates with a declared fallback stay eligible carrying a
   `fallback-required` condition; without an accepted fallback they are excluded.

Missing → stop and ask.

## The six dimensions

| Dim | What |
|---|---|
| Visual | palette / typography / hierarchy / texture |
| Interaction | core actions / states / keyboard reach |
| Motion | duration / easing / where motion matters |
| Perspective | IA / user viewpoint / primary path |
| Accessibility | WCAG AA / reduced-motion / keyboard |
| Responsive | breakpoints / touch / density |

Stage 0 captures weights; later stages prioritize accordingly.

## Batched exploration — vary ONE axis per batch (avoid combinatorial explosion)

The six dimensions are two different kinds of thing; treat them differently:

- **Variation axes** (you make variants *of* these): **Visual** (palette /
  type / layout / density) and **Motion** (the animation treatment). These are
  what differ *between* variants.
- **Quality lenses** (applied to *every* variant, never varied): Interaction,
  **Perspective** (IA / primary path — every variant needs a coherent one),
  Accessibility, Responsive — plus the HCI usability heuristics. Every variant
  must clear these; they are bars, not choices.

**Never cross-product the axes.** 3 visual × 3 motion = 9 variants; add a third
axis and it's 27 — exponential. Instead **factor the search: vary one axis per
batch, lock the lead, then vary the next axis on top of the lead.** Additive
(3 + 3 = 6), not multiplicative.

**Canonical sequence for a create run** (Stage 0-1 — brief + references — and the
reference *research* are done once up front and reused; `direction-candidates` are
produced **per batch** — Batch-1 visual candidates up front, Batch-2 motion candidates
*after* the LEAD locks (they depend on it); each batch then runs the Stage 3 generation
loop with the batch's axis as the only variable):

1. **Batch 1 — Integrated chassis directions** (not flat visual skins). 3-4 variants
   that differ as integrated chassis SYSTEMS: the visual axis (palette / type /
   layout / density) PLUS an explicit **page-scoped motion/3D stance** — which may
   be, and usually is, **none** (`page_scoped_mechanism=null` = a static visual
   chassis; that is a first-class stance, not a missing feature). The chassis owns
   what only the chassis can own: global layout grammar + navigation, global scroll
   model, any persistent WebGL/canvas stage, any chassis-level 3D mechanism and its
   native 2D carrier, the motion vocabulary + token floor, the performance ceiling
   + fallback policy, and the sectional/atomic budgets inherited downstream
   (`references/execution-contracts.md` §1/§5). **Runtime gate**: any pool-sourced
   mechanism candidate MUST pass the deterministic resolver BEFORE its candidate
   card is written — `scripts/resolve_candidates.py` with `phase=chassis`,
   `chassis_stage=batch1-directions`, state `CHASSIS_OPEN`, `perf_budget` = the
   §Inputs-8 performance budget; only `eligible` entries
   may appear as cards (excluded entries may be summarized as a count, never shown
   as selectable), and the resolution JSON is kept as evidence under
   `<out>/motion/resolutions/`. Hold motion at a plain default otherwise (load-in
   only, or none) — sectional choreography and atomic decoration are LATER phases'
   decisions, absent from every Batch-1 variant. User picks a **LEAD**; its
   `token-candidates` become the locked chassis. For IA-fed runs, the lock also records the LEAD's
   **composition pattern** in the chassis `CHASSIS.md` (a named pattern + landmark
   structure — e.g. "cockpit: icon rail + ticker + dense hairline grid + right
   detail pane" — plus which spec block sits in which region). IA round-2 reads
   exactly this to generalize the composition to the other screens; an unlabeled
   chassis forces round-2 to reverse-engineer the pattern from `index.html`.
   **Locking is additionally gated by a DETERMINISTIC contrast check**: before the
   lock, compute WCAG contrast (python inline is fine) for every text-role token
   against the surface token(s) it sits on — AA = 4.5:1 below 18.66px-bold/24px.
   Present any failing pair to the user BEFORE locking; they may knowingly accept
   (record the override + ratio in CHASSIS.md), but a silent lock of failing tokens
   becomes hereditary debt for every downstream wave surface. (Origin: 2026-07-03 —
   66 axe-failing nodes across 3 surfaces + hero, all inherited from a locked
   faint/pending pair that no gate ever measured. LLM red-team eyeballing is a
   probabilistic lens; token math is a machine's job.)
   **Lock ceremony (Motion Architecture)**: locking now also writes the
   **Motion Architecture block** into `CHASSIS.md` (shape:
   `references/execution-contracts.md` §5 — global_scroll_model /
   persistent_3d_stage / page_scoped_mechanism / chassis_mechanism_ids /
   motion_stance / performance_ceiling / reduced_motion_strategy /
   sectional_budget / atomic_budget) and advances the run's pipeline-state
   artifact via `scripts/pipeline_state.py`: `set page_scoped_mechanism` (null is
   declared, never implied) + `set chassis_ref` + `approve --gate chassis
   --approval-text "<user's verbatim words>"` + `transition --to CHASSIS_LOCKED`.
   The state machine is monotonic: **once CHASSIS_LOCKED, a chassis-effective
   mechanism can never become selectable again in this run** — reopening the
   chassis is a separate explicit new run, never an automatic promotion later.
2. **Batch 2 — Motion treatment (tunes the LEAD's vocabulary — never adds a
   chassis mechanism).** Visuals frozen to the LEAD. 2-3 variants that
   differ *only* on the motion axis (GSAP), authored per the §Stage 3 motion step —
   **and they must differ by motion VOCABULARY (what moves / the metaphor), never
   merely by intensity.** An intensity ladder of ONE vocabulary (load-in →
   scroll-reveal → +loops of the same settle/fade moves) reads as three
   near-identical variants at first glance (2026-07-07 Loop run: the user rejected
   exactly this ladder; the rework cost a full batch). Draw each candidate from a
   different vocabulary family — displacement (settle/slide) · ink/drawing (stroke
   draw-in, clip write-on) · space (scrub parallax/depth) · numbers-only (counters
   as the sole movers) · light (sweeps/highlights) — then tune each family's
   intensity to the register. Each candidate's one-line descriptor must answer
   "what KIND of thing moves here", not "how much". User picks a motion stance;
   record it in the chassis' motion tokens.
   **Hard rule — tuning, not adding**: Batch-2 may tune the CHOSEN chassis'
   motion vocabulary and architecture, but may NOT introduce a new mechanism
   whose effective footprint is chassis. Pool-sourced Batch-2 candidates go
   through the resolver with `phase=chassis`, `chassis_stage=batch2-tuning` —
   it deterministically excludes chassis-footprint candidates
   (`CHASSIS_MECHANISM_IN_TUNING`) while keeping component-level vocabulary
   (text reveals, load-ins, parallax) eligible. A page-spanning mechanism the
   user genuinely wants belongs in Batch-1 as an integrated direction, not
   smuggled into Batch-2.
3. **Composition-ready gate → Sectional Score.** After the lock,
   `composition_ready` must become true before any per-surface orchestration is
   chosen: IA-fed runs reach it when IA Round-2 Stage-F passes; a single-page run
   reaches it at lock (the approved chassis page structure IS the composition) —
   record it via `pipeline_state.py set composition_ready true` with the gate
   reference as evidence. Then run **§Sectional Score** (below) — select at most
   ONE bounded orchestration per nominated surface, or skip.
4. **Hand to `anchor-prototype-wave`** (Base Wave) with the now-fully-locked
   chassis (visual + motion), the approved composition, and the sectional
   contracts (state must be `SECTIONAL_LOCKED` → the wave's preflight verifies
   and advances to `BASE_WAVE_READY`).

This keeps every batch at N ≤ 5 and makes attribution clean — a Batch-2
difference is *only* motion, because the visuals are frozen (the same control-a-
variable discipline the lab's testbed uses).

**Slop gates + pre-emit 六轴自评（每批出稿纪律，hallmark 适配——见
`references/slop-gates.md`，引用不复制）**：每个 variant 出稿前先跑六轴自评
（P/H/E/S/R/V 各 1-5 分；**任一轴 <3 强制返工一轮**再交人评），文件头留一行 stamp
`/* pre-emit critique: P# H# E# S# R# V# */`；每批收尾对本批共性做**一次**
slop-gate sweep（(a) 桶为主，命中条件才查 (b) 桶），结果记 run-notes 一行
（`slop sweep: pass` / `FAIL: 门号`）。其中 **V (Variety) 轴按结构距离打分——换色/
换皮不算 variety**：同批 variants 必须结构指纹互异，这是对既有「一批一轴」纪律的
收紧（Batch-2 的 vocabulary-family 强制即此轴在 motion 面的同款约束）。
instruction-layer 自查，非机器 gate。

**Greedy, not globally optimal:** the best motion for the LEAD may not be the
best motion for a runner-up direction. Accepted trade for tractability. If it
matters, run one cheap cross-check at the end (winning motion on the runner-up
visual) — do not reintroduce the full cross-product.

**Base-case reference pools (optional).** A run may be handed a style pool
and/or a motion-effect pool as *inspiration for when nothing better comes to
mind* — NOT a menu you must pick from. Propose original directions first; reach
for a pool only as a fallback or a springboard to push past. Default pools ship
**with this skill** at `references/style-pool.md` (Batch 1 visual),
`references/font-pool.md` (Batch 1 typography — pairings by vibe),
`references/palette-pool.md` (Batch 1 token-level color — SaaS + luxury rows seeded from
real DESIGN.md), `references/motion-pool.md` (Batch 2 motion),
`references/threed-pool.md` (3D/canvas components & signature effects — carries a mandatory
**perf-cost tier** per entry; a laggy hero fails its purpose on weak hardware; also the
library-canonical **mechanism-tag schema + consumption contract** for graduated pool entries:
filter-chain not ranking, no duplicate mechanism within a batch, written fit-rationale per
candidate, enumerate-all-survivors-then-assign, row order carries no priority) and
`references/component-pattern-pool.md` (WHERE to get reusable component code by workflow
category — Actions/Input/Nav/Containment/Data-Display/Feedback — pointers, not a list) —
they deploy alongside the skill so they're always available; a project may override with its
own pool. **Machine-consumption layer (2026-07-10)**: every covered pool row carries exactly one
record in `references/execution-registry.json` (row badge `【⚙执行册】`; shapes + resolver +
state-machine canon = `references/execution-contracts.md`); pool-sourced mechanism candidates in
ANY phase must pass `scripts/resolve_candidates.py` before candidate cards are written, and
`scripts/check_registry_sync.py` keeps rows ↔ records in lockstep. `references/reference-sources.md` is the companion registry of WHERE to look
(tiered by buildable-fidelity) + the reference-first / selection workflow consulted in
Stage 1. Human-facing OPERATOR MANUAL for the whole create pipeline (how the user drives
a run: every decision gate + what they get + where references plug in + the materialization
ladder): the lab repo's root `README.md` (`GUIDE.md` here is a pointer stub) — a map for
humans, never an operating instruction for agents (this SKILL.md wins on conflict).

**Library growth is human-gated — never auto-promote our own run output.** The pools point at
**external, credible standards**; our own outputs (a nice page, the picked LEAD, a high score) are
*fit for this project*, not exemplars, and never self-enter the pools. Only externally-sourced
references found during a run flow back, and only by surfacing a candidate (anchor + URL + why +
provenance) for the user to accept. Full per-pool rules + governance live in **one source**:
`references/reference-sources.md` §5.

> Within a batch, variants differ *meaningfully on the batch axis* (e.g. not the
> same layout with three accent colors), not across unrelated dimensions.

## Sectional Score — pick each surface's ONE primary orchestration (+ optional component tier) (after composition, before Base Wave)

Selection order is global system → bounded section → existing component
(`chassis → sectional → atomic`); this ceremony is the middle step. It exists so
per-surface choreography is chosen against the KNOWN composition — never
improvised by wave subagents, and never decided before the sections exist on
paper. Shapes: `references/execution-contracts.md` §3/§4/§6.

**Gate (machine-enforced)**: state ≥ `CHASSIS_LOCKED` AND `composition_ready=true`
(`scripts/pipeline_state.py verify --min-state CHASSIS_LOCKED
--require-composition-ready`); the ceremony moves the state
`SECTIONAL_OPEN → SECTIONAL_LOCKED`.

**Read the surface's `archetype` first (if an IA spec is present).** It is per-screen, derived
from that screen's `primary_task`, and it constrains what this surface must DO regardless of the
locked style — `references/archetype-rules.md` carries the iron rules and the six-dimension weight
priors. Two consequences here: a candidate that cannot satisfy the surface's iron rules is not a
candidate (a `narrative-scrolly` surface may not take a mechanism that hijacks scroll velocity;
a `data-dashboard` surface may not take one that animates layout under a scrub), and the weight
prior says where this surface's exploration budget goes. **No archetype = flat prior + corpus-wide
rules only** — do not invent one to fill the slot; the honest degrade is the designed path.

Per nominated surface (nominate FEW — most surfaces need none):
1. Build the deployment proposal honestly (owner scope, bounded container, local
   progress, releases-on-exit, global side effects) + a shortlist of pool
   candidate ids.
   **Content-shape discovery (optional, default off).** When you can name a
   surface's content, CLASSIFY it — from the IA `content_hint`'s WHAT-info (if an
   IA spec is present) plus the locked composition — into a
   `content_shape: {role, items, density}` (the 8 roles are `collection` / `comparison` /
   `sequence` / `metrics` / `spec` / `narrative` / `headline` / `figure`; the full contract
   table is `testbed/material/content-roles.md`, **lab checkout only — not shipped**),
   and you MAY pass that on the resolver input and OMIT the hand-built shortlist.
   The resolver then DISCOVERS every material that can host that content, runs
   buildability + semantic, and returns candidates cleanest-first (contracts §3.1)
   — the "this section is a comparison / collection / spec / … — which materials
   can carry it, and does one even beat native?" path. Passing no `content_shape`
   keeps the hand-shortlist path above exactly as-is. The `content_hint` is
   composition-free by IA design; turning it into a role IS a Sectional-Score
   judgment — legitimate, because per-surface arrangement is precisely what this
   ceremony decides.
2. Run `scripts/resolve_candidates.py` with `phase=sectional`, the run's
   pipeline_state, register, the chassis `sectional_budget` as perf budget, and
   `occupied_drivers` (taste §8: at most one master scroll orchestration per
   page). **Chassis-effective candidates are excluded BEFORE presentation**
   (`INELIGIBLE_CHASSIS_LOCKED`) — the gallery may summarize an exclusion count,
   but excluded entries never become selectable cards. Keep the resolution JSON
   as evidence under `<out>/motion/resolutions/` (preflight verifies it).
3. For each `eligible` id, go back and READ its pool row (the
   `【⚙执行册】`-badged row) before writing anything — **the registry only
   FILTERS; the pool row is where the human-language judgment lives**
   (手感 / 适合 / mechanism evidence / 人评注 / reuse caveats). Cards and
   fit-rationales are written FROM the pool row, never from registry fields.
   Present ONLY `eligible` candidates (render ⚠ register warnings + fallback
   conditions on the card); the user selects ONE or skips the surface.
   When a `content_shape` was used, each `eligible` card also carries its
   `content_role` `{preserves, breaks}` — show the **breaks** honestly, not just
   the upside — and the resolution carries a `native_hint`. **Native (plain
   semantic HTML — a real `<table>` / list / `<dl>`) is ALWAYS on the menu, never
   filtered out.** When `native_hint` says native likely WINS (dense content, a
   comparison over ~8 items, a spec), present native as the default the user must
   consciously override. Choosing native is a first-class answer: record it as
   `sectional_score: null` (there is no material) with the `resolution_record`
   kept as the evidence trail — the resolution JSON's `native_hint` +
   `CONTENT_ROLE_UNFIT` entries document WHY native won, so it is never mistaken
   for an unconsidered skip.
4. Write the per-surface contract into `<out>/motion/sectional-score.json`
   (contracts §6: mechanism id, carrier, driver, fallback, resolution_record).
   `sectional_score: null` is valid and remains the default for every
   unnominated surface. STRUCTURAL/component transforms (register→bento,
   list→drawer; driver pointer|click|load only) go in the optional
   `component_scores` array (contracts §6 component tier) — each entry passes
   the same resolver + pool-row-reading + contract rigor as the primary.
5. Record the pick verbatim: `pipeline_state.py approve --gate sectional` +
   `set sectional_status selected` (or `skipped` when the user opts out of
   sectional entirely — equally an explicit answer, never a self-served default).
6. `transition --to SECTIONAL_LOCKED`. After this, sectional choices are frozen
   inputs to Base Wave; changing one is an explicit re-open conversation with
   the user, never a wave-side improvisation.

**Repeated content shapes — ask before reusing (never auto-propagate).** When the
same content shape recurs across surfaces (every section a card collection; three
panels each a comparison), do NOT silently reuse one surface's pick for the rest.
Ask the user outright: *"unify — one material across all these sections — or vary,
each its own?"* Propagate only after they answer (hero surfaces lean varied,
app/dashboard lean unified, but you ALWAYS ask). Each instance still re-runs its
own buildability — the same material can fit one section's item count and overflow
another's.

Hard rules: at most ONE primary sectional orchestration per surface —
scroll/timeline-driven orchestration is EXCLUSIVE to that primary slot.
Structural/component transforms (driver pointer|click|load) may additionally
ship as `component_scores` entries (contracts §6 component tier; user-approved
relax 2026-07-18, Averonel option-2 — before that date this rule was a flat
"one per surface"). EVERY entry, primary or component, must remain removable
without invalidating adjacent sections, navigation, or the global scroll model
(the registry's boundary requirements must be evidenced in the built section);
no duplicate `mechanism_family` across one run's surfaces without the user
knowingly accepting the repeat.

## Pipeline

### Stage 0 — Idea intake → `idea-brief.md`

With an IA info-spec (§Inputs 7), Stage 0 pre-fills from it: "what are you building" / "who,
when" / primary path come from the spec's `product`, `register`, and the hero's `primary_task` —
don't re-grill the user for them. Still ask: vibe references, dimension weights, variant count,
output type/dir. Gate #0 (Stage 1) is asked as usual.

Ask 4 questions (only as many as needed; don't grill):
1. One sentence: what are you building?
2. Who uses it, in what situation?
3. "Looks like / feels like" references (vibe, not URLs)?
4. What will the output be used for? (investor demo / design exploration
   / engineering reference / personal portfolio)

Then capture dimension weights, and confirm the remaining §Inputs (variant count /
output type / output dir — or note they're taking defaults). Write `<out>/idea-brief.md`:

```md
# Idea Brief — <date> — <nickname>
## What  <one line>
## Who & When  user / scene / output use
## Vibe references  (atmosphere, not URLs)
## Dimension priorities  table of 6 dims × weight 1-5
## Out of scope  (anything user explicitly rules out)
## Open questions  (non-blocking)
```

Also open the run's motion pipeline-state artifact (the irreversible-sequence
spine every later gate advances): `python scripts/pipeline_state.py init
--out-dir <out>/motion --run <date>-<nickname>` → state `CHASSIS_OPEN`.

### Stage 1 — Reference acquisition → `reference/` + `reference-manifest.md`

**Stage 1 opens with a HARD STOP-AND-ASK gate (gate #0). You MUST put this question to the user in their own turn and WAIT for their answer, framed by INTENT not mechanism: _"Do you have a specific reference in mind — a product / site / brand you want this grounded in — or no specific target, so we explore the style space?"_ ("external fetch vs built-in pools" is only the downstream mechanism — too vague to lead with). Never self-answer it, never assume a branch, never fold it into a recommendation you then act on, never treat "the verification/demo just needs X" as license to pick for them. No Stage-1 work — no manifest, no anchor-matching, no generation — proceeds until the user has explicitly chosen a branch. Writing "I chose NO-external" into a doc is NOT asking.**

- **No specific target → explore the style space** (mechanism: NO external, built-in pools) → work from the bundled pools (`style-pool` / `font-pool` / `palette-pool` / `motion-pool` /
  `component-pattern-pool` for component-code pointers) and **match the closest real exemplar product yourself**.
  **HARD RULE — the ANCHOR variant:** exactly ONE of the Batch-1 variants MUST be a *faithful, recognizable
  rendering of the single closest real product* from the pool — not a loose "inspired-by" original, but a
  variant a reviewer would look at and say "yes, that's basically the \<product\> look." (e.g. a
  monitoring-console brief → the closest real product is an observability tool like Sentry → one variant is a
  faithful Sentry-style rendering.) **Reproduce the product's real _working UI_ — the app / console users
  actually spend time in — NOT its marketing / landing page, which is usually a different, flashier look**
  (e.g. Sentry's _app_ = white main content + dark-violet sidebar, but its _landing page_ is all-dark-violet;
  the anchor must be the app). It gives the reviewer a real-world yardstick to judge the original
  directions against. Label it **ANCHOR** in the gallery tab + comparison-report and name the product it
  reproduces; interpret its *system* (palette / type / layout / density), never copy assets (`do-not-copy`).
  The **remaining** variants are original directions that only *borrow* from the pools (must differ
  meaningfully from the anchor, per the batch-axis rule). No fetch; pool + the faithful anchor drive the batch.
- **Has a specific target → ground the design in it** (mechanism: YES external, fetch) → consult `references/reference-sources.md` by intent: implementation / complex-motion → code
  buckets (C = GSAP/vanilla first, then B = React/Framer with an `interpret-to-gsap` flag for HTML output);
  inspiration / "like \<vibe|brand\>" → galleries + the DESIGN.md exemplar card for that brand. It tiers every
  source on two honest axes (visual vs motion fidelity) — this skill reads code well but cannot *watch* a running
  animation, so complex dynamic effects get steered to sources whose real implementation is readable. When the
  user hands **many** candidate sources, run that file's **§2 selection workflow** (bucket → 6-gate rubric →
  capped/deduped/tagged shortlist) and present the shortlist before locking.

Lock the reference list **with the user** before any clone or fetch.
For each reference:
- Source URL + license.
- Why it's in (which dim it informs).
- What to extract (specific surfaces / patterns / palettes).

Then either `git clone` (if it's a public repo) or fetch key
screenshots/pages. Write `reference-manifest.md` with one row per
reference: source, license, intent, do-not-copy notes.

**Never clone without confirmation. Never auto-pick references.**

### Stage 2 — Research & analysis → `research/`

Per reference, write a `research/extract-<vendor>.md` card:
- Palette (extracted hex / oklch).
- Typography (families, scale).
- Motion (durations, easing).
- Notable patterns (3-5 specific patterns, with screenshot or selector).
- What's worth borrowing for *this* product (per the prioritized dims).

Then `research/cross-reference.md`: matrix of vendors × dims, noting
where they agree/diverge.

Finally `research/direction-candidates.md`: **N candidate directions for the
current batch** (at least 3, at most 5), each varying **only the current batch's
axis** — Batch 1 = the visual axis (palette / typography / layout / density),
Batch 2 = the motion axis. Hold the non-axis dimensions frozen. Each = its axis
treatment + 2-3 keyword adjectives (Batch-1 directions hold motion at a plain
default; the motion stance is decided in Batch 2). Directions must be
**meaningfully different on the batch axis** — not the same thing with three
accent colors.

### Stage 3 — Prototype package generation → `prototypes/variant-<id>/`

Author the batch's variants — **inline in the parent by default; fan out one
subagent per variant only when generating ≥4** (parallel, ≤5 active), per
§Topology. Each variant produces:

```
prototypes/variant-<id>/
├── index.html | index.tsx       ← product face (5-sec read of style)
├── palette.json                 ← machine-readable
├── palette.html                 ← human swatch viewer
├── token-candidates.css         ← full design tokens (color/type/spacing/radius/shadow/motion)
├── token-candidates.json        ← same, machine-readable
├── surface-<name>.html          ← OPTIONAL. Batch-1 ships the product face + tokens (enough to pick a LEAD); the full surface set is anchor-wave's job after the chassis locks
└── readme.md                    ← rationale + dim decisions + what was borrowed
```

Rules for the variant:
- HTML or TSX, not both in one variant.
- All colors via `var(--token-*)`; nothing hardcoded.
- No Lorem ipsum, no "Click me" placeholders. Use the idea brief's real
  scenario text.
- `index` is the **product face**, not a palette showcase — it must let
  a reviewer see what the product *is* in 5 seconds.
- Each surface you ship shows at least 3 meaningful states (default / hover /
  empty / error / loading / selected — pick what's relevant).
- **Motion**: in **Batch 1**, hold motion at a plain default (load-in only, or
  none) — motion is *not* a Batch-1 variable. In **Batch 2** (the motion batch),
  the motion stance IS the axis you vary: implement it with GSAP per the Stage-3
  motion step above — at least one intentional moment (load-in or scroll reveal),
  wrapped in `gsap.matchMedia()` for reduced-motion. No motion beats decorative
  motion; don't add GSAP just to use it; differ the stance meaningfully across the
  Batch-2 variants, don't ship the same reveals on all.
  *Reviewer aid (optional, dev-time only)*: a Batch-2 candidate MAY temporarily
  include **GSDevTools** (`gsap-plugins` §Development → GSDevTools) so
  the human reviewer can scrub / slow-mo / replay each timeline while picking the
  motion stance — motion is judged by eye, and a scrubber beats reloading. It is
  strictly a review-loop tool: strip the plugin script and the
  `GSDevTools.create(...)` call before the stance is locked — no GSDevTools
  reference may survive into the chassis or any downstream deliverable (the
  gsap-plugins skill's own "Do Not" list bans shipping it).
- **IA-fed runs — honor the structure.** Every variant must carry ALL the hero spec's blocks at
  their given tiers (a variant that demotes/drops a tier-1 block is off-spec, whatever it looks
  like), support the scan_path order for the primary task, and express `within_page_flow`
  relationships (the MECHANISM — pane vs expand vs overlay — is the variant's compositional
  choice; the RELATIONSHIP is not). In fan-out mode the parent inlines the hero spec JSON
  verbatim into each variant subagent's prompt. Red-team accordingly: structure violations are
  regenerate-level findings, same severity as Lorem ipsum. In `comparison-report.md`, mark the
  Perspective dimension "locked by IA spec" and judge variants on fidelity to it.

**Per-variant usability audit (HCI lens)** — after authoring each variant but before the gallery + comparison-report write, run a usability audit against the **canonical HCI heuristic set in `anchor-prototype-wave` §4b** (single source — read it there; do NOT re-list it here, so the two cannot drift). Write findings into each variant's `readme.md` under a `## Usability findings` section (BLOCKER/MAJOR/MINOR + fix recs). Findings inform comparison-report.md but don't block variant acceptance.

**Gallery layout — `prototypes/_index.html` (hard rule; no other layout permitted)**:
1. **Fixed top bar** (position: sticky; top: 0; z-index ≥ 100): one tab per variant, including the hybrid if produced. Each tab shows: variant ID + 1-3 word style descriptor (e.g., "V1 · Command", "V2 · Warm", "V3 · Grid", "V4 · Hybrid"). Active tab visually distinguished (accent underline or filled background). This variant selector is the **primary, fixed top bar** — never demoted, restyled away, or replaced; any sub-variant row (point 7) sits as a secondary strip directly **below** it.
2. **Variant marker pills** on tabs: "LEAD" pill on the user-accepted variant; "HYBRID" pill on any hybrid variant produced by a revision request.
3. **Main pane** (below top bar): renders the active variant as a full-bleed `<iframe>` pointing at `variant-N/index.html`. Pane height fills remaining viewport.
4. **Variant metadata footer** (below the iframe, fixed or pinned): palette swatches (5-6 colors), density / motion / type one-liner in mono, links to `variant-N/readme.md` and `variant-N/palette.html`.
5. **Switching**: clicking a tab updates the iframe `src` AND `location.hash` (so `_index.html#variant-2` deep-links to that variant). On page load, read `location.hash` and activate the matching tab (default to LEAD if no hash).
6. All client-side JS, inline. No external deps. Card-grid layouts are NOT permitted — the top-bar switcher is the only sanctioned shape.
7. **Optional second tab row — sub-variants of a direction** (e.g. palette / theme / density treatments of the LEAD). Same switcher mechanics, but driven by a URL param the variant reads (e.g. `variant-d/index.html?theme=acid` → the page swaps a **coordinated token set** — a full color scheme: bg / ink / border / accent together, NOT a single accent token, so the whole page incl. buttons + their hard shadows re-themes as one) so ONE variant file serves every sub-variant — no duplicated files. Show this row when a within-direction sub-axis is being explored (the visual axis often has palette as a cheap sub-axis worth eyeballing before lock); the param-default is the variant's own tokens. This is the gallery surface for exploring a sub-axis **without** spawning a whole new batch.

Then write `prototypes/_index.html` (single-page variant switcher per Layout above) and `prototypes/comparison-report.md`:

```md
# Prototype Comparison — <date> — <project>
## Variants overview  (table: id × one-line style × palette tone × density × motion × output type)
## Dimension fit  (6 dims × each variant × short fit note)
## Borrowing matrix  (each reference × which variants used it)
## Cross-variant patterns
- Patterns recurring across ALL variants (break these — convergence, not divergence)
- Patterns unique to one variant (the actual differentiation)
- Usability disagreements across variants (e.g., "V2 weak on scanning; V1 weak on type rhythm")
## Recommendation framework  (which user type → which variant; risk vs novelty trade)
## Open questions  (for the reviewer)
```

**Red-team pass** (anti-AI-slop): before reporting done, scan each
variant for: generic hero + centered title + gradient blob, default card
grid, Lorem ipsum, palette.html looking nicer than the actual product
mocks, variants that are differentiated only by accent color. If any
hit, regenerate that variant.

### Report to user

Single message:
- N variants produced; file paths.
- Comparison report URL.
- Anything red-teamed and regenerated.
- Anything the user needs to decide before downstream (which variant
  wins, or "merge X+Y into a new run").

## Hard boundaries

- **Don't write to the user's main codebase.** All output under
  `<out>/`.
- **Don't decide for the user.** References, direction count, variant
  count, archetype choice, output type — all user calls.
- **Don't clone references without explicit confirmation per reference.**
- **Don't write final production code.** This skill stops at
  review-ready HTML/TSX mocks.
- **Don't auto-call any downstream skill.** Mention in the comparison
  report which downstream skill fits each variant; let the user invoke.

## Failure modes & responses

| Symptom | Response |
|---|---|
| Variants come out too similar | Back to Stage 2; produce more differentiated directions |
| User says references were wrong in Stage 1 | Back to Stage 0; redo brief |
| HTML/TSX has console errors | Fix immediately; don't accept "mostly works" |
| Variant uses Lorem ipsum | Regenerate that variant |
| Stage 3 mixes HTML and TSX in one variant | Regenerate; one type per variant |
| User wants new dim weight mid-Stage-3 | Back to Stage 0; don't sneak dims in late |

## When to stop and ask

1. **Stage-1 gate #0 — a specific reference target, or explore the style space?** A MANDATORY
   user decision, asked in the user's turn and answered by them (frame by *intent*, not the
   "external vs pools" mechanism). NEVER self-select the branch; no Stage-1 work proceeds until
   they choose. (See Stage 1 opening.)
2. Any input from §Inputs is missing or ambiguous.
3. Before any `git clone` or external fetch in Stage 1.
4. After Stage 3, for variant accept/reject (the LEAD pick).
5. **Pipeline-step transitions after the LEAD are the user's call.** Whether to run
   **Batch-2 motion**, **which Sectional Score candidate each nominated surface gets
   (or skip)**, and when to **lock the chassis + hand to `anchor-prototype-wave`**,
   are STOP-AND-ASK gates: **present the choice (including any proposed skip) as an explicit
   either/or, WAIT for the answer, then record the approval in `.goals/pipeline-gate.json`**
   (the `pipeline-gate` hook hard-blocks the wave fan-out without that sentinel) **and in the
   run's pipeline-state artifact (`pipeline_state.py approve` — verbatim words; the state
   machine refuses lock/sectional/atomic transitions without them)**. Recommending
   a skip is fine; *acting* on it before the user answers is self-answering it (see gate #0).
   A plan card that pre-bakes the skip and collects a "yes" does not count.
6. If a Stage 3 variant fails red-team 3 times, stop and ask whether to
   drop it or revise the direction.

No other approval gates.

## Run pointer (`RUN.md`)

If a `RUN.md` exists at the run root (a run started by `ui-pipeline`), **re-render it** at each
stage boundary — never hand-edit it:

```bash
python ${CLAUDE_PLUGIN_ROOT}/core/ui-pipeline/scripts/render_run.py --run-root <run-root>
```

It is generated from the machine state plus what is on disk, so the statuses, the pointer and
the verbatim approvals are recomputed rather than remembered. Editing it by hand produces
exactly the lying resume pointer the generator exists to prevent, and `preflight_wave.py`
rejects a pointer with no render stamp or a stale one.

`RUN.md` is a resume pointer, never a gate input. Gate decisions read the machine state
(`pipeline_state.py`); if the two ever disagree, the machine state wins.

## Trigger phrases

English:
- "explore N UI directions"
- "generate variant prototypes for review"
- "from idea to prototype package"
- "N variants for me to pick"

中文:
- "出几版 prototype / UI direction"
- "做几版 dashboard 方向给我评审"
- "从 idea 到 prototype package"
- "出 N variant 让我挑方向"
