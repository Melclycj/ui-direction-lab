#!/usr/bin/env python3
"""Deterministic renderer: IA info-spec v1 -> grey-box review board + outline.

Contract: ../references/data-contracts.md (iii). board.html and outline.md are PURE
renderings of info-spec.json — one data, two views; regenerate, never hand-edit.
The board is deliberately NOT a composition: neutral single column per screen,
tier-sized grey boxes, grayscale + ONE muted annotation ink. Pure stdlib.

Usage: render_board.py <info-spec.json> [--out <dir>] [--lang en|zh]
       (default out: <spec-dir>/board; default lang: en — chrome strings only,
        content comes verbatim from the spec)
"""
import argparse
import html
import json
import os
import sys

ANNOTATION_INK = "#3b5bdb"  # the ONE annotation color (schematic/blueprint convention)

STRINGS = {
    "en": {
        "banner": ("<strong>SCHEMATIC — information structure only.</strong> Composition (where "
                   "things sit, what widgets render them) is deliberately undecided; it is "
                   "varied and chosen later in <code>prototyping-ui-directions</code>. Review "
                   "WHAT each screen holds, priority (box height = tier), scan order (numbered), "
                   "grouping and flow — not looks."),
        "board_title": "IA review board",
        "meta": ("register: %s &middot; screens: %d &middot; hero: %s &middot; "
                 "source: %s (spec_version %s)"),
        "screen_map": "Product screen map",
        "external_exit": "external exit",
        "link_map": "Link map (static &mdash; no wired journeys)",
        "hero_tag": "&#9733; HERO",
        "hero_title": "hero screen",
        "primary_task": "PRIMARY TASK",
        "archetype": "KIND",
        "flow": "Within-page flow",
        "arrivals": "How you get here (arrivals)",
        "departures": "Where you can go (departures)",
        "no_arrivals": "no inbound link &mdash; entry screen or unreachable (validator warns on orphans)",
        "warn_noback": "no path back to the hero via link_map (return edges missing)",
        "task_paths": "Task paths (declared journeys &mdash; walk each one)",
        "tp_ext": "external exit",
        "return_conv": "Return convention (declared &mdash; judge it here)",
        "entry_tag": "&#8962; entry",
        "warn_noback_entry": "no path back to the entry via link_map (return edges missing)",
        "footer": "pure rendering of %s &mdash; regenerate via render_board.py, never hand-edit",
        "o_title": "# IA outline — %s (register: %s)",
        "o_note": "> Pure rendering of `%s` — same data as board.html. Hero = **%s**.",
        "o_hero": " ★HERO",
        "o_primary": "Primary task",
        "o_scan": "Scan path",
        "o_blocks": "Blocks",
        "o_flow": "Within-page flow",
        "o_arrivals": "Arrivals (how you get here)",
        "o_departures": "Departures (where you can go)",
        "o_task_paths": "## Task paths (declared journeys)",
        "o_noback": " ⚠ no path back to hero",
        "o_return_conv": "Return convention",
        "o_links": "## Link map (static)",
        "o_ext": " (external)",
    },
    "zh": {
        "banner": ("<strong>示意图 —— 只审信息结构。</strong>构图（放在哪里、用什么控件呈现）"
                   "故意未定，之后在 <code>prototyping-ui-directions</code> 里出多版供挑选。"
                   "请审每屏该有什么信息、主次（盒高 = tier 层级）、扫描顺序（编号）、"
                   "分组与流向 —— 不审外观。"),
        "board_title": "IA 评审板",
        "meta": ("register：%s &middot; 屏数：%d &middot; 主屏：%s &middot; "
                 "来源：%s（spec_version %s）"),
        "screen_map": "产品屏幕地图",
        "external_exit": "外部出口",
        "link_map": "跨屏链接（静态 &mdash; 不做接线跳转）",
        "hero_tag": "&#9733; 主屏",
        "hero_title": "主屏（hero）",
        "primary_task": "主任务",
        "archetype": "类型",
        "flow": "页内流",
        "arrivals": "怎么到我这来（入边）",
        "departures": "从我能去哪（出边）",
        "no_arrivals": "无入边 &mdash; 入口屏或不可达（孤儿屏由 validator 警告）",
        "warn_noback": "沿 link_map 走不回主屏（缺返程边）",
        "task_paths": "任务路线图（声明的任务旅程 &mdash; 逐条走查）",
        "tp_ext": "外部出口",
        "return_conv": "返回惯例（已声明 &mdash; 请在此审它本身）",
        "entry_tag": "&#8962; 入口",
        "warn_noback_entry": "沿 link_map 走不回入口（缺返程边）",
        "footer": "本页为 %s 的纯渲染 &mdash; 用 render_board.py 重新生成，勿手改",
        "o_title": "# IA 大纲 — %s（register：%s）",
        "o_note": "> `%s` 的纯渲染 —— 与 board.html 同一份数据。主屏 = **%s**。",
        "o_hero": " ★主屏",
        "o_primary": "主任务",
        "o_scan": "扫描路径",
        "o_blocks": "信息块",
        "o_flow": "页内流",
        "o_arrivals": "到达（怎么到我这来）",
        "o_departures": "离开（从我能去哪）",
        "o_task_paths": "## 任务路线图（声明的任务旅程）",
        "o_noback": " ⚠ 走不回主屏",
        "o_return_conv": "返回惯例",
        "o_links": "## 跨屏链接（静态）",
        "o_ext": "（外部）",
    },
}

CSS = """
:root { color-scheme: light; }
* { box-sizing: border-box; margin: 0; }
body { font-family: system-ui, -apple-system, "Segoe UI", sans-serif; background: #f4f4f2;
       color: #26282b; padding: 32px 24px 96px; max-width: 880px; margin: 0 auto; }
.banner { border: 2px solid ANNOT; background: #eef1fb; color: #26282b; padding: 14px 16px;
          font-size: 14px; line-height: 1.5; margin-bottom: 28px; }
.banner strong { color: ANNOT; letter-spacing: .04em; }
h1 { font-size: 22px; margin-bottom: 4px; }
.meta { font-family: ui-monospace, Consolas, monospace; font-size: 12px; color: #6b6f76;
        margin-bottom: 32px; }
section.screen { margin-bottom: 48px; border-top: 1px solid #c9cbce; padding-top: 20px; }
section.map { margin-bottom: 48px; border-top: 1px solid #c9cbce; padding-top: 20px; }
h2 { font-size: 16px; }
h2 .route { font-family: ui-monospace, Consolas, monospace; font-size: 12px; color: #6b6f76;
            font-weight: 400; margin-left: 8px; }
h2 .star { color: ANNOT; }
.task { margin: 10px 0 16px; font-size: 13px; padding: 8px 12px; background: #fff;
        border-left: 3px solid ANNOT; }
.task b { color: ANNOT; font-weight: 600; letter-spacing: .03em; }
.strip { display: flex; flex-direction: column; gap: 8px; }
.blk { position: relative; background: #e3e3e0; border: 1px solid #b9bab6; padding: 10px 14px;
       display: flex; flex-direction: column; justify-content: center; }
.blk.t1 { min-height: 118px; }
.blk.t2 { min-height: 72px; }
.blk.t3 { min-height: 44px; }
.blk .label { font-weight: 600; font-size: 14px; }
.blk .hint { font-size: 12.5px; color: #55585d; margin-top: 4px; max-width: 62ch; }
.blk .tags { position: absolute; top: 8px; right: 10px; font-family: ui-monospace, Consolas,
             monospace; font-size: 10.5px; color: #6b6f76; text-align: right; }
.blk .scan { position: absolute; left: -14px; top: 50%; transform: translateY(-50%);
             width: 26px; height: 26px; border-radius: 50%; background: ANNOT; color: #fff;
             font-size: 13px; font-weight: 700; display: flex; align-items: center;
             justify-content: center; }
.flows { margin-top: 14px; font-size: 12.5px; }
.flows h3, .edges h3 { font-size: 11px; letter-spacing: .08em; text-transform: uppercase;
                       color: #6b6f76; margin-bottom: 6px; }
.flows li, .edges li { list-style: none; padding: 3px 0; }
.flows .arrow, .edges .arrow { color: ANNOT; font-weight: 700; }
.flows .rel { color: #55585d; }
.nodes { display: flex; flex-wrap: wrap; gap: 10px; margin: 14px 0 16px; }
.node { background: #e3e3e0; border: 1px solid #b9bab6; padding: 10px 16px; font-size: 13px;
        font-weight: 600; }
.node.hero { border: 2px solid ANNOT; }
.node .r { display: block; font-family: ui-monospace, Consolas, monospace; font-size: 10.5px;
           color: #6b6f76; font-weight: 400; }
.node.ext { border-style: dashed; font-weight: 400; color: #6b6f76; }
.node.warn { border: 2px dashed ANNOT; }
.node .warn-note { display: block; font-family: ui-monospace, Consolas, monospace;
                   font-size: 10px; color: ANNOT; font-weight: 400; margin-top: 2px; }
.tp { margin: 18px 0 6px; }
.tp h3 { font-size: 13px; margin-bottom: 8px; }
.tp h3 .tpid { font-family: ui-monospace, Consolas, monospace; font-size: 10.5px;
               color: #6b6f76; font-weight: 400; margin-left: 8px; }
.tp .line { display: flex; flex-wrap: wrap; align-items: center; gap: 6px; }
.tp .stop { background: #e3e3e0; border: 1px solid #b9bab6; padding: 7px 12px;
            font-size: 12.5px; font-weight: 600; }
.tp .stop.ext { border-style: dashed; font-weight: 400; color: #6b6f76; }
.tp .hop { display: flex; flex-direction: column; align-items: center; max-width: 20ch; }
.tp .hop .arrow { color: ANNOT; font-weight: 700; }
.tp .hop .via { font-size: 10.5px; color: #6b6f76; text-align: center; line-height: 1.3; }
footer { margin-top: 40px; font-family: ui-monospace, Consolas, monospace; font-size: 11px;
         color: #6b6f76; }
""".replace("ANNOT", ANNOTATION_INK)


def esc(s):
    return html.escape(str(s if s is not None else ""))


def entry_of(spec):
    """v1.2.1: the return anchor is the ENTRY screen (entry_id, default hero_id) — hero carries
    the primary JTBD and is not necessarily the front door."""
    return spec.get("entry_id") or spec.get("hero_id")


def back_reach_set(spec):
    """Screens that can WALK BACK to the entry along non-external link_map edges (entry included).

    Render hint only (2026-07-08, loop-ia-ab SP): missing return paths are shown with a dashed
    ⚠ node on the screen map. Gate logic lives in validate_infospec.py, not here."""
    anchor = entry_of(spec)
    rev = {}
    for l in spec.get("link_map", []) or []:
        if l.get("external"):
            continue
        rev.setdefault(l.get("to"), set()).add(l.get("from"))
    seen, stack = {anchor}, [anchor]
    while stack:
        for src in rev.get(stack.pop(), ()):
            if src not in seen:
                seen.add(src)
                stack.append(src)
    return seen


def ordered_blocks(screen):
    """Deterministic strip order: scan_path first (in order), then remaining by tier, spec order."""
    blocks = screen.get("blocks", [])
    by_id = {b.get("id"): b for b in blocks}
    scan = [r for r in (screen.get("scan_path") or []) if r in by_id]
    rest = [b for b in blocks if b.get("id") not in scan]
    rest.sort(key=lambda b: (b.get("tier", 9), blocks.index(b)))
    return [by_id[r] for r in scan] + rest, {r: i + 1 for i, r in enumerate(scan)}


def render_screen(screen, hero_id, S, links=None):
    sid = screen.get("id", "?")
    star = (' <span class="star" title="%s">%s</span>' % (S["hero_title"], S["hero_tag"])
            ) if sid == hero_id else ""
    out = ['<section class="screen" id="screen-%s">' % esc(sid)]
    out.append('<h2>%s%s <span class="route">%s &middot; %s</span></h2>'
               % (esc(screen.get("title", sid)), star, esc(sid), esc(screen.get("route", ""))))
    out.append('<p class="task"><b>%s</b> &mdash; %s</p>'
               % (S["primary_task"], esc(screen.get("primary_task", ""))))
    # The archetype is DERIVED from the task above, so it is rendered right beside it: the gate
    # asks the human to judge the derivation, and a field they cannot see is a field they cannot
    # correct. Absent stays absent — no placeholder inviting someone to fill a guess in.
    if screen.get("archetype"):
        out.append('<p class="task"><b>%s</b> &mdash; %s</p>'
                   % (S["archetype"], esc(screen["archetype"])))
    out.append('<div class="strip">')
    blocks, scan_no = ordered_blocks(screen)
    for b in blocks:
        bid = b.get("id", "?")
        badge = ('<span class="scan">%d</span>' % scan_no[bid]) if bid in scan_no else ""
        out.append(
            '<div class="blk t%d">%s<span class="tags">tier %s &middot; %s<br>%s</span>'
            '<span class="label">%s</span><span class="hint">%s</span></div>'
            % (b.get("tier", 3), badge, esc(b.get("tier", "?")), esc(b.get("group", "")),
               esc(bid), esc(b.get("label", "")), esc(b.get("content_hint", ""))))
    out.append("</div>")
    flows = screen.get("within_page_flow") or []
    if flows:
        out.append('<div class="flows"><h3>%s</h3><ul>' % S["flow"])
        for f in flows:
            out.append('<li>%s <span class="arrow">&mdash;%s&rarr;</span> %s '
                       '<span class="rel">&middot; %s</span></li>'
                       % (esc(f.get("from")), esc(f.get("trigger")), esc(f.get("to")),
                          esc(f.get("relationship"))))
        out.append("</ul></div>")
    links = links or []
    arrivals = [l for l in links if l.get("to") == sid]
    departures = [l for l in links if l.get("from") == sid]
    out.append('<div class="flows"><h3>%s</h3><ul>' % S["arrivals"])
    if arrivals:
        for l in arrivals:
            out.append('<li>%s <span class="arrow">&rarr;</span> %s '
                       '<span class="rel">&middot; %s</span></li>'
                       % (esc(l.get("from")), esc(sid), esc(l.get("via"))))
    else:
        out.append('<li><span class="rel">%s</span></li>' % S["no_arrivals"])
    out.append("</ul></div>")
    if departures:
        out.append('<div class="flows"><h3>%s</h3><ul>' % S["departures"])
        for l in departures:
            ext = ' <span class="rel">%s</span>' % S["o_ext"].strip() if l.get("external") else ""
            out.append('<li>%s <span class="arrow">&rarr;</span> %s '
                       '<span class="rel">&middot; %s</span>%s</li>'
                       % (esc(sid), esc(l.get("to")), esc(l.get("via")), ext))
        out.append("</ul></div>")
    out.append("</section>")
    return "\n".join(out)


def render_map(spec, S):
    hero_id = spec.get("hero_id")
    entry = entry_of(spec)
    conv = spec.get("return_convention")
    conv_ok = isinstance(conv, str) and conv.strip()
    can_return = back_reach_set(spec)
    out = ['<section class="map"><h2>%s</h2>' % S["screen_map"]]
    if conv_ok:
        # declared convention satisfies the return rule globally -- render it for judgment
        # instead of per-node warnings (contract iii, v1.2)
        out.append('<p class="task"><b>%s</b> &mdash; %s</p>' % (S["return_conv"], esc(conv)))
    out.append('<div class="nodes">')
    for s in spec.get("screens", []):
        sid = s.get("id")
        cls = "node hero" if sid == hero_id else "node"
        star = "&#9733; " if sid == hero_id else ""
        tag = ""
        if sid == entry and entry != hero_id:
            tag = ' <span class="r">%s</span>' % S["entry_tag"]
        warn = ""
        if not conv_ok and sid != entry and sid not in can_return:
            cls += " warn"
            warn = '<span class="warn-note">&#9888; %s</span>' % S["warn_noback_entry"]
        out.append('<div class="%s">%s%s%s<span class="r">%s</span>%s</div>'
                   % (cls, star, esc(s.get("title", sid)), tag, esc(s.get("route", "")), warn))
    externals = {l.get("to") for l in spec.get("link_map", []) or [] if l.get("external")}
    for ext in sorted(externals):
        out.append('<div class="node ext">%s<span class="r">%s</span></div>'
                   % (esc(ext), S["external_exit"]))
    out.append("</div>")
    links = spec.get("link_map") or []
    if links:
        out.append('<div class="edges"><h3>%s</h3><ul>' % S["link_map"])
        for l in links:
            ext = ' <span class="rel">%s</span>' % S["o_ext"].strip() if l.get("external") else ""
            out.append('<li>%s <span class="arrow">&rarr;</span> %s '
                       '<span class="rel">&middot; %s</span>%s</li>'
                       % (esc(l.get("from")), esc(l.get("to")), esc(l.get("via")), ext))
        out.append("</ul></div>")
    out.append("</section>")
    return "\n".join(out)


def render_task_paths(spec, S):
    """Contract v1.1 subway view — PURE projection of task_paths[]; never derives a journey."""
    tps = spec.get("task_paths") or []
    if not tps:
        return ""
    screen_ids = {s.get("id") for s in spec.get("screens", [])}
    titles = {s.get("id"): s.get("title", s.get("id")) for s in spec.get("screens", [])}
    via = {}
    for l in spec.get("link_map", []) or []:
        via.setdefault((l.get("from"), l.get("to")), l.get("via", ""))
    out = ['<section class="map"><h2>%s</h2>' % S["task_paths"]]
    for tp in tps:
        path = tp.get("path") or []
        out.append('<div class="tp"><h3>%s<span class="tpid">%s</span></h3><div class="line">'
                   % (esc(tp.get("label", "")), esc(tp.get("id", ""))))
        for n, stop in enumerate(path):
            ext = stop not in screen_ids
            out.append('<span class="stop%s">%s%s</span>'
                       % (" ext" if ext else "", esc(titles.get(stop, stop)),
                          (' <span class="r">%s</span>' % S["tp_ext"]) if ext else ""))
            if n < len(path) - 1:
                out.append('<span class="hop"><span class="arrow">&rarr;</span>'
                           '<span class="via">%s</span></span>'
                           % esc(via.get((stop, path[n + 1]), "")))
        out.append("</div></div>")
    out.append("</section>")
    return "\n".join(out)


def render_board(spec, spec_name, S):
    parts = [
        "<!doctype html><html><head><meta charset=\"utf-8\">",
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">",
        "<title>IA board &mdash; %s (%s)</title>" % (esc(spec.get("product")),
                                                     esc(spec.get("register"))),
        "<style>%s</style></head><body>" % CSS,
        '<div class="banner">%s</div>' % S["banner"],
        "<h1>%s &mdash; %s</h1>" % (esc(spec.get("product")), S["board_title"]),
        '<p class="meta">%s</p>' % (S["meta"] % (esc(spec.get("register")),
                                                 len(spec.get("screens", [])),
                                                 esc(spec.get("hero_id")), esc(spec_name),
                                                 esc(spec.get("spec_version")))),
        render_map(spec, S),
        render_task_paths(spec, S),
    ]
    hero_id = spec.get("hero_id")
    screens = list(spec.get("screens", []))
    screens.sort(key=lambda s: 0 if s.get("id") == hero_id else 1)  # hero first, else spec order
    for s in screens:
        parts.append(render_screen(s, hero_id, S, spec.get("link_map") or []))
    parts.append("<footer>%s</footer></body></html>" % (S["footer"] % esc(spec_name)))
    return "\n".join(parts)


def render_outline(spec, spec_name, S):
    L = [S["o_title"] % (spec.get("product"), spec.get("register")), ""]
    L.append(S["o_note"] % (spec_name, spec.get("hero_id")))
    L.append("")
    links_all = spec.get("link_map") or []
    conv = spec.get("return_convention")
    conv_ok = isinstance(conv, str) and conv.strip()
    if conv_ok:
        L.append("> **%s**: %s" % (S["o_return_conv"], conv))
        L.append("")
    can_return = back_reach_set(spec)
    entry = entry_of(spec)
    for s in spec.get("screens", []):
        sid = s.get("id")
        hero = S["o_hero"] if sid == spec.get("hero_id") else ""
        noback = (S["o_noback"] if (not conv_ok and sid != entry
                                    and sid not in can_return) else "")
        L.append("## %s%s%s — `%s`" % (s.get("title"), hero, noback, s.get("route")))
        L.append("")
        L.append("- **%s**: %s" % (S["o_primary"], s.get("primary_task")))
        if s.get("archetype"):
            L.append("- **%s**: %s" % (S["archetype"], s.get("archetype")))
        scan = s.get("scan_path") or []
        if scan:
            L.append("- **%s**: %s" % (S["o_scan"], " → ".join(scan)))
        L.append("- **%s**:" % S["o_blocks"])
        for b in s.get("blocks", []):
            L.append("  - `[T%s · %s]` **%s** (`%s`) — %s"
                     % (b.get("tier"), b.get("group"), b.get("label"), b.get("id"),
                        b.get("content_hint")))
        flows = s.get("within_page_flow") or []
        if flows:
            L.append("- **%s**:" % S["o_flow"])
            for f in flows:
                L.append("  - %s —%s→ %s · %s"
                         % (f.get("from"), f.get("trigger"), f.get("to"), f.get("relationship")))
        arrivals = [l for l in links_all if l.get("to") == sid]
        departures = [l for l in links_all if l.get("from") == sid]
        if arrivals:
            L.append("- **%s**: %s" % (S["o_arrivals"],
                     "; ".join("%s → · %s" % (l.get("from"), l.get("via")) for l in arrivals)))
        if departures:
            L.append("- **%s**: %s" % (S["o_departures"],
                     "; ".join("→ %s%s · %s" % (l.get("to"),
                               S["o_ext"] if l.get("external") else "", l.get("via"))
                               for l in departures)))
        L.append("")
    links = spec.get("link_map") or []
    if links:
        L.append(S["o_links"])
        L.append("")
        for l in links:
            ext = S["o_ext"] if l.get("external") else ""
            L.append("- %s → %s%s · %s" % (l.get("from"), l.get("to"), ext, l.get("via")))
        L.append("")
    tps = spec.get("task_paths") or []
    if tps:
        L.append(S["o_task_paths"])
        L.append("")
        via = {}
        for l in links:
            via.setdefault((l.get("from"), l.get("to")), l.get("via", ""))
        for tp in tps:
            path = tp.get("path") or []
            L.append("- **%s** (`%s`): %s" % (tp.get("label"), tp.get("id"), " → ".join(path)))
            for n in range(len(path) - 1):
                L.append("  - %s → %s · %s"
                         % (path[n], path[n + 1], via.get((path[n], path[n + 1]), "?")))
        L.append("")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description="Render IA info-spec -> board.html + outline.md")
    ap.add_argument("spec", help="path to info-spec.json")
    ap.add_argument("--out", help="output dir (default: <spec-dir>/board)")
    ap.add_argument("--lang", choices=sorted(STRINGS), default="en",
                    help="chrome language (content comes verbatim from the spec)")
    args = ap.parse_args()

    try:
        with open(args.spec, encoding="utf-8") as f:
            spec = json.load(f)
    except (OSError, json.JSONDecodeError) as e:
        print("UNREADABLE: %s" % e)
        return 2

    S = STRINGS[args.lang]
    out_dir = args.out or os.path.join(os.path.dirname(os.path.abspath(args.spec)), "board")
    os.makedirs(out_dir, exist_ok=True)
    spec_name = os.path.basename(args.spec)

    board_path = os.path.join(out_dir, "board.html")
    with open(board_path, "w", encoding="utf-8") as f:
        f.write(render_board(spec, spec_name, S))
    outline_path = os.path.join(out_dir, "outline.md")
    with open(outline_path, "w", encoding="utf-8") as f:
        f.write(render_outline(spec, spec_name, S))

    print("wrote %s" % board_path)
    print("wrote %s" % outline_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
