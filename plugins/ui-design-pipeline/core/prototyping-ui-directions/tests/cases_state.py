#!/usr/bin/env python3
"""Pipeline-state cases for run_tests.py — monotonic transitions, evidence
gates, write-once approvals, the sectional-skip path and verify()."""
from __future__ import annotations

import os
import tempfile

STATE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "scripts", "pipeline_state.py")


def run_state_cases(run, expect, fix_dir: str) -> None:
    with tempfile.TemporaryDirectory() as td:
        sf = os.path.join(td, "pipeline-state.json")

        code, out = run(STATE, "init", "--out-dir", td, "--run", "test-run")
        expect("state: init", code, out, 0, ["OK init", "CHASSIS_OPEN"])

        code, out = run(STATE, "init", "--out-dir", td, "--run", "test-run")
        expect("state: init refuses overwrite (reopen = NEW run)", code, out, 1, ["already exists"])

        code, out = run(STATE, "transition", "--state-file", sf, "--to", "CHASSIS_LOCKED",
                        "--evidence", "trying to lock")
        expect("state: lock refused without user approval", code, out, 1,
               ["REFUSED", "user_approvals.chassis"])

        code, out = run(STATE, "approve", "--state-file", sf, "--gate", "chassis",
                        "--approval-text", "批准,锁这个 LEAD", "--evidence", "gallery pick turn")
        expect("state: chassis approval recorded", code, out, 0, ["OK approve chassis"])

        code, out = run(STATE, "transition", "--state-file", sf, "--to", "CHASSIS_LOCKED",
                        "--evidence", "lock attempt 2")
        expect("state: lock still refused without chassis_ref", code, out, 1, ["chassis_ref"])

        run(STATE, "set", "--state-file", sf, "--field", "chassis_ref",
            "--value", "testbed/chassis/northway-brutalist", "--evidence", "LEAD path")
        code, out = run(STATE, "transition", "--state-file", sf, "--to", "CHASSIS_LOCKED",
                        "--evidence", "lock attempt 3")
        expect("state: lock still refused without page_scoped_mechanism declaration", code, out, 1,
               ["page_scoped_mechanism"])

        code, out = run(STATE, "set", "--state-file", sf, "--field", "page_scoped_mechanism",
                        "--value", "null", "--evidence", "static visual chassis decision")
        expect("state: page_scoped_mechanism=null is a valid explicit stance", code, out, 0, ["OK set"])

        code, out = run(STATE, "transition", "--state-file", sf, "--to", "CHASSIS_LOCKED",
                        "--evidence", "user approved lock", "--by", "user-approval")
        expect("state: chassis locks with approval + ref + stance", code, out, 0,
               ["OK transition CHASSIS_OPEN -> CHASSIS_LOCKED"])

        code, out = run(STATE, "transition", "--state-file", sf, "--to", "SECTIONAL_OPEN",
                        "--evidence", "opening sectional")
        expect("state: sectional refused before composition_ready", code, out, 1,
               ["composition_ready"])

        run(STATE, "set", "--state-file", sf, "--field", "composition_ready", "--value", "true",
            "--evidence", "IA Round-2 Stage-F gate passed")
        code, out = run(STATE, "transition", "--state-file", sf, "--to", "SECTIONAL_OPEN",
                        "--evidence", "composition ready")
        expect("state: sectional opens after composition_ready", code, out, 0,
               ["OK transition CHASSIS_LOCKED -> SECTIONAL_OPEN"])

        code, out = run(STATE, "transition", "--state-file", sf, "--to", "BASE_WAVE_READY",
                        "--evidence", "skip attempt")
        expect("state: skipping states refused", code, out, 1, ["skips states"])

        code, out = run(STATE, "transition", "--state-file", sf, "--to", "CHASSIS_OPEN",
                        "--evidence", "go back")
        expect("state: backward transition refused", code, out, 1, ["backward"])

        run(STATE, "set", "--state-file", sf, "--field", "sectional_status", "--value", "selected",
            "--evidence", "user picked #15 on approach")
        code, out = run(STATE, "transition", "--state-file", sf, "--to", "SECTIONAL_LOCKED",
                        "--evidence", "locking sectional")
        expect("state: sectional lock refused without sectional approval", code, out, 1,
               ["user_approvals.sectional"])

        run(STATE, "approve", "--state-file", sf, "--gate", "sectional",
            "--approval-text", "就用 15 那个", "--evidence", "sectional pick turn")
        code, out = run(STATE, "transition", "--state-file", sf, "--to", "SECTIONAL_LOCKED",
                        "--evidence", "sectional approved")
        expect("state: sectional locks", code, out, 0, ["-> SECTIONAL_LOCKED"])

        code, out = run(STATE, "transition", "--state-file", sf, "--to", "BASE_WAVE_READY",
                        "--evidence", "contracts written")
        expect("state: base wave ready", code, out, 0, ["-> BASE_WAVE_READY"])

        code, out = run(STATE, "transition", "--state-file", sf, "--to", "ATOMIC_OPEN",
                        "--evidence", "opening atomic")
        expect("state: atomic refused without policy approval", code, out, 1,
               ["atomic_policy"])

        run(STATE, "approve", "--state-file", sf, "--gate", "atomic_policy",
            "--approval-text", "预算3个目标,transform/opacity 就行", "--evidence", "policy turn")
        run(STATE, "set", "--state-file", sf, "--field", "atomic_status", "--value", "policy-approved",
            "--evidence", "atomic-policy.json written")
        code, out = run(STATE, "transition", "--state-file", sf, "--to", "ATOMIC_OPEN",
                        "--evidence", "policy approved")
        expect("state: atomic opens with approved policy", code, out, 0, ["-> ATOMIC_OPEN"])

        code, out = run(STATE, "transition", "--state-file", sf, "--to", "COMPLETE",
                        "--evidence", "closing")
        expect("state: complete refused before atomic verified", code, out, 1,
               ["atomic_status=verified"])

        run(STATE, "set", "--state-file", sf, "--field", "atomic_status", "--value", "patched",
            "--evidence", "patches applied")
        run(STATE, "set", "--state-file", sf, "--field", "atomic_status", "--value", "verified",
            "--evidence", "layout diff + reduced-motion green")
        code, out = run(STATE, "transition", "--state-file", sf, "--to", "COMPLETE",
                        "--evidence", "all checks green")
        expect("state: complete after verified", code, out, 0, ["-> COMPLETE"])

        code, out = run(STATE, "verify", "--state-file", sf, "--require-state", "COMPLETE",
                        "--require-composition-ready", "--require-approval", "chassis,sectional,atomic_policy")
        expect("state: verify green on the finished run", code, out, 0, ["OK verify"])

    # matrix 9 (state half): sectional skipped + atomic never opened -> valid path to COMPLETE
    with tempfile.TemporaryDirectory() as td:
        sf = os.path.join(td, "pipeline-state.json")
        run(STATE, "init", "--out-dir", td, "--run", "skip-run")
        run(STATE, "approve", "--state-file", sf, "--gate", "chassis",
            "--approval-text", "ok lock it", "--evidence", "t")
        run(STATE, "set", "--state-file", sf, "--field", "chassis_ref",
            "--value", "testbed/chassis/grove-linen", "--evidence", "t")
        run(STATE, "set", "--state-file", sf, "--field", "page_scoped_mechanism",
            "--value", "null", "--evidence", "t")
        run(STATE, "transition", "--state-file", sf, "--to", "CHASSIS_LOCKED", "--evidence", "t")
        run(STATE, "set", "--state-file", sf, "--field", "composition_ready", "--value", "true",
            "--evidence", "single-page structure approved at lock")
        run(STATE, "transition", "--state-file", sf, "--to", "SECTIONAL_OPEN", "--evidence", "t")
        run(STATE, "set", "--state-file", sf, "--field", "sectional_status", "--value", "skipped",
            "--evidence", "user skipped sectional")
        code, out = run(STATE, "transition", "--state-file", sf, "--to", "SECTIONAL_LOCKED",
                        "--evidence", "skip is valid")
        expect("state: sectional_status=skipped locks without sectional approval", code, out, 0,
               ["-> SECTIONAL_LOCKED"])
        run(STATE, "transition", "--state-file", sf, "--to", "BASE_WAVE_READY", "--evidence", "t")
        code, out = run(STATE, "verify", "--state-file", sf, "--min-state", "SECTIONAL_LOCKED",
                        "--require-sectional", "selected,skipped")
        expect("state: verify accepts the skip path (matrix 9)", code, out, 0, ["OK verify"])
        code, out = run(STATE, "transition", "--state-file", sf, "--to", "COMPLETE",
                        "--evidence", "atomic disabled for this run")
        expect("state: BASE_WAVE_READY -> COMPLETE shortcut when atomic never opens", code, out, 0,
               ["-> COMPLETE"])

    # verify blocks on a fresh run (matrix 10 state half: atomic gate unreachable early)
    with tempfile.TemporaryDirectory() as td:
        sf = os.path.join(td, "pipeline-state.json")
        run(STATE, "init", "--out-dir", td, "--run", "fresh")
        code, out = run(STATE, "verify", "--state-file", sf, "--require-state", "BASE_WAVE_READY")
        expect("state: verify blocks a fresh run pretending readiness", code, out, 1, ["BLOCK: state"])
        code, out = run(STATE, "set", "--state-file", sf, "--field", "sectional_status",
                        "--value", "selected", "--evidence", "premature")
        expect("state: sectional_status cannot jump past pending", code, out, 1, ["REFUSED"])
