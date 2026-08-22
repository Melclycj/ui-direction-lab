**English** | [简体中文](README.zh-CN.md)

# UI Direction Lab

**A design pipeline that turns one line of product intent into a locked design system and a full set of production-grade pages** — built as Claude Code skills, with a deterministic gate and a named human decision at every step.

The premise: taste is not automatable, but everything around it is. Machines check that the code is correct, that it obeys the locked design chassis, and that nothing drifted since it was last verified. *Which direction is good* stays a human call — at named decision points (nine on the main line, two more once motion is engaged, two more if the IA companion runs), not implicitly buried in a prompt.

![Vernata home — WebGL skyline hero, built by this pipeline](docs/media/vernata-home.png)

---

## What has been built with it

### Vernata — marketing site for an AI delivery studio

Three pages produced end-to-end by the pipeline: a home page with a WebGL systems gallery, a delivered-work page, and a booking page wired to a Cloudflare Pages Function and a transactional email backend. Design tokens are a single locked chassis shared across all three.

Production-ready; awaiting a domain; its repository is not public. This is also the
run photographed in [What a run actually looks like](#what-a-run-actually-looks-like) below —
every artifact in that walkthrough came from building this site.

---

> **Install** · `/plugin marketplace add Melclycj/ui-direction-lab` then
> `/plugin install ui-design-pipeline@ui-direction-lab` — 22 skills, Python ≥ 3.9,
> standard library only. [Full instructions below.](#install)

---

## How the pipeline works

Three skills carry the run, and the line drawn between them is the whole design:

- **`information-architecture`** settles *what information is on each screen and what dominates*
  — blocks, tier, scan order, the task the screen serves, the link map. It is deliberately
  **layout-open**: it does not decide where anything sits, and it is linted for leaking that
  decision, because the choice belongs to you one stage later.
- **`prototyping-ui-directions`** varies *composition and visual together* — sidebar or top nav,
  table or bento, plus type, palette and motion — across whole competing directions. You pick
  one. Your pick freezes into the chassis: tokens, composition pattern, motion stance.
- **`anchor-prototype-wave`** produces every remaining page against that frozen chassis, in
  parallel, validating and self-repairing each one.

IA runs **twice**, and the second run is what makes the third skill safe: it generalises the
composition you just locked into grey-box wireframes for the screens nobody has designed yet.
Those become the wave's `production_source`, and against such a source the wave is **barred from
re-laying anything out**. It colours; it does not compose. Skip round 2 and every page invents
its own layout, and the product stops being one product. Only a single-screen run can skip it.

The rest is gates. `●` = you decide; everything else runs unattended.

```
[one line of product intent]
   │
   │   ┌ IA ROUND 1 · optional, for anything past a single screen ──────────┐
   │   │ Normalise whatever you have — a feature list, rough sections, or a │
   ├───┤ paragraph of intent — into a whole-product info-spec plus a        │
   │   │ grey-box review board.                                             │
   │   │ ● you approve INFORMATION STRUCTURE. Grey on purpose: you judge    │
   │   │   what each screen holds and what dominates, not how it looks.     │
   │   └────────────────────────────────────────────────────────────────────┘
   │     the hero screen's spec enters the main line as a hard constraint
   ▼
Stage 0 · intent Q&A ............... ● 4 questions, all defaultable
   ▼
gate #0 ............................ ● a reference to work from,
                                       or open exploration?
   ▼
BATCH 1 · 3–4 visual directions .... ● pick the LEAD
  the exploration branch always
  includes one ANCHOR — a faithful
  rebuild of a real product, there
  to keep the others honest
   ▼
contrast gate · WCAG computed ...... ● fix, or accept knowingly — the ratio
  per text-role token pair,            is written down, because that debt is
  before anything is frozen            inherited by every page produced later
   ▼
BATCH 2 · 2–3 motion stances ....... ● pick one
  visual frozen pixel-identical
  to the LEAD
   ▼
LOCK THE CHASSIS → tokens + CHASSIS.md
   │
   │   ┌ IA ROUND 2 · same swimlane, now that composition is settled ───────┐
   ├───┤ Generalise the locked composition pattern to every remaining       │
   │   │ screen as grey-box wireframes — flag gaps, never invent content.   │
   │   │ ● Stage-F gate: you walk them                                      │
   │   └────────────────────────────────────────────────────────────────────┘
   │     wireframes become the wave's production_source: colour only,
   │     never re-layout
   ▼
● Sectional Score .................. at most one bounded section
                                       choreography — or skip, which is
                                       the default answer
   ▼
● lock → wave ...................... an explicit approval word; a hook
                                       blocks the fan-out without it
   ▼
SURFACE WAVE · N pages in parallel
  each page: validate → score →      ● you are interrupted only when a page
  fix-on-fail, up to 3 retries         still fails after the third try
   ▼
● Atomic Pass ...................... you approve a BUDGET — how many targets,
                                       which properties — not each effect
   ▼
● accept the gallery
   │
   └─►optional, on request: audit & polish ║ visual regression ║ certification
```

**One axis per batch.** Visuals change, then freeze; then motion changes. Deliberate — it is
what stops the review becoming a combinatorial mess where you cannot tell which change you
are reacting to.

**Motion is a separate axis with its own three widths and its own gates** — see
[Motion](#motion) below.

---

## What a run actually looks like

The diagram above, executed once — for the Vernata site, which the pipeline built under the
product's earlier name, **Averonel**. Every frame is an artifact that run produced.

### 1 · The information plan — IA round 1

![IA round 1 — grey review board for the hero screen](docs/media/run-1-ia-board.png)

**On screen** — every block the screen will hold, one row each, ordered by scan path (the
numbered dots), sized by priority tier, tagged with the role it plays; above them, the single
task this screen exists to serve.

**How to read it** — read straight down the numbers and ask whether that is the order a stranger
should meet the product in, and whether the tallest boxes are what you would actually want
remembered. It is grey because there is nothing here to be persuaded by: no typeface, no colour,
no image. What you are judging is the information and its priority, alone.

**What you give back** — approve, or move, re-tier and cut blocks. A human gate; the run stops
here until you answer.

**What it binds** — every direction in the next stage must carry these blocks at these tiers.
All this step does is **mark the information** — what it is, what it is worth, what order it is
met in — so that whatever gets built later emphasises what a reader needs to notice. What it
deliberately leaves open is *where anything sits*, because that is the choice you get next.

### 2 · The directions — batch 1, then motion

![Batch 1 direction gallery — five directions, V5 Civic Control selected](docs/media/run-2-directions.png)

**On screen** — whole competing directions, each a working page, switched from the top bar. The
footer carries the selected one's palette and its reasoning in a single line of data.

**How to read it** — judge them against each other, not against an ideal in your head. One of
them is the **ANCHOR**, a faithful rebuild of a real product, kept in the lineup precisely so the
generated ones have something honest to lose to.

**What you give back** — one LEAD, and **you are not confined to what is on offer.** Ask for a
cross of two (this run did — the selected fifth tab is a hybrid requested mid-review). Ask for
palette, theme or density sub-variants of one direction: they appear as a second tab row off the
same file, so trying a colour scheme costs no new batch. Or ask for another batch entirely, in a
style none of these five went near. The gallery is a place to keep looking, not a form to submit.

Before the pick freezes, contrast is computed for every text-role token pair and you either fix a
failure or accept it knowingly. Motion is a second, separate pick.

**What it binds** — your pick becomes the chassis: tokens, motion stance, and the composition
pattern. The approval is stored in your own words — here 「锁 V5 + Dossier depth，放掉 V1」,
*lock V5 plus the Dossier-depth motion stance, drop V1*. From this point the composition is no
longer negotiable, which is what makes the next step possible.

### 3 · The layout law — IA round 2

![IA round 2 — grey-box wireframe of the delivered-work page](docs/media/run-3-wireframe.png)

**On screen** — the screens nobody has designed yet, drawn as grey boxes using the composition
pattern lifted out of the chassis you just locked. Here that pattern is `civic-register`: left
registration rail, rule-separated indexed sections, no cards. Unknowns appear as explicit
`[SLOT]`s marked PENDING.

**How to read it** — this is the page you are going to ship, minus colour and content. If a
block sits wrong here it will sit wrong live, and this is the cheapest moment it will ever be to
move.

**What you give back** — walk each screen and approve it, or say what is missing. The skill's
standing rule is *flag, never invent*: it will not fill a gap with plausible content to make the
wireframe look finished.

**What it binds** — **this is the step that keeps a multi-page product one product.** Moving a
block between regions or swapping the flow mechanism is on the wave's banned list; it colours
what you signed off. Without it you would be reviewing twelve opinions instead of one product.

### 4 · The production wave

![The delivered-work page as shipped](docs/media/vernata-work.png)

**On screen** — the shipped page. Compare it to frame 3: same rail, same section order, same
record panels, same `LIVE · IN USE` tags. Colour, type and real content are the only things that
arrived.

**How to read it** — as a check on the wireframe, not as a fresh design. Anything here you did
not see in grey is something that slipped past a gate.

**What you give back** — almost nothing, deliberately. You said an approval word to start the
wave, and you accept the gallery at the end. In between you are interrupted only when a page
still fails validation after three self-repair attempts.

**What it binds** — nothing about composition was renegotiated at production time. That argument
had already been had, twice, in grey.

---

## Motion

Motion is chosen **widest-first**, and the order is enforced rather than recommended. An
irreversible state machine — `CHASSIS_OPEN → CHASSIS_LOCKED → SECTIONAL_OPEN → SECTIONAL_LOCKED
→ BASE_WAVE_READY → ATOMIC_OPEN → COMPLETE` — advances only on a recorded approval of yours, and
never runs backwards. Three widths, three separate moments in the run:

| Width | What it owns | Where it is decided | The default |
|---|---|---|---|
| **Chassis** — page-scoped mechanism | the global scroll model, any persistent WebGL/canvas stage, the motion vocabulary and token floor, the performance ceiling and its fallback policy | declared per direction in **Batch 1**, picked in **Batch 2**, where the visual is frozen pixel-identical so the only thing you can be reacting to is the motion | `null` — a static visual chassis. A first-class stance, and the usual answer |
| **Sectional** — one bounded choreography | one section's orchestration on a nominated surface: bounded container, local progress, releases on exit | the **Sectional Score** ceremony, after composition is settled and before the wave starts | none. Most surfaces are never nominated, and skip is the default answer |
| **Atomic** — effects on components that already exist | small effects patched onto the real DOM under a no-reflow budget | the **Atomic Pass**, after `BASE_WAVE_READY`, chosen against the real DOM and filtered by a resolver | you approve a *budget* — how many targets, which properties — not each effect |

Once the chassis locks, a page-level mechanism can never be introduced later; there is no path
back up the ladder. The production wave is barred from improvising atomic effects at all, and a
preflight plus a hook both refuse to let the Atomic Pass start early.

### Why a library, and not motion written fresh each time

Because motion is the one thing here that is both hard to say and easy to get wrong.

**Hard to say.** Most people cannot describe an animation in words — not for lack of taste, but
because the vocabulary barely exists outside the people who build them. "Make it feel premium" is
not a specification. A library turns *describing* into *pointing at*, which anyone can do
accurately.

**Easy to get wrong.** An agent improvising motion returns a different result every run —
different mechanism, different quality, cost unknowable until it is already built, and no way to
tell a good outcome from a lucky one. Choosing from mechanisms already built and measured takes
that variance out of the decision, leaving only the question a human can actually answer: does
this motion suit this product?

### What ships where

This plugin ships the **decision layer**: a motion pool of 31 numbered mechanisms, plus 3D,
component, palette, font and style pools. Every entry carries a build recipe against the GSAP
skills — which GSAP plugin, which call, what to stagger — so the pool is usable on its own.

The layer underneath ships as a package of its own. Each of those entries also points at the
module that proves it — the pools reference `material/…` modules 74 times — and those modules
are published as [**ui-material-library**](https://github.com/Melclycj/ui-material-library),
installed separately ([why they are not bundled](#where-this-comes-from)). The per-entry tags
come from that corpus too — driver, mechanism, carrier, content register, and a compute-cost
rating — none of which can be written honestly from watching a demo video. Somebody built the
thing, ran it, and measured it.

That is the library's real job: a motion decision is only worth making if the mechanism behind
it has been built once and its cost is known.

**Without the library installed** the pipeline still runs whole; it just stops pretending. A
described mechanism degrades to *described but not built*, said in so many words, and the
optional pre-filter that proposes candidate modules by content shape refuses rather than
quietly returning nothing. With both installed, the pipeline's reconciliation script finds the
library and every pointer resolves again — `check_registry_sync.py --material-root` pins the
location explicitly if it cannot.

### The library itself — 54 verified modules

**Not an output of this pipeline — an input to it.** Each module was extracted by hand from a
real implementation, not generated, then frozen by a verification harness before anything ships.

Scroll-driven WebGL scenes, shader transitions, physics slideshows, layout-FLIP choreography,
pointer-reactive grids. Each is one applyable module plus a demo that consumes that same module —
**never a second implementation** — with a machine-checked receipt proving the shipped code is
byte-identical to what was verified. Seven are in production on the Vernata site.

| | |
|---|---|
| ![Shard-constructed vessel, each piece repelled by the pointer](docs/media/piece-shard-vessel.jpg) | ![Infinite draggable WebGL slider with RGB-split distortion](docs/media/piece-draggable-rgb-slider.jpg) |
| ![Scroll-rotated gallery built from pure CSS 3D transforms — no canvas](docs/media/piece-css3d-scroll-rotate.jpg) | ![Triangle-mesh image transition, two switchable variations](docs/media/piece-polygon-image-transition.jpg) |
| ![Pointer-driven RGB-shift distortion over a hovered image](docs/media/piece-motion-hover-distortion.jpg) | ![Three thousand particles morphing through a scroll-scrubbed sequence](docs/media/piece-particle-shape-morph.jpg) |

*Six of fifty-four. Every frame above was captured by running the module's own demo — the same file a consuming page imports.*

---

## What the machine actually guarantees about the UI

Generating a page is the easy half. The hard half is that a model asked for "a modern
landing page" will reliably produce the same page — centred hero, purple-blue gradient,
emoji bullets, a palette that drifts warm on one section and cool on the next. This
pipeline treats those as **failures with names**, checked by code, not as taste notes
someone might remember to apply.

Every produced surface runs a validator that returns `BLOCK` / `FIX_NEEDED` / `PASS`.
The ones that matter visually:

| Enforced | What it stops |
|---|---|
| **Contrast, computed before the lock** | Every text-role token pair is run through WCAG *before* the design system is frozen. Failures come back as a list of specific pairs. You may accept one knowingly — and the ratio is written into `CHASSIS.md`, because that debt is inherited by every page produced afterwards. |
| **Gradients banned unless allowlisted** | Any `linear-gradient` / `radial-gradient` outside a semantic allowlist blocks the page. This is the single most recognisable tell of generated design, so it is a gate, not advice. |
| **Accessibility floor blocks, not warns** | A `<button>` with no accessible name, an `<input>` with no label or `aria-label`, or any declared motion without a `prefers-reduced-motion` fallback — each stops the page. |
| **You get the pattern you claimed** | A surface declared as an overlay must actually contain a panel *and* a scrim; a drawer must carry an anchor-side rule. A page cannot claim a UI pattern it did not build. |
| **Named anti-slop rules** | Enforced by a red-team pass, quoting its own wording: *"the AI Purple/Blue aesthetic is strictly BANNED — no purple button glows, no neon gradients"*; no emoji anywhere including alt text; one palette per project, no drifting between warm and cool greys; centred heroes banned above a layout-variance threshold. |
| **Content is grounded, not invented** | A surface built from a production source is checked against it. Mock links are labelled as mock rather than looking real. |

Behind those sits the part you never see: the lock from design system to page production
is held by a **hook, not an instruction** — the model may propose skipping a step, but it
cannot act on that until you answer with an explicit approval word. That one became code
after instructions alone were measured to be insufficient.

**152 automated checks** cover the machinery itself: 97 pipeline assertions, 16 production test
functions, 16 information-architecture fixtures, and 23 on the resume pointer — including that
rendering it never writes to the state it reads. All green from a clean install.

### The standards behind those checks

The blocking rules above are published standards, not house style: **WCAG 2.1 AA** contrast with
**APCA** (`Lc ≥ 60` / `Lc ≥ 45`) as a cross-check, **WAI-ARIA** state semantics, **WCAG 2.2.2**
for pause-on-hover-and-focus, and `prefers-reduced-motion` for anyone who asked for less.

A second and larger set is used as **review lenses that produce findings but never block** — one
named HCI set, held in a single file so the two core skills cannot drift apart: visual hierarchy
(Tognazzini, Krug), data-ink density (Tufte), F/Z scanning (NN/g), typographic rhythm
(Bringhurst), cognitive load (Hick's, Miller's, Fitts's — choices ≤ 7±2, targets ≥ 44px),
affordance clarity (Norman), aesthetic-usability (Kurosu & Kashimura), Jakob's Law. Findings
arrive tagged BLOCKER / MAJOR / MINOR with `file:line` citations and feed the polish companion.
They deliberately do not gate a release: a heuristic score is a judgement, and judgements are not
allowed to masquerade as gates here.

The information layer has its own lineage — Priority Guides and Page Description Diagrams
(Dan Brown, 1999) for tiering, OOUX for object anchoring.

### Honest boundaries

Stated up front, because a tool that overstates itself is worse than one that does less:

- **Whether it looks good is always a human call.** Scorers guarantee "written correctly, obeys the chassis" — nothing more.
- **A validator cannot see inside a `<canvas>`.** WebGL surfaces are machine-checked for console errors, leaks and API misuse; how they *feel* must be watched with human eyes.
- **It stops at the front end — for now.** Variants and produced surfaces are static review code; cross-page links are mocked and labelled as such. An explicit interface for wiring a prototype to a real backend is the next thing being built, rather than left to ad-hoc glue per project.
- One run serves one register. A marketing site and an app console are two runs and two chassis.
- **The extensions are the least-proven part of the plugin.** See [Optional extensions](#optional-extensions) for what that means concretely.
- **The reference pools keep some Chinese on purpose.** Their descriptive layer is written in English, but recorded human verdicts are quoted verbatim in the language they were given in — mostly Chinese — and a handful of machine-parsed identifiers stay untouched because tooling matches on them exactly. What remains is provenance, not an untranslated backlog; the pipeline behaves identically either way.

---

## Install

```
/plugin marketplace add Melclycj/ui-direction-lab
/plugin install ui-design-pipeline@ui-direction-lab
```

22 skills, 1.4 MB. Requires Python ≥ 3.9 — standard library only, no pip packages.

**6 of the 22 are registered for discovery**, costing ~1.1k tokens of always-on description
context. The other 16 — the Three.js layer, the wave extensions, the authoring rulebooks — ship
at their normal paths and are read by the skill that needs them, so they cost nothing until they
are used. Registering all 22 would have cost roughly twice that for discovery that never happens.

Installing also installs **one hook**, a `PreToolUse` gate on subagent dispatch. It intercepts
only a spawn that would author a wave surface without your recorded approval; exploration,
reviews and every other agent pass through untouched, and it fails open on its own errors rather
than bricking a session.

Third-party skills this pipeline calls — GreenSock's GSAP set, Anthropic's `frontend-design`, and four others — are **nominated rather than redistributed**: each call site names how to install it from its own source, and what degrades if you don't. Details in [`plugins/ui-design-pipeline/README.md`](plugins/ui-design-pipeline/README.md).

### How you call it

The plugin ships **skills, not commands of its own** — there is no `/run-pipeline` to memorise.
Two ways in:

- **Describe what you want.** *"Design the marketing site for a booking tool"* or *"give me a few
  UI directions"* is enough. One line about the product; the pipeline asks for the rest in order.
- **Name one explicitly.** Registered skills are namespaced — `/ui-design-pipeline:ui-pipeline`.

Either way you land on **`ui-pipeline`**, the front door. It establishes one run directory, asks
a single question — how many screens? — and routes: one screen goes straight to directions, two
or more start at IA, because that is the step that stops every later page inventing its own
layout. From there it hands off down the chain by itself.

### Resuming an interrupted run

A run spans several sessions, and re-asking a human for decisions they already made is the most
expensive failure this pipeline has. So each run keeps a `RUN.md` at its root — stage by stage,
what is done, what comes next, and every approval in the words the user actually gave. Say
you want to continue and the front door reads it before asking you anything.

**It is generated, not maintained.** "Remember to update the ledger" is an instruction, and one
missed update leaves a pointer claiming the run is somewhere it is not — worse than no pointer,
because the next session believes it. Instead `RUN.md` is recomputed from the append-audited
machine state plus what is on disk, and stamped with the hash of the state it came from. The
wave preflight refuses to start on a stale or hand-written stamp.

The honest limit: this makes the pointer unable to lie, not guaranteed to be current. Only the
wave forces a re-render.

### Optional extensions

Three opt-in add-ons hang off the production wave. They stay off unless you name them in the
wave's `extensions:` input; the full table (name, hook point, what each adds) lives in
`core/anchor-prototype-wave/SKILL.md` §Extensions.

| Name | What it adds | Purely additive? |
|---|---|---|
| `versions` | snapshots every surface, plus a version switcher on each page and update badges in the gallery | yes — it runs after the wave |
| `elements` | atom foundation pages (buttons, forms, nav) built on the same chassis, useful for checking the chassis holds at atom level | yes — extra pages; the product surfaces are untouched |
| `dark-mode` | light and dark on every surface via a token override, a theme toggle and per-prototype persistence | **no** — it is woven into surface authoring, so every produced surface's code changes |

**Honest state.** This is the least-exercised part of the plugin. `versions` has been reworked
twice; `dark-mode` and `elements` have not been touched since the initial commit. None of the
three is covered by the 152 automated checks, and none of them was used in the run shown above.
They relax no gate — the validator's `dark-by-default` ban still applies under `dark-mode`.
Treat them as specified and wired, not as proven.

---

## Repository map

| Path | What it is |
|---|---|
| `plugins/ui-design-pipeline/` | The distributable plugin — 22 skills, the approval hook, its own README |
| ├ `core/` | The front door, then the two engines: direction exploration, then chassis-locked production |
| ├ `companions/` | Information architecture, plus the audit-polish and visual-regression companions that run on any frontend directory |
| ├ `authoring/` | Rulebooks the engines read while authoring: the anti-slop taste red-team, a ~165-system design-system catalog |
| ├ `extensions/` | Opt-in add-ons to the production wave: dark mode, atom pages, version snapshots |
| └ `three/` | 11 Three.js / WebGL skills (10 vendored MIT + 1 original) |
| `docs/media/` | The screenshots above — captured by running each thing, not mocked up |

Only `plugins/` is installed. The showcase assets sit outside it on purpose: a plugin
install copies the whole plugin directory and ignores `.gitignore`, so 2.0MB of
screenshots would otherwise land on every installer's disk.

### Where this comes from

This repository is the published face of a working lab that stays private. The lab holds
what a published repository should not: third-party skills kept for local use and
deliberately not redistributed, the raw iteration runs behind every admitted module, and a
work ledger that quotes its author and names clients.

The 54-piece material corpus is published too — as
[**ui-material-library**](https://github.com/Melclycj/ui-material-library), its own package
rather than part of this one, for two reasons past size. It grows in batches while the
pipeline's skills stay stable, so one shared version number would mean bumping the pipeline
every time a module lands. And each piece has to clear a provenance pass before it can be
redistributed — three of the original 57 have been withdrawn on licence grounds — a rhythm
that belongs to the library, not the pipeline.

Both public repositories are generated from the lab by a one-way sync; nothing is edited in
either of them directly.

---

## Status

Actively developed. The pipeline and the material library are in daily use; the plugin packaging landed in August 2026. The site above is complete and awaiting deployment.

Licensed MIT — see [`LICENSE`](LICENSE). Third-party provenance is recorded per piece; vendored groups carry their upstream terms verbatim rather than a restated summary.
