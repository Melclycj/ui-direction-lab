# IA data contracts — LOCKED v1 (2026-07-03)

> v1.2.1 (2026-07-08): OPTIONAL `entry_id` — the return rule (and the board's ⚠) anchors to the
> register's **ENTRY screen**, not to the hero: hero = primary-JTBD carrier (§i.5) and is not
> necessarily where the user starts (user catch, same day). Defaults to `hero_id`, so every
> existing spec behaves identically; when declared, the hero itself must also walk back to entry.
> v1.2.0 (2026-07-08): **return-path ENFORCEMENT** (user-ratified: no approval step — machine
> rule with a human override valve). Every non-hero screen must be able to WALK BACK to the hero
> along non-external `link_map` edges, OR the spec declares a global `return_convention` (e.g.
> "每屏 masthead 带返回总览入口"), OR the screen is listed in `return_overrides[]` (a genuine
> terminal screen — user's explicit say-so only, same discipline as `lint_overrides`). Otherwise
> BLOCK. Migration note: older specs with one-way link maps (e.g. the loop-ia-ab archive) now
> FAIL until they add return edges or declare a convention — that is the rule having teeth.
> v1.1.0 (2026-07-08): OPTIONAL `task_paths[]` added to §i (declared task journeys; the board's
> subway view renders them, the validator enforces every hop is a real `link_map` edge). Origin:
> loop-ia-ab SP batch 2 — the human reviewer needs to walk journeys, and a journey cannot be
> derived deterministically from screens+link_map (deriving = judgment, renderers only project).
> Backward compatible: specs without the field validate and render exactly as before.
> v1.0.1 (2026-07-03): CJK lint terms added to §i.4; tier comment wording PDD-aligned per
> ratified prior-art (`references/ia-principles.md`). Prose-only — no shape change.

The (F) schemas from `.goals/plans/ia-companion.plan.md` Step 2, finalized. Everything in the
`information-architecture` skill keys off this file: the SKILL.md prose produces artifacts that
MUST match these shapes; the deterministic scripts (`scripts/validate_infospec.py`,
`scripts/render_board.py`) enforce and render them. Change this file only with a version bump +
a re-read of every consumer.

**Three artifacts, one source of truth**: the **info-spec** (i) is the source data. The **review
board** (iii) and the outline are pure renderings of it. The **wireframes** (ii) are the round-2
projection of it through a locked composition. Nothing downstream re-decides what the info-spec
settled; nothing here decides what it deliberately leaves open (composition).

---

## The constitutional split (linchpin — never violate)

"Layout" is TWO layers:

| Layer | Owner | Varies? | Examples |
|---|---|---|---|
| **Information structure** | IA (this skill) | FIXED — all variants share it | which blocks a screen holds, tier 1/2/3 priority, grouping, primary task, scan path, within-page flow, cross-screen links, hero pick |
| **Composition** | `prototyping-ui-directions` | VARIED — user picks | sidebar vs topnav, single vs multi-pane, table vs bento, density, where the hero block sits, widget choice (modal vs inline) |

The info-spec MUST stay **composition-free**. Anything answering "where does it sit / what widget
renders it" is composition and is prototyping's to vary. This is deterministically linted (§i.4).

---

## (i) info-spec v1 — round-1 output; what prototyping intakes

One JSON file per run: `<out>/info-spec.json`.

### i.1 Shape

```jsonc
{
  "spec_version": 1,
  "register": "app",                  // the SINGLE register this run serves (N=1, mandatory).
                                      // A string, never an array. Multi-register product → run again.
  "product": "Tally",
  "hero_id": "reconcile",             // must be a screens[].id — see hero-pick criterion §i.5
  "entry_id": "reconcile",            // OPTIONAL (v1.2.1) — the register's ENTRY screen (where a
                                      // session starts). Defaults to hero_id. The v1.2 return
                                      // rule + board ⚠ anchor HERE — hero is the primary-JTBD
                                      // screen and may be a deep working screen, not the front door.
  "lint_overrides": [],               // optional; each entry = a word from the lint list the user
                                      // explicitly approved in THIS run (human-gated, like wave OV-1)
  "screens": [
    {
      "id": "reconcile",              // kebab-case, unique across screens[]
      "title": "Reconcile",
      "route": "/reconcile",
      "primary_task": "clear yesterday's mismatches before standup",   // ONE user job, one sentence
      "scan_path": ["unreconciled-total", "recon-items", "item-detail"],
      // ordered blocks[].id refs — where the eye must land 1st, 2nd, 3rd to serve primary_task.
      // INFORMATION priority order, NOT visual/reading order (composition decides where things sit).
      // Entries MUST reference blocks[].id (validator-enforced). Task *actions* live in
      // primary_task / within_page_flow, not here.  [refined from the plan draft, which mixed
      // an action ("resolve") into the path — dropped so the field is deterministically checkable]
      "blocks": [
        {
          "id": "unreconciled-total",
          "label": "Unreconciled money figure",
          "tier": 1,                  // 1 = primary (dominates) · 2 = secondary · 3 = tertiary
          "group": "work",            // free string; blocks sharing a group belong together
          "content_hint": "the single number that says how much money is still unexplained today"
          // WHAT information is present — NEVER how it is arranged. No table/rows/cards/grid/…
          // tier (PDD-aligned, see ia-principles.md): 1 vital-to-understanding ·
          // 2 functions-well/majority · 3 useful-not-vital
        }
      ],
      "within_page_flow": [
        {
          "from": "recon-items.item", // blocks[].id, optionally with a `.sub` suffix whose prefix
                                      // must still be a valid blocks[].id (validator-enforced)
          "trigger": "select",        // the user act (select / expand / submit / filter / …)
          "to": "item-detail",        // blocks[].id
          "relationship": "detail is secondary, surfaced on demand"
          // names the INFORMATION relationship (what surfaces what, what's subordinate) —
          // NEVER the UI mechanism (side-pane vs modal vs inline-expand = composition)
        }
      ]
    }
  ],
  "link_map": [
    { "from": "reconcile", "to": "transaction-detail", "via": "select an item → its full record" },
    { "from": "reports", "to": "docs-site", "via": "help link out of the console", "external": true }
    // from/to must reference screens[].id UNLESS "external": true (an exit out of this register —
    // marketing site, docs, third-party). External exits are labels only; they get NO screen spec.
  ],
  "return_convention": "每屏 masthead 带返回总览入口",
  // OPTIONAL (v1.2) — a GLOBAL return convention, declared in data instead of relied on by
  // unspoken habit. When present (non-empty string), it satisfies the return rule for every
  // screen; the board renders it so the gate reviewer judges the convention itself.
  "return_overrides": [],
  // OPTIONAL (v1.2) — screen ids exempted from the return rule (genuine terminal screens).
  // Populated ONLY on the user's explicit say-so (record their words in run notes — same
  // discipline as lint_overrides). Stale/unknown entries WARN.
  "task_paths": [                     // OPTIONAL (v1.1) — declared task journeys for the board's
    {                                 // subway view. Human-authored at Stage B, human-reviewed at
      "id": "clear-mismatches",       // the board gate. kebab-case, unique across task_paths.
      "label": "clear yesterday's mismatches end to end",   // the user job (linted like primary_task)
      "path": ["reconcile", "transaction-detail", "reconcile"]
      // ordered journey, ≥2 entries. Every entry is a screens[].id; the LAST entry may instead be
      // an external link_map target (journeys may END at an exit, never pass through one).
      // TEETH: every consecutive hop (path[n] → path[n+1]) MUST exist as a link_map edge in that
      // direction — a declared journey the link_map cannot carry is a BLOCK (§i.3 family).
      // Renderers only PROJECT these; nothing may auto-derive a journey (that would be judgment).
    }
  ]
}
```

### i.2 Required / optional

Required: `spec_version` (=1) · `register` (single string) · `product` · `hero_id` · `screens[]`
(≥1) · per screen `id/title/route/primary_task/blocks[]` (≥1 block) · per block
`id/label/tier/group/content_hint`. Optional: `scan_path` (WARN if absent — a screen without a
priority path is usually under-designed) · `within_page_flow` · `link_map` · `lint_overrides` ·
`task_paths` (v1.1 — per entry `id/label/path[]` all required).
Every screen SHOULD have ≥1 tier-1 block (WARN otherwise: a screen where nothing dominates has no
information hierarchy yet).

### i.3 Referential rules (validator BLOCKs)

- `hero_id` ∈ screens ids; screen ids unique; block ids unique within a screen.
- `scan_path[*]` ∈ that screen's block ids.
- `within_page_flow[*].from` (prefix before optional `.sub`) and `.to` ∈ that screen's block ids.
- `link_map[*].from/.to` ∈ screen ids unless `external: true`.
- `tier` ∈ {1,2,3}. `register` is a non-empty string (an array = hard error: N=1 is mandatory).
- `task_paths[*]` (v1.1, when present): `id` unique across task_paths; `path` ≥2 entries; every
  entry ∈ screen ids EXCEPT the last, which may be an external `link_map` target; every
  consecutive hop must exist as a `link_map` edge in that direction. `label` is composition-linted
  (§i.4 fields list gains `label` of task_paths).
- Coverage (v1.1, fires only when `task_paths` is non-empty): a screen visited by NO task_path →
  WARN (journey set incomplete, or the screen is questionable); a `link_map` edge used by NO
  task_path → NOTE (navigation convenience is fine). Semantic alignment of a journey's `label`
  with the screens' `primary_task`s stays HUMAN — the board gate's review-walk, never a machine
  check.
- Return rule (v1.2, BLOCK; anchor refined v1.2.1): every screen other than the **entry**
  (`entry_id`, default `hero_id`) must reverse-reach the ENTRY along non-external `link_map`
  edges — the hero itself included when it is not the entry — UNLESS `return_convention` is
  declared (non-empty string; linted §i.4) or the screen is in `return_overrides[]` (NOTE when
  used; WARN on stale/unknown entries). `entry_id` when present must be a screens[].id.
  Single-screen specs are exempt. `return_convention` present but empty/non-string → BLOCK
  malformed.

### i.4 Composition lint (deterministic; the linchpin's teeth)

Linted fields: `label`, `content_hint`, `primary_task`, `relationship`, `via`. Word-boundary,
case-insensitive.

- **BLOCK words** (unambiguous UI mechanisms): `table, grid, card, cards, sidebar, side-pane,
  pane, modal, drawer, accordion, tab, tabs, carousel, bento, kanban, navbar, topnav, dropdown,
  tooltip, masonry, breadcrumb, hero-section, column, columns, row, rows`
- **WARN words** (often-but-not-always composition; human judges): `list, chart, panel, tile,
  badge, pill, header, footer, button, toggle, strip, banner, widget`
- **CJK terms** (substring-matched — no word boundaries in CJK; multi-char terms only, single
  chars like 行/列 would false-positive on ordinary prose): BLOCK = `表格 网格 卡片 侧边栏 侧栏
  弹窗 模态框 抽屉 折叠面板 标签页 页签 轮播 看板 导航栏 顶栏 下拉菜单 面包屑 分栏 双栏 三栏
  瀑布流`; WARN = `列表 图表 面板 磁贴 按钮 横幅 弹层 开关`. A Chinese-language spec is linted
  to the same standard as an English one — say "走势" not "图表", "每笔打款带有…" not "打款表格".

A BLOCK fails validation (exit 1) unless the word is in `lint_overrides` — and an override may
only enter that array by the **user's** explicit say-so in the run (record their words in the run
notes; same discipline as wave OV-1 overrides). Say "trend over time", not "line chart"; say
"each item carries expected amount, posted amount, difference, status", not "a table with 4
columns".

### i.5 Hero-pick criterion (settled)

**hero = the screen carrying the product's primary job-to-be-done** — where this register's user
accomplishes the core task most often / at highest stakes. Tie-breaker (secondary only): the more
structurally representative screen (richer superset of block kinds), so the chassis built on it
generalizes further at round-2. The skill must name the runner-up and why it lost.

### i.6 What prototyping receives

The **hero screen's entry only** (plus `register`, `product`, and the hero's `link_map` rows for
mocked-link context) — NOT the whole spec. Round-1 emits specs for ALL screens, but the other
screens stay dormant until round-2; feeding them to prototyping would tempt it to design the whole
product. Prototyping varies composition + visual ON TOP of this fixed info structure; every
variant must honor blocks/tiers/scan_path/flow.

---

## (ii) wireframe artifact v1 — round-2 output; what anchor-wave intakes

**Form: grey-box HTML** (locked; layout-JSON rejected — wave already has a `production_source`
path that reads an HTML page, and a grey-box page is directly human-reviewable).

- One file per non-hero screen: `<out>/wireframes/<screen-id>/index.html`.
- **DOM structure COMMITS the locked composition** (real landmarks — nav/aside/main/section — in
  their committed positions, the pattern extracted from the locked chassis), but **unstyled/grey**:
  grayscale only, system font stack, no chassis tokens, no motion, no brand.
- **Traceability markers (required)**: the root carries
  `data-ia-composition="<pattern-name>"`; every info-spec block renders as an element with
  `data-ia-block="<block-id>" data-ia-tier="<n>"`. Deterministic check: every block id in the
  screen's info-spec appears exactly once in its wireframe.
- **Flag-don't-invent**: a non-hero screen whose info structure has no hero precedent gets a
  visible `data-ia-flag` placeholder + a note in the run report — never an invented composition.

### The wave seam (VERIFIED against `anchor-prototype-wave` SKILL.md §Inputs)

Wave's `production_source` behavior is: *"The subagent reads this file to extract the section
list + state shape + affordances"* — then **RE-AUTHORS the DOM**. It does NOT paint the wireframe
verbatim, so the committed composition CAN drift in today's wave.

**Contract status: wave-side amendment APPLIED 2026-07-03** (user-approved proposal, record:
`skill-edit-proposal-anchor-wave.md` in the build run): a `production_source` carrying
`data-ia-*` markers is honored — coloring, not re-composing — and the `data-ia-block` markers
are preserved in the output DOM. Verification discipline stays: after coloring, diff marker
coverage/structure against the wireframe (plan Step 9 does this on the fixture).

Everything else about the wave run is unchanged: wave stays hi-fi mock (not production);
within-page flow is kept; cross-page = static link map + mocked links (wave §Authoring rule 6);
NO cross-page wired journey.

---

## (iii) review board v1 — the human gate's artifact

`scripts/render_board.py` renders `info-spec.json` → `board.html` + `outline.md`. **Both are pure
renderings of (i)** — one data, two views; regenerate any time, never hand-edit.

### board.html (grey-box schematic — deliberately NOT a composition)

- **Per-screen strip**: neutral **single column**, full-width grey boxes — one per block.
  - **Order** (deterministic): scan_path blocks first in scan_path order, then remaining blocks by
    tier ascending, then spec order. **Size by tier**: tier 1 tall / tier 2 medium / tier 3 short.
  - Annotations: numbered scan-path badges (①②③) on the boxes; group name on each box's edge;
    the screen's `primary_task` as a banner; within-page-flow rendered as an arrow list
    (`from —trigger→ to: relationship`) under the strip.
- **Product screen map**: one node per screen (hero flagged ★), `link_map` edges rendered as a
  labeled edge list (via + external marker). No graph layout engine — a wrapped node row + edge
  list is enough to review completeness.
- **Review-walk views (2026-07-08)**: per-screen **arrivals/departures** lists (projection of the
  screen's `link_map` rows); a **back-to-hero reachability ⚠** on map nodes that cannot walk back
  to the hero along non-external edges (suppressed when `return_convention` is declared — the
  convention line renders instead, so the reviewer judges the convention; enforcement lives in
  the validator, v1.2); and, when `task_paths[]` (v1.1) is present, a **task-path subway view** —
  one strip per declared journey, hops annotated with the edge's `via`. All pure projections; the
  renderer never invents a journey.
- **Style guard**: grayscale + ONE muted annotation ink only; system fonts; boxes deliberately
  ugly-neutral. A visible banner states: **"SCHEMATIC — information structure only. Composition
  (where things sit, what widgets) is decided later in prototyping. Review WHAT/priority/flow,
  not looks."** This is what keeps the reviewer judging information, not layout.

**Language**: `render_board.py --lang en|zh` switches the board/outline **chrome** strings
(banner, PRIMARY TASK/主任务, flow headings…); the **content** always comes verbatim from the
info-spec, so a Chinese review board = a Chinese-authored info-spec + `--lang zh`. One data,
either language of rendering.

### outline.md (fallback + diffable)

The same data as a markdown outline: per screen — title/route/primary_task, blocks as a tier-tagged
list with content_hints, scan path, flow lines; then the link map. Zero-cost fallback because the
info-spec is the source data anyway.

### Gate protocol

Human-gated BEFORE prototyping: user reviews board (or outline), edits/approves **information
structure only**. Approval recorded in the run notes. Only then does the hero spec go to
prototyping.

---

## Script-vs-prompt boundary (settled)

| Work | Where | Why |
|---|---|---|
| Schema + referential checks + composition lint | `scripts/validate_infospec.py` (deterministic) | known failure patterns → regex/structure gates, lab style |
| Board + outline rendering | `scripts/render_board.py` (deterministic) | pure projection of data; must not "improve" anything |
| Altitude normalization, IA design (blocks/tiers/scan/flow), hero pick, round-2 composition generalization | SKILL.md prose (AI judgment) | design judgment; quality is **human-evaled at the board gate** — no LLM scoring of IA, no SkillOpt (lab invariant) |
