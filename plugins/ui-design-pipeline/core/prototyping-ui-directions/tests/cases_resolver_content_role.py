#!/usr/bin/env python3
"""Content-role pre-filter cases for run_tests.py (Job 2a).

Exercises the OPTIONAL `content_shape` upstream stage of resolve_candidates.py
against a HERMETIC fixture registry + fixture material manifests (fx-bento /
fx-gallery / fx-decor) — NOT the concurrently-mutating real library. Pins:

  * OFF path adds no content-role keys (inert when content_shape absent)
  * DISCOVERY surfaces only role hosts, cleanest-first
  * ①buildability FAIL -> CONTENT_ROLE_UNFIT; decorative -> CONTENT_ROLE_NOT_HOSTED
  * survivors STILL run the mechanical chain (two levels, not a replacement)
  * native_hint is always emitted; flags when native likely WINS
  * content_shape structural validation errors are exit-1 input errors

The real-library reproduction of the pilot's 3 examples is a LIVE check run by
the parent (real content_roles drift), not pinned here.
"""
from __future__ import annotations

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
RESOLVE = os.path.join(HERE, "..", "scripts", "resolve_candidates.py")

SECTION_CARRIER = {
    "owner_scope": "section", "bounded_container": True, "local_progress": "0..1",
    "releases_on_exit": True, "persistent_stage_scope": "section",
    "top_level_siblings_depend": False, "global_side_effects": [],
}
# a discovered candidate whose eligible list is non-empty renders as:  "eligible": [\n    {
NONEMPTY_ELIGIBLE = '"eligible": [\n    {'


def _inp(**kw) -> str:
    base = {"phase": "sectional", "pipeline_state": "SECTIONAL_OPEN", "chassis_stage": None,
            "register": None, "carrier": SECTION_CARRIER, "perf_budget": "heavy",
            "occupied_drivers": []}
    base.update(kw)
    return json.dumps(base, ensure_ascii=False)


def run_resolver_content_role_cases(run, expect, fix_dir: str) -> None:
    reg = os.path.join(fix_dir, "registry", "content-role.json")
    matroot = os.path.join(fix_dir, "material")

    def rz(stdin: str):
        return run(RESOLVE, "--input", "-", "--registry", reg, "--material-root", matroot, stdin=stdin)

    # OFF: content_shape absent -> the pre-filter is a total no-op, no new keys.
    code, out = rz(_inp(candidate_ids=["motion-pool:#1"]))
    expect("content-role: OFF path adds no content-role keys (inert)", code, out, 0,
           ['"id": "motion-pool:#1"'],
           forbid=["content_shape", "native_hint", "content_role", "CONTENT_ROLE"])

    # DISCOVERY comparison: only the comparison host (fx-bento) surfaces; the
    # collection-only gallery is never discovered; native stays a fallback.
    code, out = rz(_inp(content_shape={"role": "comparison", "items": 3, "density": "sparse"}))
    expect("content-role: discovery comparison surfaces only the comparison host", code, out, 0,
           ['"id": "motion-pool:#1"', '"content_role"', '"native_hint"', "永远备选"],
           forbid=['"id": "motion-pool:#2"'])

    # DISCOVERY comparison, over the item ceiling + dense -> UNFIT, native WINS.
    code, out = rz(_inp(content_shape={"role": "comparison", "items": 12, "density": "dense"}))
    expect("content-role: 12 dense items overflow the comparison host -> UNFIT + native wins",
           code, out, 0,
           ["CONTENT_ROLE_UNFIT", "件数溢出", "native 原生表"],
           forbid=[NONEMPTY_ELIGIBLE])

    # DISCOVERY collection: all three hosts eligible, CLEANEST FIRST (0-break
    # gallery #2 and legacy #4 by id, then 1-break bento #1).
    code, out = rz(_inp(content_shape={"role": "collection", "items": 5, "density": "card-rich"}))
    ids = []
    try:
        ids = [e["id"] for e in json.loads(out)["eligible"]]
    except Exception:  # noqa: BLE001
        pass
    order_ok = ids == ["motion-pool:#2", "motion-pool:#4", "motion-pool:#1"]
    expect("content-role: collection discovery is cleanest-first (gallery/legacy before bento)",
           code if order_ok else 1, out, 0,
           ['"id": "motion-pool:#2"', '"id": "motion-pool:#1"'])

    # FILTER mode: an explicit decorative candidate (content_roles=null) -> NOT_HOSTED.
    code, out = rz(_inp(content_shape={"role": "collection", "items": 5, "density": "card-rich"},
                        candidate_ids=["motion-pool:#3"]))
    expect("content-role: filter mode excludes a decorative material (null roles)", code, out, 0,
           ["CONTENT_ROLE_NOT_HOSTED"], forbid=[NONEMPTY_ELIGIBLE])

    # TWO LEVELS: a material that PASSES the content-role gate still runs the
    # mechanical chain — gallery (driver pointer) is knocked out by an occupied
    # pointer driver while bento (driver click) survives.
    code, out = rz(_inp(content_shape={"role": "collection", "items": 5, "density": "card-rich"},
                        occupied_drivers=["pointer"]))
    expect("content-role: survivors still run the mechanical chain (driver conflict downstream)",
           code, out, 0, ["DRIVER_CONFLICT", '"id": "motion-pool:#1"'])

    # native 铁律: a role nothing hosts -> empty eligible + native-wins hint (role=spec wins).
    code, out = rz(_inp(content_shape={"role": "spec", "items": 5, "density": "sparse"}))
    expect("content-role: unhosted role yields native-wins hint + empty eligible", code, out, 0,
           ["native 原生表"], forbid=[NONEMPTY_ELIGIBLE])

    # content_shape structural validation -> exit-1 input errors.
    code, out = rz(_inp(content_shape={"role": "collection", "items": 0, "density": "card"}))
    expect("content-role: items must be a positive integer", code, out, 1, ["content_shape.items"])
    code, out = rz(_inp(content_shape={"role": "", "items": 5, "density": "card"}))
    expect("content-role: role must be a non-empty string", code, out, 1, ["content_shape.role"])

    # ---- affordance axes (require; contracts §3.1, added 2026-08-01) --------

    def shape(**req):
        s = {"role": "collection", "items": 5, "density": "card-rich"}
        if req:
            s["require"] = req
        return s

    # require.viewing: the gallery user's need — bento (viewing=all) excluded
    # with a readable reason; one-at-a-time gallery survives + echoes affordances.
    code, out = rz(_inp(content_shape=shape(viewing=["one-at-a-time", "several"])))
    expect("affordance: viewing require excludes the all-visible host (bento)", code, out, 0,
           ["CONTENT_AFFORDANCE_MISMATCH", "viewing=all", '"id": "motion-pool:#2"', '"affordances"'],
           forbid=['"eligible": [\n    {\n      "id": "motion-pool:#1"'])

    # require.composition: text-only content — captioned-only gallery excluded,
    # bento (hosts all three) survives.
    code, out = rz(_inp(content_shape=shape(composition=["text-only"])))
    expect("affordance: composition require excludes the captioned-only gallery", code, out, 0,
           ["CONTENT_AFFORDANCE_MISMATCH", "composition 缺", '"id": "motion-pool:#1"'])

    # backward compat: NO require -> untagged fx-legacy stays eligible and no
    # affordance keys appear anywhere (pre-axes output shape).
    code, out = rz(_inp(content_shape=shape()))
    expect("affordance: no require -> untagged piece eligible, no affordance keys", code, out, 0,
           ['"id": "motion-pool:#4"'], forbid=["CONTENT_AFFORDANCE", '"affordances"'])

    # a require naming an axis a piece never declared excludes THAT piece only.
    code, out = rz(_inp(content_shape=shape(viewing=["one-at-a-time"]),
                        candidate_ids=["motion-pool:#4"]))
    expect("affordance: require on an undeclared axis excludes the legacy piece", code, out, 0,
           ["CONTENT_AFFORDANCE_MISMATCH", "未声明"], forbid=[NONEMPTY_ELIGIBLE])

    # vocab enforcement: unknown require value / unknown axis = input errors.
    code, out = rz(_inp(content_shape=shape(viewing=["fullscreen"])))
    expect("affordance: unknown viewing value is an input error", code, out, 1,
           ["content_shape.require.viewing", "unknown value"])
    code, out = rz(_inp(content_shape=shape(layout=["grid"])))
    expect("affordance: unknown require axis is an input error", code, out, 1,
           ["unknown axis"])
