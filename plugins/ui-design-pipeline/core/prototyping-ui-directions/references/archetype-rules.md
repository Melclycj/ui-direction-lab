# Surface archetypes — what a surface must DO, per kind

> **Provenance**: condensed from this lab's earlier `~/.claude/skills/prototyping-ui-directions/templates/product-archetypes/`
> (7 archetypes, ~4835 lines). Only the iron rules and the weight priors are carried over —
> the layout-engine notes, pattern indexes and reference anchors stayed behind. Backported
> 2026-08-21 after an audit found the repo copy had no archetype axis at all.

An archetype answers **"what kind of thing is this surface, and what must it therefore do"**.
It is not a look. A dashboard can wear any visual direction; it still owes you tabular figures,
three async states and a URL that survives a filter.

## Orthogonal to two things you already have

| Axis | Question | Where it lives |
|---|---|---|
| **L3 style** | what does it look like | `style-pool` / the locked chassis |
| **`content_shape.role`** | what shape of content does this surface carry | `testbed/material/content-roles.md`, 8 roles |
| **`archetype`** (this file) | what must this surface DO as a kind of product | here |

They overlap without collapsing: a `metrics` content shape often lands on a `data-dashboard`
archetype, `narrative` often on `narrative-scrolly`. But **`canvas` has no content-shape
equivalent** — it is an interaction contract, not a content shape. Judge them separately.

**Conflict rule**: when an iron rule and the locked L3 style disagree, **the style wins the skin,
the archetype wins the skeleton.** A brutalist dashboard is still tabular-nums.

## Per surface, not per product

A product has surfaces of different kinds — a marketing front page, an editor, a settings screen.
The archetype is assigned **per screen**, at IA Stage B, derived from that screen's `primary_task`.
Nobody scores anything: the derivation is the IA's, and the human corrects it at the Stage C gate
they already walk.

---

## The seven

### `landing-marketing` — convert a stranger

**Nine iron rules** (structure and conversion discipline, orthogonal to the L3 skin):

- Above-the-fold value prop ≤ 8 words (≤16 CJK chars); no "We empower teams to…" / "The future of X"
- Headline + subhead + ≥1 primary CTA all visible at 0 scroll, at **both** 1440×900 and 390×844
- **One** primary-CTA colour, unique on the page
- Every claim carries evidence, or it is cut — see slop-gate #46: an unsupplied number is `—`
- Social proof is real and attributable, or absent
- One idea per section; a section that argues two things is two sections
- The scroll has a spine: each section answers the objection the previous one raised
- Forms ask for the minimum that makes the next step possible
- The footer is navigable, not a sitemap dump

### `data-dashboard` — read state and act on it

**Eight iron rules**:

- All figures in `tabular-nums`
- ≤ 3 chart types per view
- ≤ 3 accent colours, semantic, and **never colour alone** — colour-blind redundancy required
- Data-ink ratio: no chartjunk
- Every async surface has all three states: loading + empty + error
- Numeric hierarchy comes from **scale contrast**, not decoration
- Dark mode re-calibrated for data (not pure black on pure white; chart palette re-checked)
- Filter / range / selection / tab state goes in the URL

### `canvas` — make things in a space

**Six iron rules**:

- Conventional action semantics — menus use Create / Duplicate / Delete / Group / Move / Zoom, not invented verbs
- **Invention belongs in the feedback layer, never in the information architecture** — keyboard, selection model and copy semantics stay predictable
- Animations ≤ 500ms (micro 150-300, complex ≤ 400)
- `prefers-reduced-motion` fallbacks complete
- Non-blocking operations — cancel/interrupt hooks present, pointer events never frozen
- Do not pollute the main visual: glow / shimmer / bloom / particles ≤ 2 per screen

### `narrative-scrolly` — carry a reader through a story

**Eight iron rules**:

- With JS off or `prefers-reduced-motion` on, the story reads **in narrative order with zero information lost**
- Never hijack native scroll velocity; smooth-scroll lerp ≥ 0.1 and off under reduced-motion; no forced scroll-snap
- Each pin / sticky segment ≤ **3×100vh** of scroll distance
- Tab order = visual and narrative order; a skip-link exists; step content is focusable without scrolling to it
- LCP < 2.5s, CLS < 0.1; every sticky / sequence / reveal container reserves its size
- Step triggers use IO / ScrollTrigger callbacks, **debounced and idempotent** — a bare `scroll` listener is a reject
- Scroll-tied animation touches only `transform / opacity / clip-path`; a layout property inside a scrub is a reject
- Long stories show progress (bar or chapter dots); a reveal exposes one narrative unit at a time

### `creative-eye` — an experimental surface whose effects are the point

**Eight iron rules** — the legitimacy of an experimental interaction is that it *elevates* the
experience; anything that makes content harder to reach is rejected however good it looks:

- Every cursor / hover / gaze effect has a touch **and** keyboard equivalent (attach effects behind `pointer: fine`)
- Effects never block access to content — the cursor never blocks selection or clicks; hover-revealed content is reachable in the DOM
- `prefers-reduced-motion: reduce` kills **all** decorative motion; content fully visible and static
- Effect budget: heavy effects ≤ 2 per screen; magnetic subjects ≤ 5; WebGL hero ≤ 1 site-wide
- WebGL / shader degrades gracefully — static fallback when unavailable; above-the-fold content never depends on WebGL
- Content readable with no JS — clean semantic base markup, effects are progressive enhancement
- Performance budget: cursor lerp < 1ms inside rAF; ≥60fps desktop / ≥30fps mobile; WebGL hero ≤ 1.5MB
- The cursor never hijacks system behaviour — text caret / grab semantics still switch; hiding the system cursor demands an equivalent

### `game-style` — feedback and progression as the experience

**Eight iron rules**, of two kinds. Rules 1/4/5/6 are feel and performance; **2/3/7 are ethics and
carry an absolute veto — there is no "style exception" to them**:

- Celebration is capped: ≤1200ms complete, ≤1 per action, never chained, never taking the full screen
- **Honest progress** — progress reflects real state, never padded, never stalling at 99% to force a purchase
- **No fake urgency or dark patterns** — no fake countdowns, no streak blackmail, no pay-to-continue, no loot-box gambling
- Juice never blocks input — the next action is clickable during a celebration; animations interruptible
- Particles budgeted: confetti ≤ one burst of 80-150 for ≤2s; persistent shimmer / glow ≤ 1 per screen
- Motion-sensitive fallback keeps the feedback *semantics* while dropping bounce / particles / shake
- **A streak may not hold the user hostage** — offer a freeze or a make-up, never shame, never loss-aversion pressure
- Anti-childish-slop: no emoji piles, no rainbow, no sound spam; juice is restraint

### `bubble-physics` — physicality as enhancement

**Eight iron rules**. The philosophy: physics is **enhancement, not access** — it may never become
the only route to completing a task, nor perpetual visual noise:

- Physics drives `transform` / `opacity` only (`filter` / `clip-path` sparingly, ≤2 per screen)
- Every physics-driven affordance has a non-physics route to the same outcome
- Simulation stops when off-screen or when the tab is hidden
- `prefers-reduced-motion` replaces simulation with its end state, not with nothing
- Collision / overlap never hides content permanently
- Input stays responsive while the simulation runs
- Budgeted body count — a page-wide simulation is one, not several
- No perpetual motion as decoration: the system settles

---

## Six-dimension weight priors

Derived, never asked. The archetype implies the weights; the human corrects at the IA gate if a
particular surface is unusual. Scale is relative (all-5 == all-3): it decides where depth goes.

| archetype | Visual | Interaction | Motion | Perspective | A11y | Responsive |
|---|---|---|---|---|---|---|
| `landing-marketing` | 5 | 2 | 4 | 4 | 3 | 5 |
| `data-dashboard` | 3 | 4 | 2 | 5 | 4 | 3 |
| `canvas` | 4 | 5 | 5 | 5 | 3 | 2 |
| `narrative-scrolly` | 5 | 3 | 5 | 4 | 3 | 4 |
| `creative-eye` | 5 | 4 | 5 | 5 | 2 | 3 |
| `game-style` | 5 | 5 | 5 | 4 | 2 | 2 |
| `bubble-physics` | 4 | 4 | 5 | 3 | 2 | 3 |
| *(none assigned)* | 3 | 3 | 3 | 3 | 3 | 3 |

**A weight of 2 is not permission to skip.** The accessibility floor (contrast, focus visibility,
keyboard reach, reduced-motion) holds at every weight — the number moves how much *exploration*
a dimension earns, never whether the floor applies. See `slop-gates.md` for the floor itself.

## What "no archetype" means

A surface with no archetype assigned is not an error. It gets the flat prior above and only the
corpus-wide rules. Say so rather than inventing a kind: an archetype asserted without a
`primary_task` to derive it from is a guess wearing a contract's clothes.
