#!/usr/bin/env python3
"""End-to-end pipeline fixture (plan step 13, deterministic half).

Walks ONE run through the whole irreversible sequence using the REAL registry,
the REAL tracked chassis (northway-brutalist) as chassis_ref, and every
runtime script in concert:

  init -> chassis-phase resolution -> lock (static chassis, page_scoped=null)
  -> composition_ready -> SECTIONAL_OPEN -> sectional resolution (#15) ->
  contract + approval -> SECTIONAL_LOCKED -> base-wave preflight -> mini Base
  Wave surface -> BASE_WAVE_READY -> atomic policy + approval -> ATOMIC_OPEN ->
  atomic preflight -> atomic resolution (#8) -> backup/patch/layout-diff ->
  check_atomic_result -> validate_motion_artifacts -> verified -> COMPLETE.

Honest boundary: the surface here is a fixture page and the layout rects are
fixture geometry (the patch is transform/opacity-only, so zero drift is the
truthful expectation) — live console / responsive / reduced-motion / feel
checks belong to the browser half of step 13, not this suite.
"""
from __future__ import annotations

import json
import os
import shutil
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPTS = os.path.join(HERE, "..", "scripts")
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
RESOLVE = os.path.join(SCRIPTS, "resolve_candidates.py")
STATE = os.path.join(SCRIPTS, "pipeline_state.py")
VALIDATE = os.path.join(SCRIPTS, "validate_motion_artifacts.py")
PREFLIGHT = os.path.join(REPO, "core", "anchor-prototype-wave", "scripts", "preflight_wave.py")
ATOMIC_CHECK = os.path.join(REPO, "core", "anchor-prototype-wave", "scripts", "check_atomic_result.py")

SECTION_CARRIER = {"owner_scope": "section", "bounded_container": True, "local_progress": "0..1",
                   "releases_on_exit": True, "persistent_stage_scope": "section",
                   "top_level_siblings_depend": False, "global_side_effects": [],
                   "local_pin_allowed": True, "section_height_change_allowed": True}
COMPONENT_CARRIER = {"owner_scope": "component", "bounded_container": True, "local_progress": None,
                     "releases_on_exit": True, "persistent_stage_scope": "section",
                     "top_level_siblings_depend": False, "global_side_effects": []}

SURFACE_HTML = """<html><head><style>
:root { --token-accent: #b7ff2e; --token-motion-fast: 180ms; }
@media (prefers-reduced-motion: reduce) { .reveal { transition: none } }
@media (max-width: 640px) { .cols { display: block } }
</style></head><body>
<main class="cols">
<section id="approach"><h2>Approach</h2><div class="feature" data-feature="workflow-audit">audit</div></section>
</main>
</body></html>
"""


def run_e2e_case(run, expect, fix_dir: str) -> None:  # noqa: PLR0915 — one linear story on purpose
    with tempfile.TemporaryDirectory() as td:
        rd = os.path.join(td, "testbed", "runs", "e2e-fixture")
        motion = os.path.join(rd, "motion")
        os.makedirs(rd, exist_ok=True)

        def st(*args):
            return run(STATE, *args)

        def j(obj):
            return json.dumps(obj, ensure_ascii=False)

        code, out = st("init", "--out-dir", motion, "--run", "e2e-fixture")
        expect("e2e: init", code, out, 0, ["OK init"])
        sf = os.path.join(motion, "pipeline-state.json")

        # chassis-phase resolution (batch1 integrated directions; evidence kept)
        code, out = run(RESOLVE, "--input", "-", "--out",
                        os.path.join(motion, "resolutions", "chassis-001.json"),
                        stdin=j({"phase": "chassis", "pipeline_state": "CHASSIS_OPEN",
                                 "chassis_stage": "batch1-directions", "register": "ai-product",
                                 "carrier": dict(SECTION_CARRIER, owner_scope="page",
                                                 persistent_stage_scope="page"),
                                 "perf_budget": "medium", "occupied_drivers": [],
                                 "candidate_ids": ["threed-pool:C-08", "threed-pool:C-17"]}))
        expect("e2e: chassis-phase resolution (C-08 eligible, C-17 excluded)", code, out, 0,
               ['"id": "threed-pool:C-08"', "PHASE_NOT_ALLOWED"])
        # (C-17 graduated via observe-rewrite M-37 + A-6 user ruling: selectable,
        #  sectional-only — so in the CHASSIS phase it is excluded by phase, not
        #  by availability. The exclusion evidence in the record is the point.)

        # static-chassis decision + lock ceremony
        st("set", "--state-file", sf, "--field", "chassis_ref",
           "--value", "testbed/chassis/northway-brutalist", "--evidence", "tracked LEAD fixture")
        st("set", "--state-file", sf, "--field", "page_scoped_mechanism", "--value", "null",
           "--evidence", "static visual chassis (fixture mirrors the Averonel decision)")
        st("approve", "--state-file", sf, "--gate", "chassis",
           "--approval-text", "批准锁定 fixture chassis", "--evidence", "fixture lock turn")
        code, out = st("transition", "--state-file", sf, "--to", "CHASSIS_LOCKED",
                       "--evidence", "lock", "--by", "user-approval")
        expect("e2e: chassis locked", code, out, 0, ["-> CHASSIS_LOCKED"])

        # chassis-effective candidates die after lock (matrix 2 inside the real flow)
        code, out = run(RESOLVE, "--input", "-", stdin=j(
            {"phase": "sectional", "pipeline_state": "SECTIONAL_OPEN", "chassis_stage": None,
             "register": "ai-product",
             "carrier": dict(SECTION_CARRIER, owner_scope="page", persistent_stage_scope="page"),
             "perf_budget": "medium", "occupied_drivers": [],
             "candidate_ids": ["threed-pool:C-08"]}))
        expect("e2e: page-scoped proposal after lock excluded", code, out, 0,
               ["INELIGIBLE_CHASSIS_LOCKED"])

        st("set", "--state-file", sf, "--field", "composition_ready", "--value", "true",
           "--evidence", "single-page structure approved at lock")
        st("transition", "--state-file", sf, "--to", "SECTIONAL_OPEN", "--evidence", "opening sectional")

        # sectional resolution + contract + approval + lock
        code, out = run(RESOLVE, "--input", "-", "--out",
                        os.path.join(motion, "resolutions", "sectional-001.json"),
                        stdin=j({"phase": "sectional", "pipeline_state": "SECTIONAL_OPEN",
                                 "chassis_stage": None, "register": "ai-product",
                                 "carrier": SECTION_CARRIER, "perf_budget": "medium",
                                 "occupied_drivers": [],
                                 "candidate_ids": ["motion-pool:#15"]}))
        expect("e2e: sectional resolution (#15 eligible)", code, out, 0,
               ['"effective_footprint": "sectional"'])
        with open(os.path.join(motion, "sectional-score.json"), "w", encoding="utf-8") as fh:
            json.dump({"approach": {"sectional_score": {
                "target": "approach", "mechanism": "motion-pool:#15",
                "carrier": "local-pinned-stage", "driver": "scroll",
                "fallback": "static-chapters",
                "resolution_record": "motion/resolutions/sectional-001.json"}}}, fh, indent=1)
        st("approve", "--state-file", sf, "--gate", "sectional",
           "--approval-text", "approach 用 15", "--evidence", "sectional pick turn")
        st("set", "--state-file", sf, "--field", "sectional_status", "--value", "selected",
           "--evidence", "user picked #15")
        code, out = st("transition", "--state-file", sf, "--to", "SECTIONAL_LOCKED",
                       "--evidence", "sectional locked")
        expect("e2e: sectional locked", code, out, 0, ["-> SECTIONAL_LOCKED"])

        code, out = run(PREFLIGHT, "--motion-dir", motion, "--stage", "base-wave")
        expect("e2e: base-wave preflight green", code, out, 0, ["PREFLIGHT OK"])

        # mini Base Wave output (fixture surface)
        surf = os.path.join(rd, "wave", "approach")
        os.makedirs(surf, exist_ok=True)
        with open(os.path.join(surf, "index.html"), "w", encoding="utf-8") as fh:
            fh.write(SURFACE_HTML)
        code, out = st("transition", "--state-file", sf, "--to", "BASE_WAVE_READY",
                       "--evidence", "wave e2e-fixture: 1 PASS", "--by", "gate")
        expect("e2e: base wave ready", code, out, 0, ["-> BASE_WAVE_READY"])

        # atomic ceremony
        with open(os.path.join(motion, "atomic-policy.json"), "w", encoding="utf-8") as fh:
            json.dump({"atomic_policy": {"enabled": True, "max_targets": 3,
                                         "allowed_properties": ["transform", "opacity", "filter",
                                                                "color", "border", "shadow"],
                                         "allow_overlay_canvas": False, "no_reflow": True,
                                         "performance_budget": "light"}}, fh, indent=1)
        st("approve", "--state-file", sf, "--gate", "atomic_policy",
           "--approval-text", "预算 3 个目标 ok", "--evidence", "policy turn")
        st("set", "--state-file", sf, "--field", "atomic_status", "--value", "policy-approved",
           "--evidence", "atomic-policy.json written")
        st("transition", "--state-file", sf, "--to", "ATOMIC_OPEN", "--evidence", "policy approved")
        code, out = run(PREFLIGHT, "--motion-dir", motion, "--stage", "atomic")
        expect("e2e: atomic preflight green", code, out, 0, ["PREFLIGHT OK"])

        code, out = run(RESOLVE, "--input", "-", "--out",
                        os.path.join(motion, "resolutions", "atomic-001.json"),
                        stdin=j({"phase": "atomic", "pipeline_state": "ATOMIC_OPEN",
                                 "chassis_stage": None, "register": "ai-product",
                                 "carrier": COMPONENT_CARRIER, "perf_budget": "light",
                                 "occupied_drivers": [],
                                 "candidate_ids": ["motion-pool:#8"],
                                 "proposed_mutations": {"motion-pool:#8": ["pseudo-elements",
                                                                           "opacity-filter"]}}))
        expect("e2e: atomic resolution (#8 eligible)", code, out, 0,
               ['"effective_footprint": "atomic"'])

        # patch under the budget: backup, transform/opacity-only touch, rect capture
        audits = os.path.join(rd, "wave", "audits", "atomic")
        os.makedirs(audits, exist_ok=True)
        before_p = os.path.join(audits, "approach.before.html")
        shutil.copyfile(os.path.join(surf, "index.html"), before_p)
        patched = SURFACE_HTML.replace(
            '<div class="feature" data-feature="workflow-audit">audit</div>',
            '<div class="feature reveal" data-feature="workflow-audit" '
            'style="transition: opacity var(--token-motion-fast)">audit</div>')
        with open(os.path.join(surf, "index.html"), "w", encoding="utf-8") as fh:
            fh.write(patched)
        with open(os.path.join(audits, "approach.layout-diff.json"), "w", encoding="utf-8") as fh:
            json.dump({"tolerance_px": 0.5,
                       "rects": {"[data-feature='workflow-audit']":
                                 {"before": [24, 180, 320, 48], "after": [24, 180, 320, 48]}}},
                      fh, indent=1)
        with open(os.path.join(motion, "atomic-result-approach.json"), "w", encoding="utf-8") as fh:
            json.dump({"atomic_result": {"surface": "approach",
                                         "effects": [{"target": "[data-feature='workflow-audit']",
                                                      "mechanism": "motion-pool:#8",
                                                      "resolution_record": "motion/resolutions/atomic-001.json"}],
                                         "layout_diff": "pass", "reduced_motion": "pass"}}, fh, indent=1)
        code, out = run(ATOMIC_CHECK,
                        "--result", os.path.join(motion, "atomic-result-approach.json"),
                        "--policy", os.path.join(motion, "atomic-policy.json"),
                        "--before", before_p, "--after", os.path.join(surf, "index.html"),
                        "--layout-diff", os.path.join(audits, "approach.layout-diff.json"))
        expect("e2e: atomic patch passes the discipline gate", code, out, 0, ["ATOMIC OK"])

        code, out = run(VALIDATE, "--motion-dir", motion)
        expect("e2e: full artifacts validation green", code, out, 0, ["OK motion artifacts valid"])

        st("set", "--state-file", sf, "--field", "atomic_status", "--value", "patched",
           "--evidence", "1 effect applied")
        st("set", "--state-file", sf, "--field", "atomic_status", "--value", "verified",
           "--evidence", "check_atomic_result + validate_motion_artifacts green")
        code, out = st("transition", "--state-file", sf, "--to", "COMPLETE",
                       "--evidence", "all machine checks green; gallery review = human half")
        expect("e2e: COMPLETE", code, out, 0, ["-> COMPLETE"])
        code, out = st("verify", "--state-file", sf, "--require-state", "COMPLETE",
                       "--require-approval", "chassis,sectional,atomic_policy")
        expect("e2e: final verify", code, out, 0, ["OK verify"])
