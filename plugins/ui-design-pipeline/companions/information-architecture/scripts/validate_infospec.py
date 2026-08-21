#!/usr/bin/env python3
"""Deterministic validator for IA info-spec v1.

Contract: ../references/data-contracts.md (i). Checks schema shape, referential
integrity, the N=1 register rule, and the composition-leak lint (the linchpin's
teeth). Pure stdlib; no network.

Exit codes: 0 = clean (warnings allowed) / 1 = BLOCKs present / 2 = unreadable input.
"""
import argparse
import json
import re
import sys

# Contract i.4 -- unambiguous UI mechanisms. A hit BLOCKs unless the word is in
# lint_overrides (which only the USER may populate -- record their words in run notes).
BLOCK_WORDS = [
    "table", "grid", "card", "cards", "sidebar", "side-pane", "pane", "modal",
    "drawer", "accordion", "tab", "tabs", "carousel", "bento", "kanban",
    "navbar", "topnav", "dropdown", "tooltip", "masonry", "breadcrumb",
    "hero-section", "column", "columns", "row", "rows",
]
# Contract i.4 -- often-but-not-always composition; human judges at the board gate.
WARN_WORDS = [
    "list", "chart", "panel", "tile", "badge", "pill", "header", "footer",
    "button", "toggle", "strip", "banner", "widget",
]
# Contract i.4 -- CJK terms, substring-matched (\b word boundaries don't exist in CJK).
# Multi-char terms only: single chars like 行/列 false-positive on ordinary prose.
BLOCK_WORDS_CJK = [
    "表格", "网格", "卡片", "侧边栏", "侧栏", "弹窗", "模态框", "抽屉", "折叠面板",
    "标签页", "页签", "轮播", "看板", "导航栏", "顶栏", "下拉菜单", "面包屑",
    "分栏", "双栏", "三栏", "瀑布流",
]
WARN_WORDS_CJK = [
    "列表", "图表", "面板", "磁贴", "按钮", "横幅", "弹层", "开关",
]

VALID_TIERS = {1, 2, 3}


# The seven surface kinds. Iron rules and six-dimension weight priors for each live in
# prototyping-ui-directions/references/archetype-rules.md — this list only guards the
# spelling, because a kind nothing downstream has rules for is worse than no kind at all.
ARCHETYPES = {
    "landing-marketing", "data-dashboard", "canvas", "narrative-scrolly",
    "creative-eye", "game-style", "bubble-physics",
}

def _rx(word):
    return re.compile(r"(?<![\w-])" + re.escape(word) + r"(?![\w-])", re.IGNORECASE)


BLOCK_RES = [(w, _rx(w)) for w in BLOCK_WORDS]
WARN_RES = [(w, _rx(w)) for w in WARN_WORDS]


class Report:
    def __init__(self):
        self.blocks = []   # (path, message)
        self.warns = []
        self.notes = []

    def block(self, path, msg):
        self.blocks.append((path, msg))

    def warn(self, path, msg):
        self.warns.append((path, msg))

    def note(self, path, msg):
        self.notes.append((path, msg))


def lint_text(report, path, text, overrides):
    if not isinstance(text, str):
        return
    for word, rx in BLOCK_RES:
        if rx.search(text):
            if word.lower() in overrides:
                report.note(path, "composition word '%s' present but user-overridden" % word)
            else:
                report.block(path, "composition leak: '%s' (BLOCK word) in %r" % (word, text))
    for word, rx in WARN_RES:
        if rx.search(text):
            report.warn(path, "possible composition leak: '%s' (WARN word) in %r" % (word, text))
    for word in BLOCK_WORDS_CJK:
        if word in text:
            if word in overrides:
                report.note(path, "composition word '%s' present but user-overridden" % word)
            else:
                report.block(path, "composition leak: '%s' (BLOCK word) in %r" % (word, text))
    for word in WARN_WORDS_CJK:
        if word in text:
            report.warn(path, "possible composition leak: '%s' (WARN word) in %r" % (word, text))


def validate(spec, report):
    if spec.get("spec_version") != 1:
        report.block("spec_version", "must be 1, got %r" % spec.get("spec_version"))

    register = spec.get("register")
    if isinstance(register, list):
        report.block("register", "is an array -- N=1 register is MANDATORY; run once per register")
    elif not isinstance(register, str) or not register.strip():
        report.block("register", "must be a single non-empty string")

    if not isinstance(spec.get("product"), str) or not spec["product"].strip():
        report.block("product", "must be a non-empty string")

    overrides = spec.get("lint_overrides", [])
    if not isinstance(overrides, list) or any(not isinstance(w, str) for w in overrides):
        report.block("lint_overrides", "must be a list of strings")
        overrides = []
    overrides_l = {w.lower() for w in overrides}
    used = set()

    screens = spec.get("screens")
    if not isinstance(screens, list) or not screens:
        report.block("screens", "must be a non-empty array")
        screens = []

    screen_ids = []
    for i, scr in enumerate(screens):
        sid = scr.get("id")
        spath = "screens[%d](%s)" % (i, sid or "?")
        if not isinstance(sid, str) or not sid.strip():
            report.block(spath + ".id", "missing/empty")
            continue
        if sid in screen_ids:
            report.block(spath + ".id", "duplicate screen id %r" % sid)
        screen_ids.append(sid)

        for field in ("title", "route", "primary_task"):
            if not isinstance(scr.get(field), str) or not scr[field].strip():
                report.block("%s.%s" % (spath, field), "missing/empty")
        lint_text(report, spath + ".primary_task", scr.get("primary_task", ""), overrides_l)

        # archetype (v1.3, optional): WHAT KIND of surface this is, derived from primary_task.
        # Absence is a legitimate answer — a screen whose kind is genuinely unclear should say
        # nothing rather than pick, and downstream degrades to the flat weight prior. A value
        # outside the known set is a different thing: it is a typo or an invented kind, and
        # nothing downstream would have rules for it, so it BLOCKs rather than passing quietly.
        if "archetype" in scr:
            arch = scr.get("archetype")
            if not isinstance(arch, str) or arch not in ARCHETYPES:
                report.block(spath + ".archetype",
                             "unknown archetype %r — one of: %s (or omit the field)"
                             % (arch, " / ".join(sorted(ARCHETYPES))))

        blocks = scr.get("blocks")
        if not isinstance(blocks, list) or not blocks:
            report.block(spath + ".blocks", "must be a non-empty array")
            blocks = []
        block_ids = set()
        has_tier1 = False
        for j, blk in enumerate(blocks):
            bid = blk.get("id")
            bpath = "%s.blocks[%d](%s)" % (spath, j, bid or "?")
            if not isinstance(bid, str) or not bid.strip():
                report.block(bpath + ".id", "missing/empty")
            elif bid in block_ids:
                report.block(bpath + ".id", "duplicate block id %r in screen" % bid)
            else:
                block_ids.add(bid)
            if blk.get("tier") not in VALID_TIERS:
                report.block(bpath + ".tier", "must be 1, 2 or 3; got %r" % blk.get("tier"))
            elif blk["tier"] == 1:
                has_tier1 = True
            for field in ("label", "group", "content_hint"):
                if not isinstance(blk.get(field), str) or not blk[field].strip():
                    report.block("%s.%s" % (bpath, field), "missing/empty")
            lint_text(report, bpath + ".label", blk.get("label", ""), overrides_l)
            lint_text(report, bpath + ".content_hint", blk.get("content_hint", ""), overrides_l)
        if blocks and not has_tier1:
            report.warn(spath, "no tier-1 block -- nothing dominates; hierarchy undesigned?")

        scan = scr.get("scan_path")
        if scan is None:
            report.warn(spath, "no scan_path -- priority path for the primary task is undeclared")
        elif not isinstance(scan, list):
            report.block(spath + ".scan_path", "must be an array of block ids")
        else:
            for k, ref in enumerate(scan):
                if ref not in block_ids:
                    report.block("%s.scan_path[%d]" % (spath, k),
                                 "%r is not a block id of this screen" % ref)

        for k, flow in enumerate(scr.get("within_page_flow", []) or []):
            fpath = "%s.within_page_flow[%d]" % (spath, k)
            frm = flow.get("from", "")
            frm_base = frm.split(".", 1)[0] if isinstance(frm, str) else ""
            if frm_base not in block_ids:
                report.block(fpath + ".from", "%r does not resolve to a block id" % frm)
            if flow.get("to") not in block_ids:
                report.block(fpath + ".to", "%r is not a block id" % flow.get("to"))
            for field in ("trigger", "relationship"):
                if not isinstance(flow.get(field), str) or not flow[field].strip():
                    report.block("%s.%s" % (fpath, field), "missing/empty")
            lint_text(report, fpath + ".relationship", flow.get("relationship", ""), overrides_l)

    hero = spec.get("hero_id")
    if hero not in screen_ids:
        report.block("hero_id", "%r is not a screens[].id" % hero)

    linked = set()
    edges = set()        # (from, to) directed, external targets included
    ext_targets = set()  # link_map targets marked external:true
    for k, link in enumerate(spec.get("link_map", []) or []):
        lpath = "link_map[%d]" % k
        external = bool(link.get("external"))
        frm, to = link.get("from"), link.get("to")
        if frm not in screen_ids:
            report.block(lpath + ".from", "%r is not a screen id" % frm)
        else:
            linked.add(frm)
        if not external and to not in screen_ids:
            report.block(lpath + ".to",
                         "%r is not a screen id (mark external:true for exits)" % to)
        elif not external:
            linked.add(to)
        else:
            ext_targets.add(to)
        edges.add((frm, to))
        if not isinstance(link.get("via"), str) or not link["via"].strip():
            report.block(lpath + ".via", "missing/empty")
        lint_text(report, lpath + ".via", link.get("via", ""), overrides_l)

    # Contract v1.1 -- OPTIONAL task_paths[]: declared journeys the board renders as subway
    # strips. TEETH: every hop must be a real link_map edge; only the LAST entry may be an
    # external target (journeys may end at an exit, never pass through one).
    task_paths = spec.get("task_paths")
    if task_paths is not None:
        if not isinstance(task_paths, list):
            report.block("task_paths", "must be an array when present")
            task_paths = []
        tp_ids = set()
        for k, tp in enumerate(task_paths):
            tpath = "task_paths[%d](%s)" % (k, (tp.get("id") if isinstance(tp, dict) else None) or "?")
            if not isinstance(tp, dict):
                report.block(tpath, "must be an object")
                continue
            tid = tp.get("id")
            if not isinstance(tid, str) or not tid.strip():
                report.block(tpath + ".id", "missing/empty")
            elif tid in tp_ids:
                report.block(tpath + ".id", "duplicate task_path id %r" % tid)
            else:
                tp_ids.add(tid)
            if not isinstance(tp.get("label"), str) or not tp["label"].strip():
                report.block(tpath + ".label", "missing/empty")
            lint_text(report, tpath + ".label", tp.get("label", ""), overrides_l)
            path = tp.get("path")
            if not isinstance(path, list) or len(path) < 2:
                report.block(tpath + ".path", "must be an array of >=2 stops")
                continue
            last = len(path) - 1
            for n, stop in enumerate(path):
                ppath = "%s.path[%d]" % (tpath, n)
                if stop in screen_ids:
                    continue
                if n == last and stop in ext_targets:
                    continue
                report.block(ppath, "%r is not a screen id%s" % (
                    stop, " (external targets are allowed only as the LAST stop)"
                    if stop in ext_targets else ""))
            for n in range(len(path) - 1):
                hop = (path[n], path[n + 1])
                if hop not in edges:
                    report.block("%s.path[%d->%d]" % (tpath, n, n + 1),
                                 "hop %r -> %r is not a link_map edge -- the declared journey "
                                 "cannot be carried by the link map" % hop)

        # v1.1 coverage (cheap cross-layer consistency; only meaningful once journeys exist):
        # a screen no journey visits is either an incomplete journey set or a questionable
        # screen (WARN); an edge no journey uses is often just navigation convenience (NOTE).
        if task_paths:
            visited, used_hops = set(), set()
            for tp in task_paths:
                path = tp.get("path") if isinstance(tp, dict) else None
                if isinstance(path, list):
                    visited.update(path)
                    for n in range(len(path) - 1):
                        used_hops.add((path[n], path[n + 1]))
            for sid in screen_ids:
                if sid not in visited:
                    report.warn("screens(%s)" % sid,
                                "not visited by any task_path -- journey set incomplete, "
                                "or the screen is questionable")
            for k, link in enumerate(spec.get("link_map", []) or []):
                hop = (link.get("from"), link.get("to"))
                if hop not in used_hops:
                    report.note("link_map[%d]" % k,
                                "edge %r -> %r used by no task_path (fine if it is a "
                                "navigation convenience)" % hop)

    for sid in screen_ids:
        if sid not in linked and len(screen_ids) > 1:
            report.warn("screens(%s)" % sid, "orphan -- appears in no link_map edge")

    # Contract v1.2 -- return rule (user-ratified ENFORCE, no approval step): every screen other
    # than the ENTRY must reverse-reach the entry along non-external edges, unless a global
    # return_convention is declared or the screen is user-exempted in return_overrides[].
    # v1.2.1: anchor = entry_id (default hero_id) -- hero is the primary-JTBD screen and is not
    # necessarily the front door; when they differ, the hero too must walk back to entry.
    entry = spec.get("entry_id")
    if entry is not None and entry not in screen_ids:
        report.block("entry_id", "%r is not a screens[].id" % entry)
        entry = None
    if entry is None:
        entry = hero
    conv = spec.get("return_convention")
    if conv is not None and (not isinstance(conv, str) or not conv.strip()):
        report.block("return_convention", "must be a non-empty string when present")
        conv = None
    if isinstance(conv, str):
        lint_text(report, "return_convention", conv, overrides_l)
    r_overrides = spec.get("return_overrides", [])
    if not isinstance(r_overrides, list) or any(not isinstance(s, str) for s in r_overrides):
        report.block("return_overrides", "must be a list of screen-id strings")
        r_overrides = []
    for sid in r_overrides:
        if sid not in screen_ids:
            report.warn("return_overrides", "%r is not a screen id -- stale/unknown entry" % sid)
    if entry in screen_ids and len(screen_ids) > 1 and not conv:
        rev = {}
        for frm, to in edges:
            if to in screen_ids and frm in screen_ids:
                rev.setdefault(to, set()).add(frm)
        can_return, stack = {entry}, [entry]
        while stack:
            for src in rev.get(stack.pop(), ()):
                if src not in can_return:
                    can_return.add(src)
                    stack.append(src)
        for sid in screen_ids:
            if sid == entry or sid in can_return:
                continue
            if sid in r_overrides:
                report.note("screens(%s)" % sid,
                            "cannot walk back to entry -- user-exempted via return_overrides "
                            "(terminal screen)")
            else:
                report.block("screens(%s)" % sid,
                             "cannot walk back to the entry (%s) along link_map edges -- add "
                             "return edges, declare return_convention, or (terminal screens "
                             "only, user's say-so) list it in return_overrides" % entry)

    # unused overrides = stale approvals; keep the array honest
    # (match the exact "composition word '<w>' present..." note shape -- other note kinds,
    # e.g. return_overrides exemptions, must not feed this parse)
    noted = {n[1].split("'")[1].lower() for n in report.notes
             if n[1].startswith("composition word '") and "user-overridden" in n[1]}
    for word in overrides_l - noted:
        report.warn("lint_overrides", "override %r never used -- remove stale approval" % word)


def main():
    ap = argparse.ArgumentParser(description="Validate an IA info-spec v1 JSON file.")
    ap.add_argument("spec", help="path to info-spec.json")
    ap.add_argument("--json", dest="json_out", help="also write the report as JSON here")
    args = ap.parse_args()

    try:
        with open(args.spec, encoding="utf-8") as f:
            spec = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print("UNREADABLE: %s" % e)
        return 2

    report = Report()
    validate(spec, report)

    for label, rows in (("BLOCK", report.blocks), ("WARN", report.warns), ("NOTE", report.notes)):
        for path, msg in rows:
            print("%-5s %s - %s" % (label, path, msg))
    print("---")
    print("result: %d BLOCK / %d WARN / %d NOTE -> %s"
          % (len(report.blocks), len(report.warns), len(report.notes),
             "FAIL" if report.blocks else "PASS"))

    if args.json_out:
        with open(args.json_out, "w", encoding="utf-8") as f:
            json.dump({"blocks": report.blocks, "warns": report.warns,
                       "notes": report.notes,
                       "verdict": "FAIL" if report.blocks else "PASS"}, f, indent=2)

    return 1 if report.blocks else 0


if __name__ == "__main__":
    sys.exit(main())
