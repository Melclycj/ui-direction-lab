#!/usr/bin/env python3
"""check_registry_sync.py — coverage/sync gate between the pools and the
execution registry (execution-contracts.md §2 source-of-truth discipline).

Asserts, deterministically:
  1. registry parses + passes registry_lib.validate_records (enums, duplicate
     ids, preferred∈supported, fallback present, zero-guessing guard...).
  2. every covered pool row  <->  exactly one registry record (both directions):
       - threed-pool rows keyed `C-NN` (incl. merged `C-20/21`)
       - motion-pool numbered rows keyed `#N`
       - unnumbered rows keyed by their badge slug 【⚙执行册=<slug>】
  3. every covered pool row carries the compact execution badge 【⚙执行册…】.
  4. every record with a `material` path resolves to a real
     `<repo>/<material>/index.html`.

Exit 0 = in sync; exit 1 = problems (each printed as `PROBLEM: ...`).

Usage:
    python check_registry_sync.py [--registry P] [--threed-pool P]
        [--motion-pool P] [--repo-root P]

No third-party dependencies. Python 3.10+.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import registry_lib  # noqa: E402

BADGE_RE = re.compile(r"【⚙执行册(?:=([a-z0-9-]+))?】")
THREED_ROW_RE = re.compile(r"^\|\s*(C-\d+(?:/\d+)?)")
MOTION_ROW_RE = re.compile(r"^\|\s*(\d{1,2})\s*\|")


def parse_pool(path: Path, pool: str) -> tuple[set[str], list[str]]:
    """Return (covered ids, problems) for one pool file."""
    ids: set[str] = set()
    problems: list[str] = []
    text = path.read_text(encoding="utf-8")
    for i, line in enumerate(text.splitlines(), 1):
        row_key = None
        if pool == "threed-pool":
            m = THREED_ROW_RE.match(line)
            if m:
                row_key = m.group(1)
        else:
            m = MOTION_ROW_RE.match(line)
            if m:
                row_key = "#" + m.group(1)
        badge = BADGE_RE.search(line)
        if row_key:
            ids.add(f"{pool}:{row_key}")
            if not badge:
                problems.append(f"{pool} row {row_key} (line {i}) missing execution badge")
        if badge and badge.group(1):
            ids.add(f"{pool}:{badge.group(1)}")
    return ids, problems


def find_installed_corpus(here: Path):
    """Locate an installed ui-material-library, returning (path, how_it_was_found).

    The two packages are siblings once installed: Claude Code lays plugins out as
    <plugins>/cache/<marketplace>/<plugin>/<version>/, so from this script inside
    ui-design-pipeline the corpus is reachable without anyone passing a path. Two
    ways, most authoritative first.

    Both read INTERNAL layout that is not a promised interface, which is why
    --material-root exists and always wins: this is a convenience, never the
    contract. Returning None is a normal outcome, not an error.
    """
    plugins_dir = None
    for cand in here.parents:
        if cand.name == "cache" and cand.parent.name == "plugins":
            plugins_dir = cand.parent
            break
    if plugins_dir is None:
        return None, ""

    # 1) the installed-plugins record, which stores installPath outright.
    record = plugins_dir / "installed_plugins.json"
    if record.is_file():
        try:
            doc = json.loads(record.read_text(encoding="utf-8"))
            for key, entries in (doc.get("plugins") or {}).items():
                if not key.startswith("ui-material-library@"):
                    continue
                for entry in entries or []:
                    p = entry.get("installPath")
                    if p and (Path(p) / "material").is_dir():
                        return Path(p) / "material", "installed_plugins.json"
        except Exception:
            pass  # malformed or a changed schema: fall through to the walk

    # 2) walk the sibling layout directly. The version segment is not always a
    #    semver — an installed plugin can carry the literal "unknown" — so it is
    #    listed rather than guessed, and the NEWEST is taken by modification
    #    time rather than by name: an update leaves the previous version dir in
    #    the cache, so name order would hand back the stale corpus.
    base = plugins_dir / "cache" / "ui-material-library" / "ui-material-library"
    if base.is_dir():
        found = [d / "material" for d in base.iterdir() if (d / "material").is_dir()]
        if found:
            newest = max(found, key=lambda p: p.parent.stat().st_mtime)
            return newest, f"sibling plugin layout ({newest.parent.name})"
    return None, ""


def main() -> int:
    here = Path(__file__).resolve().parent
    refs = here.parent / "references"
    # The material corpus is LAB-ONLY: it is not shipped with the installed
    # plugin. Walk up looking for it instead of assuming a fixed depth, so the
    # same script works from the lab checkout and from a plugin install. When
    # it is absent the material-path check is SKIPPED and said so out loud —
    # never silently counted as passing.
    default_repo = ""
    for cand in here.parents:
        if (cand / "testbed" / "material").is_dir():
            default_repo = str(cand)
            break

    ap = argparse.ArgumentParser()
    ap.add_argument("--registry", default=str(refs / "execution-registry.json"))
    ap.add_argument("--threed-pool", default=str(refs / "threed-pool.md"))
    ap.add_argument("--motion-pool", default=str(refs / "motion-pool.md"))
    ap.add_argument("--repo-root", default=str(default_repo))
    # The material corpus ships as its OWN plugin (ui-material-library), so when
    # both are installed it does not sit under this repo at all. Point at it and
    # the same path check runs against the installed copy; leave it unset and the
    # behaviour is exactly what it was — verified in the lab, SKIPPED elsewhere.
    # There is no cross-plugin path resolution to infer here, so it is explicit.
    ap.add_argument("--material-root", default=os.environ.get("UI_MATERIAL_ROOT", ""),
                    help="directory holding the material pieces as <root>/<slug>/index.html")
    args = ap.parse_args()

    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
    except Exception:
        pass

    problems: list[str] = []

    # 1) registry shape
    try:
        records = registry_lib.load_registry(args.registry)
    except Exception as exc:  # noqa: BLE001 — surface parse errors as gate output
        print(f"PROBLEM: registry unreadable: {exc}")
        print("FAIL (1 problem)")
        return 1
    problems += registry_lib.validate_records(records)

    reg_ids = [r.get("id") for r in records]
    reg_id_set = set(reg_ids)

    # 2) pool coverage, both directions
    pool_ids: set[str] = set()
    for path, pool in ((Path(args.threed_pool), "threed-pool"),
                       (Path(args.motion_pool), "motion-pool")):
        if not path.exists():
            problems.append(f"pool file missing: {path}")
            continue
        ids, pool_problems = parse_pool(path, pool)
        pool_ids |= ids
        problems += pool_problems

    for missing in sorted(pool_ids - reg_id_set):
        problems.append(f"pool row {missing} has no registry record")
    for orphan in sorted(reg_id_set - pool_ids):
        problems.append(f"registry record {orphan} resolves to no pool row")

    # 4) material paths (lab-only; see default_repo above)
    checked = 0
    found_how = "--material-root"
    mat_root = Path(args.material_root) if args.material_root else None
    if mat_root is not None and not mat_root.is_dir():
        # An explicit path that does not exist is a mistake worth surfacing, never a
        # reason to quietly fall back to skipping.
        problems.append(f"--material-root does not exist: {mat_root}")
        mat_root = None
        material_scope = False
    elif mat_root is not None:
        material_scope = True
    elif bool(args.repo_root) and (Path(args.repo_root) / "testbed" / "material").is_dir():
        material_scope = True
    else:
        mat_root, found_how = find_installed_corpus(Path(__file__).resolve())
        material_scope = mat_root is not None
    if material_scope:
        repo = Path(args.repo_root)
        for rec in records:
            mat = rec.get("material")
            if not mat:
                continue
            checked += 1
            # --material-root addresses pieces by slug; the in-repo layout keeps the
            # registry's own relative path. Same check, two possible homes.
            target = (mat_root / Path(mat).name) if mat_root else (repo / mat)
            if not (target / "index.html").exists():
                # Report the registry's own relative path: that is what a reader
                # checks the registry against. Where it actually looked is added
                # only when that is not derivable from the registry entry.
                where = f" (looked in {target})" if mat_root else ""
                problems.append(
                    f"{rec.get('id')}: material path not found: {mat}/index.html{where}")

    if problems:
        for p in problems:
            print(f"PROBLEM: {p}")
        print(f"FAIL ({len(problems)} problem{'s' if len(problems) != 1 else ''})")
        return 1

    if material_scope and mat_root is not None:
        material_note = f"material paths verified ({checked}) against {mat_root} (found via {found_how})"
    elif material_scope:
        material_note = f"material paths verified ({checked})"
    else:
        material_note = ("material paths SKIPPED (no material corpus in scope — pass "
                         "--material-root or UI_MATERIAL_ROOT if ui-material-library is installed)")
    print(f"OK registry sync: {len(reg_ids)} records == {len(pool_ids)} covered pool rows; "
          f"badges present; {material_note}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
