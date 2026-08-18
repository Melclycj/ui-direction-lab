# Execution contracts — Motion Architecture shape layer (LOCKED)

> Canonical SHAPE layer for the motion/threed **execution registry**, the **runtime resolver**,
> the **pipeline-state artifact**, and the **chassis / sectional / atomic contracts**.
> Judgment layer = `prototyping-ui-directions/SKILL.md` (+ `anchor-prototype-wave/SKILL.md` downstream);
> enforcement layer = `scripts/` (PUD: registry sync + resolver + state; APW: preflight + atomic checks).
> Mirrors the `information-architecture/references/data-contracts.md` pattern: read this before
> producing or consuming any artifact below. Machine enums are enforced by
> `scripts/registry_lib.py` (single machine source; this doc explains semantics).
>
> Source-of-truth discipline (plan-ratified 2026-07-10): pool Markdown (`threed-pool.md` /
> `motion-pool.md`) stays canonical for description, provenance, mechanism evidence and human
> commentary. `execution-registry.json` is canonical ONLY for the normalized workflow fields
> below. A pool row carries a compact execution badge; the coverage check
> (`check_registry_sync.py`) requires every covered pool row ↔ exactly one registry record.

## 1 · The irreversible design sequence (state machine)

```text
CHASSIS_OPEN → CHASSIS_LOCKED → SECTIONAL_OPEN → SECTIONAL_LOCKED
             → BASE_WAVE_READY → ATOMIC_OPEN → COMPLETE
```

- **Monotonic**: no tool may move the state backward. Reopening a chassis is a NEW run
  (fresh state file), never a backward transition.
- **chassis** owns: visual language, global layout grammar + navigation, global scroll model,
  persistent WebGL/canvas stage (if any), a chassis-level 3D mechanism + its native 2D carrier
  (if any), motion vocabulary + token floor, performance ceiling + fallback policy, sectional
  and atomic budgets.
- **sectional** = ONE bounded per-surface PRIMARY orchestration (+ optional component-tier
  entries, §6 `component_scores` — structural pointer/click/load transforms; user-approved
  relax 2026-07-18), selected only after composition is known (`composition_ready=true`) and
  before Base Wave. Every entry (primary and component) must remain removable without
  invalidating adjacent sections, navigation, or the global scroll model.
- **atomic** = post-DOM decoration of existing UI under a no-reflow budget. Allowed mutations:
  transform / opacity / filter / color·border·shadow / pseudo-elements / small overlay canvas
  with no layout ownership. Forbidden: pinning, section-height change, grid/flex/template
  change, global scroll interception, navigation change, cross-section persistent state, new
  long-running heavy RAF outside the chassis budget.
- `composition_ready` semantics: IA-fed run → IA Round-2 Stage-F gate passed; single-page run →
  the selected chassis page structure is approved (chassis lock covers it).

## 2 · Registry record schema (`references/execution-registry.json`)

One record per covered pool row (selectable or explicitly not). Example (full form):

```json
{
  "id": "threed-pool:C-08",
  "source_pool": "threed-pool",
  "row_ref": "C-08",
  "title": "cinematic-scroll-cylinder",
  "selectable": true,
  "availability": "available",
  "tag_source": "pool-tags",
  "reference_scope": "full-page-demo",
  "supported_footprints": ["sectional", "chassis"],
  "preferred_footprint": "sectional",
  "allowed_phases": ["chassis", "sectional"],
  "driver": ["scroll"],
  "supported_carrier_scopes": ["section", "page"],
  "can_bound": true,
  "requires_global": false,
  "boundary_requirements": ["owner-wrapper", "local-progress-0..1", "stage-releases-on-exit"],
  "possible_mutations": ["local-section-height", "local-sticky-stage", "camera-state-within-owner"],
  "perf_cost": "medium",
  "perf_note": "…",
  "fallback": "static-chapter-sequence",
  "requires_existing_ui": false,
  "register_affinity": ["cinematic", "editorial"],
  "mechanism_family": "scroll-scrub-camera-stage",
  "material": "testbed/material/cinematic-scroll-cylinder",
  "evidence": "threed-pool C-08 🏷 tags (read-code)",
  "notes": "…"
}
```

**Defaults (a record may omit these; consumers apply them)**: `selectable:true`,
`availability:"available"`, `can_bound:true`, `requires_global:false`,
`requires_existing_ui:false`, `perf_note:""`, `notes:""`, `material:null`.
Non-selectable records (anchor-only / index-only / unavailable-source / not-graduated /
license-restricted) carry ONLY: id, source_pool, row_ref, title, selectable:false, availability,
evidence, notes — no fabricated classification fields (zero-guessing red line).
`license-restricted` = a real material exists but its license forbids the pipeline's default
(commercial) use — the resolver must never auto-nominate it; a human may knowingly deploy it in a
non-commercial context outside the resolver path.

**Field semantics**:
- `reference_scope` — how the SOURCE material is packaged, never an execution classification:
  `full-page-demo | section-demo | component-demo | technique | tutorial-demo | site-anchor | index`.
- `supported_footprints` ⊆ {chassis, sectional, atomic} — footprints the mechanism can
  honestly support. An agent may NOT self-declare a footprint outside this list.
- `preferred_footprint` — safest/default deployment for candidate ranking; never a runtime
  override.
- `allowed_phases` ⊆ {chassis, sectional, atomic} — explicit allowlist, never inferred from
  row position. Note: a component-level motion VOCABULARY effect (e.g. a text reveal) may be
  chassis-phase-allowed (Batch-2 tunes vocabulary) while its FOOTPRINT is not chassis — the
  Batch-2 restriction blocks candidates whose *effective footprint* is chassis, not everything.
- `driver` ⊆ {load, pointer, click, scroll, timeline, none} — pool 驱动 normalized:
  hover/drag/mousemove/touch → pointer; wheel/IntersectionObserver → scroll; auto-play →
  load or timeline; `none` = passive add-on riding a host mechanism.
- `supported_carrier_scopes` ⊆ {page, section, component, overlay}.
- `can_bound` — mechanism can be contained by one declared owner with a clean exit.
- `requires_global` — mechanism inherently requires page-level ownership.
- `boundary_requirements` — must be evidenced for a bounded deployment. Vocabulary:
  `owner-wrapper · local-progress-0..1 · stage-releases-on-exit · teardown-on-exit ·
  contained-canvas · scoped-input-listeners · wheel-interception-local ·
  no-global-scroll-hijack · no-nav-replacement · pause-offscreen · text-split-restores ·
  paired-asset · needs-bundler-inline`.
- `possible_mutations` — normalized CAPABILITIES (actual mutations come from the deployment
  contract). Vocabulary: `transform-only · opacity-filter · color-border-shadow ·
  pseudo-elements · overlay-canvas · dom-overlay-elements · dom-text-split ·
  dom-text-replacement · owner-canvas-stage · local-pin · local-sticky-stage ·
  local-section-height · layout-state-transition-within-owner · camera-state-within-owner ·
  color-narrative-zones · cross-section-persistent-state · global-scroll-hijack ·
  nav-replacement · body-input-interception`.
- `perf_cost` ∈ {light, medium, heavy} — normalized UPPER BOUND of the pool tier (轻→light,
  轻-中/中→medium, 中-重/重→heavy); nuance + measured fps live in `perf_note`.
- `fallback` — REQUIRED non-empty fallback identifier (weak-machine / reduced-motion strategy).
- `requires_existing_ui` — true only for DOM-targeted decorations that are meaningless
  without a concrete pre-existing target (atomic-native).
- `register_affinity` — SOFT field from pool 🏷 register; resolver marks mismatches ⚠️,
  never hard-filters (pool consumption contract rule 1).
- `mechanism_family` — same-family key for the "no duplicate mechanism in one batch" rule;
  families follow threed-pool §同机制族观察 (e.g. `velocity-sin-deform-rgb-split` covers
  C-04/C-06/C-26/C-28/C-33).
- `tag_source` ∈ {pool-tags, classified-from-row, none} — provenance of the classification:
  read-code 🏷 tags verbatim vs. derived from the row's own implementation prose (motion
  #1–#20; ratified via the Step-3 ambiguity report) vs. not classified.

## 3 · Runtime resolver I/O (`scripts/resolve_candidates.py`)

Runs BEFORE candidate cards are written, in every phase. The candidate gallery may show ONLY
`eligible`; excluded entries never become selectable cards (a summary count is fine).

**Input** (JSON file or stdin):

```json
{
  "phase": "sectional",
  "pipeline_state": "SECTIONAL_OPEN",
  "chassis_stage": null,
  "register": "ai-product",
  "carrier": {
    "owner_scope": "section",
    "bounded_container": true,
    "local_progress": "0..1",
    "releases_on_exit": true,
    "persistent_stage_scope": "section",
    "top_level_siblings_depend": false,
    "global_side_effects": [],
    "local_pin_allowed": true,
    "section_height_change_allowed": true
  },
  "perf_budget": "medium",
  "occupied_drivers": [],
  "candidate_ids": ["motion-pool:#15", "threed-pool:C-08"]
}
```

- `chassis_stage` ∈ {`batch1-directions`, `batch2-tuning`, null} — required when
  phase=chassis. `batch2-tuning` additionally excludes any candidate whose computed effective
  footprint is chassis (decision: Batch-2 tunes, never adds a chassis mechanism).
- `carrier.global_side_effects` ⊆ {document-scroll-controller, navigation-replacement,
  page-wide-background-state, body-input-interception}.
- atomic phase additionally passes `"atomic_policy": {…}` (§6) and per-candidate
  `"target": "<selector>"`.

**Effective-footprint rules** (computed from registry × proposed deployment; deterministic):
1. `owner_scope=page` or `persistent_stage_scope=page` → chassis.
2. `top_level_siblings_depend=true` → chassis.
3. any `global_side_effects` present → chassis.
4. proposed mutations include `nav-replacement | global-scroll-hijack |
   cross-section-persistent-state | body-input-interception` → chassis.
5. one bounded owner + local progress + releases-on-exit + no global side effects → sectional;
   local pin / sticky stage / internal chapters / local section-height stay sectional inside
   that owner. **Scroll length never determines footprint** (a 500svh/10000vh wrapper is still
   sectional when the stage enters and exits with the wrapper).
6. no-reflow mutations only (transform-only / opacity-filter / color-border-shadow /
   pseudo-elements / overlay-canvas / dom-overlay-elements) + component/overlay target → atomic.
7. The computed footprint MUST be ∈ the record's `supported_footprints` — an agent cannot
   self-declare an unsupported lower footprint; a full-page source demo MAY be legitimately
   adapted to a supported bounded sectional deployment.

**Filter chain** (order; first hit wins the exclusion reason):
`NOT_SELECTABLE` → `PHASE_NOT_ALLOWED` → `FOOTPRINT_UNSUPPORTED` (rule 7) →
`INELIGIBLE_CHASSIS_LOCKED` (effective=chassis while pipeline_state ≥ CHASSIS_LOCKED) →
`CHASSIS_MECHANISM_IN_TUNING` (batch2-tuning + effective=chassis) →
`NOT_ATOMIC_SAFE` (phase=atomic + effective ≠ atomic) →
`DRIVER_CONFLICT` (candidate driver ∩ occupied_drivers; scroll-choreography exclusivity) →
`PERF_OVER_BUDGET` (perf_cost > perf_budget AND no fallback accepted; with a declared
fallback the candidate stays eligible carrying `condition:"fallback-required"`) →
`MISSING_FALLBACK` (empty fallback on medium/heavy) → eligible.
`REGISTER_MISMATCH` is a ⚠️ WARNING on an eligible candidate, never an exclusion.

**Output**:

```json
{
  "resolver_version": 1,
  "input_digest": "sha256:…",
  "phase": "sectional",
  "eligible": [
    {"id": "motion-pool:#15", "effective_footprint": "sectional",
     "fit_reason": "local pinned stage; one section; medium budget",
     "warnings": [], "conditions": []}
  ],
  "excluded": [
    {"id": "threed-pool:C-03", "reason": "PERF_OVER_BUDGET", "detail": "heavy > medium, fallback not accepted"}
  ]
}
```

Resolution records are written to `<out>/motion/resolutions/<phase>-<seq>.json` and are the
EVIDENCE preflight verifies. `input_digest` makes tampering detectable.

### 3.1 · Content-role pre-filter (OPTIONAL upstream stage, default OFF)

An OPTIONAL `content_shape` input turns on a deterministic upstream stage that filters/discovers
candidates by whether their **material** can host the block's content (Job 2a). It sits BEFORE the
mechanical filter chain above — "two levels, not a replacement". **When `content_shape` is absent
the stage is a complete no-op and the output is byte-for-byte identical to a run without it** (the
only zero-regression contract that matters here).

```json
{ "…": "all fields as §3",
  "content_shape": { "role": "comparison", "items": 3, "density": "sparse" } }
```

- `content_shape.role` — a content role a material may declare in its manifest `content_roles.hosts`
  (see `testbed/material/content-roles.md`). `items` — positive integer. `density` — free string;
  only `"dense"` triggers the many-field capability check.
- **Source of truth**: content roles live ONLY on the material manifest and are reached via each
  registry record's `material` back-ref → `<material-root>/<slug>/manifest.json` `content_roles`
  (`--material-root` defaults to `testbed/material`; tests point it at fixtures). A material that is
  decorative (`content_roles: null`) / untagged (no key) / unreadable simply does not host.
- **Two modes**: with `content_shape` and NO `candidate_ids` → **DISCOVERY** (every SELECTABLE record
  whose material hosts the role becomes a candidate, cleanest-first). With `content_shape` AND explicit
  `candidate_ids` → **FILTER** (only those are considered). `candidate_ids` stays REQUIRED when
  `content_shape` is absent.
- **Two new exclusion reasons**, checked upstream of the whole §3 chain (stage 0):
  `CONTENT_ROLE_NOT_HOSTED` (material's manifest does not host the role) →
  `CONTENT_ROLE_UNFIT` (①buildability: item count out of the role's `fit.items` range, or dense content
  vs a non-dense-capable `fit.density`). Survivors flow into the unchanged mechanical chain.
- **Output additions** (present ONLY when `content_shape` is active): top-level `content_shape` echo +
  `native_hint` (the native 铁律 — native is ALWAYS an option; the hint flags when it likely WINS:
  dense, comparison > 8 items, or role = spec). Each eligible entry gains a `content_role`
  `{role, preserves[], breaks[], notes[]}` block. The resolver never removes native and never picks —
  a human still chooses from the honest menu.
- **Affordance axes** (`require`, added 2026-08-01 — user-ruled "complete per axis"): `content_shape`
  MAY carry `"require": {"viewing": [<acceptable>], "composition": [<needed>]}`. Controlled vocab
  (source of truth `testbed/material/content-roles.md` Layer B): viewing ∈ {one-at-a-time, several,
  all} — the material's declared value must be IN the acceptable list ("don't need all-visible" =
  omit `all`); composition ∈ {image-only, text-only, captioned-image} — the material's declared list
  must CONTAIN every needed value. Materials declare per role under `by_role[role].affordances`
  (single-item roles omit `viewing` by construction). Unmet → exclusion reason
  **`CONTENT_AFFORDANCE_MISMATCH`** (detail names the axis + declared vs required), checked after
  buildability, before the mechanical chain. A require naming an axis the material never declared
  also excludes (detail "未声明"). Unknown require values/axes = INPUT ERROR (exit 1). When `require`
  is present each eligible `content_role` block also echoes the material's `affordances`. No
  `require` → behavior and output byte-identical to the pre-axes resolver (golden-diff enforced).

## 4 · Pipeline-state artifact (`<out>/motion/pipeline-state.json`)

```json
{
  "state": "SECTIONAL_OPEN",
  "run": "<run-id>",
  "chassis_ref": "<locked chassis path>",
  "chassis_locked": true,
  "composition_ready": true,
  "page_scoped_mechanism": null,
  "sectional_status": "pending",
  "atomic_status": "not-open",
  "user_approvals": {"chassis": "<verbatim>", "sectional": null, "atomic_policy": null},
  "state_log": [
    {"at": "<ISO>", "from": "CHASSIS_OPEN", "to": "CHASSIS_LOCKED", "by": "user-approval", "evidence": "<verbatim words / gate ref>"}
  ]
}
```

- Transitions ONLY via `scripts/pipeline_state.py transition` — it enforces monotonic order,
  appends to `state_log`, and refuses when required evidence is missing (e.g. →SECTIONAL_LOCKED
  needs every selected surface to carry a valid resolution record; →BASE_WAVE_READY needs
  sectional_status ∈ {selected, skipped}).
- `sectional_status` ∈ {not-open, pending, selected, skipped}; `atomic_status` ∈
  {not-open, policy-approved, patched, verified}.
- The model NEVER self-approves a user gate: `user_approvals.*` must quote the user verbatim
  (same discipline as `.goals/pipeline-gate.json`).

## 5 · CHASSIS.md Motion Architecture block (written at lock)

```text
## Motion Architecture
- global_scroll_model: <native | smoother | none-hijacked>
- persistent_3d_stage: <null | description + owner>
- page_scoped_mechanism: <null | registry id + deployment note>
- chassis_mechanism_ids: [<registry ids locked INTO the chassis>]
- motion_stance: <locked Batch-2 vocabulary, e.g. "Slice">
- performance_ceiling: <light | medium | heavy>
- reduced_motion_strategy: <one line>
- sectional_budget: <max 1 primary orchestration per surface (+ component tier per §6); perf tier cap>
- atomic_budget: <max_targets N; allowed properties; perf tier cap>
```

`page_scoped_mechanism=null` is a VALID and common stance (static visual chassis).

## 6 · Per-surface sectional contract & atomic policy/result

Sectional (in `<out>/motion/sectional-score.json`, keyed by surface slug; at most ONE primary
orchestration per surface; `null` valid and default):

```json
{"sectional_score": {"target": "approach", "mechanism": "motion-pool:#15",
  "carrier": "local-pinned-stage", "driver": "scroll", "fallback": "static-sequence",
  "resolution_record": "motion/resolutions/sectional-001.json"}}
```

**Component tier** (optional `component_scores` array beside `sectional_score`; added
2026-07-18 per user-approved relax, Averonel option-2): additional STRUCTURAL/component
sectional transforms on the same surface (register→bento card wall, list→drawer). Each entry
carries the same fields and the same rigor as the primary (registry mechanism, resolver
eligibility at phase=sectional, fallback, resolution_record). Machine-enforced boundaries:

- `driver` MUST be declared, MUST be `pointer` | `click` | `load` (never `scroll`/`timeline`
  — scroll orchestration stays EXCLUSIVE to the single primary `sectional_score` slot), and
  MUST appear in the mechanism's registry `driver` list.
- every component entry must remain independently removable (same removability rule as the
  primary); family-dup across surfaces still WARNs (user must knowingly accept).
- `component_scores` with `sectional_score: null` is valid (components without a primary).

```json
{"sectional_score": null,
 "component_scores": [
   {"target": "terms-register", "mechanism": "motion-pool:#26", "carrier": "bento-card-wall",
    "driver": "click", "fallback": "static-cards",
    "resolution_record": "motion/resolutions/sectional-002.json"}]}
```

Atomic policy (approved by user BEFORE Atomic Pass; `<out>/motion/atomic-policy.json`):

```json
{"atomic_policy": {"enabled": true, "max_targets": 3,
  "allowed_properties": ["transform", "opacity", "filter", "color", "border", "shadow"],
  "allow_overlay_canvas": false, "no_reflow": true, "performance_budget": "light"}}
```

Atomic result (per surface, after the pass; `<out>/motion/atomic-result-<surface>.json`):

```json
{"atomic_result": {"surface": "services",
  "effects": [{"target": "[data-feature='workflow-audit']", "mechanism": "motion-pool:#8",
               "resolution_record": "motion/resolutions/atomic-001.json"}],
  "layout_diff": "pass", "reduced_motion": "pass"}}
```

The user approves the atomic POLICY, not each effect; the agent adds eligible effects within
it; final human gallery review closes the pass.

## 7 · Preflight teeth (enforced, not advisory)

- **Base Wave spawn** requires: state ≥ SECTIONAL_LOCKED (i.e. chassis_locked=true,
  composition_ready=true, sectional_status ∈ {selected, skipped}) + a valid, digest-intact
  resolution record for every selected mechanism. Enforced by APW
  `scripts/preflight_wave.py` (exit≠0 blocks) + the project hook `pipeline-gate.js`
  (deterministic backstop).
- **Atomic Pass** requires: state = BASE_WAVE_READY + approved atomic policy. Patching captures
  before/after layout geometry (bounding rects); ANY drift → revert + block.
- Missing / stale / tampered resolver records → preflight BLOCK (case 8 of the test matrix).

## 8 · Compatibility guarantees

`sectional_score=null`, atomic disabled, and existing 2D/chassis-only runs remain fully valid
(no-effect paths are first-class). Runs that predate this contract (no
`motion/pipeline-state.json`) are legacy: the preflight only enforces when the state file
exists for the run — the pipeline-gate sentinel discipline still applies to them unchanged.
