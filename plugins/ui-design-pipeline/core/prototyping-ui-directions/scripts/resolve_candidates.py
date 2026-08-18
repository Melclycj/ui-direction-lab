#!/usr/bin/env python3
"""resolve_candidates.py — deterministic upstream candidate resolver.

Runs BEFORE candidate cards are written, in every phase (chassis / sectional /
atomic). Computes each candidate's EFFECTIVE footprint from the registry record
x the proposed deployment, walks the filter chain, and emits reason-coded
eligible/excluded JSON. The candidate gallery may show ONLY `eligible`;
excluded entries never become selectable cards.

Contract: ../references/execution-contracts.md §3 (input/output shapes,
effective-footprint rules, filter-chain order). Enums: registry_lib.py.

Usage:
    python resolve_candidates.py --input <input.json | -> \
        [--registry <execution-registry.json>] [--out <resolution.json>]

Exit 0 = resolution produced (exclusions are DATA, not errors).
Exit 1 = contract/input error (bad JSON, unknown candidate id, bad phase...).

No third-party dependencies. Python 3.10+.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import registry_lib  # noqa: E402

RESOLVER_VERSION = 1

STATES = ("CHASSIS_OPEN", "CHASSIS_LOCKED", "SECTIONAL_OPEN", "SECTIONAL_LOCKED",
          "BASE_WAVE_READY", "ATOMIC_OPEN", "COMPLETE")
CHASSIS_STAGES = ("batch1-directions", "batch2-tuning")

# --- content-role pre-filter (Job 2a, default OFF) ---------------------------
# Ported in spirit from testbed/material/_harness/suggest-material.js (the pilot
# resolver). This is an OPTIONAL upstream stage: when the input carries no
# "content_shape", NONE of this runs and the output is byte-for-byte identical
# to the pre-2a resolver. It is deterministic — pure functions over manifest
# JSON reached via each registry record's `material` back-ref. It never invents
# candidates or verdicts; native is ALWAYS an option (native_hint below), and a
# human still picks. The mechanical filter chain below is UNCHANGED; surviving
# candidates flow into it exactly as before ("two levels, not a replacement").

def _find_material_root() -> Path:
    """Locate the LAB-ONLY material corpus.

    It is not shipped with the installed plugin, so walk up looking for it
    rather than assuming a fixed depth: the same script then works from the lab
    checkout and from a plugin install.

    When absent this returns a path that does not exist. Callers that do NOT
    pass `content_shape` (the pre-filter is optional and default OFF) never
    touch it and are unaffected. Callers that DO pass one are refused with an
    explicit INPUT ERROR in main() — never handed a silently empty candidate
    set, which would read as "no material fits" instead of "no material here".
    """
    here = Path(__file__).resolve().parent
    for cand in here.parents:
        mat = cand / "testbed" / "material"
        if mat.is_dir():
            return mat
    return here.parents[2] / "testbed" / "material"  # non-existent; documented no-op


CONTENT_ROLE_DIR_DEFAULT = _find_material_root()

# Affordance axes (controlled vocab; source of truth: testbed/material/content-roles.md
# Layer B — locked 2026-08-01, user-ruled "complete per axis, no open-ended vocabulary").
VIEWING_VOCAB = {"one-at-a-time", "several", "all"}
COMPOSITION_VOCAB = {"image-only", "text-only", "captioned-image"}


def _parse_items(spec: str) -> tuple[int, float]:
    """fit.items string -> (min, max). Mirrors suggest-material.js parseItems."""
    s = str(spec)
    m = re.search(r"(\d+)\s*[-–]\s*(\d+)", s)
    if m:
        return (int(m.group(1)), int(m.group(2)))
    m = re.search(r"(\d+)\s*[-–]\s*N", s, re.IGNORECASE)
    if m:
        return (int(m.group(1)), math.inf)
    m = re.search(r"~\s*(\d+)", s)
    if m:
        n = int(m.group(1))
        return (math.ceil(n * 0.6), math.ceil(n * 1.6))
    m = re.search(r"(\d+)", s)
    if m:
        return (int(m.group(1)), int(m.group(1)))
    return (2, math.inf)


def _dense_capable(density: str) -> bool:
    return bool(re.search(r"cell|dense|键值", str(density)))


def _content_buildability(shape: dict, role_spec: dict) -> tuple[bool, list[str]]:
    """①buildability: block(items, density) vs a material's by_role[role].fit."""
    fit = role_spec.get("fit") or {}
    lo, hi = _parse_items(fit.get("items", ""))
    reasons: list[str] = []
    ok = True
    items = shape["items"]
    if items > hi:
        ok = False
        reasons.append(f"件数溢出({items} > 上限 {'∞' if hi == math.inf else hi})")
    if items < lo:
        ok = False
        reasons.append(f"件数不足({items} < 下限 {lo})")
    if shape.get("density") == "dense" and not _dense_capable(fit.get("density", "")):
        ok = False
        reasons.append(f"密度不合(内容稠密, 素材 fit.density={fit.get('density')} 装不下多字段)")
    return ok, reasons


def _content_advisories(role_spec: dict) -> list[str]:
    """Advisory flags pulled from the role's requires/breaks text (non-blocking)."""
    t = json.dumps(role_spec, ensure_ascii=False)
    a: list[str] = []
    if "独占页面滚动" in t:
        a.append("独占页面滚动(与其它滚动编排冲突,mid-page 慎用)")
    if "无 reduced-motion" in t or "a11y 缺口" in t:
        a.append("a11y 缺口(无 reduced-motion,需补)")
    if "aria" in t or "a11y 底线" in t or "<button>" in t:
        a.append("要补真 <button>+aria")
    return a


def native_hint(shape: dict) -> str:
    """The native 铁律: native is ALWAYS an option; flag when it likely wins."""
    role, items, density = shape.get("role"), shape.get("items", 0), shape.get("density")
    wins = density == "dense" or (role == "comparison" and items > 8) or role == "spec"
    return ("native 原生表 — 这块很可能 native 赢(稠密/大对比,素材会破坏可读性或并排比)"
            if wins else
            "native 原生渲染 — 永远备选(素材没挣到位置就用它)")


def load_content_roles(material_root: Path, material_ref: str | None) -> dict | None:
    """Read a material's content_roles via its registry `material` back-ref.
    Returns the hosting block ({hosts, by_role}); None when the material is
    absent / unparseable / decorative (null) / not-yet-tagged (no key)."""
    if not material_ref:
        return None
    mf = material_root / Path(material_ref).name / "manifest.json"
    try:
        m = json.loads(mf.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001 — missing/unparseable manifest = not a host
        return None
    cr = m.get("content_roles")
    if isinstance(cr, dict) and cr.get("hosts"):
        return cr
    return None


def _content_clean_score(shape: dict, role_spec: dict) -> int:
    """Rank key (user ruling 2026-07-26 #3): buildable first, then cleanest
    (fewest breaks + advisories)."""
    ok, _ = _content_buildability(shape, role_spec)
    return (0 if ok else 100) + len(role_spec.get("breaks") or []) + len(_content_advisories(role_spec))


def discover_hosting(records: dict, material_root: Path, shape: dict) -> list[str]:
    """DISCOVERY: every SELECTABLE registry record whose material hosts the role,
    cleanest-first. Deterministic (registry order, then clean-score, then id)."""
    role = shape["role"]
    scored: list[tuple[int, str]] = []
    for rid, rec in records.items():
        if not rec.get("selectable"):
            continue
        cr = load_content_roles(material_root, rec.get("material"))
        if not cr or role not in (cr.get("hosts") or []):
            continue
        scored.append((_content_clean_score(shape, cr["by_role"][role]), rid))
    scored.sort(key=lambda t: (t[0], t[1]))
    return [rid for _, rid in scored]


def validate_content_shape(shape) -> str | None:
    """Structural validation for the optional content_shape input."""
    if not isinstance(shape, dict):
        return "content_shape must be an object {role, items, density}"
    role = shape.get("role")
    if not isinstance(role, str) or not role:
        return "content_shape.role must be a non-empty string"
    items = shape.get("items")
    if not isinstance(items, int) or isinstance(items, bool) or items < 1:
        return "content_shape.items must be a positive integer"
    density = shape.get("density")
    if not isinstance(density, str) or not density:
        return "content_shape.density must be a non-empty string"
    req = shape.get("require")
    if req is not None:
        if not isinstance(req, dict):
            return "content_shape.require must be an object {viewing?, composition?}"
        for axis, vocab in (("viewing", VIEWING_VOCAB), ("composition", COMPOSITION_VOCAB)):
            if axis not in req:
                continue
            vals = req[axis]
            if not isinstance(vals, list) or not vals:
                return f"content_shape.require.{axis} must be a non-empty list"
            bad = [v for v in vals if v not in vocab]
            if bad:
                return f"content_shape.require.{axis} has unknown value(s) {bad}; vocab: {sorted(vocab)}"
        unknown = [k for k in req if k not in ("viewing", "composition")]
        if unknown:
            return f"content_shape.require has unknown axis(es) {unknown}"
    return None


def compute_effective_footprint(carrier: dict, muts: list[str]) -> tuple[str, str]:
    """Contract §3 effective-footprint rules, in order. Returns (footprint, why)."""
    if carrier.get("owner_scope") == "page" or carrier.get("persistent_stage_scope") == "page":
        return "chassis", "page-scoped ownership (owner_scope/persistent_stage_scope=page)"
    if carrier.get("top_level_siblings_depend"):
        return "chassis", "top-level sibling sections depend on one persistent stage/state"
    leaks = carrier.get("global_side_effects") or []
    if leaks:
        return "chassis", f"leaked global side effects: {leaks}"
    forcing = sorted(set(muts) & registry_lib.CHASSIS_FORCING_MUTATIONS)
    if forcing:
        return "chassis", f"mutation forces page ownership: {forcing}"

    owner = carrier.get("owner_scope")
    atomic_ok = bool(muts) and all(m in registry_lib.ATOMIC_SAFE_MUTATIONS for m in muts)
    if owner in ("component", "overlay") and atomic_ok:
        return "atomic", "no-reflow mutations on a component/overlay target"

    bounded = bool(carrier.get("bounded_container")) and bool(carrier.get("releases_on_exit"))
    if owner in ("section", "component", "overlay") and bounded:
        return "sectional", "one bounded owner, releases on exit, no global side effects"

    return "chassis", "owner does not bound/release cleanly -> de facto page ownership"


def resolve_one(rec: dict, inp: dict, proposed_mut_map: dict,
                content_shape: dict | None = None, material_root: Path | None = None) -> dict:
    """Returns {"eligible": {...}} or {"excluded": {...}} for one candidate.

    content_shape / material_root default to None → the content-role pre-filter
    is entirely skipped and this behaves byte-for-byte like the pre-2a resolver.
    """
    rid = rec["id"]
    phase = inp["phase"]
    state = inp["pipeline_state"]

    def excl(reason: str, detail: str) -> dict:
        return {"excluded": {"id": rid, "reason": reason, "detail": detail}}

    # 0) content-role pre-filter (upstream; only when the input opts in)
    cr_block = None
    if content_shape is not None:
        cr = load_content_roles(material_root, rec.get("material"))
        role = content_shape["role"]
        if not cr or role not in (cr.get("hosts") or []):
            return excl("CONTENT_ROLE_NOT_HOSTED", f"material does not host content role {role!r}")
        role_spec = cr["by_role"][role]
        ok, why_cr = _content_buildability(content_shape, role_spec)
        if not ok:
            return excl("CONTENT_ROLE_UNFIT", "; ".join(why_cr))
        # affordance axes (only when the shape carries a `require`; contracts §3.1)
        req = content_shape.get("require") or {}
        aff = role_spec.get("affordances") or {}
        if req:
            if "viewing" in req:
                pv = aff.get("viewing")
                if pv is None:
                    return excl("CONTENT_AFFORDANCE_MISMATCH",
                                "affordances.viewing 未声明(require 点名了该轴)")
                if pv not in req["viewing"]:
                    return excl("CONTENT_AFFORDANCE_MISMATCH",
                                f"viewing={pv} 不在可接受集合 {req['viewing']}")
            if "composition" in req:
                have = aff.get("composition") or []
                missing = [v for v in req["composition"] if v not in have]
                if missing:
                    return excl("CONTENT_AFFORDANCE_MISMATCH",
                                f"composition 缺 {missing}(该件声明 {have or '无'})")
        cr_block = {
            "role": role,
            "preserves": role_spec.get("preserves") or [],
            "breaks": role_spec.get("breaks") or [],
            "notes": _content_advisories(role_spec),
        }
        if req:
            cr_block["affordances"] = aff

    # 1) NOT_SELECTABLE
    if not rec.get("selectable"):
        return excl("NOT_SELECTABLE", f"availability={rec.get('availability')}")

    # 2) PHASE_NOT_ALLOWED
    if phase not in (rec.get("allowed_phases") or []):
        return excl("PHASE_NOT_ALLOWED", f"allowed_phases={rec.get('allowed_phases')}")

    # effective footprint (registry capabilities unless the proposal narrows them)
    muts = proposed_mut_map.get(rid, rec.get("possible_mutations") or [])
    carrier = inp.get("carrier") or {}
    effective, why = compute_effective_footprint(carrier, muts)

    # 3) FOOTPRINT_UNSUPPORTED (no self-lowering / no unsupported promotion)
    if effective not in (rec.get("supported_footprints") or []):
        return excl("FOOTPRINT_UNSUPPORTED",
                    f"computed {effective} ({why}); supported={rec.get('supported_footprints')}")

    # 4) chassis-effective candidates are only ever legal in the still-open chassis phase
    if effective == "chassis":
        if state != "CHASSIS_OPEN" or phase != "chassis":
            return excl("INELIGIBLE_CHASSIS_LOCKED",
                        f"effective footprint chassis ({why}) but state={state}, phase={phase}")
        if inp.get("chassis_stage") == "batch2-tuning":
            return excl("CHASSIS_MECHANISM_IN_TUNING",
                        "Batch-2 tunes the locked vocabulary; it may not introduce a chassis-footprint mechanism")

    # 5) NOT_ATOMIC_SAFE
    if phase == "atomic" and effective != "atomic":
        return excl("NOT_ATOMIC_SAFE", f"computed {effective} ({why}); Atomic Pass patches must not own layout")

    # 6) DRIVER_CONFLICT
    occupied = set(inp.get("occupied_drivers") or [])
    conflict = sorted(set(rec.get("driver") or []) & occupied)
    if conflict:
        return excl("DRIVER_CONFLICT", f"driver(s) {conflict} already occupied")

    # 7) perf budget
    warnings: list[str] = []
    conditions: list[str] = []
    budget = inp.get("perf_budget") or "heavy"
    try:
        over = registry_lib.perf_rank(rec["perf_cost"]) > registry_lib.perf_rank(budget)
    except ValueError:
        return excl("PERF_OVER_BUDGET", f"unknown perf tier: {rec.get('perf_cost')!r} vs budget {budget!r}")
    if over:
        fallback = str(rec.get("fallback") or "").strip()
        if not fallback:
            return excl("MISSING_FALLBACK", f"perf {rec['perf_cost']} > budget {budget} and no fallback declared")
        if not inp.get("accept_fallbacks", True):
            return excl("PERF_OVER_BUDGET", f"perf {rec['perf_cost']} > budget {budget}; fallback not accepted")
        conditions.append(f"fallback-required:{fallback}")

    # boundary evidence warnings (verified for real by downstream validators)
    boundary = rec.get("boundary_requirements") or []
    if "local-progress-0..1" in boundary and not carrier.get("local_progress"):
        warnings.append("boundary requirement local-progress-0..1 not evidenced in the proposal")

    # register affinity is SOFT: warn, never filter (pool consumption contract rule 1)
    register = inp.get("register")
    affinity = rec.get("register_affinity") or []
    if register and affinity and register not in affinity:
        warnings.append(f"register-affinity: {affinity} vs run register '{register}' — human judge")

    fit = f"{why}; perf {rec['perf_cost']} within budget {budget}" if not over else \
          f"{why}; perf {rec['perf_cost']} over budget {budget} — {conditions[-1]}"
    elig = {"id": rid, "effective_footprint": effective, "fit_reason": fit,
            "warnings": warnings, "conditions": conditions}
    if cr_block is not None:
        elig["content_role"] = cr_block
    return {"eligible": elig}


def main() -> int:
    here = Path(__file__).resolve().parent
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True, help="input JSON path, or - for stdin")
    ap.add_argument("--registry", default=str(here.parent / "references" / "execution-registry.json"))
    ap.add_argument("--out", default=None, help="write the resolution record here (evidence file)")
    ap.add_argument("--material-root", default=str(CONTENT_ROLE_DIR_DEFAULT),
                    help="dir holding <slug>/manifest.json (content-role pre-filter source)")
    args = ap.parse_args()

    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
    except Exception:
        pass

    try:
        raw = sys.stdin.read() if args.input == "-" else Path(args.input).read_text(encoding="utf-8")
        inp = json.loads(raw)
    except Exception as exc:  # noqa: BLE001
        print(f"INPUT ERROR: cannot read input JSON: {exc}", file=sys.stderr)
        return 1

    phase = inp.get("phase")
    if phase not in registry_lib.PHASES:
        print(f"INPUT ERROR: phase must be one of {sorted(registry_lib.PHASES)}, got {phase!r}", file=sys.stderr)
        return 1
    state = inp.get("pipeline_state")
    if state not in STATES:
        print(f"INPUT ERROR: pipeline_state must be one of {STATES}, got {state!r}", file=sys.stderr)
        return 1
    if phase == "chassis" and inp.get("chassis_stage") not in CHASSIS_STAGES:
        print(f"INPUT ERROR: phase=chassis requires chassis_stage in {CHASSIS_STAGES}", file=sys.stderr)
        return 1

    content_shape = inp.get("content_shape")
    material_root = Path(args.material_root)
    if content_shape is not None:
        cs_err = validate_content_shape(content_shape)
        if cs_err:
            print(f"INPUT ERROR: {cs_err}", file=sys.stderr)
            return 1

    # candidate_ids stays REQUIRED unless the content-role pre-filter is active,
    # in which case it may DISCOVER hosting materials from the registry.
    explicit_ids = inp.get("candidate_ids")
    if content_shape is None:
        if not isinstance(explicit_ids, list) or not explicit_ids:
            print("INPUT ERROR: candidate_ids must be a non-empty list", file=sys.stderr)
            return 1
    elif explicit_ids is not None and not isinstance(explicit_ids, list):
        print("INPUT ERROR: candidate_ids must be a list when provided", file=sys.stderr)
        return 1

    try:
        records = {r["id"]: r for r in registry_lib.load_registry(args.registry)}
    except Exception as exc:  # noqa: BLE001
        print(f"INPUT ERROR: registry unreadable: {exc}", file=sys.stderr)
        return 1

    if content_shape is not None and not explicit_ids:
        # DISCOVERY reads per-material manifests out of the material corpus. That
        # corpus is LAB-ONLY — absent in a plugin install. Without this guard the
        # run would return an empty candidate set and say nothing, which reads as
        # "no material fits your content" when the truth is "there is no material
        # library here". Refuse loudly instead; the caller can omit content_shape
        # (the pre-filter is optional, default off) or pass --material-root.
        if not material_root.is_dir():
            print(f"INPUT ERROR: content_shape was supplied but no material corpus is in scope "
                  f"(looked for {material_root}). The material library is lab-only and does not "
                  f"ship with the plugin. Omit content_shape to run the resolver without the "
                  f"content-role pre-filter, or pass --material-root at a real corpus.",
                  file=sys.stderr)
            return 1
        cand_ids = discover_hosting(records, material_root, content_shape)
    else:
        cand_ids = explicit_ids
        unknown = [cid for cid in cand_ids if cid not in records]
        if unknown:
            print(f"INPUT ERROR: unknown candidate id(s): {unknown}", file=sys.stderr)
            return 1

    proposed_mut_map = inp.get("proposed_mutations") or {}
    eligible, excluded = [], []
    for cid in cand_ids:
        verdict = resolve_one(records[cid], inp, proposed_mut_map,
                              content_shape=content_shape, material_root=material_root)
        if "eligible" in verdict:
            eligible.append(verdict["eligible"])
        else:
            excluded.append(verdict["excluded"])

    digest = hashlib.sha256(json.dumps(inp, sort_keys=True, ensure_ascii=False).encode("utf-8")).hexdigest()
    out = {
        "resolver_version": RESOLVER_VERSION,
        "input_digest": f"sha256:{digest}",
        "phase": phase,
        "pipeline_state": state,
        "eligible": eligible,
        "excluded": excluded,
    }
    # content-role echo + native 铁律 — appended ONLY when the pre-filter is
    # active, so the default (OFF) output stays byte-for-byte as before.
    if content_shape is not None:
        out["content_shape"] = content_shape
        out["native_hint"] = native_hint(content_shape)
    text = json.dumps(out, indent=2, ensure_ascii=False)
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
