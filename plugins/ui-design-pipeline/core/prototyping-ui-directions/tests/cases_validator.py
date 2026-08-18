#!/usr/bin/env python3
"""validate_motion_artifacts.py cases — defense-in-depth (plan step 11):
state monotonicity/tamper, approvals-vs-state, sectional contract vs registry,
resolution-record integrity, family-dup WARN, atomic policy/result discipline."""
from __future__ import annotations

import json
import os
import tempfile

VALIDATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts",
                        "validate_motion_artifacts.py")


def _write(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=1)


def _state(state="SECTIONAL_LOCKED", **over):
    doc = {"state": state, "run": "r1", "chassis_ref": "x", "chassis_locked": True,
           "composition_ready": True, "page_scoped_mechanism": None,
           "sectional_status": "skipped", "atomic_status": "not-open",
           "user_approvals": {"chassis": "批准", "sectional": None, "atomic_policy": None},
           "state_log": [{"at": "t", "event": "init", "to": "CHASSIS_OPEN", "by": "system", "evidence": "e"}]}
    doc.update(over)
    return doc


def _resolution(motion, name, mech, phase="sectional", state="SECTIONAL_OPEN"):
    _write(os.path.join(motion, "resolutions", name),
           {"resolver_version": 1, "input_digest": "sha256:abc", "phase": phase,
            "pipeline_state": state,
            "eligible": [{"id": mech, "effective_footprint": phase if phase != "sectional" else "sectional",
                          "fit_reason": "t", "warnings": [], "conditions": []}],
            "excluded": []})


def run_validator_cases(run, expect, fix_dir: str) -> None:
    with tempfile.TemporaryDirectory() as td:
        motion = os.path.join(td, "motion")
        _write(os.path.join(motion, "pipeline-state.json"), _state())
        code, out = run(VALIDATE, "--motion-dir", motion)
        expect("validator: minimal state green", code, out, 0, ["OK motion artifacts valid"])

        bad = _state()
        bad["state_log"] += [
            {"at": "t", "event": "transition", "from": "CHASSIS_OPEN", "to": "CHASSIS_LOCKED", "by": "user-approval", "evidence": "e"},
            {"at": "t", "event": "transition", "from": "CHASSIS_LOCKED", "to": "SECTIONAL_OPEN", "by": "system", "evidence": "e"},
            {"at": "t", "event": "transition", "from": "SECTIONAL_OPEN", "to": "CHASSIS_LOCKED", "by": "system", "evidence": "e"},
        ]
        _write(os.path.join(motion, "pipeline-state.json"), bad)
        code, out = run(VALIDATE, "--motion-dir", motion)
        expect("validator: backward state_log = monotonicity violation", code, out, 1,
               ["monotonicity violated"])

        tampered = _state("SECTIONAL_LOCKED")
        tampered["state_log"] += [
            {"at": "t", "event": "transition", "from": "CHASSIS_OPEN", "to": "CHASSIS_LOCKED", "by": "user-approval", "evidence": "e"},
        ]
        _write(os.path.join(motion, "pipeline-state.json"), tampered)
        code, out = run(VALIDATE, "--motion-dir", motion)
        expect("validator: state disagreeing with its own log = tamper", code, out, 1,
               ["disagrees with last logged transition"])

        _write(os.path.join(motion, "pipeline-state.json"),
               _state("ATOMIC_OPEN", atomic_status="policy-approved"))
        code, out = run(VALIDATE, "--motion-dir", motion)
        expect("validator: ATOMIC_OPEN without atomic_policy approval", code, out, 1,
               ["user_approvals.atomic_policy is empty"])

    with tempfile.TemporaryDirectory() as td:
        motion = os.path.join(td, "motion")
        _write(os.path.join(motion, "pipeline-state.json"),
               _state(sectional_status="selected",
                      user_approvals={"chassis": "批准", "sectional": "用15", "atomic_policy": None}))
        _resolution(motion, "s1.json", "motion-pool:#15")
        _write(os.path.join(motion, "sectional-score.json"),
               {"approach": {"sectional_score": {"target": "approach", "mechanism": "motion-pool:#15",
                                                 "carrier": "local-pinned-stage", "driver": "scroll",
                                                 "fallback": "static-sequence",
                                                 "resolution_record": "motion/resolutions/s1.json"}}})
        code, out = run(VALIDATE, "--motion-dir", motion)
        expect("validator: valid sectional contract green", code, out, 0, ["OK motion artifacts valid"])

        _write(os.path.join(motion, "sectional-score.json"),
               {"approach": {"sectional_score": {"mechanism": "motion-pool:#99",
                                                 "fallback": "x", "resolution_record": "motion/resolutions/s1.json"}}})
        code, out = run(VALIDATE, "--motion-dir", motion)
        expect("validator: unknown mechanism id caught", code, out, 1, ["not in execution registry"])

        _resolution(motion, "s2.json", "motion-pool:#21")
        _write(os.path.join(motion, "sectional-score.json"),
               {"approach": {"sectional_score": {"mechanism": "motion-pool:#21",
                                                 "fallback": "x", "resolution_record": "motion/resolutions/s2.json"}}})
        code, out = run(VALIDATE, "--motion-dir", motion)
        expect("validator: phase-membership enforced (cursor is not sectional)", code, out, 1,
               ["does not allow the sectional phase"])

        _resolution(motion, "s3.json", "threed-pool:C-04")
        _resolution(motion, "s4.json", "threed-pool:C-33")
        _write(os.path.join(motion, "sectional-score.json"),
               {"a": {"sectional_score": {"mechanism": "threed-pool:C-04", "fallback": "x",
                                          "resolution_record": "motion/resolutions/s3.json"}},
                "b": {"sectional_score": {"mechanism": "threed-pool:C-33", "fallback": "x",
                                          "resolution_record": "motion/resolutions/s4.json"}}})
        code, out = run(VALIDATE, "--motion-dir", motion)
        expect("validator: duplicate mechanism_family across surfaces WARNs (not blocks)",
               code, out, 0, ["WARN: duplicate mechanism_family", "velocity-sin-deform-rgb-split"])

        # component tier (contracts §6, user-relax 2026-07-18): structural
        # pointer|click|load entries beside (or without) the primary slot
        _resolution(motion, "c1.json", "motion-pool:#26")
        _write(os.path.join(motion, "sectional-score.json"),
               {"approach": {"sectional_score": None,
                             "component_scores": [
                                 {"target": "terms", "mechanism": "motion-pool:#26",
                                  "carrier": "bento-card-wall", "driver": "click",
                                  "fallback": "static-cards",
                                  "resolution_record": "motion/resolutions/c1.json"}]}})
        code, out = run(VALIDATE, "--motion-dir", motion)
        expect("validator: component tier green (null primary + click component)",
               code, out, 0, ["OK motion artifacts valid"])

        _write(os.path.join(motion, "sectional-score.json"),
               {"approach": {"sectional_score": None,
                             "component_scores": [
                                 {"target": "terms", "mechanism": "motion-pool:#26",
                                  "carrier": "bento-card-wall", "driver": "scroll",
                                  "fallback": "static-cards",
                                  "resolution_record": "motion/resolutions/c1.json"}]}})
        code, out = run(VALIDATE, "--motion-dir", motion)
        expect("validator: component driver=scroll rejected (exclusive to primary)",
               code, out, 1, ["component driver must be one of"])

        _write(os.path.join(motion, "sectional-score.json"),
               {"approach": {"sectional_score": None,
                             "component_scores": [
                                 {"target": "terms", "mechanism": "motion-pool:#26",
                                  "carrier": "bento-card-wall", "driver": "load",
                                  "fallback": "static-cards",
                                  "resolution_record": "motion/resolutions/c1.json"}]}})
        code, out = run(VALIDATE, "--motion-dir", motion)
        expect("validator: component driver outside registry driver list rejected",
               code, out, 1, ["registry driver list"])

        _write(os.path.join(motion, "sectional-score.json"),
               {"approach": {"sectional_score": None,
                             "component_scores": [
                                 {"target": "terms", "mechanism": "motion-pool:#26",
                                  "carrier": "bento-card-wall", "driver": "click",
                                  "fallback": "static-cards"}]}})
        code, out = run(VALIDATE, "--motion-dir", motion)
        expect("validator: component missing resolution_record caught",
               code, out, 1, ["resolution_record is required"])

    with tempfile.TemporaryDirectory() as td:
        motion = os.path.join(td, "motion")
        _write(os.path.join(motion, "pipeline-state.json"),
               _state("ATOMIC_OPEN", atomic_status="patched",
                      user_approvals={"chassis": "批准", "sectional": None, "atomic_policy": "预算ok"}))
        _write(os.path.join(motion, "atomic-policy.json"),
               {"atomic_policy": {"enabled": True, "max_targets": 1,
                                  "allowed_properties": ["transform", "background"],
                                  "allow_overlay_canvas": False, "no_reflow": True,
                                  "performance_budget": "light"}})
        code, out = run(VALIDATE, "--motion-dir", motion)
        expect("validator: policy property outside atomic contract", code, out, 1,
               ["outside the atomic contract"])

        _write(os.path.join(motion, "atomic-policy.json"),
               {"atomic_policy": {"enabled": True, "max_targets": 1,
                                  "allowed_properties": ["transform", "opacity"],
                                  "allow_overlay_canvas": False, "no_reflow": True,
                                  "performance_budget": "light"}})
        _resolution(motion, "a1.json", "motion-pool:#8", phase="atomic", state="ATOMIC_OPEN")
        _resolution(motion, "a2.json", "motion-pool:#9", phase="atomic", state="ATOMIC_OPEN")
        _write(os.path.join(motion, "atomic-result-s.json"),
               {"atomic_result": {"surface": "s",
                                  "effects": [
                                      {"target": ".x", "mechanism": "motion-pool:#8",
                                       "resolution_record": "motion/resolutions/a1.json"},
                                      {"target": ".y", "mechanism": "motion-pool:#9",
                                       "resolution_record": "motion/resolutions/a2.json"}],
                                  "layout_diff": "pass", "reduced_motion": "pass"}})
        code, out = run(VALIDATE, "--motion-dir", motion)
        expect("validator: atomic effects exceed policy budget", code, out, 1,
               ["exceed atomic_policy.max_targets"])

        _write(os.path.join(motion, "atomic-result-s.json"),
               {"atomic_result": {"surface": "s",
                                  "effects": [{"target": ".x", "mechanism": "motion-pool:#15",
                                               "resolution_record": "motion/resolutions/a1.json"}],
                                  "layout_diff": "pass", "reduced_motion": "pass"}})
        code, out = run(VALIDATE, "--motion-dir", motion)
        expect("validator: non-atomic mechanism in atomic result caught", code, out, 1,
               ["does not allow the atomic phase"])

        _write(os.path.join(motion, "atomic-result-s.json"),
               {"atomic_result": {"surface": "s",
                                  "effects": [{"target": ".x", "mechanism": "motion-pool:#8",
                                               "resolution_record": "motion/resolutions/a1.json"}],
                                  "layout_diff": "fail", "reduced_motion": "pass"}})
        code, out = run(VALIDATE, "--motion-dir", motion)
        expect("validator: layout_diff claim must be pass before COMPLETE", code, out, 1,
               ["layout_diff is 'fail'"])
