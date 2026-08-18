#!/usr/bin/env python3
"""import_verbatim.py — deterministic import of an already-approved page into a wave.

Backs the `verbatim_source` page provenance (anchor-prototype-wave §Inputs item 2,
§Pipeline stage 2). The locked chassis hero / a surface kept from a previous wave
is APPROVED — it must land in the wave byte-for-byte, never re-authored. A model
doing this by hand can drop a referenced asset or silently edit content (= break
the lock). This script makes the mechanical part deterministic and, via --verify,
turns the "never re-author a verbatim page" anti-pattern into a runnable gate.

Division of labour (deliberate): this script owns the MECHANICAL, high-risk part
(copy + relative-asset resolution + lock-integrity proof). Stamping the copy's
mocked product links with `data-nav-target` stays a model edit — it needs the
semantic link→screen mapping a script cannot judge. --verify tolerates exactly
those additive stamps and nothing else.

Usage:
    python import_verbatim.py --source <approved-dir> --dest <out>/<slug>
        Copy <source>/index.html + every relative asset it references into <dest>.
        Source is READ-ONLY. Does NOT stamp (model does that afterward).

    python import_verbatim.py --source <approved-dir> --dest <out>/<slug> --verify
        Assert <dest> is <source> byte-for-byte EXCEPT for added data-nav-target
        attributes on index.html, and every referenced asset is present + identical.
        Exit 1 on any other difference (= the lock was broken). Run after stamping.
"""

import argparse
import re
import shutil
import sys
from pathlib import Path

for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

# Tags whose href/src point at a copiable asset. <a href> is NOT here — those are
# page navigation (mock/wired links), handled by wire_navigation.py, never copied.
ASSET_TAG_RE = re.compile(r"<(?:link|script|img|source)\b[^>]*>", re.IGNORECASE)
ASSET_URL_RE = re.compile(r"""\b(?:href|src)\s*=\s*(?:"([^"]*)"|'([^']*)')""", re.IGNORECASE)
NAV_TARGET_STRIP_RE = re.compile(r"""\s*data-nav-target\s*=\s*(?:"[^"]*"|'[^']*')""")

_SKIP_PREFIXES = ("http://", "https://", "//", "data:", "#", "mailto:", "tel:", "javascript:", "/")


def is_relative_asset(url: str) -> bool:
    url = url.strip()
    if not url:
        return False
    return not url.lower().startswith(_SKIP_PREFIXES)


def find_relative_assets(html: str):
    """Relative asset paths referenced by index.html, in first-seen order."""
    seen = []
    for tag in ASSET_TAG_RE.findall(html):
        for m in ASSET_URL_RE.finditer(tag):
            url = m.group(1) if m.group(1) is not None else m.group(2)
            if is_relative_asset(url) and url not in seen:
                seen.append(url)
    return seen


def read_bytes(path: Path) -> bytes:
    with open(path, "rb") as fh:
        return fh.read()


def read_text_exact(path: Path) -> str:
    # newline="" + utf-8 so comparison is byte-exact modulo the utf-8 round-trip
    with open(path, "r", encoding="utf-8", newline="") as fh:
        return fh.read()


def strip_nav_targets(html: str) -> str:
    return NAV_TARGET_STRIP_RE.sub("", html)


def cmd_import(source: Path, dest: Path) -> int:
    src_index = source / "index.html"
    if not src_index.is_file():
        print(f"ERROR: no index.html in source {source}")
        return 1
    html = read_text_exact(src_index)
    assets = find_relative_assets(html)

    dest.mkdir(parents=True, exist_ok=True)
    if (dest / "index.html").exists():
        print(f"NOTE: {dest}/index.html exists — overwriting with verbatim source copy")
    shutil.copy2(src_index, dest / "index.html")

    copied, missing = [], []
    for rel in assets:
        src_asset = source / rel
        if not src_asset.is_file():
            missing.append(rel)
            continue
        dst_asset = dest / rel
        dst_asset.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_asset, dst_asset)
        copied.append(rel)

    print(f"imported {source.name} -> {dest}")
    print(f"  index.html + {len(copied)} relative asset(s): {', '.join(copied) or '-'}")
    if missing:
        # A referenced-but-absent relative asset means the page was already broken
        # at the source, or references something outside the dir. Report, don't guess.
        print(f"  WARN: {len(missing)} referenced asset(s) NOT found in source (page may be broken): {', '.join(missing)}")
    print("  (stamp data-nav-target on the copy next, then re-run with --verify)")
    return 0


def _first_diff(a: str, b: str):
    n = min(len(a), len(b))
    for i in range(n):
        if a[i] != b[i]:
            lo = max(0, i - 40)
            return i, a[lo:i + 40], b[lo:i + 40]
    if len(a) != len(b):
        i = n
        return i, a[max(0, i - 40):i + 40], b[max(0, i - 40):i + 40]
    return None


def cmd_verify(source: Path, dest: Path) -> int:
    src_index, dst_index = source / "index.html", dest / "index.html"
    if not src_index.is_file():
        print(f"ERROR: no index.html in source {source}")
        return 1
    if not dst_index.is_file():
        print(f"BROKEN: {dest}/index.html missing (import not run?)")
        return 1

    violations = []
    src_html = read_text_exact(src_index)
    dst_html = read_text_exact(dst_index)
    # Invariant: identical modulo data-nav-target stamps (the ONLY sanctioned edit).
    if strip_nav_targets(src_html) != strip_nav_targets(dst_html):
        diff = _first_diff(strip_nav_targets(src_html), strip_nav_targets(dst_html))
        detail = ""
        if diff:
            i, sa, da = diff
            detail = f" first diff @char {i}:\n    source: ...{sa!r}...\n    dest  : ...{da!r}..."
        violations.append(
            "index.html differs from source beyond data-nav-target stamps — "
            "the verbatim page was edited/re-authored (LOCK BROKEN)." + detail
        )

    # Assets must be present and byte-identical (they carry no stamps).
    checked = 0
    for rel in find_relative_assets(src_html):
        checked += 1
        src_asset, dst_asset = source / rel, dest / rel
        if not src_asset.is_file():
            continue  # already surfaced by import; source-side gap, not a copy defect
        if not dst_asset.is_file():
            violations.append(f"asset missing in dest: {rel}")
        elif read_bytes(src_asset) != read_bytes(dst_asset):
            violations.append(f"asset differs from source (should be verbatim): {rel}")

    for v in violations:
        print(f"BROKEN: {v}")
    print(f"verify: index.html + {checked} asset(s) checked, {len(violations)} lock violation(s)")
    return 1 if violations else 0


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--source", required=True, help="approved page dir (locked chassis / prior surface); READ-ONLY")
    p.add_argument("--dest", required=True, help="wave surface dir <out>/<slug> to import into")
    p.add_argument("--verify", action="store_true", help="assert dest == source modulo data-nav-target stamps; exit 1 if lock broken")
    args = p.parse_args()

    source, dest = Path(args.source), Path(args.dest)
    if not source.is_dir():
        print(f"ERROR: --source not a directory: {source}")
        return 1
    return cmd_verify(source, dest) if args.verify else cmd_import(source, dest)


if __name__ == "__main__":
    sys.exit(main())
