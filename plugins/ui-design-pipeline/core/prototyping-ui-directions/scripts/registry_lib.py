#!/usr/bin/env python3
"""registry_lib.py — load + validate the motion/threed execution registry.

Shape canon: ../references/execution-contracts.md (this module is the MACHINE
source for the enums; the contracts doc explains their semantics — change both
together). Consumed by check_registry_sync.py, resolve_candidates.py and
pipeline_state.py.

No third-party dependencies. Python 3.10+.
"""
from __future__ import annotations

import json
from pathlib import Path

# --- controlled vocabularies (execution-contracts.md §2) ---------------------

FOOTPRINTS = {"chassis", "sectional", "atomic"}
PHASES = {"chassis", "sectional", "atomic"}
DRIVERS = {"load", "pointer", "click", "scroll", "timeline", "none"}
CARRIER_SCOPES = {"page", "section", "component", "overlay"}
PERF_TIERS = ("light", "medium", "heavy")  # ordered: index = rank
AVAILABILITY = {"available", "unavailable-source", "shelved", "anchor-only",
                "index-only", "not-graduated", "license-restricted"}
TAG_SOURCES = {"pool-tags", "classified-from-row", "none"}
REFERENCE_SCOPES = {"full-page-demo", "section-demo", "component-demo",
                    "technique", "tutorial-demo", "site-anchor", "index"}

BOUNDARY_VOCAB = {
    "owner-wrapper", "local-progress-0..1", "stage-releases-on-exit",
    "teardown-on-exit", "contained-canvas", "scoped-input-listeners",
    "wheel-interception-local", "no-global-scroll-hijack", "no-nav-replacement",
    "pause-offscreen", "text-split-restores", "paired-asset",
    "needs-bundler-inline",
}

MUTATION_VOCAB = {
    "transform-only", "opacity-filter", "color-border-shadow", "pseudo-elements",
    "overlay-canvas", "dom-overlay-elements", "dom-text-split",
    "dom-text-replacement", "owner-canvas-stage", "local-pin",
    "local-sticky-stage", "local-section-height",
    "layout-state-transition-within-owner", "camera-state-within-owner",
    "color-narrative-zones", "cross-section-persistent-state",
    "global-scroll-hijack", "nav-replacement", "body-input-interception",
}

# mutations that force effective footprint = chassis (contracts §3 rule 4)
CHASSIS_FORCING_MUTATIONS = {
    "global-scroll-hijack", "nav-replacement", "cross-section-persistent-state",
    "body-input-interception",
}

# mutations an Atomic Pass may perform (contracts §1 atomic; §3 rule 6)
ATOMIC_SAFE_MUTATIONS = {
    "transform-only", "opacity-filter", "color-border-shadow", "pseudo-elements",
    "overlay-canvas", "dom-overlay-elements", "dom-text-split",
    "dom-text-replacement",
}

# fields a NON-selectable record must NOT carry (zero-guessing guard:
# no fabricated classification on unavailable / not-graduated / anchor rows)
CLASSIFICATION_FIELDS = (
    "supported_footprints", "preferred_footprint", "allowed_phases", "driver",
    "supported_carrier_scopes", "boundary_requirements", "possible_mutations",
    "perf_cost", "fallback", "mechanism_family",
)

DEFAULTS = {
    "selectable": True,
    "availability": "available",
    "can_bound": True,
    "requires_global": False,
    "requires_existing_ui": False,
    "material": None,
    "perf_note": "",
    "notes": "",
    "boundary_requirements": [],
    "possible_mutations": [],
    "register_affinity": [],
}

SOURCE_POOLS = {"threed-pool", "motion-pool"}


def perf_rank(tier: str) -> int:
    """light=0 < medium=1 < heavy=2; unknown -> raises ValueError."""
    return PERF_TIERS.index(tier)


def load_registry(path: str | Path) -> list[dict]:
    """Load records and apply DEFAULTS (immutably: returns new dicts)."""
    raw = json.loads(Path(path).read_text(encoding="utf-8"))
    records = raw.get("records")
    if not isinstance(records, list):
        raise ValueError("registry has no records[] list")
    out = []
    for rec in records:
        merged = dict(DEFAULTS)
        merged.update(rec)
        out.append(merged)
    return out


def _subset_check(rec_id: str, field: str, values, vocab, problems: list[str]) -> None:
    if not isinstance(values, list) or not values:
        problems.append(f"{rec_id}: {field} must be a non-empty list")
        return
    bad = [v for v in values if v not in vocab]
    if bad:
        problems.append(f"{rec_id}: {field} has invalid value(s) {bad}")


def _subset_check_may_be_empty(rec_id: str, field: str, values, vocab, problems: list[str]) -> None:
    if not isinstance(values, list):
        problems.append(f"{rec_id}: {field} must be a list")
        return
    bad = [v for v in values if v not in vocab]
    if bad:
        problems.append(f"{rec_id}: {field} has invalid value(s) {bad}")


def validate_records(records: list[dict]) -> list[str]:
    """Return a list of problem strings (empty = valid)."""
    problems: list[str] = []
    seen_ids: set[str] = set()

    for rec in records:
        rid = rec.get("id") or "<missing-id>"
        if rid in seen_ids:
            problems.append(f"duplicate id: {rid}")
        seen_ids.add(rid)

        pool = rec.get("source_pool")
        if pool not in SOURCE_POOLS:
            problems.append(f"{rid}: source_pool invalid: {pool!r}")
        elif not str(rid).startswith(pool + ":"):
            problems.append(f"{rid}: id must start with '{pool}:'")

        avail = rec.get("availability")
        if avail not in AVAILABILITY:
            problems.append(f"{rid}: availability invalid: {avail!r}")
        if rec.get("tag_source") not in TAG_SOURCES:
            problems.append(f"{rid}: tag_source invalid: {rec.get('tag_source')!r}")

        if rec.get("selectable"):
            if avail != "available":
                problems.append(f"{rid}: selectable record must have availability=available (got {avail!r})")
            if rec.get("tag_source") == "none":
                problems.append(f"{rid}: selectable record needs tag_source pool-tags|classified-from-row")
            if rec.get("reference_scope") not in REFERENCE_SCOPES:
                problems.append(f"{rid}: reference_scope invalid: {rec.get('reference_scope')!r}")

            _subset_check(rid, "supported_footprints", rec.get("supported_footprints"), FOOTPRINTS, problems)
            _subset_check(rid, "allowed_phases", rec.get("allowed_phases"), PHASES, problems)
            _subset_check(rid, "driver", rec.get("driver"), DRIVERS, problems)
            _subset_check(rid, "supported_carrier_scopes", rec.get("supported_carrier_scopes"), CARRIER_SCOPES, problems)
            _subset_check_may_be_empty(rid, "boundary_requirements", rec.get("boundary_requirements"), BOUNDARY_VOCAB, problems)
            _subset_check_may_be_empty(rid, "possible_mutations", rec.get("possible_mutations"), MUTATION_VOCAB, problems)

            pref = rec.get("preferred_footprint")
            sup = rec.get("supported_footprints") or []
            if pref not in FOOTPRINTS:
                problems.append(f"{rid}: preferred_footprint invalid: {pref!r}")
            elif isinstance(sup, list) and sup and pref not in sup:
                problems.append(f"{rid}: preferred_footprint {pref!r} not in supported_footprints")

            if rec.get("perf_cost") not in PERF_TIERS:
                problems.append(f"{rid}: perf_cost invalid: {rec.get('perf_cost')!r}")
            if not str(rec.get("fallback") or "").strip():
                problems.append(f"{rid}: fallback is required and must be non-empty")
            if not str(rec.get("mechanism_family") or "").strip():
                problems.append(f"{rid}: mechanism_family is required")
        else:
            if avail == "available":
                problems.append(f"{rid}: non-selectable record must give a reason availability (not 'available')")
            fabricated = [f for f in CLASSIFICATION_FIELDS
                          if f in rec and rec.get(f) not in (None, [], "", {})
                          and rec.get(f) != DEFAULTS.get(f)]
            if fabricated:
                problems.append(f"{rid}: non-selectable record carries fabricated classification fields {fabricated}")

    return problems
