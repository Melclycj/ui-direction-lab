---
name: anchor-prototype-wave
version: 1.5.0
description: >
  Take a locked visual anchor (chassis tokens) + a page list and produce
  a reviewable hi-fi prototype wave: master gallery index.html + N per-surface
  <slug>/index.html files. Spawns parallel surface subagents under strict
  write-scope, runs deterministic Python validators (regex checks for known
  failure patterns), LLM grader, scorer with maturity-aware floor, and a
  fix-on-fail loop up to 3 retries. Pairs upstream with
  `prototyping-ui-directions` (for variant exploration before the anchor
  is locked). Trigger: "generate the wave from this anchor",
  "make hi-fi mocks from chassis + pages".
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# anchor-prototype-wave

Concise spec for producing a reviewable hi-fi prototype wave from a locked chassis. Python validators (`scripts/`) do the actual enforcement; this file tells the model how to orchestrate the pipeline and when to escalate.

**Upstream**: `prototyping-ui-directions` (variant exploration before chassis lock). **Downstream**: see §Compatible standalone companions.

## Inputs (ask once, never invent)

1. **Anchor**: typography, radius scale, hairline, accent, banned tokens,
   status colors, surface colors, text colors, spacing scale, micro shadow.
2. **Page list**: each entry has `slug`, `title`, `route`, `intent`, `group`,
   `morphology` (one of: overlay, drawer, wizard, canvas, form, list, full-page,
   dashboard, inspector, audit-view, chat, command-tool), `maturity` (mature |
   creative | marquee), AND **one of**:
   - `production_source`: path to the page in your existing codebase. The
     subagent reads this file to extract the section list + state shape +
     affordances. Preferred when re-skinning an existing app.
   - `must_have[]`: 4-8 concrete affordances per page, written by hand
     (e.g. "inline-editable title column", "bulk-select + bulk-action bar",
     "status pill clickable to cycle"). Required for greenfield prototyping
     where there is no production file to ground against.
   - `verbatim_source`: path to an ALREADY-APPROVED page (the locked chassis
     hero dir, or a surface kept from a previous wave). The parent COPIES it
     verbatim instead of authoring — use when the screen already passed a
     human gate. A wave that wires navigation (`wire_navigation`) should
     include the product's hero screen this way, so the output is a complete
     product, not orphan sub-screens. Verbatim entries need no contract /
     `must_have` (they are not re-authored) and are exempt from the
     "stops and asks" rule below.

   Also optional: `must_not_have[]` (forbidden patterns), `content_brief`
   (free-form notes).

   One-line `intent` is **not a spec on its own**. Without either
   `production_source` or `must_have[]` ≥ 4 items, the skill stops and asks —
   the validator's `required_mvp_affordances` gate (min 3) is non-negotiable.

   > **Morphology labels are validator-backed — pick the one that matches the DOM you'll build.**
   > A few carry deterministic requirements in `validate_surface.py`; the one that recurs as a
   > mislabel: **`inspector` means a *tabbed* inspector** (the validator requires `role="tab"` or
   > `data-tab=`). A stacked single-column record/detail page (header → sections → actions, no
   > tabs) is **`full-page`** — or **`audit-view`** for an evidence/record view — both of which
   > have no tab requirement. Labeling a stacked detail page `inspector` triggers a
   > `surface_morphology` gate_0 BLOCK/REDO. When unsure between the two, prefer `full-page`.

   **IA-wireframe production sources (detectable via `data-ia-*` markers).** If the
   `production_source` file carries `data-ia-composition` on its root + `data-ia-block` markers,
   it is an `information-architecture` round-2 wireframe: its composition is **already decided
   and human-gated — HONOR it, do not re-derive.** Keep the wireframe's landmark/region structure
   and every block's placement as-authored; the wave's job on such a source is to APPLY the
   chassis (tokens, type, spacing, states, motion per §Authoring) — coloring, not re-composing.
   **Preserve the `data-ia-block` markers in the output DOM** (they make composition fidelity
   diffable downstream). `data-ia-flag` elements arrive pre-resolved by the IA gate — their
   placement is committed too. Everything else is unchanged: §Authoring universal rules, the MVP
   footer (checklist derived from the wireframe's blocks + contract), all validators and
   morphology gates still apply.

   **Coloring-mode wiring emphasis.** A coloring author's attention drifts to fidelity (keep the
   structure, preserve markers, apply tokens) — and interaction-wiring quality was observed to
   drop relative to freely-composing authors (2026-07-07 Loop A/B run: affordance-lens findings
   0/5/1 vs 0/2/2, wiring MAJORs concentrated on the wireframe-sourced line). Composition is
   already decided, so REINVEST the freed attention into wiring. Self-check every interactive
   element before returning: (1) state-changing controls carry `aria-pressed`/`aria-checked` +
   a label that swaps with state; (2) any `role` implies its full behavior (`radiogroup` →
   arrow-key roaming, else drop the role); (3) focus lands somewhere sensible after a panel
   opens/closes/confirm-hides; (4) mutually-exclusive disclosures actually exclude each other;
   (5) an action's promised effect is really written back into page state, or honestly mocked —
   never a status text that lies.

3. **Output dir**, default `ui-lab/<date>-<anchor-slug>-anchor-prototypes/`.

4. **`wire_navigation`** (optional, default **false**): when true, run the
   deterministic nav-linker pass (§Pipeline 7.5) after all surface verdicts
   settle — mocked links stamped `data-nav-target` (§Authoring rule 6) whose
   target surface was built in this wave are rewritten into real relative
   links. Absent/false = rule 6 mock discipline unchanged, wave output
   identical to today.

5. **`motion_pipeline`** (optional): path to the run's `motion/` dir (carrying
   `pipeline-state.json` + `sectional-score.json` + `resolutions/` — produced by
   `prototyping-ui-directions` per its
   `${CLAUDE_PLUGIN_ROOT}/core/prototyping-ui-directions/references/execution-contracts.md`).
   When present, THIS wave is a **Base Wave**: stage 0 preflight is enforced,
   each surface's `sectional_score` contract is a hard authoring input, motion
   beyond the chassis stance + that contract is FORBIDDEN (see §Authoring:
   motion), and the §Atomic Pass becomes available after `BASE_WAVE_READY`.
   Absent → legacy wave, behavior unchanged (the `.goals/pipeline-gate.json`
   sentinel discipline still applies).

Missing/ambiguous → stop and ask. Never silently invent.

## Authoring: universal interaction rules (required)

These rules MUST be applied at authoring time on every surface. They are universal for any product UI; the polish round shouldn't have to add them.

> Canonical source for these 5 rules: `taste-skill` §3 Rule 7 (Universal Interaction Compliance). They are reproduced here verbatim because surface subagents author without reading companion skills — if you change one copy, change both.

1. **Fitts compliance — every interactive ≥ 44×44 px hit target.** Visible glyph can be smaller (16-24 px) but its clickable area must be wrapped to ≥44px via padding or an invisible hit-area wrapper. Applies to: checkboxes, kebab buttons, filter chips, nav links, toggle buttons, theme toggles, sort carets, close buttons, action buttons.
2. **State-changing controls — explicit ARIA + dynamic labels.** Any control that toggles state (checkbox, toggle button, expandable section, complete/incomplete) MUST have `aria-pressed` (or `aria-checked` if role=checkbox) that updates on toggle. The accessible label MUST also update reflecting state (`"Mark complete: <task>"` ↔ `"Mark incomplete: <task>"`). Static label + class-only state change is not enough.
3. **Letter-spacing only via tokens — no raw values.** Letter-spacing MUST reference chassis tokens (e.g., `var(--tracking-tight)`, `var(--tracking-display)`, `var(--tracking-eyebrow)`). Raw values like `-0.02em` or `0.005em` are forbidden. If the chassis is missing a tracking token you need, add it to the anchor's token set — don't inline.
4. **Responsive shell minimum.** Every surface root uses `min-height: 100dvh` (not `100vh` — the dynamic viewport unit avoids the iOS Safari address-bar bug). Every multi-column layout has at least one media query (`@media (max-width: 640px)`) collapsing to single-column or hiding the sidebar behind a toggle. "Desktop-only" is not an excuse — render gracefully on narrow viewports even if not the primary target.
5. **Affordance contract.** If you write `cursor: grab` (or `move`, `pointer` on a non-button), a corresponding interaction handler MUST exist OR the affordance MUST be replaced with a non-fake alternative (kebab "Move to..." menu, explicit drag handle, etc.). Same rule for `role="textbox"` (needs `contenteditable`), `role="checkbox"` (needs `aria-checked` wiring), `cursor: pointer` on non-interactive elements (don't lie).
6. **Mocked cross-page links — no dead navigation, AND the mock must be visible.** A prototype surface is a single page; any link or CTA that would navigate to ANOTHER page (a route like `/work/x`, or a relative path to a surface not built in this wave) MUST NOT 404. Either point it at a sibling surface that *was* built, or disable it: `href="#"` + `data-mock="true"` + `onclick="return false;"` + a `title` saying it's mocked + an HTML comment. Never ship links to non-existent paths. **Additionally, `[data-mock="true"]` controls must LOOK inert**: muted treatment (reduced opacity, no hover state-change, `cursor: default`) plus a persistent cue (small "mocked" tag) where space allows — `title` alone is hover-only and invisible on touch. A dead control that affords exactly like a live one is a false affordance (hit 3/3 surfaces in the 2026-07-03 IA-wave audit).

   **Nav-target stamp + attribute-selector styling (enables the opt-in nav-linker pass).** When the mocked destination is another screen of THIS product (not an external site), ALSO stamp `data-nav-target="<target-screen-slug>"` on the link — the deterministic wiring pass (§Pipeline 7.5) reads it to rewrite the link when that surface was built in the same wave. Two styling requirements make the rewrite clean: (a) write the inert treatment through the `[data-mock]` ATTRIBUTE selector (e.g. `a[data-mock] { opacity: .55; cursor: default; }`), never a parallel class — removing the attribute must restore the live look with zero edits; (b) show the visible "mocked" tag via a `[data-mock]` descendant selector (e.g. `a[data-mock] .mock-tag { display: inline; }` + default hidden) so it disappears when the link is wired.
7. **Hierarchy must be visible, not just semantic.** The page's primary block/figure — `data-ia-tier="1"` in an IA-fed wave, the contract's headline affordance otherwise — gets a REAL visual weight step (type-scale step up / weight / space), not merely first position in the DOM. Pre-return smell check: a declared type-scale token (e.g. `--token-font-size-xl`) that NO element consumes usually means the hero figure ended up undersized (two independent 2026-07-03 audits found exactly this).

These rules supersede any conflicting authoring instinct. They were learned in polish rounds and promoted here so future waves catch them on the first pass.

## Authoring: slop gates + pre-emit 自评（lightweight pointer）

Base Wave 铺面沿用 PUD 侧的出稿负面清单（`../prototyping-ui-directions/references/slop-gates.md`，
hallmark 适配版——引用不复制）：**每 wave 扫一次 (a) + (e) 两桶**（对本 wave 共性，结果记 run-notes 一行
`slop sweep: pass` / `FAIL: 门号`）；每个 surface 出稿前跑六轴 pre-emit 自评，文件头留一行 stamp
`/* pre-emit critique: P# H# E# S# R# V# */`（任一轴 <3 → 该 surface 返工一轮再交）。
不加重 Base Wave 流程：sweep 是 wave 级一次、不是 per-surface 逐门过；instruction-layer 自查，非机器 gate。

**内容角色素材的 ③quality 地板 = 复用上面这些，不新造门。** 当一个 surface 用的是内容角色引擎荐来的素材
（PUD §Sectional Score 的 content-shape 路径；①buildability ②semantic 已在 resolver 侧判过），它 build 侧的
第 ③ 坎 quality 就落在**已有地板**上——这一节的 slop sweep + 六轴 pre-emit，加上 §Authoring 通用规则 5 的
**affordance 契约**（真 `<button>`+aria，不假装）和 §Authoring: motion 的 **mandatory reduced-motion**（素材
自带的降级分支必须保留、内容脚本不跑也要可见）。**不为内容角色新增任何 gate / 脚本 / hook**：③quality =
「别在铺面时弄丢素材自带的 a11y/reduced-motion + 沿用现有 slop 自查」；`<canvas>` 类质量仍交人评 loop
（确定性 validator 看不进 canvas，老边界不变）。

## Authoring: MVP feature checklist footer (required)

Every surface page MUST end with a footer that:

1. **Lists the route** (e.g. `/cases/:id?tab=command`) so reviewers can match the prototype to its product context.
2. **Renders the contract's `must_have[]` (or production-source-derived MVP section list) as a visible checklist** — one item per line, each prefixed with a check icon. Three purposes:
   - Reviewer can spot-check: every checked item should be visible in the surface above.
   - Records what was promised vs built, surfacing scope drift.
   - Forcing function on the author — if you can't add the check, you didn't build the affordance.

Canonical pattern (inline below):

```html
<footer class="footer">
  <div>
    <span class="footer__title">Route path</span>
    <div class="footer__route">/cases/:id?tab=command</div>
    <p class="footer__item">Resolved · /cases/C-2034?tab=command</p>
  </div>
  <div>
    <span class="footer__title">MVP feature checklist</span>
    <div class="footer__list">
      <span class="footer__item">
        <svg class="check" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"/></svg>
        <!-- one line per must_have[] item, paraphrased to UI noun-phrase -->
      </span>
      ...
    </div>
  </div>
</footer>
```

The footer is **not decorative**. It is the prototype's audit surface — every check claims a corresponding visible affordance in the rendered page above.

## Authoring: motion (GSAP — opt-in per surface)

Motion is **not** default-on. An overlay / form / dashboard should be calm — add motion only when the surface's `maturity` is `creative` / `marquee`, or its contract sets `motion: true`. When you do:

- **Base Wave discipline (motion-pipeline runs — hard rule).** When inputs carry
  `motion_pipeline`, a surface's motion comes from exactly TWO sources: (a) the
  chassis' locked motion stance/vocabulary (CHASSIS.md Motion Architecture), and
  (b) that surface's `sectional_score` contract (implement its mechanism within
  the registry's boundary requirements — owner wrapper, local progress, clean
  release). **No improvised atomic decoration**: no hover garnish, no extra
  scroll reveals, no per-surface "one nice touch" beyond the stance — those are
  the Atomic Pass's job, chosen against the REAL DOM after `BASE_WAVE_READY`,
  under the user-approved atomic budget. A surface whose contract says
  `sectional_score: null` gets the chassis stance and NOTHING else. Selection
  order is global system → bounded section → existing component; the wave sits
  between the last two and must not reach forward.

- **Engine = GSAP.** Framework-agnostic and the only real option for the HTML surfaces this skill produces (Framer Motion is React-only). The parent `Read`s the relevant `gsap-*` SKILL.md (`gsap-core` + `gsap-scrolltrigger`; add `gsap-timeline` / `gsap-plugins` — Flip, SplitText — as needed) and **inlines the concrete GSAP patterns into each motion surface's subagent prompt**. Leaf subagents do not read companions (per §Topology), so motion guidance must arrive pre-extracted like everything else.
- **Drive motion from chassis tokens** (duration / easing), never raw values — same discipline as the letter-spacing rule in §Authoring.
- **Reduced-motion is mandatory.** Wrap motion in `gsap.matchMedia()` with a `(prefers-reduced-motion: reduce)` branch that reveals everything instantly (see `gsap-core` §matchMedia). Progressive enhancement: content must be present and visible even if the script never runs.
- **Restraint over spectacle.** An app surface earns one or two intentional moments (a list reveal, a state transition via Flip) — not perpetual animation. `taste-skill` §8 owns the WHEN / taste policy; the `gsap-*` skills own the HOW.
- **3D / canvas stages (conditional).** If a surface's contract calls for a 3D or particle canvas (`morphology: canvas`, or a contract note requesting a 3D stage), the parent `Read`s the `three/*` skills (`${CLAUDE_PLUGIN_ROOT}/three/threejs-fundamentals/SKILL.md` + `${CLAUDE_PLUGIN_ROOT}/three/threejs-scroll-stage/SKILL.md`, more as needed — see `${CLAUDE_PLUGIN_ROOT}/three/README.md`) and inlines the needed patterns into that surface's subagent prompt (leaves don't read companions, same as GSAP above). 3D obeys the same discipline as DOM motion: ScrollTrigger drives, the canvas only receives progress (`setProgress(p)`); one `gsap.ticker` loop (never a second RAF); colors derive from chassis tokens; full disposal chain on teardown; reduced-motion static frame; never Framer Motion in the same tree. Honest boundary: the deterministic validators cannot see inside a `<canvas>` — canvas quality is judged by the human review loop, not the regex gates.

The deterministic validators (`scripts/`) are motion-agnostic — they neither block nor reward GSAP. Motion quality is judged by the LLM grader (`interaction_quality`) + the usability audit, not the regex gates.

## Authoring: staying on-system for un-tokened cases (Agent Prompt Guide)

The anchor tokens can't spell out every component / state / edge surface a wave needs. When a surface subagent must build something the locked tokens don't cover, it stays on-system by **deriving from the tokens, never inventing**. This discipline applies on every wave; a chassis MAY additionally carry a filled **Agent Prompt Guide** block (template below) that pre-answers the recurring gaps for its specific look — when present, the parent inlines it into each surface subagent's prompt (leaves don't read companion files — same rule as §Authoring: motion).

> Adopted from the DESIGN.md "Agent Prompt Guide" (section 9) format — the prose layer that keeps a downstream agent on-brand for cases the token table doesn't cover. **Honest divergence: DESIGN.md ships no usable motion; our chassis LOCK motion (tokens + GSAP), so we adopt its static-spec rigor but NEVER regress motion to match it.**

**Default discipline (applies even when a chassis has no Agent Prompt Guide block yet):**
- **Derive, never invent.** Un-tokened values come FROM the tokens — new spacing = an existing scale step; a new shade = a mix of existing ink/accent levels, not a fresh hue/hex/px. Can't derive it → stop and flag, don't guess.
- **Inherit the non-negotiables:** single accent only; no second hue; numbers in the mono token; the chassis's layout rule (e.g. hairline rows vs cards); type/tracking via `--token-*` (never raw) — this is §Authoring universal-interaction rule 3, restated for un-tokened work.
- **Don't regress motion.** If the chassis locks a motion stance, new surfaces apply that same stance (see §Authoring: motion) — never fall back to static "because the tokens didn't say". The motion is locked, not optional.
- **When genuinely stuck, surface the gap** to a human; don't scaffold a competing pattern.

**Agent Prompt Guide block — template a chassis fills in its `CHASSIS.md`** (optional today; recommended for new chassis):

```markdown
## Agent Prompt Guide — staying on-system (for anchor-wave / build agents)
> Read before authoring any surface/component the locked tokens don't spell out.

- Derive, never invent: un-tokened values come from existing tokens (scale step /
  ink·accent mix), not new hue/hex/px. Can't derive → stop + flag.
- Non-negotiables (inherit lock): single accent <accent> only; no 2nd hue; numbers
  in <mono>; <layout rule, e.g. hairline rows NO cards>; type via --token-size-*,
  tracking via --token-tracking-*.
- Voice / register: <one line, e.g. "quiet-luxury editorial: drama = type scale + air">.
- Motion — do NOT regress (our edge over DESIGN.md): stance = <locked motion>. New
  surfaces reuse it (load-sweep first screen / scroll-sweep below fold) via GSAP +
  matchMedia reduced-motion. Never drop to static.
- Stuck → surface the gap to a human; don't scaffold a competing pattern.
```

Filled example (grove-linen, shown here — the locked `CHASSIS.md` isn't edited): accent `#8f5133`; mono DM Mono; layout hairline editorial rows NO cards; register quiet-luxury Didone editorial; motion Trace hybrid sweep (load first screen / scroll below fold).

## Topology — parent orchestrates, subagents author leaves

This skill MUST run in the **parent context**. The parent thread:
- Writes `_context.md` + per-surface contracts
- Spawns leaf-work subagents in parallel for surface authoring (≤10 per batch)
- Runs validators + scorer + retry decisions
- Aggregates manifest + master gallery + closeout
- Invokes `codex-dispatch` for cross-AI review — NOT shipped (nominated;
  lab checkout has it at `vendor/codex-dispatch/SKILL.md`). `Read` it and
  follow its routing (do NOT try to invoke via `Skill` tool — won't fire on
  project-local skills). **If it does not resolve**: skip the cross-AI pass
  and record `companion_skipped: codex-dispatch` on the closeout — never
  substitute a self-review and call it cross-AI

Leaf-work surface subagents:
- Receive their full surface spec inline in the prompt
- Write ONLY `<slug>/index.html`
- Do NOT need to consult any companion skill — all guidance arrives
  pre-extracted in their prompt
- Return one line: file path + verdict

Do NOT spawn a single "run anchor-wave for me" orchestrator subagent —
cross-AI review and codex-dispatch fallback are parent-level decisions
that need visibility across all surface audits. (Harness behavior: the
`Skill` tool won't fire on project-local skills, so companions are
invoked by `Read`ing their SKILL.md.)

## Pipeline (one shot)

### 0. Motion preflight (only when inputs carry `motion_pipeline`)

```bash
python ${CLAUDE_PLUGIN_ROOT}/core/anchor-prototype-wave/scripts/preflight_wave.py \
  --motion-dir <run>/motion --stage base-wave
```

Exit ≠ 0 = **do not spawn anything** — the design sequence is not settled
(chassis unlocked / composition not ready / sectional undecided / a selected
mechanism's resolution record missing, stale or tampered). Fix upstream in
`prototyping-ui-directions` (its §Sectional Score ceremony), never by editing
the state file by hand — `pipeline_state.py` is its only legal writer. A run
without `motion/` is legacy: the script prints `LEGACY` and exits 0.

### 1. Write context + contracts
- `<out>/audits/_context.md` — paste the anchor verbatim + the banned-token list.
- `<out>/audits/contracts/<slug>.contract.json` per surface:
  ```json
  {
    "surface_slug": "...",
    "claimed_surface_type": "overlay|drawer|...|form",
    "surface_innovation_target": "mature|creative|marquee",
    "production_source": "<path or null>",
    "research_only_reason": "<reason if no production_source>",
    "intent": "one-line",
    "must_have": ["..."],
    "must_not_have": ["..."],
    "motion": false
  }
  ```

### 2. Spawn surface subagents in parallel (≤10 per batch; >10 auto-split)
- **Verbatim entries are copied by script, not authored.** For each page
  carrying `verbatim_source`, run the deterministic importer — do NOT hand-copy
  (a dropped asset or a stray content edit silently breaks the lock):

  ```bash
  python ${CLAUDE_PLUGIN_ROOT}/core/anchor-prototype-wave/scripts/import_verbatim.py \
    --source <verbatim_source> --dest <out>/<slug>
  ```

  It copies `index.html` + every relative asset it references (the source dir is
  READ-ONLY). Then the ONLY permitted edit on the copy: additive
  `data-nav-target="<sibling-slug>"` stamps on its rule-6 mocked product links
  (older chassis predate the stamp convention) — zero layout / token / copy
  changes, external links unstamped (this stamp is semantic, so it stays a model
  edit). Then PROVE the lock held — asserts dest == source modulo the stamps,
  exit 1 = re-authored / asset dropped / asset altered:

  ```bash
  python ${CLAUDE_PLUGIN_ROOT}/core/anchor-prototype-wave/scripts/import_verbatim.py \
    --source <verbatim_source> --dest <out>/<slug> --verify
  ```

  Verbatim surfaces skip stages 3-7 (already human-approved; no contract to gate
  against) and enter `audits/manifest.json` with `"verdict": "VERBATIM_IMPORT"`;
  the gallery renders their tile normally but tally pills never count them as
  PASS. Honest boundary: verbatim pages are NOT retrofitted with newer wave
  conventions (MVP footer, visible-inert cues…) — the lock wins over the latest
  brief; the `VERBATIM_IMPORT` verdict is the reviewer's cue.
- `mature` → sonnet; `creative` / `marquee` → opus.
- Each subagent's prompt includes: the anchor doc, the surface contract,
  the banned-token list, and a hard rule: **write ONLY `<out>/<slug>/index.html`**.
  Begin every spawn prompt with the literal marker `surface-authoring subagent
  for <slug>` — the project pipeline-gate hook keys on that marker; wording a
  spawn to dodge it dodges the gate, which is a violation, not a loophole. For
  motion-pipeline runs the prompt also inlines the surface's `sectional_score`
  contract (or `null`) + the §Authoring: motion Base-Wave discipline verbatim.
  For surfaces that get motion (§Authoring: motion), the parent also inlines
  the pre-extracted GSAP patterns from the relevant `gsap-*` skills.
- Tools allowed: Read, Write, Edit, Grep, Glob. No shell, no other writes.

### 3. Run deterministic validator per surface
```bash
python ${CLAUDE_PLUGIN_ROOT}/core/anchor-prototype-wave/scripts/validate_surface.py \
  <out>/<slug> \
  --contract <out>/audits/contracts/<slug>.contract.json \
  --out <out>/audits/<slug>.audit.json \
  --wave-slug <wave>
```

The validator writes `audits/<slug>.audit.json` with hard-gate results + an
initial verdict (`REDO` | `FIX_NEEDED` | `PENDING_SOFT_SCORE`).

### 4. LLM grader (only if Stage 3 yielded `PENDING_SOFT_SCORE`)
Spawn a sonnet subagent with the surface HTML + `audits/<slug>.audit.json`.
It fills `soft_scores` (six dims, 0-10):

```
chassis_consistency       (weight 0.20)
mvp_coverage              (weight 0.20)
visual_quality            (weight 0.15)
interaction_quality       (weight 0.15)
consistency_with_siblings (weight 0.15)
innovation                (weight 0.15)
```

Anchors for grading: 10 = best-in-class for the morphology; 5 = typical
shipping product; 3 = obvious AI slop / generic.

### 4b. Usability/HCI audit (per surface, parallel to grader)

> Canonical Usability/HCI heuristic set for the lab (SINGLE SOURCE). `prototyping-ui-directions` Stage 3 *points here* rather than re-listing, so the two cannot drift.

In parallel with the soft-score grader, spawn a separate sonnet subagent to audit each surface against HCI heuristics:

- **Visual hierarchy** (Tognazzini, Krug): does the most important info dominate? Does the eye land in the right place first?
- **Density** (Tufte): data-ink ratio; packed but not noisy.
- **Scanning patterns** (NN/g): can the user F/Z-pattern through the page?
- **Typography rhythm** (Bringhurst): meaningful weight/size contrasts.
- **Cognitive load** (Hick's, Miller's, Fitts's): choices ≤ 7±2, targets ≥ 44px.
- **Affordance clarity** (Norman): what's clickable is obvious.
- **Aesthetic-usability** (Kurosu & Kashimura): polished, calm, confident.
- **Jakob's Law**: matches expectations from comparable products.
- **States that do their job**: an error state offers a recovery action, not just "something went
  wrong"; an empty state carries the CTA that fills it; button and link copy uses the product's
  own verb ("Save case"), never a generic one ("Submit" / "Click me" / "提交").

Output: `audits/<slug>.usability.md` with findings tagged BLOCKER/MAJOR/MINOR + fix recommendations + file:line citations. Separate from the contract audit — different lens. Findings are **informational** here (do NOT block PASS_9PLUS), but they feed `frontend-audit-polish` if the user runs it next.

### 5. Run scorer
```bash
python ${CLAUDE_PLUGIN_ROOT}/core/anchor-prototype-wave/scripts/score_audit_json.py \
  <out>/audits/<slug>.audit.json \
  --contract <out>/audits/contracts/<slug>.contract.json
```

The weighted bar is **maturity-aware** (mature 8.5 / creative 8.75 / marquee 9.0) — it mirrors the
innovation floor, so a `mature` utility page is **not** held to a showcase-grade 9.0 and need not be
over-designed just to pass. Pass `--quality-bar N` to override. Writes final verdict:
`PASS_9PLUS | FIX_NEEDED | REDO`.

### 6. Fix-on-fail loop (≤3 retries per failing surface)
- `REDO`: re-spawn a **fresh write subagent** (no diff context, full
  re-author). Use for `gate_0` form-mismatch or `gate_1` no-production-source.
- `FIX_NEEDED`: re-spawn a **patch subagent** (surgical; preserve untouched
  regions). Use for `threshold_only`, `inner_widget_missing`, other gate
  blocks, or floor violators.
- Each retry's prompt **must verbatim quote** the failing gates + evidence
  selectors from the prior `audits/<slug>.audit.json`.
- After 3 retries still failing → write `ESCALATE_HUMAN` into the audit and
  stop on this surface (do NOT auto-PASS).

### 7. Cross-AI review (trigger matrix)
- **The reviewer must not restate our self-grade.** Ask it for problems we missed, each citing a
  selector and a line number and naming a product that solves it better, and for a grade moved
  up or down with a reason — "9.0 confirmed" is a failed review, not a passed surface.
- `REDO` or `FIX_NEEDED` surface that came back PASS on retry → required.
- `PASS_9PLUS` surface → sample 15% (rounded up).
- Overlay/drawer/full-page morphology where contract was ambiguous → required.
- **Invocation order — try BOTH before declaring failure**:
  1. `mcp__codex__codex` (if the MCP tool is in your available-tools list).
  2. If MCP route is denied, missing, or errors → fall back to the official
     `codex@openai-codex` plugin command (`/codex:review` for cross-model
     review; `/codex:adversarial-review` when the surface needs an
     adversarial pass).
     ⚠ **Do NOT shell out to `codex exec` yourself.** `codex-dispatch` v2
     (`vendor/codex-dispatch/SKILL.md`) explicitly removed that path — the
     old self-shelling skill was replaced by the official plugin, and this
     block used to describe the v1 behaviour. Read the vendored skill for
     the current routing, scope caps and quota fallback.
- Only after **both** routes fail, record the actual error in
  `cross_review_error` on the audit. Do NOT silently mark as skipped after
  one route fails.
- If `codex-dispatch` is not readable at either path AND the
  `codex@openai-codex` plugin commands are unavailable, record
  `cross_review_skipped: codex_dispatch_unavailable` on the audit. Do not
  invent a review.

### 7.5. Nav-linker pass (only if inputs set `wire_navigation: true`)

After every surface's verdict has settled — the fix-on-fail loop re-authors
pages (a REDO page's fresh author writes rule-6 mock links from scratch), so
wiring earlier would be undone:

```bash
python ${CLAUDE_PLUGIN_ROOT}/core/anchor-prototype-wave/scripts/wire_navigation.py <out>
python ${CLAUDE_PLUGIN_ROOT}/core/anchor-prototype-wave/scripts/wire_navigation.py <out> --check
```

Wires links carrying `data-mock` + `data-nav-target` whose target surface
exists in this wave (`href="../<slug>/index.html"`, mock attrs stripped,
`data-nav-wired="true"` added); unbuilt targets and unstamped/external links
keep their full mock treatment. Idempotent — safe to re-run after any late
fix (a wave MAY additionally run it earlier, e.g. before audits, but 7.5 is
the canonical point). `--check` must exit 0 before stage 8 — it crawls every
wired link and asserts it lands on a built page of this wave. Flag
absent/false → skip this stage entirely (wave output unchanged).

### 8. Master gallery + manifest + cross-cutting summary

**Gallery layout — `<out>/index.html` (hard rule; no other layout permitted)**:
1. **Hero block** (top, not sticky): anchor name + wave date + total surface count + verdict tally pills (PASS / FIX / REDO / ESCALATE) on a single row. Optional second line: accent swatch + radius scale + banned-token list in mono.
2. **Search + filter bar** (sticky on scroll, full-width):
   - Text `<input>` filtering tiles by `slug`, `title`, `route`, `morphology`, `group` (substring match, case-insensitive, live as user types).
   - Filter chips for groups (one chip per unique `group` value + "All").
   - Filter chips for verdict (PASS / FIX / REDO / ESCALATE + "All").
   - All client-side JS, inline. No external deps.
3. **Grouped tile grid** — surfaces grouped by `group` field, one section per group:
   - Each tile = **iframe thumbnail of `<slug>/index.html`** (no text-row layout permitted) + tile footer with: title, `<slug> · <morphology> · <maturity>` mono line, score, verdict pill.
   - ESCALATE tiles render in their broken state — do NOT hide them, they're the evidence.
   - Tile size: ~280px wide minimum; iframe `pointer-events: none` + `transform: scale(0.35)` so the thumbnail is a static preview, not interactive.
4. **Dark mode toggle** in the top-right of the hero block (same bootstrap pattern as surfaces per §Authoring).
5. Audit-dashboard / text-row layouts are NOT permitted in `index.html`. That information belongs in `audits/closeout.md` and per-surface `audit.json` files.
- Write `<out>/audits/manifest.json` with per-surface verdicts + scores + usability finding counts.
- Write `<out>/audits/closeout.md` summarizing PASS/FIX/REDO/ESCALATE counts.
- Write `<out>/audits/cross-cutting.md` — scan all per-surface audits (contract + usability) and emit:
  - **Pattern findings**: validator warnings/blocks that hit ≥2 surfaces (e.g., 3 surfaces with `pill_mono_drift` → propose one chassis-level fix).
  - **Vocabulary drift**: status token names, morphology classes, terminology variants across surfaces.
  - **IA observations**: things spotted only by comparing surfaces (label inconsistencies, navigation drift).
  - **Patterns to promote**: design moves with high scores worth replicating across the wave.
  - **Reference-pool candidates (human-gated — do NOT auto-promote our own output)**: the reference library exists to
    point at **external, credible standards**, so wave outputs (a high-scoring surface, a shipped chassis) are NOT
    promoted into `prototyping-ui-directions`'s pools as exemplars — being good *for this wave* ≠ an industry standard.
    What you MAY do is **list externally-sourced references the wave surfaced** (a real font/effect/site found while
    building, with anchor + URL + provenance) as *candidates for the user to admit* — never self-add. Governance +
    per-pool rules (style = surface for human to eyeball; motion = only when real source code was read) live in
    `${CLAUDE_PLUGIN_ROOT}/core/prototyping-ui-directions/references/reference-sources.md` §5. Contrast with spec-promotion below, which DOES
    harden design *rules* into Contract Amendments — that's our own process output; reference *material* must stay
    externally-anchored.
  - **Spec-promotion candidates** (REQUIRED): a list of findings that are *universal/authorable rules* — things that should be baked into the authoring brief for next time (i.e., Type A gaps), not left to the polish round to catch repeatedly. Each candidate cites the specific rule and where in this skill's §Authoring it should live. Examples from past waves: Fitts 44px, aria-pressed on toggles, letter-spacing-via-tokens-only, responsive shell minimum, affordance contract.

Cross-cutting findings are the natural input for `frontend-audit-polish` on a follow-up iteration. Spec-promotion candidates feed back into the authoring spec so each polish round shrinks over time as the brief absorbs lessons.

- **Promote candidates to `_context.md` as Contract Amendments** (the canonical project contract surface). For each `Spec-promotion candidate`:
  - If the candidate is a *cross-surface token / pattern / vocabulary rule* (status-vocabulary lock, shadow-tier canonical, granule shape contract, decorative-gradient carve-out, save-bar pattern, etc.) → append a new section to `<out>/audits/_context.md` under `## Contract Amendments` (create that heading if absent). Each amendment numbered, with a one-sentence rule + a `Rationale:` line citing the wave slug + the cross-cutting finding it came from. Token-name renames must list the migration map.
  - If the candidate is an *authorable rule belonging in `SKILL.md` §Authoring* (e.g. Fitts 44px, aria-pressed on toggles, letter-spacing via tokens) → leave it as a candidate in `cross-cutting.md` only. The user promotes manually via `skill-edit-proposal.md`.
  - Skip the whole promotion step if inputs include `auto_promote_amendments: false` (user wants to review candidates before they bind).

`_context.md` is the canonical project contract. The downstream `frontend-audit-polish` skill reads its `## Contract Amendments` section as a hard rule for every patch subagent. Promotion here is what closes the loop: findings → ratified amendments → next wave's surfaces ship clean of them on the first pass; next polish round's patches refuse to violate them.

### 8.6 Advance the pipeline state (motion-pipeline runs)

After stage 8 artifacts are written and every surface verdict is settled (no
un-escalated REDO/FIX pending):

```bash
python ${CLAUDE_PLUGIN_ROOT}/core/prototyping-ui-directions/scripts/pipeline_state.py \
  transition --state-file <run>/motion/pipeline-state.json \
  --to BASE_WAVE_READY --by gate --evidence "wave <slug>: <verdict tally>"
```

(In this lab, PUD scripts live at `core/prototyping-ui-directions/scripts/`.)
`BASE_WAVE_READY` is the Atomic Pass's entry condition; without it the atomic
preflight blocks (matrix case 10).

### 9. Report to user
Single message:
- Surface count + PASS / FIX / REDO / ESCALATE breakdown.
- Master gallery file URL.
- List of ESCALATE_HUMAN surfaces with their blocking gates + evidence.

## Atomic Pass — patch the REAL DOM under a no-reflow budget (motion-pipeline runs only)

Atomic effects decorate EXISTING UI (transform / opacity / filter /
color·border·shadow / pseudo-elements / small overlays with no layout
ownership). They are chosen by inspecting what the Base Wave actually built —
never authored into it. Shapes:
`${CLAUDE_PLUGIN_ROOT}/core/prototyping-ui-directions/references/execution-contracts.md` §6.

**Entry ceremony (machine-enforced)**:
1. The user approves the atomic POLICY — a budget, not per-effect sign-off:
   write `<run>/motion/atomic-policy.json`, then `pipeline_state.py approve
   --gate atomic_policy --approval-text "<user's verbatim words>"`,
   `set atomic_status policy-approved`, `transition --to ATOMIC_OPEN`.
2. `python ${CLAUDE_PLUGIN_ROOT}/core/anchor-prototype-wave/scripts/preflight_wave.py
   --motion-dir <run>/motion --stage atomic` must exit 0 — it blocks before
   `BASE_WAVE_READY`, without approval, or with a non-conformant policy.

**Per-surface pass**:
1. Back up: copy `<slug>/index.html` → `audits/atomic/<slug>.before.html`.
2. Inspect the REAL DOM; pick candidate targets worth a touch. Restraint:
   `max_targets` is a ceiling, not a quota.
3. Resolve: `resolve_candidates.py` with `phase=atomic`,
   `pipeline_state=ATOMIC_OPEN`, a component/overlay carrier, the policy's
   `performance_budget`, and per-candidate `proposed_mutations`. Only
   `eligible` mechanisms may be applied (a pinning / section-height proposal
   computes sectional and is excluded). Resolution JSON stays under
   `<run>/motion/resolutions/` as evidence.
4. Patch within `allowed_properties` only; overlay ADDITIONS only when
   `allow_overlay_canvas` is true; `gsap.matchMedia()` reduced-motion branch
   mandatory, same as all motion.
5. Capture layout geometry before + after into
   `audits/atomic/<slug>.layout-diff.json`:
   `{"tolerance_px": 0.5, "rects": {"<selector>": {"before": [x,y,w,h], "after": [x,y,w,h]}}}`
   — for each patched target + its parent + adjacent siblings, via
   `el.getBoundingClientRect()` in the running page. The capture is browser
   evidence; the CHECK below is the deterministic part.
6. Write `<run>/motion/atomic-result-<slug>.json`, then run
   `scripts/check_atomic_result.py --result … --policy … --before
   audits/atomic/<slug>.before.html --after <slug>/index.html --layout-diff
   audits/atomic/<slug>.layout-diff.json`. Exit ≠ 0 = **REVERT the patch**
   (restore the backup), then drop the effect or re-resolve a lighter one —
   never argue with the geometry.
7. Re-run the existing surface checks: console clean, responsive,
   reduced-motion, functionality spot-check.
8. All patched surfaces green → `set atomic_status patched` → `set
   atomic_status verified` (evidence = check outputs) → final human gallery
   review → `transition --to COMPLETE`.

Spawn marker: if atomic patching fans out to subagents, begin each prompt with
the literal marker `atomic-patch subagent for <slug>` (the pipeline-gate hook
keys on it — same contract as the wave marker). Honest boundary: the checker
verifies policy / structure / geometry EVIDENCE deterministically; whether an
atomic touch looks good is still the human gallery review's call.

## Hard write boundaries (all stages)

```
❌ workspace/src/**          ❌ backend/src/**
❌ tailwind.config.* / vite.config.* / root package.json
❌ _reference/** / vault/raw/**
❌ docker-compose*.yml / migrations/** / drizzle/**
❌ ${CLAUDE_PLUGIN_ROOT}/**  (unless user explicitly asks to modify this skill)
❌ verbatim_source dirs      (stage 2 copies FROM them; never write INTO them)
```

Subagent write scope: ONLY its own `<slug>/index.html`. The main thread is
the only writer for `_context.md`, contracts, audits, manifest, gallery.
Boundary violations → revert via `git checkout` and re-spawn with stricter
scope prompt.

## When to stop and ask

0. **Pipeline-gate (project hook, if installed — ui skills lab).** The FIRST surface
   fan-out is hard-blocked by `.claude/hooks/pipeline-gate.js` until `.goals/pipeline-gate.json`
   records the user's explicit approval of the upstream **lock chassis → wave** transition
   (and of any proposed **Batch-2 skip**). Write that sentinel ONLY AFTER the user answers the
   either/or: `{"gate":"anchor-wave","run":"<id>","proposed":"…","user_approval":"<user's words>","approved_at":"<ISO-now>","ttl_seconds":14400}`. This enforces the upstream decision; it adds no internal ratification step to the wave itself.
1. Inputs missing or ambiguous (§Inputs).
2. A surface escalates to `ESCALATE_HUMAN` after 3 retries. Report failing
   gates + evidence; ask: manual edit / drop the surface / continue anyway.
3. User asks to modify this skill itself. Write a proposal under
   `<out>/audits/skill-edit-proposal.md` and wait for explicit go-ahead
   before touching `${CLAUDE_PLUGIN_ROOT}/core/anchor-prototype-wave/**`.
4. **Motion-pipeline runs — the atomic POLICY is the user's call** (enable it?
   how many targets? overlays allowed?): record their verbatim words via
   `pipeline_state.py approve --gate atomic_policy` before ATOMIC_OPEN.
   Per-effect choices WITHIN the approved policy are the agent's; the final
   gallery review closes the pass. The model never self-approves a state
   transition.

Nothing else stops the pipeline. No mode flags, no plan ratification step.

## Anti-patterns

- Treating composite avg ≥ 9 as PASS while a hard gate is BLOCK. The scorer
  short-circuits — trust it.
- Spawning a surface subagent without a contract JSON.
- Auto-PASS after 3 retries. ESCALATE_HUMAN is mandatory.
- Running cross-AI review on every surface. Use the trigger matrix.
- Inventing a `production_source` to satisfy `gate_1`. If there isn't one,
  set `research_only_reason` in the contract.
- Hardcoding model names. Surface subagents: mature→sonnet, creative/marquee→opus.
  Grader: sonnet. Cross-review: codex (if installed).
- Re-composing an IA-wireframe `production_source` (moving blocks between regions, swapping the
  flow mechanism). Its composition passed a deterministic check + a human gate upstream — on
  such a source the wave is a coloring pass, not a layout pass.
- Re-authoring or "improving" a `verbatim_source` page, or editing its source dir. Verbatim =
  copy + additive nav-target stamps on the copy, nothing else.
- Improvising atomic decoration during Base Wave authoring (hover garnish, extra scroll
  reveals, "one nice touch" beyond the chassis stance + sectional contract). Atomic effects
  enter ONLY via the Atomic Pass — post-DOM, resolver-filtered, within the approved policy.
- Starting the Atomic Pass before `BASE_WAVE_READY` or without an approved policy — the
  preflight and the state machine both refuse; work the ceremony, don't work around it.
- Hand-editing `motion/pipeline-state.json`. `pipeline_state.py` is its only legal writer;
  the artifacts validator treats a state that disagrees with its own append-audited
  `state_log` as tamper.

## Extensions (opt-in, default off)

If the user's inputs include an `extensions:` field listing extension names, the parent invokes each at its hook point by `Read`-ing `${CLAUDE_PLUGIN_ROOT}/extensions/<extension-name>/SKILL.md` and following its workflow.

| Name | Hook point | What it adds |
|---|---|---|
| `versions` | after Stage 8 | Snapshot each surface to `<slug>/versions/<date>-<label>/`; inject version-switcher widget; update gallery with update badges. |
| `elements` | as Stage 2b (parallel to surface authoring) | Author atom foundation pages (`elements/01-atoms-buttons.html`, `02-surface-card-drawer.html`, `03-forms.html`, `04-nav-structural.html`) consuming the same anchor. |
| `dark-mode` | woven into Stage 2 surface authoring | Adds light + dark mode to every surface via 9-patch token-override + theme toggle UI + per-prototype localStorage persistence. Base skill defaults all surfaces to light; this extension makes them theme-switchable. |

If `extensions:` is absent or empty, base pipeline runs unchanged.

## Compatible standalone companions

These are not extensions — invoke them as separate skills before or after a wave run. They work on any frontend directory, not just anchor-wave output.

| Skill | When |
|---|---|
| `frontend-visual-regression` | After wave completes (or any iteration) to capture Playwright baselines + run regression checks. |
| `frontend-audit-polish` | After audit docs accumulate, to apply audit findings as batched patches across surfaces. Closes the iterative-development loop. |
| `taste-skill` | Anti-AI-slop red-team during Stage 2 authoring (Read its SKILL.md and apply rules per-surface). |
| `gsap-*` | Motion authoring engine — see §Authoring: motion. Parent reads the needed `gsap-*` skills and inlines patterns into motion surfaces' subagent prompts. |
| `codex-dispatch` | Cross-AI review via Codex CLI — already referenced in Stage 7. |

## File layout produced

```
<out>/
├── index.html                          ← master gallery
├── <slug-1>/index.html                 ← per-surface hi-fi
├── <slug-N>/index.html
└── audits/
    ├── _context.md
    ├── manifest.json
    ├── closeout.md
    ├── contracts/<slug>.contract.json
    └── <slug>.audit.json               ← validator + grader + scorer JSON
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

English:
- "generate the wave from this anchor"
- "make hi-fi mocks from chassis + pages"
- "produce a prototype wave"
- "run anchor-prototype-wave"

中文:
- "用这个 anchor 出一波 prototype"
- "把这些页面照这个 anchor 全生成出来"
- "出一波 hi-fi mocks"
