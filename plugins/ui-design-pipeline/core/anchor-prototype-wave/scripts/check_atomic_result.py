#!/usr/bin/env python3
"""check_atomic_result.py — deterministic Atomic Pass discipline gate
(plan step 9 / test-matrix cases 10-12's atomic half).

The Atomic Pass patches EXISTING UI under a no-reflow budget. This script
verifies the evidence trail of one patched surface:

  1. POLICY conformance — effects count <= max_targets; policy well-formed.
  2. STATIC patch scan — lines ADDED between the pre-atomic backup and the
     patched page must not contain structural/forbidden signatures:
     grid/flex-template changes, ScrollTrigger pin, position:sticky, global
     scroll interception, <section>/<nav>/<header>/<main>/<aside>/<footer>
     tag-count changes, new requestAnimationFrame loops (unless the policy
     allows overlay canvas), position:fixed additions (same condition).
  3. LAYOUT DIFF — a captured before/after bounding-rect JSON (browser-captured
     evidence; capture snippet lives in anchor-prototype-wave SKILL.md §Atomic
     Pass) must show zero drift beyond tolerance. The checker COMPUTES the
     verdict from the numbers — the result file's "layout_diff: pass" claim is
     verified, never trusted.

Exit 0 = discipline held; exit 1 = REVERT REQUIRED (problems printed).
Honest boundary: the static scan is a regex net and the layout JSON is
agent-captured evidence — the deterministic part is the COMPARISON; producing
truthful captures is the runner's obligation (same honesty model as the wave's
other validators). Python 3.10+, stdlib only.

Usage:
    python check_atomic_result.py --result <motion>/atomic-result-<s>.json \
        --policy <motion>/atomic-policy.json \
        --before audits/atomic/<s>.before.html --after <s>/index.html \
        [--layout-diff audits/atomic/<s>.layout-diff.json] [--tolerance 0.5]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

STRUCTURAL_TAGS = ("section", "nav", "header", "main", "aside", "footer")

FORBIDDEN_ALWAYS = [
    (re.compile(r"grid-template", re.I), "grid-template change"),
    (re.compile(r"\bpin\s*:\s*(true|1|['\"])", re.I), "ScrollTrigger pin"),
    (re.compile(r"position\s*:\s*sticky", re.I), "position:sticky addition"),
    (re.compile(r"document\.(body|documentElement)\.style\.(overflow|scrollBehavior)", re.I),
     "global scroll interception"),
    (re.compile(r"addEventListener\(\s*['\"]wheel['\"][^)]*\)\s*;?(?![^\n]*passive)", re.I),
     "non-passive wheel listener (scroll interception)"),
]
FORBIDDEN_UNLESS_OVERLAY = [
    (re.compile(r"position\s*:\s*fixed", re.I), "position:fixed addition"),
    (re.compile(r"requestAnimationFrame\s*\(", re.I), "new rAF loop"),
]


def added_lines(before: str, after: str) -> list[str]:
    b = {}
    for ln in before.splitlines():
        key = ln.strip()
        b[key] = b.get(key, 0) + 1
    out = []
    for ln in after.splitlines():
        key = ln.strip()
        if b.get(key, 0) > 0:
            b[key] -= 1
        elif key:
            out.append(ln)
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--result", required=True)
    ap.add_argument("--policy", required=True)
    ap.add_argument("--before", required=True)
    ap.add_argument("--after", required=True)
    ap.add_argument("--layout-diff", default=None)
    ap.add_argument("--tolerance", type=float, default=0.5)
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
    except Exception:
        pass

    problems: list[str] = []

    def load(p: str, what: str):
        try:
            return json.loads(Path(p).read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            problems.append(f"{what} unreadable: {exc}")
            return None

    pol_doc = load(args.policy, "policy") or {}
    policy = pol_doc.get("atomic_policy") or {}
    res_doc = load(args.result, "result") or {}
    result = res_doc.get("atomic_result") or {}
    effects = result.get("effects") or []

    # 1) policy conformance
    max_targets = policy.get("max_targets")
    if isinstance(max_targets, int) and len(effects) > max_targets:
        problems.append(f"{len(effects)} effects exceed atomic_policy.max_targets={max_targets}")
    if policy.get("no_reflow") is not True:
        problems.append("atomic_policy.no_reflow must be true")
    for eff in effects:
        if not eff.get("target"):
            problems.append("effect missing target selector")

    # 2) static patch scan on ADDED lines
    try:
        before = Path(args.before).read_text(encoding="utf-8")
        after = Path(args.after).read_text(encoding="utf-8")
    except Exception as exc:  # noqa: BLE001
        problems.append(f"before/after unreadable: {exc}")
        before = after = ""
    if before and after:
        allow_overlay = policy.get("allow_overlay_canvas") is True
        adds = added_lines(before, after)
        for ln in adds:
            for rx, label in FORBIDDEN_ALWAYS:
                if rx.search(ln):
                    problems.append(f"forbidden addition ({label}): {ln.strip()[:120]}")
            if not allow_overlay:
                for rx, label in FORBIDDEN_UNLESS_OVERLAY:
                    if rx.search(ln):
                        problems.append(f"forbidden addition without allow_overlay_canvas ({label}): {ln.strip()[:120]}")
        for tag in STRUCTURAL_TAGS:
            nb = len(re.findall(rf"<{tag}\b", before, re.I))
            na = len(re.findall(rf"<{tag}\b", after, re.I))
            if nb != na:
                problems.append(f"structural tag count changed: <{tag}> {nb} -> {na}")

    # 3) layout diff (computed, never trusted)
    if args.layout_diff:
        diff = load(args.layout_diff, "layout-diff") or {}
        rects = diff.get("rects") or {}
        if not rects:
            problems.append("layout-diff carries no rects — capture the before/after geometry")
        tol = float(diff.get("tolerance_px", args.tolerance))
        for sel, pair in rects.items():
            b, a = pair.get("before"), pair.get("after")
            if not (isinstance(b, list) and isinstance(a, list) and len(b) == 4 and len(a) == 4):
                problems.append(f"layout-diff[{sel}]: before/after must be [x,y,w,h]")
                continue
            drift = max(abs(float(b[i]) - float(a[i])) for i in range(4))
            if drift > tol:
                problems.append(f"layout drift on {sel}: {drift:.2f}px > {tol}px — REVERT the patch")
        if result.get("layout_diff") == "pass" and any("layout drift" in p for p in problems):
            problems.append("result claims layout_diff=pass but the captured geometry disagrees")
    elif result.get("layout_diff") == "pass":
        problems.append("result claims layout_diff=pass but no --layout-diff evidence was provided")

    if problems:
        for p in problems:
            print(f"PROBLEM: {p}")
        print(f"ATOMIC BLOCK ({len(problems)}) — revert the patch or fix the evidence")
        return 1
    print(f"ATOMIC OK: {len(effects)} effect(s) within policy; no structural additions; zero layout drift")
    return 0


if __name__ == "__main__":
    sys.exit(main())
