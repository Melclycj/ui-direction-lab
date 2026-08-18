#!/usr/bin/env python3
"""pipeline_state.py — the run-local pipeline-state artifact + its ONLY legal
mutation path (execution-contracts.md §4).

State machine (monotonic; append-audited; the model never self-approves):

  CHASSIS_OPEN -> CHASSIS_LOCKED -> SECTIONAL_OPEN -> SECTIONAL_LOCKED
  -> BASE_WAVE_READY -> ATOMIC_OPEN -> COMPLETE
  (special legal edge: BASE_WAVE_READY -> COMPLETE when atomic never opens)

Commands:
  init        --out-dir D --run ID                       create <D>/pipeline-state.json (refuses overwrite)
  show        --state-file P                             print the artifact
  set         --state-file P --field F --value V --evidence "..." [--by ...]
              fields: composition_ready (false->true) | sectional_status (forward)
                      | atomic_status (forward) | chassis_ref (write-once)
                      | page_scoped_mechanism (write-once, pre/at lock)
  approve     --state-file P --gate chassis|sectional|atomic_policy
              --approval-text "<user's verbatim words>" --evidence "..."
  transition  --state-file P --to STATE --evidence "..." [--by ...]
  verify      --state-file P [--require-state S] [--min-state S]
              [--require-composition-ready] [--require-sectional selected,skipped]
              [--require-atomic STATUS] [--require-approval chassis,...]

Exit 0 = done/verified; exit 1 = refused (reason printed). Refusals never
mutate the artifact. No third-party dependencies. Python 3.10+.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ORDER = ("CHASSIS_OPEN", "CHASSIS_LOCKED", "SECTIONAL_OPEN", "SECTIONAL_LOCKED",
         "BASE_WAVE_READY", "ATOMIC_OPEN", "COMPLETE")
SECTIONAL_ORDER = ("not-open", "pending", "selected", "skipped")  # selected|skipped both terminal
ATOMIC_ORDER = ("not-open", "policy-approved", "patched", "verified")
BY = ("user-approval", "gate", "system")
APPROVAL_GATES = ("chassis", "sectional", "atomic_policy")


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save(path: str, doc: dict) -> None:
    Path(path).write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def refuse(msg: str) -> int:
    print(f"REFUSED: {msg}")
    return 1


def log_entry(doc: dict, **kw) -> None:
    entry = {"at": now()}
    entry.update(kw)
    doc.setdefault("state_log", []).append(entry)


def cmd_init(args) -> int:
    out = Path(args.out_dir) / "pipeline-state.json"
    if out.exists():
        return refuse(f"{out} already exists — a reopened chassis is a NEW run, never a reset")
    out.parent.mkdir(parents=True, exist_ok=True)
    doc = {
        "state": "CHASSIS_OPEN",
        "run": args.run,
        "chassis_ref": None,
        "chassis_locked": False,
        "composition_ready": False,
        "page_scoped_mechanism": "__unset__",
        "sectional_status": "not-open",
        "atomic_status": "not-open",
        "user_approvals": {"chassis": None, "sectional": None, "atomic_policy": None},
        "state_log": [],
    }
    log_entry(doc, event="init", to="CHASSIS_OPEN", by="system", evidence=f"run {args.run} opened")
    save(str(out), doc)
    print(f"OK init: {out} (state CHASSIS_OPEN)")
    return 0


def cmd_show(args) -> int:
    print(json.dumps(load(args.state_file), indent=2, ensure_ascii=False))
    return 0


def _forward_only(order: tuple, cur: str, new: str) -> bool:
    try:
        return order.index(new) > order.index(cur)
    except ValueError:
        return False


def cmd_set(args) -> int:
    doc = load(args.state_file)
    f, v = args.field, args.value
    if f == "composition_ready":
        if v != "true":
            return refuse("composition_ready can only move false->true")
        if doc.get("composition_ready"):
            return refuse("composition_ready already true (write-once)")
        doc["composition_ready"] = True
    elif f == "sectional_status":
        cur = doc.get("sectional_status")
        if cur in ("selected", "skipped"):
            return refuse(f"sectional_status {cur} is terminal")
        legal = (cur == "not-open" and v == "pending") or \
                (cur == "pending" and v in ("selected", "skipped"))
        if not legal:
            return refuse(f"sectional_status {cur} -> {v} is not a legal move "
                          "(not-open->pending->selected|skipped, one step at a time)")
        if v in ("selected", "skipped") and doc.get("state") != "SECTIONAL_OPEN":
            return refuse(f"sectional selection happens only while SECTIONAL_OPEN (state={doc.get('state')})")
        doc["sectional_status"] = v
    elif f == "atomic_status":
        cur = doc.get("atomic_status")
        if v not in ATOMIC_ORDER or ATOMIC_ORDER.index(v) != ATOMIC_ORDER.index(cur) + 1:
            return refuse(f"atomic_status {cur} -> {v} must advance one step ({ATOMIC_ORDER})")
        if v == "policy-approved" and doc.get("state") != "BASE_WAVE_READY":
            return refuse(f"atomic policy is approved at BASE_WAVE_READY (state={doc.get('state')})")
        if v in ("patched", "verified") and doc.get("state") != "ATOMIC_OPEN":
            return refuse(f"atomic patching/verification happens only while ATOMIC_OPEN (state={doc.get('state')})")
        doc["atomic_status"] = v
    elif f == "chassis_ref":
        if doc.get("chassis_ref"):
            return refuse("chassis_ref is write-once")
        doc["chassis_ref"] = v
    elif f == "page_scoped_mechanism":
        if doc.get("page_scoped_mechanism") != "__unset__":
            return refuse("page_scoped_mechanism is write-once")
        if doc["state"] not in ("CHASSIS_OPEN", "CHASSIS_LOCKED"):
            return refuse("page_scoped_mechanism is a chassis-phase declaration")
        doc["page_scoped_mechanism"] = None if v in ("null", "none", "None") else v
    else:
        return refuse(f"field {f!r} is not settable via this tool")
    log_entry(doc, event="set", field=f, to=v, by=args.by, evidence=args.evidence)
    save(args.state_file, doc)
    print(f"OK set {f}={v}")
    return 0


def cmd_approve(args) -> int:
    doc = load(args.state_file)
    gate = args.gate
    if gate not in APPROVAL_GATES:
        return refuse(f"gate must be one of {APPROVAL_GATES}")
    if doc["user_approvals"].get(gate):
        return refuse(f"user_approvals.{gate} already recorded (write-once)")
    text = (args.approval_text or "").strip()
    if not text:
        return refuse("approval-text must quote the user's approving words verbatim (non-empty)")
    doc["user_approvals"][gate] = text
    log_entry(doc, event="approve", field=f"user_approvals.{gate}", by="user-approval",
              evidence=args.evidence, approval_text=text)
    save(args.state_file, doc)
    print(f"OK approve {gate}")
    return 0


def cmd_transition(args) -> int:
    doc = load(args.state_file)
    cur, to = doc["state"], args.to
    if to not in ORDER:
        return refuse(f"unknown state {to!r}")
    ci, ti = ORDER.index(cur), ORDER.index(to)
    if ti <= ci:
        return refuse(f"backward/self transition {cur} -> {to} (monotonic state machine)")
    special_skip = (cur == "BASE_WAVE_READY" and to == "COMPLETE")
    if ti != ci + 1 and not special_skip:
        return refuse(f"{cur} -> {to} skips states; only one step at a time "
                      "(exception: BASE_WAVE_READY -> COMPLETE when atomic never opens)")

    # per-target requirements (evidence-gated; the model cannot self-approve)
    if to == "CHASSIS_LOCKED":
        if not doc["user_approvals"].get("chassis"):
            return refuse("CHASSIS_LOCKED needs user_approvals.chassis (run `approve --gate chassis` with the user's verbatim words first)")
        if not doc.get("chassis_ref"):
            return refuse("CHASSIS_LOCKED needs chassis_ref set first")
        if doc.get("page_scoped_mechanism") == "__unset__":
            return refuse("CHASSIS_LOCKED needs an explicit page_scoped_mechanism declaration (null is valid — declare it)")
        doc["chassis_locked"] = True
    elif to == "SECTIONAL_OPEN":
        if not doc.get("chassis_locked"):
            return refuse("SECTIONAL_OPEN requires a locked chassis")
        if not doc.get("composition_ready"):
            return refuse("SECTIONAL_OPEN requires composition_ready=true (IA Round-2 Stage-F passed, or single-page structure approved)")
        if doc.get("sectional_status") == "not-open":
            doc["sectional_status"] = "pending"
    elif to == "SECTIONAL_LOCKED":
        if doc.get("sectional_status") not in ("selected", "skipped"):
            return refuse("SECTIONAL_LOCKED requires sectional_status selected|skipped")
        if doc.get("sectional_status") == "selected" and not doc["user_approvals"].get("sectional"):
            return refuse("sectional_status=selected needs user_approvals.sectional (verbatim)")
    elif to == "BASE_WAVE_READY":
        if doc.get("sectional_status") not in ("selected", "skipped"):
            return refuse("BASE_WAVE_READY requires sectional_status selected|skipped")
    elif to == "ATOMIC_OPEN":
        if not doc["user_approvals"].get("atomic_policy"):
            return refuse("ATOMIC_OPEN needs user_approvals.atomic_policy (the user approves the POLICY, not each effect)")
        if doc.get("atomic_status") != "policy-approved":
            return refuse("ATOMIC_OPEN requires atomic_status=policy-approved")
    elif to == "COMPLETE":
        if special_skip:
            if doc.get("atomic_status") != "not-open":
                return refuse("BASE_WAVE_READY -> COMPLETE shortcut is only for runs where atomic never opened")
        elif doc.get("atomic_status") != "verified":
            return refuse("COMPLETE (from ATOMIC_OPEN) requires atomic_status=verified (layout diff + reduced-motion checks green)")

    doc["state"] = to
    log_entry(doc, event="transition", **{"from": cur}, to=to, by=args.by, evidence=args.evidence)
    save(args.state_file, doc)
    print(f"OK transition {cur} -> {to}")
    return 0


def cmd_verify(args) -> int:
    doc = load(args.state_file)
    problems = []
    if args.require_state and doc["state"] != args.require_state:
        problems.append(f"state {doc['state']} != required {args.require_state}")
    if args.min_state and ORDER.index(doc["state"]) < ORDER.index(args.min_state):
        problems.append(f"state {doc['state']} < required minimum {args.min_state}")
    if args.require_composition_ready and not doc.get("composition_ready"):
        problems.append("composition_ready is false")
    if args.require_sectional:
        allowed = [s.strip() for s in args.require_sectional.split(",")]
        if doc.get("sectional_status") not in allowed:
            problems.append(f"sectional_status {doc.get('sectional_status')} not in {allowed}")
    if args.require_atomic and doc.get("atomic_status") != args.require_atomic:
        problems.append(f"atomic_status {doc.get('atomic_status')} != {args.require_atomic}")
    if args.require_approval:
        for gate in [g.strip() for g in args.require_approval.split(",")]:
            if not doc.get("user_approvals", {}).get(gate):
                problems.append(f"user_approvals.{gate} missing")
    if problems:
        for p in problems:
            print(f"BLOCK: {p}")
        return 1
    print(f"OK verify: state={doc['state']}")
    return 0


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
    except Exception:
        pass
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("init"); p.add_argument("--out-dir", required=True); p.add_argument("--run", required=True)
    p = sub.add_parser("show"); p.add_argument("--state-file", required=True)
    p = sub.add_parser("set")
    p.add_argument("--state-file", required=True); p.add_argument("--field", required=True)
    p.add_argument("--value", required=True); p.add_argument("--evidence", required=True)
    p.add_argument("--by", default="system", choices=BY)
    p = sub.add_parser("approve")
    p.add_argument("--state-file", required=True); p.add_argument("--gate", required=True)
    p.add_argument("--approval-text", required=True); p.add_argument("--evidence", required=True)
    p = sub.add_parser("transition")
    p.add_argument("--state-file", required=True); p.add_argument("--to", required=True)
    p.add_argument("--evidence", required=True); p.add_argument("--by", default="system", choices=BY)
    p = sub.add_parser("verify")
    p.add_argument("--state-file", required=True)
    p.add_argument("--require-state", default=None); p.add_argument("--min-state", default=None)
    p.add_argument("--require-composition-ready", action="store_true")
    p.add_argument("--require-sectional", default=None)
    p.add_argument("--require-atomic", default=None)
    p.add_argument("--require-approval", default=None)

    args = ap.parse_args()
    try:
        return {"init": cmd_init, "show": cmd_show, "set": cmd_set,
                "approve": cmd_approve, "transition": cmd_transition,
                "verify": cmd_verify}[args.cmd](args)
    except FileNotFoundError as exc:
        print(f"REFUSED: state file unreadable: {exc}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
