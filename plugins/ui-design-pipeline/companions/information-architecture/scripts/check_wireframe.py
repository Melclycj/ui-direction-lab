#!/usr/bin/env python3
"""Deterministic checker for IA round-2 grey-box wireframes.

Contract: ../references/data-contracts.md (ii). A wireframe COMMITS the locked
composition but stays unstyled: every spec block appears exactly once as
data-ia-block, tiers match, root declares data-ia-composition, no scripts /
motion / external assets, greyscale only. Pure stdlib.

Usage: check_wireframe.py <wireframe.html> --spec <info-spec.json> --screen <screen-id>
Exit codes: 0 = clean (warnings allowed) / 1 = BLOCKs / 2 = unreadable input.
"""
import argparse
import json
import re
import sys
from html.parser import HTMLParser

HEX_RE = re.compile(r"#([0-9a-fA-F]{6}|[0-9a-fA-F]{3})\b")


class WireframeScan(HTMLParser):
    def __init__(self):
        super().__init__()
        self.blocks = []        # (block_id, tier_attr)
        self.flags = []         # data-ia-flag values
        self.composition = None
        self.scripts = 0
        self.external_refs = []
        self.style_chunks = []
        self._in_style = False
        self._root_seen = False

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if not self._root_seen and tag in ("html", "body", "main", "div"):
            # composition attr must sit on the document root element (html or first container)
            if "data-ia-composition" in a:
                self.composition = a["data-ia-composition"]
            if tag == "html":
                self._root_seen = self.composition is not None
        elif "data-ia-composition" in a and self.composition is None:
            self.composition = a["data-ia-composition"]
        if "data-ia-block" in a:
            self.blocks.append((a["data-ia-block"], a.get("data-ia-tier")))
        if "data-ia-flag" in a:
            self.flags.append(a["data-ia-flag"])
        if tag == "script":
            self.scripts += 1
        if tag == "style":
            self._in_style = True
        if tag in ("link", "img", "iframe", "source"):
            ref = a.get("href") or a.get("src") or ""
            if ref.startswith(("http://", "https://", "//")):
                self.external_refs.append(ref)
        if "style" in a:
            self.style_chunks.append(a["style"])

    def handle_endtag(self, tag):
        if tag == "style":
            self._in_style = False

    def handle_data(self, data):
        if self._in_style:
            self.style_chunks.append(data)


def non_greyscale_hexes(css_text, max_spread=8):
    """Near-greyscale is fine (warm greys like #e3e3e0); real hues are not."""
    bad = set()
    for m in HEX_RE.finditer(css_text):
        h = m.group(1)
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        vals = [int(h[i:i + 2], 16) for i in (0, 2, 4)]
        if max(vals) - min(vals) > max_spread:
            bad.add("#" + h)
    return sorted(bad)


def main():
    ap = argparse.ArgumentParser(description="Check an IA round-2 grey-box wireframe.")
    ap.add_argument("wireframe", help="path to wireframes/<id>/index.html")
    ap.add_argument("--spec", required=True, help="path to info-spec.json")
    ap.add_argument("--screen", required=True, help="screen id within the spec")
    args = ap.parse_args()

    try:
        with open(args.wireframe, encoding="utf-8") as f:
            html_text = f.read()
        with open(args.spec, encoding="utf-8") as f:
            spec = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print("UNREADABLE: %s" % e)
        return 2

    screen = next((s for s in spec.get("screens", []) if s.get("id") == args.screen), None)
    if screen is None:
        print("UNREADABLE: screen %r not in spec" % args.screen)
        return 2

    scan = WireframeScan()
    scan.feed(html_text)

    blocks_expected = [b.get("id") for b in screen.get("blocks", [])]
    tiers = {b.get("id"): b.get("tier") for b in screen.get("blocks", [])}
    seen = {}
    for bid, tier_attr in scan.blocks:
        seen.setdefault(bid, []).append(tier_attr)

    blocks_r, warns, notes = [], [], []

    for bid in blocks_expected:
        hits = seen.get(bid, [])
        if not hits:
            blocks_r.append("block %r missing (every spec block appears exactly once)" % bid)
        elif len(hits) > 1:
            blocks_r.append("block %r appears %d times (must be exactly once)" % (bid, len(hits)))
        elif hits[0] != str(tiers[bid]):
            blocks_r.append("block %r data-ia-tier=%r != spec tier %r" % (bid, hits[0], tiers[bid]))
    for bid in seen:
        if bid not in blocks_expected:
            blocks_r.append("unknown data-ia-block %r (not in the screen's spec)" % bid)

    if not scan.composition:
        blocks_r.append("root data-ia-composition missing (the wireframe must name its pattern)")
    if scan.scripts:
        blocks_r.append("%d <script> tag(s) -- wireframes carry NO motion/behavior" % scan.scripts)
    for ref in scan.external_refs:
        blocks_r.append("external asset %r -- wireframes are self-contained" % ref)

    bad_hex = non_greyscale_hexes("\n".join(scan.style_chunks))
    if bad_hex:
        warns.append("non-greyscale color(s) %s -- grey-box means grey" % ", ".join(bad_hex))
    for flag in scan.flags:
        notes.append("data-ia-flag=%r -- needs user resolution at the Stage-F gate" % flag)

    for label, rows in (("BLOCK", blocks_r), ("WARN", warns), ("NOTE", notes)):
        for msg in rows:
            print("%-5s %s" % (label, msg))
    print("---")
    print("result: %d BLOCK / %d WARN / %d NOTE -> %s (screen=%s, pattern=%s)"
          % (len(blocks_r), len(warns), len(notes),
             "FAIL" if blocks_r else "PASS", args.screen, scan.composition or "?"))
    return 1 if blocks_r else 0


if __name__ == "__main__":
    sys.exit(main())
