# Changelog

All notable changes to `ui-design-pipeline`. Versions follow the `version` field in
`.claude-plugin/plugin.json` — bump it on every release, or installers never see the update.

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
