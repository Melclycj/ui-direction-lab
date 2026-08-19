#!/usr/bin/env python3
"""render_run.py — RUN.md is GENERATED, never maintained.

WHY THIS EXISTS
---------------
The resume pointer for a multi-session run was originally specified as "update
RUN.md at every stage boundary". That is an instruction, and instructions rot:
one missed update and the pointer lies about where the run stopped. A pointer
that lies is worse than no pointer, because the next session believes it.

So RUN.md is not maintained by anyone. It is DERIVED, every time, from two
sources that cannot drift:

  1. `<run-root>/directions/motion/pipeline-state.json` — the append-audited
     machine state. It already holds the stage, the gate flags, and the
     user's approvals VERBATIM (`pipeline_state.py approve` refuses an empty
     approval-text and is write-once), plus a timestamped state_log.
  2. The run root itself — artifacts on disk say what happened. An
     `ia/info-spec.json` means IA round 1 produced a spec; `ia/wireframes/`
     means round 2 ran; `surfaces/*/index.html` means the wave ran.

Nothing here writes pipeline-state.json. This script is a READER. Gate
decisions keep reading the machine state directly; RUN.md is a human
convenience, and a convenience must never be able to move a gate.

FRESHNESS
---------
Every render stamps the sha256 of the state file it was rendered from:

    <!-- rendered-from: sha256:<digest> state=<STATE> log=<n> -->

`--check` recomputes that digest and fails if it moved. mtime is deliberately
not used: a checkout or a file copy rewrites mtimes and would produce both
false alarms and false confidence. `preflight_wave.py` calls `--check` so the
pointer is provably fresh before the most expensive step in the pipeline.

HONEST LIMIT
------------
This guarantees RUN.md never LIES (it is recomputed, not remembered). It does
not guarantee RUN.md is always CURRENT — only the wave preflight forces a
re-render. A run interrupted between the two IA rounds still relies on someone
running this. Re-running it is always safe and always cheap.

Usage:
    python render_run.py --run-root <dir>              # (re)write RUN.md
    python render_run.py --run-root <dir> --check      # exit 1 if missing/stale
    python render_run.py --run-root <dir> --print      # to stdout, write nothing

Exit 0 = ok; exit 1 = stale/missing (--check) or unreadable state.
Python 3.9+, stdlib only.
"""
from __future__ import annotations

import argparse
import glob
import hashlib
import json
import os
import re
import sys

STAMP_RE = re.compile(r"<!-- rendered-from: (sha256:[0-9a-f]{64}|no-state) ")

# (key, label) — the 11 stages the pipeline actually gates on.
STAGES = [
    ("ia1", "IA round 1 — information structure"),
    ("batch1", "Batch 1 — directions + LEAD pick"),
    ("contrast", "Contrast gate"),
    ("batch2", "Batch 2 — motion stance"),
    ("lock", "Chassis lock"),
    ("ia2", "IA round 2 — wireframes (Stage-F)"),
    ("sectional", "Sectional Score"),
    ("lockwave", "lock -> wave"),
    ("wave", "Surface wave"),
    ("atomic", "Atomic Pass"),
    ("accept", "Accept gallery"),
]

ORDER = ("CHASSIS_OPEN", "CHASSIS_LOCKED", "SECTIONAL_OPEN", "SECTIONAL_LOCKED",
         "BASE_WAVE_READY", "ATOMIC_OPEN", "COMPLETE")


def at_least(state, target):
    """True when `state` has reached `target` on the irreversible ladder."""
    try:
        return ORDER.index(state) >= ORDER.index(target)
    except ValueError:
        return False


def read_state(run_root):
    """Return (doc, digest, path). doc is None when the run has no machine state yet."""
    path = os.path.join(run_root, "directions", "motion", "pipeline-state.json")
    if not os.path.exists(path):
        return None, "no-state", path
    raw = open(path, "rb").read()
    return json.loads(raw.decode("utf-8")), "sha256:" + hashlib.sha256(raw).hexdigest(), path


def probe(run_root):
    """What the filesystem proves happened, independent of the state machine."""
    j = lambda *p: os.path.join(run_root, *p)
    g = lambda pat: sorted(glob.glob(j(*pat)))
    return {
        "info_spec": os.path.exists(j("ia", "info-spec.json")),
        "board": os.path.exists(j("ia", "board", "board.html")),
        "variants": g(("directions", "variant-*", "index.html")),
        "chassis_md": os.path.exists(j("directions", "CHASSIS.md")),
        "wireframes": g(("ia", "wireframes", "*", "index.html")),
        "surfaces": g(("surfaces", "*", "index.html")),
    }


def statuses(doc, fs):
    """Derive one status per stage. Never guesses: unknown stays 'pending'."""
    d = doc or {}
    state = d.get("state")
    appr = d.get("user_approvals") or {}
    locked = bool(d.get("chassis_locked")) or fs["chassis_md"]
    st = {k: "pending" for k, _ in STAGES}
    ev = {k: "" for k, _ in STAGES}

    if fs["info_spec"]:
        st["ia1"] = "done"; ev["ia1"] = "`ia/info-spec.json`"
    if fs["variants"]:
        st["batch1"] = "done" if locked else "in progress"
        ev["batch1"] = "%d variant(s) in `directions/`" % len(fs["variants"])
    # The contrast gate is a precondition of the lock: it cannot be behind it.
    if locked:
        st["contrast"] = "done"; ev["contrast"] = "precedes the lock"
    if d.get("page_scoped_mechanism", "__unset__") != "__unset__":
        st["batch2"] = "done"
        ev["batch2"] = "`page_scoped_mechanism` = %r" % d.get("page_scoped_mechanism")
    if locked:
        st["lock"] = "done"
        ev["lock"] = "`directions/CHASSIS.md`" if fs["chassis_md"] else "state `chassis_locked`"
    if fs["wireframes"]:
        st["ia2"] = "done" if d.get("composition_ready") else "in progress"
        ev["ia2"] = "%d wireframe(s)" % len(fs["wireframes"])
    elif d.get("composition_ready"):
        st["ia2"] = "done"; ev["ia2"] = "`composition_ready`"
    ss = d.get("sectional_status")
    if ss == "skipped":
        st["sectional"] = "skipped"; ev["sectional"] = "skip is the default answer"
    elif ss == "selected":
        st["sectional"] = "done"; ev["sectional"] = "`motion/sectional-score.json`"
    elif ss and ss != "not-open":
        st["sectional"] = "in progress"; ev["sectional"] = "`sectional_status` = %r" % ss
    if appr.get("chassis") and at_least(state, "SECTIONAL_LOCKED"):
        st["lockwave"] = "done"; ev["lockwave"] = "approved verbatim"
    if fs["surfaces"]:
        st["wave"] = "done" if at_least(state, "ATOMIC_OPEN") or state == "COMPLETE" else "in progress"
        ev["wave"] = "%d surface(s)" % len(fs["surfaces"])
    astat = d.get("atomic_status")
    if astat == "skipped":
        st["atomic"] = "skipped"
    elif appr.get("atomic_policy"):
        st["atomic"] = "done" if state == "COMPLETE" else "in progress"
        ev["atomic"] = "budget approved verbatim"
    if state == "COMPLETE":
        st["accept"] = "done"; ev["accept"] = "state `COMPLETE`"
    return st, ev


def next_action(st):
    for key, label in STAGES:
        if st[key] in ("pending", "in progress"):
            verb = "start" if st[key] == "pending" else "finish"
            owner = {
                "ia1": "`information-architecture` round 1",
                "batch1": "`prototyping-ui-directions` Batch 1",
                "contrast": "`prototyping-ui-directions` contrast gate",
                "batch2": "`prototyping-ui-directions` Batch 2",
                "lock": "`prototyping-ui-directions` chassis lock",
                "ia2": "`information-architecture` round 2 (Stage-F gate)",
                "sectional": "`prototyping-ui-directions` Sectional Score",
                "lockwave": "your explicit approval word, then `anchor-prototype-wave`",
                "wave": "`anchor-prototype-wave`",
                "atomic": "`anchor-prototype-wave` Atomic Pass",
                "accept": "you, accepting the gallery",
            }[key]
            return "%s **%s** — %s" % (verb, label, owner)
    return "nothing — the run is COMPLETE"


def blocked_on(doc, st):
    d = doc or {}
    appr = d.get("user_approvals") or {}
    if st["lockwave"] == "pending" and st["lock"] == "done" and not appr.get("chassis"):
        return "your verbatim approval of the chassis lock (the model may not self-approve it)"
    if st["batch1"] == "in progress":
        return "your LEAD pick"
    if st["ia1"] == "pending":
        return "nothing — the run has not started"
    return "nothing"


def decisions(doc):
    """Verbatim human approvals, straight out of the append-audited state log."""
    d = doc or {}
    out = []
    for entry in d.get("state_log") or []:
        if entry.get("event") == "approve" and entry.get("approval_text"):
            out.append((entry.get("at", "?"),
                        (entry.get("field") or "").replace("user_approvals.", ""),
                        entry["approval_text"]))
    if out:
        return out
    # A state written before the log carried approval_text still has the values.
    for gate, text in (d.get("user_approvals") or {}).items():
        if text:
            out.append(("(unlogged)", gate, text))
    return out


def render(run_root, doc, digest):
    d = doc or {}
    fs = probe(run_root)
    st, ev = statuses(d, fs)
    nick = d.get("run") or os.path.basename(os.path.abspath(run_root))
    L = []
    L.append("<!-- rendered-from: %s state=%s log=%d -->"
             % (digest, d.get("state", "none"), len(d.get("state_log") or [])))
    L.append("<!-- GENERATED by core/ui-pipeline/scripts/render_run.py — do not hand-edit."
             "  Edits are silently overwritten on the next render, and a hand-edited pointer"
             "  is exactly the lying pointer this file exists to prevent. -->")
    L.append("")
    L.append("# RUN — %s" % nick)
    L.append("")
    L.append("- **Run root**: `%s`" % run_root.replace(os.sep, "/"))
    L.append("- **Machine state**: `%s`" % (d.get("state") or "not initialised"))
    L.append("")
    L.append("## Current pointer")
    L.append("")
    L.append("**Next action**: %s" % next_action(st))
    L.append("")
    L.append("**Blocked on**: %s" % blocked_on(d, st))
    L.append("")
    L.append("## Stages")
    L.append("")
    L.append("| # | Stage | Status | Evidence |")
    L.append("|---|---|---|---|")
    for i, (key, label) in enumerate(STAGES, 1):
        L.append("| %d | %s | %s | %s |" % (i, label, st[key], ev[key] or ""))
    L.append("")
    L.append("## Human decisions (verbatim)")
    L.append("")
    dec = decisions(d)
    if dec:
        for at, gate, text in dec:
            L.append("- `%s` · **%s** · 「%s」" % (at, gate, text))
    else:
        L.append("_None recorded yet._")
    L.append("")
    L.append("---")
    L.append("")
    L.append("_Derived from `directions/motion/pipeline-state.json` plus what is on disk._")
    L.append("_Gate decisions read the machine state directly; this file never feeds a gate._")
    L.append("")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run-root", required=True)
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if RUN.md is missing or was rendered from a different state")
    ap.add_argument("--print", dest="to_stdout", action="store_true",
                    help="write nothing; print the render")
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    root = args.run_root
    if not os.path.isdir(root):
        print("BLOCK: run root not found: %s" % root)
        return 1
    try:
        doc, digest, state_path = read_state(root)
    except Exception as exc:
        print("BLOCK: pipeline-state.json unreadable: %s" % exc)
        return 1

    out_path = os.path.join(root, "RUN.md")

    if args.check:
        if not os.path.exists(out_path):
            print("BLOCK: no RUN.md at %s — render it first:" % out_path)
            print("       python render_run.py --run-root %s" % root)
            return 1
        head = open(out_path, encoding="utf-8").read(400)
        m = STAMP_RE.search(head)
        if not m:
            print("BLOCK: RUN.md carries no rendered-from stamp (hand-written or truncated).")
            return 1
        if m.group(1) != digest:
            print("BLOCK: RUN.md is stale — rendered from %s, state is now %s" % (m.group(1), digest))
            print("       re-render: python render_run.py --run-root %s" % root)
            return 1
        print("OK: RUN.md is current (%s)" % digest)
        return 0

    text = render(root, doc, digest)
    if args.to_stdout:
        print(text)
        return 0
    with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)
    print("OK wrote %s (state %s)" % (out_path, (doc or {}).get("state", "none")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
