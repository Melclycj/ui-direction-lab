#!/usr/bin/env python3
"""Regression suite for wire_navigation.py + import_verbatim.py.

Solidifies the scratchpad-only tests from the nav-linker / verbatim-import work
(anchor-prototype-wave v1.3.0 / v1.4.0 / v1.4.1) into a durable, tracked corpus
so a /clear can't lose them. Mirrors companions/information-architecture/tests/
run_tests.py in spirit: every fixture pins an exit code + must-mention substrings
so a future edit can't silently loosen a gate.

Both scripts MUTATE a wave dir, so each case copies its fixture into a fresh
tempdir first; the tracked fixtures/ are never modified. Pure stdlib; run from
anywhere:

    python core/anchor-prototype-wave/tests/run_tests.py

Exit 0 = all green / 1 = mismatches (each printed).

A-checklist coverage (ui-skills LEDGER, 2026-07-08):
  item 3 (durable in-repo fixture)  -> the whole suite (was scratchpad-only)
  item 4 (7.5 x ESCALATE collision) -> wire/escalate: wiring is on-disk-existence-
                                       keyed, NOT verdict-keyed, so inbound links
                                       to an ESCALATE page get wired and --check
                                       stays green (documented behaviour, see README)
  item 5 (7.5 idempotency)          -> wire/basic re-run is byte-identical
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
FIX = os.path.join(HERE, "fixtures")
WIRE = os.path.join(HERE, "..", "scripts", "wire_navigation.py")
IMPORT = os.path.join(HERE, "..", "scripts", "import_verbatim.py")
VSRC = os.path.join(FIX, "verbatim", "source")  # import source dir; READ-ONLY

failures = []


def run(script, *args):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")  # Windows pipes default GBK
    r = subprocess.run([sys.executable, script, *args],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=env)
    return r.returncode, r.stdout + r.stderr


def fail(name, detail, out=""):
    failures.append("%s: %s" % (name, detail))
    print("FAIL %s: %s" % (name, detail))
    if out:
        print("     ---8<--- captured output ---8<---")
        for line in out.splitlines():
            print("     " + line)


def expect(name, code, out, exp_code, needles, forbid=()):
    probs = []
    if code != exp_code:
        probs.append("exit %s != %s" % (code, exp_code))
    for n in needles:
        if n not in out:
            probs.append("missing %r" % n)
    for n in forbid:
        if n in out:
            probs.append("unexpected %r (should be absent)" % n)
    if probs:
        fail(name, "; ".join(probs), out)
    else:
        print("ok   %s" % name)


def md5_tree(root):
    tree = {}
    for dp, _dn, fn in os.walk(root):
        for f in fn:
            p = os.path.join(dp, f)
            with open(p, "rb") as fh:
                tree[os.path.relpath(p, root)] = hashlib.md5(fh.read()).hexdigest()
    return tree


def copy_fixture(rel, tmp):
    dst = os.path.join(tmp, os.path.basename(rel))
    shutil.copytree(os.path.join(FIX, rel), dst)
    return dst


def read(path):
    with open(path, "r", encoding="utf-8", newline="") as fh:
        return fh.read()


def write(path, text):
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)


# ---------------------------------------------------------------- wire_navigation

def test_wire_basic(tmp):
    d = copy_fixture("wire/basic", tmp)
    code, out = run(WIRE, d)
    # overview->detail + detail->overview = 2 wired; ghost kept (unbuilt); no-target kept
    expect("wire/basic wire", code, out, 0,
           ["2 link(s) wired", "-> detail", "-> overview", "unbuilt-target (ghost)"])
    after1 = md5_tree(d)
    # item 5: idempotent -- a 2nd wire finds nothing new and leaves files byte-identical
    code2, out2 = run(WIRE, d)
    expect("wire/basic idempotent (0 new)", code2, out2, 0, ["0 link(s) wired"])
    if md5_tree(d) != after1:
        fail("wire/basic idempotent (bytes)", "files changed on 2nd wire run")
    else:
        print("ok   wire/basic idempotent (byte-identical)")
    # --check must be green: both wired links resolve to built pages
    code3, out3 = run(WIRE, d, "--check")
    expect("wire/basic check", code3, out3, 0, ["2 wired link(s), 0 broken"])


def test_wire_mock_class(tmp):
    d = copy_fixture("wire/mock-class", tmp)
    code, out = run(WIRE, d)
    # wired but the link still carries an is-mock CLASS -> non-blocking WARN, exit 0
    expect("wire/mock-class wire (WARN, non-blocking)", code, out, 0,
           ["1 link(s) wired", "WARN", "is-mock", "1 WARN"])
    code2, out2 = run(WIRE, d, "--check")
    expect("wire/mock-class check (WARN, exit 0)", code2, out2, 0,
           ["1 wired link(s), 0 broken", "1 WARN", "is-mock"])


def test_wire_mock_inner_badge(tmp):
    # finding #4: the <a>'s OWN class is clean; the "mock" badge lives in an inner
    # <span class="mock-tag"> that stays visible after wiring. The WARN must fire on
    # the inner badge (the blind spot the class-only check used to miss), exit unchanged.
    d = copy_fixture("wire/mock-inner-badge", tmp)
    code, out = run(WIRE, d)
    expect("wire/mock-inner-badge wire (inner-badge WARN, non-blocking)", code, out, 0,
           ["1 link(s) wired", "WARN", "inner mock", "1 WARN"])
    code2, out2 = run(WIRE, d, "--check")
    expect("wire/mock-inner-badge check (inner-badge WARN, exit 0)", code2, out2, 0,
           ["1 wired link(s), 0 broken", "1 WARN", "inner mock"])


def test_wire_mock_inner_badge_gated(tmp):
    # low-noise half of finding #4: a CORRECTLY default-hidden badge (rule-6 gating done
    # right) is still physically present in the wired link's markup but is invisible, so
    # wire_navigation must NOT warn. This pins that the gate-aware check has no false
    # positives on well-authored waves.
    d = copy_fixture("wire/mock-inner-badge-gated", tmp)
    code, out = run(WIRE, d)
    expect("wire/mock-inner-badge-gated wire (no WARN)", code, out, 0,
           ["1 link(s) wired"], forbid=["WARN"])
    code2, out2 = run(WIRE, d, "--check")
    expect("wire/mock-inner-badge-gated check (0 WARN)", code2, out2, 0,
           ["1 wired link(s), 0 broken", "0 WARN"], forbid=["WARN:"])


def test_wire_escalate(tmp):
    d = copy_fixture("wire/escalate", tmp)
    code, out = run(WIRE, d)
    # item 4: wiring is disk-existence-keyed, not verdict-keyed. The ESCALATE page
    # ('broken') is a valid wire target AND its own back-link gets wired.
    expect("wire/escalate wire (wires to/from ESCALATE page)", code, out, 0,
           ["2 link(s) wired", "-> broken", "-> overview"])
    code2, out2 = run(WIRE, d, "--check")
    # --check stays green: the escalated page exists on disk, so the link resolves.
    expect("wire/escalate check (green despite broken page)", code2, out2, 0,
           ["2 wired link(s), 0 broken"])


def test_wire_broken_check(tmp):
    d = copy_fixture("wire/broken-check", tmp)
    code, out = run(WIRE, d)
    expect("wire/broken-check wire (no-op)", code, out, 0, ["0 link(s) wired"])
    # --check must FAIL: the pre-wired href points at ghost/, never built in this wave
    code2, out2 = run(WIRE, d, "--check")
    expect("wire/broken-check check (exit 1)", code2, out2, 1,
           ["1 broken", "leaves the wave or is broken"])


def test_wire_fragment_check(tmp):
    # 2026-07-21 finding: --check resolved the RAW href against disk, so a deep link
    # ("../detail/index.html#section-two") was looked up as a filename and reported
    # BROKEN although it navigates correctly. Verified in a browser on Averonel
    # before the fix landed. This pins both halves of the fix:
    #   - fragment / query / same-page-anchor hrefs on BUILT targets are green
    #   - stripping the fragment does NOT let a genuinely dead path pass
    d = copy_fixture("wire/fragment-check", tmp)
    code, out = run(WIRE, d)
    expect("wire/fragment-check wire (no-op, all pre-wired)", code, out, 0,
           ["0 link(s) wired"])
    code2, out2 = run(WIRE, d, "--check")
    expect("wire/fragment-check check (deep links green, dead path still broken)",
           code2, out2, 1, ["4 wired link(s), 1 broken", "../ghost/index.html#anywhere"])


# ---------------------------------------------------------------- import_verbatim

def _import(tmp):
    dest = os.path.join(tmp, "overview")
    code, out = run(IMPORT, "--source", VSRC, "--dest", dest)
    return dest, code, out


def test_verbatim_import(tmp):
    dest, code, out = _import(tmp)
    expect("verbatim import", code, out, 0, ["1 relative asset(s): style.css"])
    if not (os.path.isfile(os.path.join(dest, "index.html"))
            and os.path.isfile(os.path.join(dest, "style.css"))):
        fail("verbatim import (dest files)", "dest missing index.html or style.css")
    else:
        print("ok   verbatim import (dest has index.html + style.css)")


def test_verbatim_verify_ok(tmp):
    dest, _c, _o = _import(tmp)
    # the ONLY sanctioned edit on the copy: an additive data-nav-target stamp
    html = read(os.path.join(dest, "index.html"))
    stamped = html.replace('data-mock onclick',
                           'data-mock data-nav-target="settings" onclick', 1)
    if stamped == html:
        fail("verbatim verify ok", "fixture drift: mock link to stamp not found")
        return
    write(os.path.join(dest, "index.html"), stamped)
    code, out = run(IMPORT, "--source", VSRC, "--dest", dest, "--verify")
    expect("verbatim verify ok (stamp only -> exit 0)", code, out, 0, ["0 lock violation"])


def test_verbatim_verify_content(tmp):
    dest, _c, _o = _import(tmp)
    html = read(os.path.join(dest, "index.html"))
    write(os.path.join(dest, "index.html"), html.replace("Approved hero", "Tampered hero", 1))
    code, out = run(IMPORT, "--source", VSRC, "--dest", dest, "--verify")
    expect("verbatim verify neg: content edit (exit 1)", code, out, 1, ["LOCK BROKEN"])


def test_verbatim_verify_asset_differ(tmp):
    dest, _c, _o = _import(tmp)
    write(os.path.join(dest, "style.css"), "/* tampered */\n")
    code, out = run(IMPORT, "--source", VSRC, "--dest", dest, "--verify")
    expect("verbatim verify neg: asset differs (exit 1)", code, out, 1,
           ["asset differs from source"])


def test_verbatim_verify_asset_missing(tmp):
    dest, _c, _o = _import(tmp)
    os.remove(os.path.join(dest, "style.css"))
    code, out = run(IMPORT, "--source", VSRC, "--dest", dest, "--verify")
    expect("verbatim verify neg: asset missing (exit 1)", code, out, 1,
           ["asset missing in dest"])


# --- motion-architecture teeth (preflight / atomic checker / pipeline-gate hook) ---

PREFLIGHT = os.path.join(HERE, "..", "scripts", "preflight_wave.py")
ATOMIC = os.path.join(HERE, "..", "scripts", "check_atomic_result.py")
HOOK = os.path.join(HERE, "..", "..", "..", "hooks", "pipeline-gate.js")
NODE = shutil.which("node")


def _write(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=1)


def _mk_motion(tmp, state="SECTIONAL_LOCKED", sectional="skipped", **over):
    run_dir = os.path.join(tmp, "testbed", "runs", "r1")
    motion = os.path.join(run_dir, "motion")
    doc = {"state": state, "run": "r1", "chassis_ref": "testbed/chassis/x",
           "chassis_locked": True, "composition_ready": True,
           "page_scoped_mechanism": None, "sectional_status": sectional,
           "atomic_status": "not-open",
           "user_approvals": {"chassis": "批准", "sectional": None, "atomic_policy": None},
           "state_log": [{"at": "t", "event": "init", "to": "CHASSIS_OPEN", "by": "system", "evidence": "e"}]}
    doc.update(over)
    _write(os.path.join(motion, "pipeline-state.json"), doc)
    return run_dir, motion


def _mk_resolution(run_dir, mech="motion-pool:#15", state="SECTIONAL_OPEN"):
    _write(os.path.join(run_dir, "motion", "resolutions", "s1.json"),
           {"resolver_version": 1, "input_digest": "sha256:abc", "phase": "sectional",
            "pipeline_state": state,
            "eligible": [{"id": mech, "effective_footprint": "sectional",
                          "fit_reason": "t", "warnings": [], "conditions": []}],
            "excluded": []})
    _write(os.path.join(run_dir, "motion", "sectional-score.json"),
           {"approach": {"sectional_score": {"target": "approach", "mechanism": mech,
                                             "carrier": "local-pinned-stage", "driver": "scroll",
                                             "fallback": "static-sequence",
                                             "resolution_record": "motion/resolutions/s1.json"}}})


def test_preflight_base_wave(tmp):
    _, motion = _mk_motion(tmp)
    code, out = run(PREFLIGHT, "--motion-dir", motion, "--stage", "base-wave")
    expect("preflight: base-wave green at SECTIONAL_LOCKED (skipped)", code, out, 0, ["PREFLIGHT OK"])

    _, motion = _mk_motion(os.path.join(tmp, "b"), state="SECTIONAL_OPEN", sectional="pending")
    code, out = run(PREFLIGHT, "--motion-dir", motion, "--stage", "base-wave")
    expect("preflight: base-wave blocked before SECTIONAL_LOCKED", code, out, 1,
           ["BLOCK", "SECTIONAL_LOCKED"])

    run_dir, motion = _mk_motion(os.path.join(tmp, "c"), sectional="selected",
                                 user_approvals={"chassis": "批准", "sectional": "就用15",
                                                 "atomic_policy": None})
    code, out = run(PREFLIGHT, "--motion-dir", motion, "--stage", "base-wave")
    expect("preflight: selected without sectional-score.json blocked", code, out, 1, ["BLOCK"])

    _mk_resolution(run_dir)
    code, out = run(PREFLIGHT, "--motion-dir", motion, "--stage", "base-wave")
    expect("preflight: selected + valid resolution record green", code, out, 0, ["PREFLIGHT OK"])

    _mk_resolution(run_dir, state="CHASSIS_OPEN")
    code, out = run(PREFLIGHT, "--motion-dir", motion, "--stage", "base-wave")
    expect("preflight: stale resolution record (matrix 8) blocked", code, out, 1, ["stale"])

    _mk_resolution(run_dir)
    ss = os.path.join(run_dir, "motion", "sectional-score.json")
    doc = json.load(open(ss, encoding="utf-8"))
    doc["approach"]["sectional_score"]["mechanism"] = "threed-pool:C-29"
    _write(ss, doc)
    code, out = run(PREFLIGHT, "--motion-dir", motion, "--stage", "base-wave")
    expect("preflight: tampered mechanism (matrix 8) blocked", code, out, 1, ["tampered"])

    # component tier (contracts §6, user-relax 2026-07-18): component entries
    # need valid resolution records at spawn exactly like the primary
    _mk_resolution(run_dir)
    doc = json.load(open(ss, encoding="utf-8"))
    doc["approach"]["component_scores"] = [
        {"target": "terms", "mechanism": "motion-pool:#15", "carrier": "bento-card-wall",
         "driver": "click", "fallback": "static-cards",
         "resolution_record": "motion/resolutions/s1.json"}]
    _write(ss, doc)
    code, out = run(PREFLIGHT, "--motion-dir", motion, "--stage", "base-wave")
    expect("preflight: component entry + valid resolution record green", code, out, 0,
           ["PREFLIGHT OK"])

    doc["approach"]["component_scores"] = [
        {"target": "terms", "mechanism": "motion-pool:#15", "carrier": "bento-card-wall",
         "driver": "click", "fallback": "static-cards"}]
    _write(ss, doc)
    code, out = run(PREFLIGHT, "--motion-dir", motion, "--stage", "base-wave")
    expect("preflight: component entry without resolution record blocked", code, out, 1,
           ["component[approach#0]", "mechanism/resolution_record missing"])

    code, out = run(PREFLIGHT, "--motion-dir", os.path.join(tmp, "nope", "motion"), "--stage", "base-wave")
    expect("preflight: legacy run (no state file) passes as LEGACY (matrix 9 compat)", code, out, 0, ["LEGACY"])


def test_preflight_atomic(tmp):
    run_dir, motion = _mk_motion(tmp, state="ATOMIC_OPEN", sectional="skipped",
                                 atomic_status="policy-approved",
                                 user_approvals={"chassis": "批准", "sectional": None,
                                                 "atomic_policy": "预算3个,ok"})
    _write(os.path.join(motion, "atomic-policy.json"),
           {"atomic_policy": {"enabled": True, "max_targets": 3,
                              "allowed_properties": ["transform", "opacity"],
                              "allow_overlay_canvas": False, "no_reflow": True,
                              "performance_budget": "light"}})
    code, out = run(PREFLIGHT, "--motion-dir", motion, "--stage", "atomic")
    expect("preflight: atomic green at ATOMIC_OPEN", code, out, 0, ["PREFLIGHT OK"])

    _, motion = _mk_motion(os.path.join(tmp, "b"), state="BASE_WAVE_READY", sectional="skipped")
    code, out = run(PREFLIGHT, "--motion-dir", motion, "--stage", "atomic")
    expect("preflight: atomic blocked before ATOMIC_OPEN (matrix 10)", code, out, 1,
           ["BLOCK", "ATOMIC_OPEN"])


def _mk_atomic_fixture(tmp, after_extra="", n_effects=1, layout=None, with_diff=True):
    os.makedirs(tmp, exist_ok=True)
    before = "<html><body>\n<section>\n<div class=\"card\">x</div>\n</section>\n</body></html>\n"
    after = before.replace("<div class=\"card\">x</div>",
                           "<div class=\"card\" data-atomic=\"1\">x</div>" + after_extra)
    bp, ap_ = os.path.join(tmp, "before.html"), os.path.join(tmp, "after.html")
    open(bp, "w", encoding="utf-8").write(before)
    open(ap_, "w", encoding="utf-8").write(after)
    effects = [{"target": ".card", "mechanism": "motion-pool:#8",
                "resolution_record": "motion/resolutions/a1.json"}][:1] * n_effects
    res = os.path.join(tmp, "atomic-result-s.json")
    _write(res, {"atomic_result": {"surface": "s", "effects": effects,
                                   "layout_diff": "pass", "reduced_motion": "pass"}})
    pol = os.path.join(tmp, "atomic-policy.json")
    _write(pol, {"atomic_policy": {"enabled": True, "max_targets": 1,
                                   "allowed_properties": ["transform", "opacity"],
                                   "allow_overlay_canvas": False, "no_reflow": True,
                                   "performance_budget": "light"}})
    args = ["--result", res, "--policy", pol, "--before", bp, "--after", ap_]
    if with_diff:
        diff = os.path.join(tmp, "layout-diff.json")
        _write(diff, {"tolerance_px": 0.5,
                      "rects": {".card": {"before": [0, 0, 100, 40],
                                          "after": layout or [0, 0, 100, 40]}}})
        args += ["--layout-diff", diff]
    return args


def test_atomic_checker(tmp):
    code, out = run(ATOMIC, *_mk_atomic_fixture(tmp))
    expect("atomic: benign attribute patch + zero drift green", code, out, 0, ["ATOMIC OK"])

    code, out = run(ATOMIC, *_mk_atomic_fixture(os.path.join(tmp, "b"),
                                                after_extra="\n<style>.card{position: sticky}</style>"))
    expect("atomic: position:sticky addition blocked", code, out, 1, ["position:sticky"])

    code, out = run(ATOMIC, *_mk_atomic_fixture(os.path.join(tmp, "c"),
                                                after_extra="\n<section>new</section>"))
    expect("atomic: structural tag addition blocked", code, out, 1, ["structural tag count"])

    code, out = run(ATOMIC, *_mk_atomic_fixture(os.path.join(tmp, "d"), layout=[0, 5, 100, 40]))
    expect("atomic: layout drift blocked (matrix 11)", code, out, 1,
           ["layout drift", "REVERT"])

    code, out = run(ATOMIC, *_mk_atomic_fixture(os.path.join(tmp, "e"), n_effects=2))
    expect("atomic: max_targets exceeded blocked", code, out, 1, ["exceed"])

    code, out = run(ATOMIC, *_mk_atomic_fixture(os.path.join(tmp, "f"), with_diff=False))
    expect("atomic: pass claim without layout evidence blocked", code, out, 1,
           ["no --layout-diff evidence"])


def _run_hook(tmp, prompt):
    env = dict(os.environ, CLAUDE_PROJECT_DIR=tmp, PYTHONIOENCODING="utf-8")
    r = subprocess.run([NODE, HOOK], capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=env,
                       input=json.dumps({"tool_name": "Agent", "tool_input": {"prompt": prompt}}))
    return r.returncode, r.stdout + r.stderr


def _mk_sentinel(tmp):
    _write(os.path.join(tmp, ".goals", "pipeline-gate.json"),
           {"gate": "anchor-wave", "run": "r1", "proposed": "wave",
            "user_approval": "批准 跑", "approved_at": datetime.now(timezone.utc).isoformat(),
            "ttl_seconds": 14400})


def test_hook_motion_gate(tmp):
    if not NODE:
        print("ok   hook: SKIPPED (node not on PATH)")
        return
    run_dir, _ = _mk_motion(tmp)
    _mk_sentinel(tmp)
    wave_prompt = f"surface-authoring subagent for x — write {run_dir}/wave/x/index.html"
    code, out = _run_hook(tmp, wave_prompt)
    expect("hook: wave allowed at SECTIONAL_LOCKED + sentinel", code, out, 0, [])

    run_dir2, _ = _mk_motion(os.path.join(tmp, "b"), state="CHASSIS_LOCKED", sectional="not-open")
    _mk_sentinel(os.path.join(tmp, "b"))
    code, out = _run_hook(os.path.join(tmp, "b"),
                          f"surface-authoring subagent for x — write {run_dir2}/wave/x/index.html")
    expect("hook: wave blocked when sectional undecided", code, out, 2, ["SECTIONAL"])

    legacy = os.path.join(tmp, "c")
    os.makedirs(legacy, exist_ok=True)
    _mk_sentinel(legacy)
    code, out = _run_hook(legacy, "surface-authoring subagent for x — write out/x/index.html")
    expect("hook: legacy wave (no motion state) unchanged", code, out, 0, [])

    nos = os.path.join(tmp, "d")
    os.makedirs(nos, exist_ok=True)
    code, out = _run_hook(nos, "surface-authoring subagent for x — write out/x/index.html")
    expect("hook: wave without sentinel still blocked (original teeth intact)", code, out, 2,
           ["pipeline-gate.json"])

    run_dir3, _ = _mk_motion(os.path.join(tmp, "e"), state="ATOMIC_OPEN", sectional="skipped",
                             atomic_status="policy-approved",
                             user_approvals={"chassis": "批准", "sectional": None,
                                             "atomic_policy": "预算ok"})
    code, out = _run_hook(os.path.join(tmp, "e"),
                          f"atomic-patch subagent for x — patch {run_dir3}/wave/x/index.html")
    expect("hook: atomic allowed at ATOMIC_OPEN", code, out, 0, [])

    run_dir4, _ = _mk_motion(os.path.join(tmp, "f"), state="BASE_WAVE_READY", sectional="skipped")
    code, out = _run_hook(os.path.join(tmp, "f"),
                          f"atomic-patch subagent for x — patch {run_dir4}/wave/x/index.html")
    expect("hook: atomic blocked before ATOMIC_OPEN (matrix 10)", code, out, 2, ["ATOMIC_OPEN"])

    code, out = _run_hook(os.path.join(tmp, "g"), "atomic-patch subagent for x — patch out/x/index.html")
    expect("hook: atomic without discoverable state blocked", code, out, 2, ["no motion"])


TESTS = [
    test_wire_basic,
    test_wire_mock_class,
    test_wire_mock_inner_badge,
    test_wire_mock_inner_badge_gated,
    test_wire_escalate,
    test_wire_broken_check,
    test_wire_fragment_check,
    test_verbatim_import,
    test_verbatim_verify_ok,
    test_verbatim_verify_content,
    test_verbatim_verify_asset_differ,
    test_verbatim_verify_asset_missing,
    test_preflight_base_wave,
    test_preflight_atomic,
    test_atomic_checker,
    test_hook_motion_gate,
]


def main():
    for t in TESTS:
        with tempfile.TemporaryDirectory() as tmp:
            t(tmp)
    print("---")
    if failures:
        print("%d failure(s)" % len(failures))
        return 1
    print("all green (%d test functions)" % len(TESTS))
    return 0


if __name__ == "__main__":
    sys.exit(main())
