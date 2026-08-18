# Changelog

All notable changes to `ui-design-pipeline`. Versions follow the `version` field in
`.claude-plugin/plugin.json` — bump it on every release, or installers never see the update.

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
