---
name: information-architecture
version: 1.3.1
description: >
  Design a product's INFORMATION structure before (and after) the visual
  pipeline: what each screen holds, what dominates (tier), the scan path,
  grouping, within-page flow, cross-screen link map, and which screen is
  the hero. Round-1 (built; fixture-verified 2026-07-07, loop-ia-ab —
  Stage-A altitude-③ normalization + variants-honor-structure both
  exercised with evidence): 3-altitude intake → normalized sections →
  whole-product layout-OPEN info-spec + grey-box review board (human gate)
  → hero spec feeds `prototyping-ui-directions`. Round-2 (built;
  fixture-verified 2026-07-07 — declared-pattern path + flag-don't-invent
  full loop both exercised live): after chassis lock, extract the composition
  pattern (shell vs content regions + role→region mapping), generalize it
  into grey-box wireframes for the other screens (flag-don't-invent) →
  `anchor-prototype-wave` colors them. Owns information structure ONLY — composition (sidebar vs
  topnav, table vs bento, density) stays prototyping's to vary. Trigger:
  "信息架构 / 信息结构 / 每屏放什么信息 / information architecture /
  info spec / IA round-1 / screen map / IA wireframes (round-2)".
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# information-architecture

Companion skill for the information layer. The visual stack (`prototyping-ui-directions` /
`anchor-prototype-wave` / `taste-skill`) answers "what does it look and move like"; this skill
answers **"what information is on each screen, who dominates, and how does the user's eye and
task flow through it"** — deliberately, reviewably, upstream.

**Data contracts are LOCKED in `references/data-contracts.md`** — read it before producing any
artifact. This file is the judgment layer; the contracts file is the shape layer; `scripts/` are
the deterministic enforcement/render layer. Design-judgment canon (PDD tier semantics, Dan Brown
checklist, OOUX object anchoring — ratified prior-art 2026-07-03) lives in
`references/ia-principles.md`; lineage: Priority Guides (2012/2018) + Page Description Diagrams
(Dan Brown, 1999).

## The constitutional split (never violate)

"Layout" is two layers. This skill owns **(a) information structure** — blocks, tier 1/2/3
priority, grouping, primary task, scan path, within-page flow, link map, hero pick. It MUST NOT
fix **(b) composition** — sidebar vs topnav, single vs multi-pane, table vs bento, density, where
things sit, which widget renders what. Composition is `prototyping-ui-directions`'s variation
axis and the **user's choice**. Handing prototyping a fixed wireframe at round-1 would kill that
choice — so round-1 output is layout-OPEN by construction and deterministically linted for
composition leaks (contracts §i.4).

## Position in the pipeline — invoked TWICE (wraps prototyping)

```
I2R (WHAT/WHY) ──► IA round-1 ──► ◇ board gate ──► prototyping (hero: vary composition+visual)
                   whole-product     human approves        │ user picks LEAD
                   info-spec +       info structure        ▼
                   hero pick                          chassis LOCK (visual+motion+composition)
                                                           │
              IA round-2 ◄─────────────────────────────────┘
                   apply locked composition pattern to other screens
                   → grey-box wireframes ──► anchor-wave colors them (production_source)
```

- Sits AFTER `idea-to-requirements` (I2R owns features/WHAT/WHY). IA owns HOW-structure only;
  it never adds, removes, or re-decides features.
- **N=1 register, mandatory**: one run serves exactly ONE register (e.g. the app console OR the
  marketing site — never both). Multi-register product → separate runs, each its own IA + chassis.
  No register-maps, no auto-clustering. Input smells multi-register → stop and ask the user to
  split.
- Cross-page: static **link map** only. No wired multi-page journeys (that would balloon the
  downstream wave from mock into app).

## Topology

Runs **inline in the parent context** (like `prototyping-ui-directions`). Companions are invoked
by `Read`ing their SKILL.md (the `Skill` tool does not fire on project-local skills). Scripts run
via Bash. No fan-out — a whole-product info-spec is one coherent design judgment; splitting it
per-screen across subagents fragments the cross-screen consistency this skill exists to provide.

## Inputs (ask once, never invent)

1. **Raw material** at ANY of three altitudes: ① a functionality list ② detailed sections/screens
   ③ a main idea (a paragraph of intent). Mixtures are fine — normalization handles it.
2. **Register** (exactly one): which surface family this run serves (app / marketing / docs /
   admin…). If the material spans registers, ask the user to pick one for THIS run.
3. **Product name**.
4. **Output dir**, default `ui-lab/<date>-<product>-ia/` (in this lab's testbed:
   `testbed/runs/<date>-<product>-ia/`).

Missing/ambiguous → stop and ask. Never silently invent.

## Round-1 pipeline (built)

### Stage A — Normalize intake → `normalized-sections.md`

Detect the altitude, then normalize everything to ONE target granularity = **"detailed sections"**
(screen-sized units of the product, each with a one-line purpose):

- ③ main idea → **expand UP**: derive the sections such a product minimally needs. Every section
  not literally stated by the user is marked **`[ASSUMED]`** with one line of reasoning.
- ① functionality list → **decompose DOWN**: group functions into the screens that would carry
  them (a function used in two places appears in both, noted).
- ② detailed sections → keep as-is; only dedupe/merge obvious overlaps (noted).

**Iron rule: normalization NEVER invents features.** Expanding a bare idea may surface *structural*
necessities (a way in, a way to see results) — never new product capabilities. Anything that
smells like a feature decision gets `[ASSUMED]` + a question for the user; if the gaps are
blocking (you can't tell what the product does), STOP — that's I2R's job upstream, route there.

Output `normalized-sections.md`: the section list, each with purpose + provenance
(`stated` / `derived-from-<item>` / `ASSUMED`), plus open questions. If ASSUMED items are
load-bearing, confirm them with the user before Stage B. When the material is thin, co-create
the section/topic list WITH the user rather than filling gaps alone (ia-principles §Stage-A).

### Stage B — Whole-product IA design → `info-spec.json`

Design the information structure for EVERY screen of this register, per contracts §(i):

- **Screens** from the normalized sections (a section is usually a screen; merge/split where the
  task demands — note why).
- Per screen: `primary_task` (the ONE user job, one sentence — if you can't write it, the screen
  has no reason to exist yet: flag it); `blocks[]` with `tier` (1 dominates / 2 supports /
  3 ambient), `group`, and a **composition-free** `content_hint` (WHAT info, never arrangement —
  see the lint word list, contracts §i.4); `scan_path` (information-priority order of block ids —
  where the eye must land first/second/third to serve the primary task; NOT visual reading order);
  `within_page_flow` (information relationships: what surfaces what, what's subordinate — never
  the widget mechanism).
- **`archetype` (optional, contract v1.3)**: what KIND of surface this is, **derived from the
  `primary_task` you just wrote** — one of `landing-marketing` / `data-dashboard` / `canvas` /
  `narrative-scrolly` / `creative-eye` / `game-style` / `bubble-physics`. Never ask the user for
  it: the task you already wrote is the evidence, and the human corrects it at the Stage C gate
  they already walk. **Omit it when the task does not clearly imply a kind** — downstream degrades
  honestly to a flat prior, whereas an archetype asserted with nothing behind it is a guess wearing
  a contract's clothes. It is assigned PER SCREEN, because a product has surfaces of different
  kinds; and it is orthogonal both to the L3 style (what it looks like) and to `content_shape`
  (what shape of content it carries). Kinds, iron rules and the six-dimension weight priors:
  `prototyping-ui-directions/references/archetype-rules.md`.
- **`link_map`**: every cross-screen information hand-off (`from`/`to`/`via`), `external: true`
  for exits out of the register.
- **`task_paths[]` (optional, contract v1.1)**: declared task journeys — for each core job, the
  ordered screens the user walks (每跳必须是 link_map 真边，validator 强制；末站可为 external
  出口). The board renders them as subway strips so the gate reviewer walks JOURNEYS instead of
  staring at an edge list. Declared by you here, judged by the human at Stage C — a renderer may
  never auto-derive one.
- **Return rule (contract v1.2, ENFORCED; anchor = ENTRY, v1.2.1)**: every screen other than the
  **entry**（`entry_id`，缺省 = hero——hero 是核心任务屏，不一定是前门；两者不同时 hero 也要
  能走回入口）must be able to walk BACK to the entry along link_map edges — author explicit
  return edges, OR declare a global `return_convention`（把"每屏都有返回入口"的默契写进数据，board 会渲染它供人审）. Genuine
  terminal screens go in `return_overrides[]` on the user's explicit say-so only (record their
  words in run notes). Otherwise the validator BLOCKs — a screen you can enter but not leave is a
  defect, and "回得来" is a zero-taste invariant that belongs to the machine (origin: 2026-07-08,
  loop-ia-ab — the archived spec had zero return edges; every「← 返回」crumb lived outside the
  data, on unspoken habit).
- **Hero pick** (`hero_id`): the screen carrying the product's **primary job-to-be-done**;
  tie-break by structural representativeness (contracts §i.5). Name the runner-up and why it lost.

Design judgment guidance: tiers follow the primary task, not stakeholder politics (the thing the
user came to do is tier 1; context is tier 2; chrome/meta is tier 3). Groups follow information
kinship, not org chart. A screen with >7±2 top-level blocks is probably two screens. Every screen
must be reachable in the link_map (orphans = design smell, and the validator warns).
**Status-bearing blocks must name their EXPLANATION content in the content_hint, not just the
status vocabulary** — "each failed payout carries a failure reason; each in-transit item carries
an expected arrival", not merely "…and a paid / in-transit / failed status". Otherwise every
downstream surface can only restate the status, and a primary task phrased "explain…" is
structurally unachievable (2026-07-03 audit lesson, SP-C). Before
calling Stage B done, run the `references/ia-principles.md` checklist: PDD tier semantics
(vital / majority-function / useful-not-vital), Dan Brown's choices · disclosure · front-doors ·
focused-navigation · growth, and OOUX **object anchoring** (same domain object → same block shape
across screens — the round-2 consistency lever).

### Stage C — Validate → render → HUMAN GATE

```bash
python ${CLAUDE_PLUGIN_ROOT}/companions/information-architecture/scripts/validate_infospec.py <out>/info-spec.json
python ${CLAUDE_PLUGIN_ROOT}/companions/information-architecture/scripts/render_board.py <out>/info-spec.json --out <out>/board
```

Ask the run language up front (like I2R): a Chinese run = author the info-spec content in Chinese
+ render with `--lang zh` (chrome strings switch; content is always verbatim from the spec). The
lint covers CJK composition words too — same standard either language.

(In this lab, scripts live at `companions/information-architecture/scripts/`.)

- Validator BLOCKs (schema, referential, composition-leak) must be fixed in the spec — a lint
  override enters `lint_overrides` ONLY on the user's explicit say-so (record their words; same
  discipline as anchor-wave OV-1).
- `board/board.html` = grey-box schematic (single neutral column per screen, tier-sized boxes,
  scan badges, flow arrows list, product screen map with ★hero + back-to-hero ⚠, per-screen
  arrivals/departures, task-path subway strips when `task_paths[]` declared). `board/outline.md`
  = the same data as text. Both are pure renderings — regenerate, never hand-edit.
- **Review-walk discipline for the gate**: ①机器已管可达性（孤儿 WARN、走不回主屏 ⚠）②人查每条
  出边有没有合理返程 ③**沿每条 task_path 走一遍**——任务在屏间断在哪，一眼可见。
- Serve the board, have the **user review INFORMATION STRUCTURE only** (the board's banner says
  so: composition comes later). Iterate spec → re-render until approved. Record approval in run
  notes. **No prototyping work starts before this gate passes.**

### Handoff → prototyping (hero only)

Give `prototyping-ui-directions` the **hero screen's spec only** (+ register/product + the hero's
link_map rows), per contracts §i.6. The other screens' specs stay dormant until round-2. Variants
vary composition+visual ON TOP of the fixed info structure; each variant must honor
blocks/tiers/scan_path/flow (a variant that demotes a tier-1 block is off-spec, whatever it looks
like).

> Seam status: **APPLIED 2026-07-03** (user-approved proposal) — `prototyping-ui-directions`
> §Inputs 7 "IA info-spec" input mode + Stage-0 pre-fill + Stage-3 honor-the-structure rule +
> composition-pattern recording at chassis lock. Proposal record:
> `testbed/runs/2026-07-03-ia-mvp-verify/skill-edit-proposal-prototyping.md`.

## Round-2 — wireframes for the other screens (built 2026-07-03; spike record:
`round2-spike.md` in the build run; fixture-verified 2026-07-07 on loop-ia-ab —
declared-pattern path, `check_wireframe` ×3, and the Stage-F flag ruling loop all ran live)

Invoked by the USER after prototyping locks the chassis — never auto-fires. Inputs: the locked
chassis dir (`index.html` + `CHASSIS.md`), the round-1 approved `info-spec.json`, and the
non-hero screen list (default: all).

### Stage D — Extract the composition pattern → `composition-pattern.md`

- Source 1 (preferred): the composition pattern **declared in CHASSIS.md** (IA-fed locks record
  it — PUD §Batched step 1). Source 2 (fallback, unlabeled chassis): reverse-engineer the
  landmark skeleton from the hero `index.html` (top-level `nav/header/main/section/aside`,
  aria-labels, size hints) and flag the card `reverse-engineered` for user confirmation.
- The card MUST separate **shell regions** (persist on every screen — rail, ticker/strip) from
  **content regions** (arranged per screen), and state the **information-role → region mapping
  rules** (tier-1 work → primary region; "surfaced on demand" flow targets → detail region;
  `context` group → strip; ambient → shell edges). The reusable core is that mapping — not a
  fixed component list.
- Copy in the CHASSIS Agent Prompt Guide's **structural lines only** (derive-never-invent,
  layout rule e.g. hairline-rows-no-cards, density stance, stuck→flag). Visual + motion lines
  are explicitly left to wave's coloring — a wireframe carries neither, and must not preclude
  them (keep the slots motion needs).

### Stage E — Apply per non-hero screen → grey-box wireframes

- Assign the screen's blocks through the card's mapping rules (by tier / group / flow role).
  Arrangements come FROM the card; new region types are never invented.
- Author `<out>/wireframes/<screen-id>/index.html` per contracts §(ii): committed composition in
  DOM; grayscale only, system font, **no motion, no scripts**; root carries
  `data-ia-composition="<pattern>"`; every spec block appears exactly once as
  `data-ia-block="<id>" data-ia-tier="<n>"`; real content from content_hints (no lorem).
- **Flag, don't invent**: a block/flow with no card precedent renders in the most conservative
  slot (primary content region, tier order) with `data-ia-flag="no-hero-precedent"` + a visible
  dashed marker. Resolution is the user's at the Stage-F gate: accept placement / **extend the
  pattern card** (recorded → becomes precedent) / bounce the screen to a prototyping mini-batch.
- **Flow wiring preview（「flow→机制预案」）**: for every `within_page_flow` row touching this
  screen, the wireframe carries a design-time annotation naming the intended wiring mechanism
  UNDER THE COMMITTED COMPOSITION (inline expansion / anchor jump + highlight / cross-region
  sync / …). A flow whose mechanism would be awkward or infeasible in this composition gets
  `data-ia-flag` like any no-precedent case — the Stage-F reviewer must SEE the wiring
  consequence of a composition BEFORE committing it (origin: 2026-07-08 Loop review —
  issue-context's rail-vs-inline was a wiring-cost decision that only surfaced by collision).
  These annotations are design-time notes: the wave implements their meaning, never renders
  their text.
- **Recurring content shapes — flag "unify or vary", never auto-propagate.** IA round-2 is the
  cross-screen consistency lever, so a content shape that recurs across screens (a block whose
  `content_hint` is a hostable content role — the 8-term controlled vocabulary is `collection` /
  `comparison` / `sequence` / `metrics` / `spec` / `narrative` / `headline` / `figure`; the lab-side
  contract table lives at `testbed/material/content-roles.md`, which ships only with the lab
  checkout, so treat these eight as the vocabulary and that file as optional depth — appearing on
  more than one screen) is a consistency
  DECISION, not an automatic copy. Carry the role as a design-time annotation on the block (like
  the flow-wiring note above: the wave reads its meaning, never renders its text), and on its
  FIRST recurrence mark `data-ia-flag="content-shape-reuse"` with a one-line "unify (same
  treatment everywhere) or vary (each screen its own)?" question. Resolution is the user's at the
  Stage-F gate — never propagated before they answer. Each screen keeps its own item count, so
  downstream buildability is re-checked per screen (a shape that fits one screen can overflow
  another); a recurring shape with no hero precedent flags like any no-precedent case.

### Stage F — Check → human gate → hand to wave

```bash
python ${CLAUDE_PLUGIN_ROOT}/companions/information-architecture/scripts/check_wireframe.py \
  <out>/wireframes/<id>/index.html --spec <out>/info-spec.json --screen <id>
```

- Deterministic checks: block coverage exactly-once + tier match + root pattern attr (BLOCK);
  scripts/motion/external assets (BLOCK); non-greyscale color (WARN); flags reported (NOTE).
- **Human gate**: review wireframes + every flag — this commits composition, the last stop
  before coloring.
- Handoff: each wireframe = a wave page-list entry with `production_source: <path>` + the
  screen's morphology. Wave's IA-wireframe amendment (applied 2026-07-03) honors the committed
  composition and preserves `data-ia-block` markers in the output — still diff marker
  coverage/structure after coloring as verification.

## When to stop and ask

1. Any §Inputs item missing/ambiguous — especially **register** (multi-register material → user
   must split the runs; never auto-pick, never blend).
2. Stage A surfaces **blocking** feature gaps → route to I2R; load-bearing `[ASSUMED]` items →
   confirm before Stage B.
3. **The board gate** (Stage C): user approval of information structure is mandatory before any
   handoff to prototyping.
4. A composition-lint BLOCK the design genuinely needs → present to the user; only their approval
   puts the word in `lint_overrides`.
5. Round-2 start is the user's call (after chassis lock); the Stage-F wireframe gate and every
   `data-ia-flag` resolution (accept / extend card / bounce to prototyping) are user decisions.
6. Any edit to `prototyping-ui-directions` / `anchor-prototype-wave` → `skill-edit-proposal.md` +
   explicit user go-ahead first (lab rule). Never edit them from this skill directly.

## Hard boundaries

- **Never re-decide features** (I2R owns WHAT/WHY). Never invent scope during normalization.
- **Never fix composition in round-1 artifacts** — no wireframes, no x/y, no widget names in the
  info-spec (the lint enforces the known words; the spirit binds beyond the list).
- **Never auto-run downstream** — prototyping/wave are invoked by the user, not by this skill.
- All output under `<out>/`; in this lab, runs are gitignored churn — only skill files +
  contracts are tracked.
- Don't touch the deterministic scripts' gate logic casually — same governance as anchor-wave's
  validators (read whole file, propose, then edit).

## Anti-patterns

- Producing a wireframe (or a "suggested layout") at round-1. That kills the user's composition
  choice — the exact failure this skill was designed to avoid.
- `content_hint: "a table of payouts"` — that's composition. Say "each payout carries date,
  amount, destination, status".
- Treating `scan_path` as visual reading order. It is information priority for the primary task.
- Blending two registers into one run "to save time". N=1 is mandatory.
- Letting a reference product's composition leak into the spec (e.g. describing e2b's sidebar).
  References inform WHAT information matters, never WHERE it sits.
- LLM-scoring the IA quality. The board gate is a **human** gate (lab invariant: 视觉/品味/结构
  = 人评).

## File layout produced

```
<out>/
├── normalized-sections.md      ← Stage A (altitude-normalized, provenance-tagged)
├── info-spec.json              ← Stage B (SOURCE OF TRUTH, contracts §i)
├── board/
│   ├── board.html              ← Stage C grey-box schematic (pure render)
│   └── outline.md              ← Stage C text fallback (pure render)
├── composition-pattern.md      ← Stage D (round-2; shell/content regions + mapping rules)
├── wireframes/<screen-id>/index.html   ← Stage E (round-2; committed composition, grey)
└── run-notes.md                ← gate approvals, lint overrides + user words, hero runner-up,
                                  flag resolutions + pattern-card extensions
```

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

English: "design the information architecture" / "what goes on each screen" / "info spec" /
"IA round-1" / "screen map + hero pick" / "IA wireframes" (round-2, PHASE 2).

中文: "信息架构" / "信息结构" / "每屏放什么信息 / 谁主谁次" / "扫描路径 / 页内流" /
"先把信息层想清楚再做视觉" / "出 info spec / 屏幕地图"。
