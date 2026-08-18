#!/usr/bin/env python3
"""Resolver cases for run_tests.py — covers the plan's deterministic test
matrix items 1/2/3/4/5/6/7/13 plus batch2-tuning, footprint-unsupported and
unknown-id contract errors. Uses the REAL registry (the records under test are
plan-audited classifications)."""
from __future__ import annotations

import json
import os

RESOLVE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts", "resolve_candidates.py")

SECTION_CARRIER = {
    "owner_scope": "section", "bounded_container": True, "local_progress": "0..1",
    "releases_on_exit": True, "persistent_stage_scope": "section",
    "top_level_siblings_depend": False, "global_side_effects": [],
    "local_pin_allowed": True, "section_height_change_allowed": True,
}
PAGE_CARRIER = {
    "owner_scope": "page", "bounded_container": False, "local_progress": None,
    "releases_on_exit": False, "persistent_stage_scope": "page",
    "top_level_siblings_depend": True, "global_side_effects": ["document-scroll-controller"],
}
COMPONENT_CARRIER = {
    "owner_scope": "component", "bounded_container": True, "local_progress": None,
    "releases_on_exit": True, "persistent_stage_scope": "section",
    "top_level_siblings_depend": False, "global_side_effects": [],
}


def _inp(**kw) -> str:
    base = {"phase": "sectional", "pipeline_state": "SECTIONAL_OPEN", "chassis_stage": None,
            "register": None, "carrier": SECTION_CARRIER, "perf_budget": "medium",
            "occupied_drivers": [], "candidate_ids": []}
    base.update(kw)
    return json.dumps(base, ensure_ascii=False)


def run_resolver_cases(run, expect, fix_dir: str) -> None:
    # matrix 1: chassis effect during CHASSIS_OPEN (batch1 integrated direction) -> eligible
    code, out = run(RESOLVE, "--input", "-", stdin=_inp(
        phase="chassis", pipeline_state="CHASSIS_OPEN", chassis_stage="batch1-directions",
        carrier=PAGE_CARRIER, candidate_ids=["threed-pool:C-08"]))
    expect("resolver: chassis effect eligible while CHASSIS_OPEN", code, out, 0,
           ['"id": "threed-pool:C-08"', '"effective_footprint": "chassis"', '"excluded": []'])

    # matrix 2: same effect, page-scoped proposal during SECTIONAL_OPEN -> INELIGIBLE_CHASSIS_LOCKED
    code, out = run(RESOLVE, "--input", "-", stdin=_inp(
        carrier=PAGE_CARRIER, candidate_ids=["threed-pool:C-08"]))
    expect("resolver: chassis-effective excluded after lock", code, out, 0,
           ["INELIGIBLE_CHASSIS_LOCKED"], forbid=['"eligible": [\n    {'])

    # matrix 3: 500svh/multi-chapter mechanism inside ONE bounded owner -> sectional eligible
    code, out = run(RESOLVE, "--input", "-", stdin=_inp(
        register="ai-product", candidate_ids=["threed-pool:C-08"]))
    expect("resolver: bounded long-scroll owner stays sectional (+ register soft-warn)",
           code, out, 0,
           ['"effective_footprint": "sectional"', "register-affinity"])

    # matrix 4: atomic-native proposal that pins -> computed sectional -> excluded from Atomic Pass
    code, out = run(RESOLVE, "--input", "-", stdin=_inp(
        phase="atomic", pipeline_state="ATOMIC_OPEN", carrier=COMPONENT_CARRIER,
        candidate_ids=["motion-pool:#19"],
        proposed_mutations={"motion-pool:#19": ["local-pin", "opacity-filter"]}))
    expect("resolver: local-pin proposal is not atomic-safe", code, out, 0,
           ["NOT_ATOMIC_SAFE"])

    # matrix 5: a non-selectable entry is excluded in EVERY phase. Specimen was
    # C-17 (unavailable-source) until it graduated via observe-rewrite M-37 and
    # the user ruled it selectable (A-6, 2026-07-11); the stable specimen is now
    # an anchor-only row, which can never graduate by definition.
    for phase, state, stage in (("chassis", "CHASSIS_OPEN", "batch1-directions"),
                                ("sectional", "SECTIONAL_OPEN", None),
                                ("atomic", "ATOMIC_OPEN", None)):
        code, out = run(RESOLVE, "--input", "-", stdin=_inp(
            phase=phase, pipeline_state=state, chassis_stage=stage,
            carrier=SECTION_CARRIER if phase != "atomic" else COMPONENT_CARRIER,
            candidate_ids=["motion-pool:anchor-studio-k95"]))
        expect(f"resolver: non-selectable anchor excluded in {phase} phase", code, out, 0,
               ["NOT_SELECTABLE", "anchor-only"])

    # matrix 6: perf-heavy above budget, fallback NOT accepted -> excluded
    code, out = run(RESOLVE, "--input", "-", stdin=_inp(
        candidate_ids=["threed-pool:C-03"], accept_fallbacks=False))
    expect("resolver: heavy over budget without accepted fallback excluded", code, out, 0,
           ["PERF_OVER_BUDGET"])
    # ... and with fallback accepted -> eligible carrying the fallback condition
    code, out = run(RESOLVE, "--input", "-", stdin=_inp(
        candidate_ids=["threed-pool:C-03"], accept_fallbacks=True))
    expect("resolver: heavy over budget WITH accepted fallback -> conditional eligible",
           code, out, 0, ["fallback-required:instance-count-reduction"])

    # matrix 7: driver conflict with occupied global scroll
    code, out = run(RESOLVE, "--input", "-", stdin=_inp(
        occupied_drivers=["scroll"], candidate_ids=["threed-pool:C-08"]))
    expect("resolver: scroll driver conflict excluded", code, out, 0, ["DRIVER_CONFLICT"])

    # matrix 13: same mechanism deployed page-scoped across top-level siblings -> chassis -> excluded after lock
    carrier = dict(SECTION_CARRIER, top_level_siblings_depend=True)
    code, out = run(RESOLVE, "--input", "-", stdin=_inp(
        carrier=carrier, candidate_ids=["motion-pool:#17"]))
    expect("resolver: cross-sibling persistent deployment computed chassis -> excluded",
           code, out, 0, ["INELIGIBLE_CHASSIS_LOCKED", "top-level sibling"])

    # decision 1 machine form: Batch-2 tuning may not introduce a chassis-footprint mechanism
    code, out = run(RESOLVE, "--input", "-", stdin=_inp(
        phase="chassis", pipeline_state="CHASSIS_OPEN", chassis_stage="batch2-tuning",
        carrier=PAGE_CARRIER, candidate_ids=["threed-pool:C-29"]))
    expect("resolver: batch2-tuning blocks new chassis mechanism", code, out, 0,
           ["CHASSIS_MECHANISM_IN_TUNING"])
    code, out = run(RESOLVE, "--input", "-", stdin=_inp(
        phase="chassis", pipeline_state="CHASSIS_OPEN", chassis_stage="batch2-tuning",
        carrier=COMPONENT_CARRIER, candidate_ids=["motion-pool:#6"]))
    expect("resolver: batch2-tuning keeps component-level vocabulary eligible", code, out, 0,
           ['"id": "motion-pool:#6"', '"excluded": []'])

    # rule 7: computed footprint must be within supported_footprints — a cursor
    # overlay (supported: atomic only) proposed as a page-owning chassis
    # mechanism is an unsupported promotion. (Self-LOWERING is impossible by
    # construction: footprint is COMPUTED from the deployment, never taken from
    # the agent's claim — matrix 4 above shows the pin case landing sectional.)
    code, out = run(RESOLVE, "--input", "-", stdin=_inp(
        phase="chassis", pipeline_state="CHASSIS_OPEN", chassis_stage="batch1-directions",
        carrier=PAGE_CARRIER, candidate_ids=["motion-pool:#21"]))
    expect("resolver: unsupported footprint promotion rejected", code, out, 0,
           ["FOOTPRINT_UNSUPPORTED"])

    # contract error: unknown candidate id
    code, out = run(RESOLVE, "--input", "-", stdin=_inp(candidate_ids=["threed-pool:C-404"]))
    expect("resolver: unknown candidate id is an input error", code, out, 1,
           ["unknown candidate id"])

    # evidence file: --out writes the resolution record with an input digest
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        rec = os.path.join(td, "motion", "resolutions", "sectional-001.json")
        code, out = run(RESOLVE, "--input", "-", "--out", rec, stdin=_inp(
            candidate_ids=["motion-pool:#15"]))
        ok = code == 0 and os.path.exists(rec) and "input_digest" in out
        expect("resolver: --out writes resolution evidence with digest",
               code if ok else 1, out, 0, ['"input_digest": "sha256:', '"effective_footprint": "sectional"'])
