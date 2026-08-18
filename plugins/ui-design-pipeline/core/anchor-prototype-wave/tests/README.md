# anchor-prototype-wave — script regression tests

Durable, tracked regression suite for the two deterministic nav/verbatim scripts.
Solidifies the previously scratchpad-only checks from the nav-linker /
verbatim-import work (v1.3.0 / v1.4.0 / v1.4.1) so a `/clear` can't lose them.
Mirrors `companions/information-architecture/tests/` in spirit.

```bash
python core/anchor-prototype-wave/tests/run_tests.py
```

Exit 0 = all green. Pure stdlib. Both scripts mutate a wave dir, so every case
copies its fixture into a fresh tempdir first — the tracked `fixtures/` are never
modified.

## What each fixture pins

### `wire_navigation.py`

| Fixture | Pins |
|---|---|
| `wire/basic` | built target → wired (`../<slug>/index.html`, mock attrs stripped); unbuilt target (`ghost`) kept mock; no-target mock kept; real external untouched. **Idempotent** — a 2nd wire is a no-op and byte-identical (LEDGER A-item 5). `--check` green. |
| `wire/mock-class` | a wired link that still carries an `is-mock` **class** (rule-6(a) says style inert via the `[data-mock]` attribute, not a class) → non-blocking **WARN** in both `wire` and `--check`, exit code unchanged. The "live link in dead clothes" case a real author hit. |
| `wire/mock-inner-badge` | a wired link whose OWN class is clean but that still shows an inner `<span class="mock-tag">` badge because both its CSS rules are gated on `a[data-mock]` with **no bare default hide** → after wiring the badge falls back to visible → non-blocking **WARN**. Mirrors the real 2026-07-08 payment-method surface (finding #4). |
| `wire/mock-inner-badge-gated` | the SAME inner badge but with correct rule-6 gating (`.mock-tag{display:none}` default + `a[data-mock] .mock-tag{display:inline}`) → badge is hidden after wiring → **NO WARN**. Pins that the gate-aware check has no false positives on well-authored waves. |
| `wire/escalate` | **LEDGER A-item 4.** Wiring is keyed on on-disk existence, **not** on verdict. An `ESCALATE_HUMAN` page (`broken/`) is still a valid wire target, so an inbound link to it gets wired and its own back-link gets wired; `--check` stays **green** because the file exists. See finding below. |
| `wire/broken-check` | a pre-wired link whose href points at a never-built page → `--check` exits **1** (`leaves the wave or is broken`). |

### `import_verbatim.py`

| Fixture / case | Pins |
|---|---|
| `verbatim/source` → import | copies `index.html` + its 1 relative asset (`style.css`); the external CDN `<script>` is correctly skipped. |
| verify — stamp only | after import, an **additive** `data-nav-target` stamp on the mock link → `--verify` exit **0** (the one sanctioned edit). |
| verify — content edit | any other index.html change → exit **1** (`LOCK BROKEN`). |
| verify — asset differs | a modified copied asset → exit **1** (`asset differs from source`). |
| verify — asset missing | a deleted copied asset → exit **1** (`asset missing in dest`). |

## Finding recorded here (not a script bug)

**`wire/escalate` documents a real behaviour, not a defect.** `wire_navigation.py`
decides wire targets by "does `<slug>/index.html` exist on disk", which is
deterministic and simple by design. It does **not** read per-surface verdicts, so
it will wire an inbound link to a page that escalated (failed its gates 3×).

**Decided 2026-07-09 — keep this behaviour (wire by disk-existence); do NOT add a
"skip ESCALATE slugs" branch.** Rationale:
1. **The human gate precedes wire.** Per the skill, an escalation trips §When-to-stop
   item 2 — the pipeline stops and asks the human (manual edit / drop the surface /
   continue anyway) *before* stage 7.5 wire runs "after every surface's verdict has
   settled." So a page that reaches wire still carrying `ESCALATE_HUMAN` is one the
   human explicitly chose to keep. Wiring to it **honours** that decision; skipping
   would silently override it.
2. **Skipping creates a deferred-link bookkeeping problem.** wire is a stateless,
   idempotent one-pass op. To "skip now, wire after the fix" you'd have to persist
   which links were skipped + their targets and re-trigger a wire after the
   escalation resolves — new state to manage for no gain. Wiring now needs none of
   that: once the target is fixed the link already points at it (re-running wire is
   a no-op).
3. **No silent lie.** The master gallery renders the ESCALATE tile in its broken
   state as evidence, so a wired link landing there reads as a known-broken page.

This fixture therefore pins the status quo permanently so the behaviour can't drift.

## Inner-badge WARN (finding #4, added 2026-07-09)

The nav-linker-e2e live-browser run found a wired (live) link still showing a "mock"
badge. `wire_navigation.py`'s WARN used to inspect only the `<a>`'s own class, so an inner
`<span class="mock-tag">` badge slipped through. The WARN now also checks inner badge spans
and is **gate-aware**: it warns only when the badge class is NOT default-hidden by the
page's CSS (a bare, non-`[data-mock]`-gated `display:none`/`visibility:hidden` rule), so a
correctly-gated badge — which is physically present but invisible after wiring — does not
trip a false WARN. Honest limitation: this is a **static** CSS read (strips `/* */`
comments, takes the selector's last line). It can't evaluate computed styles, cascade
overrides, `[hidden]`/inline-style toggles, or JS-driven visibility — so it's a strong
heuristic for the rule-6 default-hide convention, not a render-accurate visibility oracle.
The live browser remains the ground truth for "is this badge actually visible".
