#!/usr/bin/env python3
"""Regression suite for validate_infospec.py (loop-ia-ab hardening, solidified 2026-07-08).

Each fixture pins an expected verdict + minimum finding counts, so future validator edits
can't silently loosen a gate (positives must stay PASS, negatives must stay FAIL for the
REASON they encode). Pure stdlib; run from anywhere:

    python companions/information-architecture/tests/run_tests.py

Exit 0 = all green / 1 = mismatches (each printed).
"""
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
FIXTURES = os.path.join(HERE, "fixtures")
VALIDATOR = os.path.join(HERE, "..", "scripts", "validate_infospec.py")

# fixture -> (verdict, min_blocks, min_warns, min_notes, must_mention substring or None)
EXPECT = {
    # v1 baseline + task_paths positives
    "return-test-spec.json":   ("PASS", 0, 0, 0, None),
    "tp-pos.json":             ("PASS", 0, 0, 0, None),
    # task_paths negatives (contract v1.1)
    "tp-neg-badhop.json":      ("FAIL", 2, 0, 0, "not a link_map edge"),
    "tp-neg-unknown.json":     ("FAIL", 1, 0, 0, "not a screen id"),
    "tp-neg-lint.json":        ("FAIL", 2, 0, 0, "composition leak"),
    "tp-neg-short.json":       ("FAIL", 1, 0, 0, ">=2 stops"),
    "tp-neg-dup.json":         ("FAIL", 1, 0, 0, "duplicate task_path id"),
    # task_paths coverage (v1.1)
    "tp-cov-warn.json":        ("PASS", 0, 1, 1, "not visited by any task_path"),
    # return rule (v1.2) -- loop-shaped spec with zero return edges lives inline below
    "ret-noback-inline":       ("FAIL", 3, 0, 0, "cannot walk back to the entry"),
    "ret-conv.json":           ("PASS", 0, 0, 0, None),
    "ret-ov.json":             ("PASS", 0, 0, 3, "user-exempted via return_overrides"),
    "ret-stale.json":          ("PASS", 0, 1, 0, "stale/unknown entry"),
    "ret-empty.json":          ("FAIL", 4, 0, 0, "must be a non-empty string"),
    # entry anchor (v1.2.1) -- hero is not necessarily the front door
    "entry-ok.json":           ("PASS", 0, 0, 0, None),
    "entry-hero-noback.json":  ("FAIL", 1, 0, 0, "cannot walk back to the entry (home)"),
    "entry-unknown.json":      ("FAIL", 1, 0, 0, "not a screens[].id"),
}


def make_inline_fixtures(tmpdir):
    """Fixtures derived from tracked ones at runtime (keeps the corpus DRY)."""
    conv = json.load(open(os.path.join(FIXTURES, "ret-conv.json"), encoding="utf-8"))
    noback = dict(conv)
    noback.pop("return_convention", None)
    p = os.path.join(tmpdir, "ret-noback-inline.json")
    json.dump(noback, open(p, "w", encoding="utf-8"), ensure_ascii=False)
    return {"ret-noback-inline": p}


def run_one(path):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")  # CJK in findings; Windows pipes default GBK
    r = subprocess.run([sys.executable, VALIDATOR, path],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=env)
    out = r.stdout
    last = [l for l in out.splitlines() if l.startswith("result:")]
    if not last:
        return None, out
    # "result: B BLOCK / W WARN / N NOTE -> VERDICT"
    head, verdict = last[0].split("->")
    nums = [int(tok) for tok in head.replace("result:", "").split() if tok.isdigit()]
    return {"verdict": verdict.strip(), "b": nums[0], "w": nums[1], "n": nums[2]}, out


def main():
    failures = []
    with tempfile.TemporaryDirectory() as tmp:
        inline = make_inline_fixtures(tmp)
        for name, (verdict, mb, mw, mn, needle) in sorted(EXPECT.items()):
            path = inline.get(name) or os.path.join(FIXTURES, name)
            got, out = run_one(path)
            if got is None:
                failures.append("%s: validator crashed or no result line\n%s" % (name, out))
                continue
            probs = []
            if got["verdict"] != verdict:
                probs.append("verdict %s != %s" % (got["verdict"], verdict))
            if got["b"] < mb:
                probs.append("BLOCK %d < %d" % (got["b"], mb))
            if got["w"] < mw:
                probs.append("WARN %d < %d" % (got["w"], mw))
            if got["n"] < mn:
                probs.append("NOTE %d < %d" % (got["n"], mn))
            if needle and needle not in out:
                probs.append("missing expected message %r" % needle)
            if probs:
                failures.append("%s: %s" % (name, "; ".join(probs)))
            else:
                print("ok   %s (%s %d/%d/%d)" % (name, got["verdict"], got["b"], got["w"], got["n"]))
    if failures:
        print("---")
        for f in failures:
            print("FAIL " + f)
        return 1
    print("--- all %d fixtures green" % len(EXPECT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
