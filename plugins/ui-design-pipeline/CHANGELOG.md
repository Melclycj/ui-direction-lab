# Changelog

All notable changes to `ui-design-pipeline`. Versions follow the `version` field in
`.claude-plugin/plugin.json` — bump it on every release, or installers never see the update.

## 0.3.1 — 2026-08-21

### Fixed
- **The landing-marketing and bubble-physics rule sets were partly invented, and are now
  transcribed.** They were written from each source file's opening lines plus inference rather
  than read in full — five of nine landing rules and three of eight bubble rules were mine, not
  the source's. Among the real ones that were missing: a 5-9 section count, CTA rhythm at
  1.5-2.5 viewport heights, an LCP and hero-media budget, F/Z reading path, and for physics the
  keyboard-completes-the-task-with-no-physics rule, throw friction and clamping, and settling
  within 1.2s. Caught by a pre-clear audit the same day, not by a reader.
- The provenance note claimed everything was carried over. Two of the seven weight-prior rows
  (narrative-scrolly, bubble-physics) have no row in the source and are this lab's proposal —
  now labelled as such, with the instruction to read a source rule in full before adding one.

## 0.3.0 — 2026-08-21

### Added
- **Surfaces have a kind, and it constrains what they must do.** Seven archetypes —
  landing-marketing, data-dashboard, canvas, narrative-scrolly, creative-eye, game-style,
  bubble-physics — each with iron rules carrying concrete numbers, plus six-dimension weight
  priors. `references/archetype-rules.md`.
- Assigned **per screen**, because a product has a marketing front page and an editor and they
  owe different things. Derived by the IA companion from the `primary_task` it already writes,
  and corrected by you at the review gate you already walk: **you are never asked to score
  anything.** The board shows the kind beside the task it came from, in both languages.
- Consumed at **both ends from one source** — Sectional Score will not propose a mechanism a
  surface's kind forbids, and slop-gates section (d) checks the kind's own rules at review.
- Two archetypes carry ethics rules with an absolute veto rather than a score: game-style's
  honest-progress / no-dark-pattern / no-streak-hostage, and creative-eye's never-block-access.
  No visual direction exempts a variant from those.

### Notes
- **Absence is a first-class answer.** No IA spec, or a screen whose kind is genuinely unclear,
  means the flat prior and the corpus-wide rules — an archetype asserted with nothing behind it
  would be a guess wearing a contract's clothes. An unknown *value*, by contrast, is blocked:
  nothing downstream has rules for a kind that does not exist.
- Style conflicts resolve one way: the locked L3 style wins the skin, the archetype wins the
  skeleton. A brutalist dashboard is still `tabular-nums`.

## 0.2.2 — 2026-08-20

Documentation only — no behaviour change.

### Added
- **The GSAP licence is now stated, and it is not the one the table already showed.** The
  nominated-skills table credits `gsap-*` as MIT, which is true of those eight skills and says
  nothing about the library the motion they teach runs on. Anyone installing this pipeline ships
  GSAP in what they build, so the terms belong here rather than in a reader's assumption.
- Verified against `gsap.com/community/standard-license/` and `gsap.com/licensing/`: free for
  commercial use since 2025-04-30 under Webflow, explicitly including the plugins that used to
  require a paid Club membership — SplitText and ScrollSmoother among them, both of which the
  generated motion already reaches for.
- Named as **proprietary, not MIT**, with its one prohibited use written down: a no-code visual
  animation builder competing with Webflow. That is not what this pipeline is, but writing it down
  means a later change of product shape re-opens the question instead of inheriting a stale yes.

## 0.2.1 — 2026-08-20

Documentation only — no behaviour change.

### Changed
- **The reference pools read in English.** The skills always did; the pools they draw candidates
  from did not, so opening `motion-pool` or `style-pool` after installing meant reading Chinese.
  The descriptive layer is now English across all eight files (23,556 CJK characters → 3,721).
- Style names got two treatments, because they are two different things. Neo-brutalist, Swiss
  International, Glassmorphism, Retro-futurism, Y2K and kinetic type were **restored** — the
  Chinese was the translation, not the original. The labels this lab coined keep theirs alongside:
  Field engineering (现场工程风), Cosmic archive (宇宙档案风), Bright collaborative (明快协作风),
  Minimal luxury (极简高级风). What defines a row is its anchor and URL, not the adjective.

### Deliberately not translated
- **Machine-parsed keys.** `check_registry_sync.py` matches the literal `【⚙执行册】` badge and the
  `C-NN` / `#N` row ids, so those are byte-identical; the sync is still 77==77.
- **Verbatim human verdicts**, in the words they were given in. Translating a recorded approval
  rewrites evidence.
- **threed-pool's status column**, which is the materialisation ledger and points at `material/…`
  paths an installer cannot resolve anyway. Its C-NN records had only the use-case call and the
  five-layer mechanism tag translated; the other cells were rebuilt byte-for-byte by script.

## 0.2.0 — 2026-08-20

A front door, a resume path, and half the always-on context back.

### Added
- **`core/ui-pipeline`** — the entry point. Asks one question (how many screens) and routes:
  one screen goes straight to `prototyping-ui-directions`, two or more start at
  `information-architecture` round 1. Before this, "give me a few UI directions" landed on the
  directions skill and silently skipped the step that stops every later page inventing its own
  layout.
- **`RUN.md`, a generated resume pointer.** A run spans sessions; re-asking a human for decisions
  they already made is this pipeline's most expensive failure. `core/ui-pipeline/scripts/
  render_run.py` recomputes the pointer from the append-audited machine state plus what is on
  disk — it is never hand-maintained, because one missed update leaves a pointer claiming the run
  is somewhere it is not, and the next session believes it. Each render stamps the sha256 of the
  state it read.
- **A freshness gate.** `preflight_wave.py` now BLOCKs the wave on a stale or unstamped `RUN.md`,
  naming the re-render command. A run without one was not started through `ui-pipeline`: noted,
  allowed. Honest limit: the pointer cannot lie, but only the wave forces it current.
- 23-case regression suite for the pointer (checks 129 → 152), including that rendering never
  writes back to the state it reads.

### Changed
- **Only 6 of 22 skills are registered.** `three/` (11), `extensions/` (3) and the two authoring
  rulebooks are read by path (`Read ${CLAUDE_PLUGIN_ROOT}/…`) and never model-invoked, so their
  descriptions bought always-on context for discovery that never happens. Dropping them from the
  manifest's `skills` array takes the description budget from ~2,022 to ~1,065 tokens (-47%) even
  after adding the entry skill. They still ship, at the same paths; they can no longer be called
  by name.
- **`taste-skill` and `design-system` moved to `authoring/`.** The manifest registers by
  directory, so staying inside `companions/` meant staying registered. 17 path references updated
  across the plugin and the lab.
- `prototyping-ui-directions` now defers to `ui-pipeline` in its description — without that, the
  entry fix would not hold, because the two competed for the same phrasing.

## 0.1.0 — 2026-08-18

First packaged release. The pipeline itself has been in use inside the
private lab since 2026-07; this is the first
version installable by anyone else.

### Added
- `.claude-plugin/plugin.json` + a root `marketplace.json`, so the lab installs with
  `/plugin marketplace add Melclycj/ui-direction-lab` instead of `cp -R`.
- 21 skills: `core/` (2), `companions/` (5), `extensions/` (3), `three/` (11).
- The `lock → wave` approval gate now ships as a plugin hook. Before this it existed only as a
  project-local hook, which meant it did not run for anyone who installed the skills — silently.
- `LICENSE` (MIT) and an installer-facing `README.md`.

### Changed
- Cross-skill references use `${CLAUDE_PLUGIN_ROOT}/…` instead of assuming a flattened
  `.claude/skills/<name>/` deployment.
- `check_registry_sync.py` and `resolve_candidates.py` search upward for the lab material corpus
  instead of climbing a fixed number of parents, and report `SKIPPED (lab-only check)` when it is
  absent rather than passing quietly.

### Not shipped (nominated instead)
- The 8 GreenSock `gsap-*` skills, `frontend-design`, `grill-with-docs`, `competitive-teardown`,
  `codex-dispatch` and `shadcn-registry` are third-party work with their own upstreams — several of
  which are installable plugins in their own right. Each call site says how to install them and what
  degrades without them. See README § *Not shipped — nominated*.
- The `testbed/` material corpus (~20MB tracked) stays in the lab repo. A separate `ui-material-library`
  package is planned.
