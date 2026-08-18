#!/usr/bin/env python3
"""validate_motion_artifacts.py — defense-in-depth validator for a run's
motion/ artifacts (execution-contracts.md §4/§6; plan step 11).

Validates, deterministically:
  - pipeline-state.json: field shapes, enum membership, state_log present and
    MONOTONIC (transition entries never move backward), approvals verbatim
    non-empty where the state implies them.
  - sectional-score.json (when present): per-surface shape; mechanism ids exist
    in the registry, are selectable, allow the sectional phase, carry a
    non-empty fallback; resolution_record files exist, phase-match, were
    produced in SECTIONAL_OPEN, and LIST the chosen mechanism as eligible
    (a hand-edited mechanism that its own resolution never approved = tamper).
  - at most ONE primary orchestration per surface (contract shape) + WARN on
    duplicate mechanism_family across surfaces (user must knowingly accept).
  - component_scores entries (contracts §6 component tier, user-relax 2026-07-18):
    same rigor as the primary PLUS declared driver must be pointer|click|load
    (scroll/timeline stay exclusive to the primary slot) and must appear in the
    mechanism's registry driver list.
  - atomic-policy.json / atomic-result-*.json (when present): shape, budget
    conformance, atomic-phase membership of mechanisms, resolution records,
    layout_diff/reduced_motion claims are "pass".

Exit 0 = valid (warnings allowed); exit 1 = problems (printed as PROBLEM: ...).

Usage:
    python validate_motion_artifacts.py --motion-dir <out>/motion [--registry P]

No third-party dependencies. Python 3.10+.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import registry_lib  # noqa: E402

ORDER = ("CHASSIS_OPEN", "CHASSIS_LOCKED", "SECTIONAL_OPEN", "SECTIONAL_LOCKED",
         "BASE_WAVE_READY", "ATOMIC_OPEN", "COMPLETE")


def load_json(path: Path, problems: list[str], what: str):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        problems.append(f"{what} unreadable: {exc}")
        return None


def check_state(doc: dict, problems: list[str]) -> None:
    if doc.get("state") not in ORDER:
        problems.append(f"pipeline-state.state invalid: {doc.get('state')!r}")
        return
    log = doc.get("state_log") or []
    if not log:
        problems.append("pipeline-state.state_log is empty (transitions must be append-audited)")
    last = 0
    for i, entry in enumerate(log):
        if entry.get("event") != "transition":
            continue
        to = entry.get("to")
        if to not in ORDER:
            problems.append(f"state_log[{i}] transition to unknown state {to!r}")
            continue
        idx = ORDER.index(to)
        if idx <= last and not (last == 0 and idx == 0):
            problems.append(f"state_log[{i}] moves backward/level ({ORDER[last]} -> {to}) — monotonicity violated")
        last = idx
    if ORDER.index(doc["state"]) != last and any(e.get("event") == "transition" for e in log):
        problems.append(f"pipeline-state.state {doc['state']} disagrees with last logged transition {ORDER[last]}")
    idx = ORDER.index(doc["state"])
    appr = doc.get("user_approvals") or {}
    if idx >= ORDER.index("CHASSIS_LOCKED") and not appr.get("chassis"):
        problems.append("state >= CHASSIS_LOCKED but user_approvals.chassis is empty")
    if doc.get("sectional_status") == "selected" and idx >= ORDER.index("SECTIONAL_LOCKED") and not appr.get("sectional"):
        problems.append("sectional selected + locked but user_approvals.sectional is empty")
    if idx >= ORDER.index("ATOMIC_OPEN") and not appr.get("atomic_policy"):
        problems.append("state >= ATOMIC_OPEN but user_approvals.atomic_policy is empty")
    if doc.get("page_scoped_mechanism") == "__unset__" and idx >= ORDER.index("CHASSIS_LOCKED"):
        problems.append("chassis locked without an explicit page_scoped_mechanism declaration")


def resolve_record_path(motion: Path, rr: str) -> Path:
    """resolution_record values are run-root-relative (e.g. motion/resolutions/x.json);
    tolerate a bare filename by probing motion/resolutions/."""
    p = motion.parent / rr
    return p if p.exists() else motion / "resolutions" / Path(rr).name


def check_resolution(path: Path, expect_phase: str, expect_state: str,
                     mechanism: str, problems: list[str], what: str) -> None:
    if not path.exists():
        problems.append(f"{what}: resolution_record missing: {path.name}")
        return
    rec = load_json(path, problems, f"{what} resolution record")
    if rec is None:
        return
    if rec.get("phase") != expect_phase:
        problems.append(f"{what}: resolution phase {rec.get('phase')!r} != {expect_phase}")
    if rec.get("pipeline_state") != expect_state:
        problems.append(f"{what}: resolution produced in state {rec.get('pipeline_state')!r}, expected {expect_state} (stale record)")
    if not str(rec.get("input_digest", "")).startswith("sha256:"):
        problems.append(f"{what}: resolution record has no sha256 input_digest")
    eligible = {e.get("id") for e in rec.get("eligible") or []}
    if mechanism not in eligible:
        problems.append(f"{what}: mechanism {mechanism} is NOT in its resolution record's eligible list (tampered or self-served)")


COMPONENT_DRIVERS = ("pointer", "click", "load")


def check_score_entry(sc: dict, what: str, surface: str, records: dict,
                      families: dict, problems: list[str], warnings: list[str],
                      motion: Path, component: bool = False) -> None:
    """Shared checks for a primary sectional_score or a component_scores entry.

    Component tier (contracts §6, user-relax 2026-07-18) additionally requires a
    declared driver in COMPONENT_DRIVERS that the registry record supports —
    scroll/timeline orchestration stays exclusive to the primary slot."""
    mech = sc.get("mechanism")
    rec = records.get(mech)
    if rec is None:
        problems.append(f"{what}: mechanism {mech!r} not in execution registry")
    else:
        if not rec.get("selectable"):
            problems.append(f"{what}: mechanism {mech} is not selectable ({rec.get('availability')})")
        if "sectional" not in (rec.get("allowed_phases") or []):
            problems.append(f"{what}: mechanism {mech} does not allow the sectional phase")
        fam = rec.get("mechanism_family")
        if fam in families and families[fam] != surface:
            warnings.append(f"duplicate mechanism_family '{fam}' across surfaces "
                            f"({families[fam]} + {surface}) — user must knowingly accept the repeat")
        families[fam] = surface
        if component:
            drv = str(sc.get("driver") or "").strip()
            if drv not in COMPONENT_DRIVERS:
                problems.append(f"{what}: component driver must be one of {'|'.join(COMPONENT_DRIVERS)}, "
                                f"got {drv!r} (scroll/timeline stay exclusive to the primary sectional_score)")
            elif drv not in (rec.get("driver") or []):
                problems.append(f"{what}: declared driver '{drv}' is not in mechanism {mech}'s "
                                f"registry driver list {rec.get('driver')}")
    if not str(sc.get("fallback") or "").strip():
        problems.append(f"{what}: fallback is required")
    rr = sc.get("resolution_record")
    if not rr:
        problems.append(f"{what}: resolution_record is required")
    else:
        check_resolution(resolve_record_path(motion, rr),
                         "sectional", "SECTIONAL_OPEN", mech, problems, what)


def main() -> int:
    here = Path(__file__).resolve().parent
    ap = argparse.ArgumentParser()
    ap.add_argument("--motion-dir", required=True)
    ap.add_argument("--registry", default=str(here.parent / "references" / "execution-registry.json"))
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
    except Exception:
        pass

    motion = Path(args.motion_dir)
    problems: list[str] = []
    warnings: list[str] = []

    state_path = motion / "pipeline-state.json"
    if not state_path.exists():
        print(f"PROBLEM: {state_path} missing")
        print("FAIL (1 problem)")
        return 1
    state = load_json(state_path, problems, "pipeline-state.json")
    if state is not None:
        check_state(state, problems)

    try:
        records = {r["id"]: r for r in registry_lib.load_registry(args.registry)}
    except Exception as exc:  # noqa: BLE001
        problems.append(f"registry unreadable: {exc}")
        records = {}

    families: dict[str, str] = {}
    ss_path = motion / "sectional-score.json"
    if ss_path.exists():
        ss = load_json(ss_path, problems, "sectional-score.json") or {}
        for surface, entry in ss.items():
            what = f"sectional[{surface}]"
            if entry is None:
                continue
            if not isinstance(entry, dict):
                problems.append(f"{what}: entry must be null or an object")
                continue
            sc = entry.get("sectional_score")
            comps = entry.get("component_scores")
            if sc is None and not comps:
                problems.append(f"{what}: entry must be null or carry sectional_score "
                                "and/or component_scores")
                continue
            if sc is not None:
                check_score_entry(sc, what, surface, records, families,
                                  problems, warnings, motion)
            if comps is not None and not isinstance(comps, list):
                problems.append(f"{what}: component_scores must be an array")
            else:
                for i, cs in enumerate(comps or []):
                    check_score_entry(cs, f"component[{surface}#{i}]", surface,
                                      records, families, problems, warnings,
                                      motion, component=True)

    pol_path = motion / "atomic-policy.json"
    policy = None
    if pol_path.exists():
        pol_doc = load_json(pol_path, problems, "atomic-policy.json") or {}
        policy = pol_doc.get("atomic_policy")
        if not isinstance(policy, dict):
            problems.append("atomic-policy.json must carry {'atomic_policy': {...}}")
            policy = None
        else:
            if policy.get("no_reflow") is not True:
                problems.append("atomic_policy.no_reflow must be true (the atomic contract IS no-reflow)")
            if not isinstance(policy.get("max_targets"), int) or policy["max_targets"] < 1:
                problems.append("atomic_policy.max_targets must be an integer >= 1")
            bad_props = [p for p in policy.get("allowed_properties") or []
                         if p not in ("transform", "opacity", "filter", "color", "border", "shadow")]
            if bad_props:
                problems.append(f"atomic_policy.allowed_properties outside the atomic contract: {bad_props}")

    for res_path in sorted(motion.glob("atomic-result-*.json")):
        doc = load_json(res_path, problems, res_path.name) or {}
        ar = doc.get("atomic_result") or {}
        what = f"atomic[{ar.get('surface', res_path.name)}]"
        effects = ar.get("effects") or []
        if policy and len(effects) > policy.get("max_targets", 0):
            problems.append(f"{what}: {len(effects)} effects exceed atomic_policy.max_targets={policy.get('max_targets')}")
        for eff in effects:
            mech = eff.get("mechanism")
            rec = records.get(mech)
            if rec is None:
                problems.append(f"{what}: mechanism {mech!r} not in execution registry")
            elif "atomic" not in (rec.get("allowed_phases") or []):
                problems.append(f"{what}: mechanism {mech} does not allow the atomic phase")
            if not eff.get("target"):
                problems.append(f"{what}: effect missing target selector")
            rr = eff.get("resolution_record")
            if not rr:
                problems.append(f"{what}: effect missing resolution_record")
            else:
                check_resolution(resolve_record_path(motion, rr), "atomic", "ATOMIC_OPEN", mech, problems, what)
        for claim in ("layout_diff", "reduced_motion"):
            if ar.get(claim) != "pass":
                problems.append(f"{what}: {claim} is {ar.get(claim)!r}, must be 'pass' before COMPLETE")

    for w in warnings:
        print(f"WARN: {w}")
    if problems:
        for p in problems:
            print(f"PROBLEM: {p}")
        print(f"FAIL ({len(problems)} problem{'s' if len(problems) != 1 else ''})")
        return 1
    print(f"OK motion artifacts valid: {motion}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
