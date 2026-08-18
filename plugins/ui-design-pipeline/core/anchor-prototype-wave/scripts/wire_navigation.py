#!/usr/bin/env python3
"""wire_navigation.py — deterministic nav-linker pass for anchor-prototype-wave output.

Rewrites mocked cross-page links (rule 6: `data-mock` + author-stamped
`data-nav-target="<slug>"`) into real relative links WHEN the target surface was
built in this wave. Everything else (external links, unbuilt targets, links
without a nav-target) stays mock. Idempotent: wired links lose `data-mock` and
gain `data-nav-wired="true"`, so a re-run is a no-op.

Both modes also emit a non-blocking WARN when a link is wired (live) but still
LOOKS mock — either (a) the `<a>`'s OWN CLASS carries a mock token (e.g. `is-mock`),
or (b) it still shows an inner mock BADGE: a mock-classed descendant (e.g.
`<span class="mock-tag">`) that the page CSS does NOT default-hide. rule 6 styles the
inert look AND the badge via the `[data-mock]` attribute selector plus a default-hidden
badge, so stripping the attribute revives the live look and hides the badge; an author
who put a mock class on the `<a>`, or gated the badge only on `[data-mock]` with no bare
default hide, leaves a live link wearing dead clothes. A correctly default-hidden badge
does NOT warn (no false positives on well-authored waves). The WARN is for the human
reviewer (restyle / accept / re-lock) — it never edits the page, never changes exit code.

Usage:
    python wire_navigation.py <out-dir>            # wire + report
    python wire_navigation.py <out-dir> --check    # crawl wired links, exit 1 on breakage

Deterministic stdlib regex, same house style as validate_surface.py. Known
limitation (documented, not defended against): attribute values containing a
literal '>' break the tag regex — wave-authored pages don't do this.
"""

import argparse
import json
import re
import sys
from pathlib import Path

# Windows consoles may be GBK; reports must never crash on non-ASCII page text.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

A_TAG_RE = re.compile(r"<a\b[^>]*>", re.IGNORECASE)
DATA_MOCK_RE = re.compile(r"""\sdata-mock(?:\s*=\s*(?:"[^"]*"|'[^']*'))?(?=[\s>])""")
NAV_TARGET_RE = re.compile(r"""\bdata-nav-target\s*=\s*(?:"([^"]*)"|'([^']*)')""")
HREF_RE = re.compile(r"""\bhref\s*=\s*(?:"[^"]*"|'[^']*')""")
ONCLICK_MOCK_RE = re.compile(
    r"""\sonclick\s*=\s*(?:"[^"]*return\s+false[^"]*"|'[^']*return\s+false[^']*')"""
)
TITLE_RE = re.compile(r"""\stitle\s*=\s*(?:"[^"]*"|'[^']*')""")
WIRED_RE = re.compile(r"""\bdata-nav-wired\s*=\s*(?:"true"|'true')""")
CLASS_RE = re.compile(r"""\bclass\s*=\s*(?:"([^"]*)"|'([^']*)')""")
# Inner-badge detector (the WARN blind-spot fix): a mock-classed descendant element
# (e.g. `<span class="mock-tag">`), capturing its class so we can check whether the
# page CSS DEFAULT-hides it — a correctly-gated badge vanishes on wiring and must NOT warn.
INNER_MOCK_BADGE_RE = re.compile(
    r"""<[a-z][^>]*\bclass\s*=\s*(?:"([^"]*mock[^"]*)"|'([^']*mock[^']*)')""", re.IGNORECASE
)
STYLE_RE = re.compile(r"<style\b[^>]*>(.*?)</style>", re.IGNORECASE | re.DOTALL)
CSS_COMMENT_RE = re.compile(r"/\*.*?\*/", re.DOTALL)
CSS_RULE_RE = re.compile(r"([^{}]*)\{([^}]*)\}")
CSS_HIDE_RE = re.compile(r"display\s*:\s*none|visibility\s*:\s*hidden", re.IGNORECASE)


def mock_looking_classes(tag: str):
    """Class tokens on this `<a>`'s OWN class that still LOOK mock (e.g. `is-mock`).

    The stamp convention (rule 6) styles inert links via the `[data-mock]` ATTRIBUTE
    selector, so stripping data-mock revives the live look for free. A page that styled
    inert via a CLASS instead (older chassis, a distracted author) leaves the link
    wired-but-dead-looking. This inspects only the opening `<a>`'s own class — an inner
    "占位/mocked" badge `<span>` is handled separately by `mock_looking_inner`.
    """
    class_match = CLASS_RE.search(tag)
    if not class_match:
        return []
    tokens = (class_match.group(1) or class_match.group(2)).split()
    return [t for t in tokens if "mock" in t.lower()]


def badge_default_hidden(page_html: str, badge_class: str) -> bool:
    """True if the page CSS DEFAULT-hides `.badge_class` — a rule NOT gated on
    `[data-mock]` that sets display:none / visibility:hidden.

    This is rule 6's 'default hidden' half: with it, stripping data-mock leaves the
    badge invisible, so a wired link's leftover badge span is correctly hidden and must
    NOT warn. An author who gated BOTH show and hide on `[data-mock]` (no bare default
    hide) leaves the badge visible once data-mock is gone — that one warns. Only <style>
    blocks are scanned, so a `.mock-tag` mention inside JS/text can't be mistaken for CSS.
    """
    needle = f".{badge_class}"
    for style in STYLE_RE.findall(page_html):
        style = CSS_COMMENT_RE.sub(" ", style)  # comments may mention .mock-tag/data-mock
        for sel, body in CSS_RULE_RE.findall(style):
            sel = sel.strip().splitlines()[-1] if sel.strip() else sel  # real selector = last line before {
            if needle in sel and "data-mock" not in sel and CSS_HIDE_RE.search(body):
                return True
    return False


def mock_looking_inner(inner_html: str, page_html: str):
    """Reasons a wired `<a>`'s inner markup shows a mock badge that is NOT default-hidden.

    rule 6 shows the visible "mocked" tag via a `[data-mock] .mock-tag` descendant and
    default-hides `.mock-tag`, so after wiring (data-mock stripped) the badge vanishes. We
    warn only when the badge class is present in the wired link AND the page CSS does NOT
    default-hide it (the author forgot the default-hide half) = a live link wearing a
    visible mock badge. This closes wire_navigation's old class-only blind spot WITHOUT
    warning on correctly-gated badges. Diagnostic only (never blocks / edits).
    """
    reasons = []
    for m in INNER_MOCK_BADGE_RE.finditer(inner_html):
        classes = (m.group(1) or m.group(2)).split()
        visible = [c for c in classes
                   if "mock" in c.lower() and not badge_default_hidden(page_html, c)]
        if visible:
            reasons.append(f"inner mock badge {visible} not default-hidden")
    return reasons


def mock_reasons(opening_tag: str, inner_html: str, page_html: str):
    """Every reason a WIRED link still looks mock (own class + visible inner badge)."""
    reasons = []
    cls = mock_looking_classes(opening_tag)
    if cls:
        reasons.append(f"own class {cls}")
    reasons.extend(mock_looking_inner(inner_html, page_html))
    return reasons


def inner_of(html: str, opening_end: int) -> str:
    """Inner markup of an `<a>` whose opening tag ends at `opening_end`, up to its `</a>`.

    `<a>` never nests, so the first `</a>` after the opening tag is the matching close.
    """
    close = html.find("</a>", opening_end)
    return html[opening_end:close] if close != -1 else html[opening_end:]


def built_slugs(out_dir: Path):
    """Surface slugs of THIS wave, each verified to actually exist on disk.

    manifest.json is the wave's fact source when present; directory scan is the
    fallback. Either way a slug only counts if <out>/<slug>/index.html exists —
    wiring to a listed-but-missing page would mint a dead link.
    """
    manifest = out_dir / "audits" / "manifest.json"
    candidates = []
    if manifest.is_file():
        try:
            data = json.loads(manifest.read_text(encoding="utf-8"))
            candidates = [s.get("slug") for s in data.get("surfaces", []) if s.get("slug")]
        except (json.JSONDecodeError, OSError) as exc:
            print(f"WARN: unreadable manifest ({exc}); falling back to directory scan")
    if not candidates:
        candidates = sorted(
            p.parent.name
            for p in out_dir.glob("*/index.html")
            if p.parent.name != "audits"
        )
    slugs = set()
    for slug in candidates:
        if (out_dir / slug / "index.html").is_file():
            slugs.add(slug)
        else:
            print(f"WARN: manifest lists '{slug}' but {slug}/index.html is missing — not a wire target")
    return slugs


def rewrite_tag(tag: str, target: str) -> str:
    """Turn one mocked <a ...> tag into a wired one. Touches only the mock attrs."""
    new = tag
    href = f'href="../{target}/index.html"'
    if HREF_RE.search(new):
        new = HREF_RE.sub(href, new, count=1)
    else:
        new = new[:2] + " " + href + new[2:]  # '<a' + href + rest
    new = DATA_MOCK_RE.sub("", new, count=1)
    new = ONCLICK_MOCK_RE.sub("", new, count=1)
    new = TITLE_RE.sub("", new, count=1)
    return new[:-1].rstrip() + ' data-nav-wired="true">'


def wire_page(html: str, built: set):
    """Rewrite all eligible tags in one page. Returns (new_html, stats)."""
    stats = {"wired": [], "kept_no_target": 0, "kept_unbuilt": [], "mock_warn": []}

    def repl(match):
        tag = match.group(0)
        if not DATA_MOCK_RE.search(tag) or WIRED_RE.search(tag):
            return tag
        target_match = NAV_TARGET_RE.search(tag)
        if not target_match:
            stats["kept_no_target"] += 1
            return tag
        target = target_match.group(1) or target_match.group(2)
        if target not in built:
            stats["kept_unbuilt"].append(target)
            return tag
        stats["wired"].append(target)
        return rewrite_tag(tag, target)

    new_html = A_TAG_RE.sub(repl, html)

    # WARN pass (diagnostic only — never edits the page, never changes the exit code):
    # a wired link that still LOOKS mock via its own class OR an inner badge span.
    for m in A_TAG_RE.finditer(new_html):
        tag = m.group(0)
        if not WIRED_RE.search(tag):
            continue
        reasons = mock_reasons(tag, inner_of(new_html, m.end()), new_html)
        if reasons:
            tm = NAV_TARGET_RE.search(tag)
            target = (tm.group(1) or tm.group(2)) if tm else "?"
            stats["mock_warn"].append((target, reasons, tag[:110]))
    return new_html, stats


def read_page(path: Path) -> str:
    with open(path, "r", encoding="utf-8", newline="") as fh:
        return fh.read()


def write_page(path: Path, html: str):
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(html)


def cmd_wire(out_dir: Path) -> int:
    built = built_slugs(out_dir)
    if not built:
        print(f"ERROR: no built surfaces found under {out_dir}")
        return 1
    print(f"wave surfaces ({len(built)}): {', '.join(sorted(built))}")
    total_wired = 0
    total_warn = 0
    for slug in sorted(built):
        page = out_dir / slug / "index.html"
        html = read_page(page)
        new_html, stats = wire_page(html, built)
        if new_html != html:
            write_page(page, new_html)
        wired_n = len(stats["wired"])
        total_wired += wired_n
        unbuilt = ", ".join(sorted(set(stats["kept_unbuilt"]))) or "-"
        print(
            f"  {slug}: wired {wired_n} "
            f"(-> {', '.join(sorted(set(stats['wired']))) or '-'}) | "
            f"kept mock: {stats['kept_no_target']} no-target, "
            f"{len(stats['kept_unbuilt'])} unbuilt-target ({unbuilt})"
        )
        for target, reasons, snippet in stats["mock_warn"]:
            total_warn += 1
            print(
                f"    WARN: wired link (-> {target}) still looks mock "
                f"({'; '.join(reasons)}) — live but reads as dead; restyle via the "
                f"[data-mock] selector or drop the badge. {snippet}"
            )
    tail = f", {total_warn} WARN (live-but-looks-mock)" if total_warn else ""
    print(f"done: {total_wired} link(s) wired across {len(built)} page(s){tail}")
    return 0


def cmd_check(out_dir: Path) -> int:
    built = built_slugs(out_dir)
    if not built:
        print(f"ERROR: no built surfaces found under {out_dir}")
        return 1
    errors = []
    warns = []
    checked = 0
    wave_pages = {(out_dir / s / "index.html").resolve() for s in built}
    for slug in sorted(built):
        page = out_dir / slug / "index.html"
        html = read_page(page)
        for match in A_TAG_RE.finditer(html):
            tag = match.group(0)
            if not WIRED_RE.search(tag):
                continue
            checked += 1
            where = f"{slug}/index.html: {tag[:100]}"
            if DATA_MOCK_RE.search(tag):
                errors.append(f"still data-mock after wiring — {where}")
                continue
            reasons = mock_reasons(tag, inner_of(html, match.end()), html)
            if reasons:
                warns.append(f"live link still looks mock ({'; '.join(reasons)}) — {where}")
            href_match = re.search(r"""\bhref\s*=\s*(?:"([^"]*)"|'([^']*)')""", tag)
            if not href_match:
                errors.append(f"wired link without href — {where}")
                continue
            href = href_match.group(1) or href_match.group(2)
            # A fragment (#section) or query (?k=v) addresses a position WITHIN the
            # target page — it is not part of the path on disk. Resolving the raw
            # href made every in-page deep link read as broken: found 2026-07-21 on
            # Averonel, where ../home/index.html#delivered-systems was reported
            # BROKEN while navigating correctly in the browser. False BROKENs are
            # worse than no check — they train the reader to ignore the report.
            path_part = re.split(r"[#?]", href, 1)[0]
            # a bare "#anchor" (or "?q=1") addresses the current page itself
            target = (page.parent / path_part).resolve() if path_part else page.resolve()
            if target not in wave_pages:
                errors.append(f"wired href leaves the wave or is broken ({href}) — {where}")
            elif not target.is_file():
                errors.append(f"wired href target missing ({href}) — {where}")
    for warn in warns:
        print(f"WARN: {warn}")
    for err in errors:
        print(f"BROKEN: {err}")
    print(f"check: {checked} wired link(s), {len(errors)} broken, {len(warns)} WARN (live-but-looks-mock)")
    return 1 if errors else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("out_dir", help="wave output dir (contains <slug>/index.html + audits/)")
    parser.add_argument(
        "--check",
        action="store_true",
        help="verify every data-nav-wired link resolves to a built wave page; exit 1 on breakage",
    )
    args = parser.parse_args()
    out_dir = Path(args.out_dir)
    if not out_dir.is_dir():
        print(f"ERROR: not a directory: {out_dir}")
        return 1
    return cmd_check(out_dir) if args.check else cmd_wire(out_dir)


if __name__ == "__main__":
    sys.exit(main())
