#!/usr/bin/env python3
"""Regression suite for the PUD motion-architecture runtime
(check_registry_sync.py + resolve_candidates.py + pipeline_state.py).

Mirrors core/anchor-prototype-wave/tests/run_tests.py in spirit: every case
pins an exit code + must-mention substrings so a future edit can't silently
loosen a gate. Pure stdlib; run from anywhere:

    python core/prototyping-ui-directions/tests/run_tests.py

Exit 0 = all green / 1 = mismatches (each printed).
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
FIX = os.path.join(HERE, "fixtures")
SCRIPTS = os.path.join(HERE, "..", "scripts")
SYNC = os.path.join(SCRIPTS, "check_registry_sync.py")
RESOLVE = os.path.join(SCRIPTS, "resolve_candidates.py")
STATE = os.path.join(SCRIPTS, "pipeline_state.py")

MINI_T = os.path.join(FIX, "pools", "mini-threed.md")
MINI_T_NOBADGE = os.path.join(FIX, "pools", "mini-threed-nobadge.md")
MINI_M = os.path.join(FIX, "pools", "mini-motion.md")

failures: list[str] = []


def run(script: str, *args: str, stdin: str | None = None):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")  # Windows pipes default GBK
    r = subprocess.run([sys.executable, script, *args],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=env, input=stdin)
    return r.returncode, r.stdout + r.stderr


def fail(name: str, detail: str, out: str = "") -> None:
    failures.append(f"{name}: {detail}")
    print(f"FAIL {name}: {detail}")
    if out:
        print("     ---8<--- captured output ---8<---")
        for line in out.splitlines():
            print("     " + line)


def expect(name: str, code: int, out: str, exp_code: int, needles, forbid=()) -> None:
    probs = []
    if code != exp_code:
        probs.append(f"exit {code} != {exp_code}")
    for n in needles:
        if n not in out:
            probs.append(f"missing {n!r}")
    for n in forbid:
        if n in out:
            probs.append(f"unexpected {n!r} (should be absent)")
    if probs:
        fail(name, "; ".join(probs), out)
    else:
        print(f"ok   {name}")


def _material_corpus_in_scope() -> bool:
    """True when the LAB-ONLY testbed/material corpus is reachable from here.

    Mirrors check_registry_sync.py's own walk-up. The corpus ships with the
    lab checkout, never with the installed plugin.
    """
    here = os.path.dirname(os.path.abspath(__file__))
    while True:
        if os.path.isdir(os.path.join(here, "testbed", "material")):
            return True
        parent = os.path.dirname(here)
        if parent == here:
            return False
        here = parent


def sync_case(name: str, registry: str, exp_code: int, needles,
              threed: str = MINI_T, motion: str = MINI_M) -> None:
    code, out = run(SYNC, "--registry", os.path.join(FIX, "registry", registry),
                    "--threed-pool", threed, "--motion-pool", motion)
    expect(name, code, out, exp_code, needles)


# --- check_registry_sync -----------------------------------------------------

def test_sync_real_green():
    code, out = run(SYNC)
    expect("sync: real registry + real pools green", code, out, 0,
           ["OK registry sync", "76 records == 76 covered pool rows"])


def test_sync_fixture_cases():
    sync_case("sync: fixture ok green", "ok.json", 0, ["OK registry sync", "3 records == 3"])
    sync_case("sync: duplicate id", "dup-id.json", 1, ["duplicate id: threed-pool:C-01"])
    sync_case("sync: orphan registry record", "orphan-record.json", 1,
              ["registry record threed-pool:C-99 resolves to no pool row"])
    sync_case("sync: pool row without record", "missing-record.json", 1,
              ["pool row threed-pool:C-02 has no registry record"])
    sync_case("sync: invalid footprint", "invalid-footprint.json", 1,
              ["supported_footprints has invalid value(s)"])
    sync_case("sync: invalid phase", "invalid-phase.json", 1,
              ["allowed_phases has invalid value(s)"])
    sync_case("sync: missing fallback", "missing-fallback.json", 1,
              ["fallback is required"])
    sync_case("sync: fabricated fields on unavailable", "fabricated-unavailable.json", 1,
              ["fabricated classification fields"])
    # LAB-ONLY case: the material-path check only runs where the material
    # corpus is in scope (lab checkout). In a plugin install the corpus is not
    # shipped, the check is skipped by design, and asserting a failure here
    # would assert something the installed shape cannot produce. Skip loudly —
    # never let it pass silently, never let it red the suite.
    if _material_corpus_in_scope():
        sync_case("sync: material path missing", "bad-material.json", 1,
                  ["material path not found: testbed/material/zzz-does-not-exist"])
    else:
        print("skip sync: material path missing "
              "(no testbed/material in scope — lab-only check)")
    sync_case("sync: badge missing on covered row", "ok.json", 1,
              ["row C-02", "missing execution badge"], threed=MINI_T_NOBADGE)


# --- resolver / pipeline-state suites are appended by later plan steps -------

def main() -> int:
    test_sync_real_green()
    test_sync_fixture_cases()

    if os.path.exists(RESOLVE):
        from cases_resolver import run_resolver_cases  # noqa: PLC0415
        run_resolver_cases(run, expect, FIX)
        from cases_resolver_content_role import run_resolver_content_role_cases  # noqa: PLC0415
        run_resolver_content_role_cases(run, expect, FIX)
    if os.path.exists(STATE):
        from cases_state import run_state_cases  # noqa: PLC0415
        run_state_cases(run, expect, FIX)
    if os.path.exists(os.path.join(SCRIPTS, "validate_motion_artifacts.py")):
        from cases_validator import run_validator_cases  # noqa: PLC0415
        run_validator_cases(run, expect, FIX)
    if os.path.exists(os.path.join(SCRIPTS, "pipeline_state.py")):
        from cases_e2e import run_e2e_case  # noqa: PLC0415
        run_e2e_case(run, expect, FIX)

    if failures:
        print(f"--- {len(failures)} failure(s)")
        return 1
    print("--- all green")
    return 0


if __name__ == "__main__":
    sys.path.insert(0, HERE)
    sys.exit(main())
