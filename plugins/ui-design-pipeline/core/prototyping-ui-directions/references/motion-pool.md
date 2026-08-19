# Motion pool (Batch 2 motion reference) — optional base cases

> ⚠️ **This is a fallback, not a menu.** Reach for it only when you cannot think of better motion, as
> a starting point; you are **not required** to pick from it.
> Used at `prototyping-ui-directions` **Batch 2 (motion treatment)** and at `anchor-prototype-wave`
> §Authoring: motion. Every entry carries a **GSAP implementation path** (pointing at a `gsap-*` skill).
> Two tiers: **text effects** (#1–#10, how a piece of text moves) and **whole-page scroll
> choreography** (#11–#20, how a whole page is choreographed to scroll).
>
> Naming: #1–#10 are **text-reveal effects** (how text *moves*), **not typefaces**.
> For the faces themselves (family selection) that is Batch 1 visual work — see `font-pool.md`.
>
> **⚙ Execution registry** (the 2026-07-10 motion-score work): every numbered effect row carries a
> `【⚙执行册】` badge, meaning there is exactly one machine-readable execution record for it in
> `execution-registry.json` (schema in `execution-contracts.md`; for unnumbered rows such as
> site-level anchors the badge carries the registration id inline). This pool's Markdown remains the
> single source of truth for description, provenance and human verdicts; an agent proposing a
> candidate must first pass it through `../scripts/resolve_candidates.py`, and the sync check is
> `../scripts/check_registry_sync.py`. Adding or graduating an entry means all three together:
> record, badge, and a green sync.

## Text effects (text-reveal) #1–#10

> **All ten graduated 2026-07-11 🎉 (motion-materialize batch A)**: every one was rebuilt in the lab
> and collected into **a single component library**, ✅`material/text-reveal-gallery` (manifest +
> `?only=<id>` single-effect preview + a pluggable `build(id, el)` / `play(id)` interface — pull it
> out and attach it to any text element; each effect matches the primary approach named in its row;
> VERIFY/TAGS live inside the piece). Five-layer tags per entry (⚡ = costed against the real code):
> #1 🏷: driver=load/replay · mechanism=SplitText chars stepped `.set` + a pseudo-caret following character by character + `steps(1)` blink · carrier=component / any text element · content=any short phrase · register=notes/demo/AI-generated feel · ⚡light
> #2 🏷: driver=load/replay · mechanism=`filter:blur(16→0)` + autoAlpha per-word stagger · carrier=component · content=any short phrase · register=suspense reveal / concept opener · ⚡light (transient blur)
> #3 🏷: driver=load/replay · mechanism=a timeline of 6 hard-cut keyframes on x/skewX + red-cyan twin clones with `mix-blend:screen` and clip band jumps = RGB separation · carrier=component · content=any short phrase · register=tech/AI/cyber · ⚡light (transient)
> #4 🏷: driver=load/replay · mechanism=the official **ScrambleTextPlugin** · carrier=component · content=any short phrase · register=information decoding · ⚡light
> #5 🏷: driver=load/replay · mechanism=`rotationX:-92→0` + `transformPerspective:620` + bottom-edge origin + back.out · carrier=component · content=any short phrase · register=contrast / reversal / feature page · ⚡light
> #6 🏷: driver=load/replay · mechanism=3 clip-path inset bands, clones sliding in alternately at x±84 then aligning (overlapping by a band to avoid seams; the final frame swaps back to the original) · carrier=component · content=any short phrase · register=high-impact headline · ⚡light
> #7 🏷: driver=load/replay · mechanism=**DrawSVGPlugin** stroking `0%→100%` per stroke + a bold layer fading in = "fill up" · carrier=SVG skeleton lettering (changing the word means redrawing the paths; the piece ships a NOVA 5-path) · content=short word · register=brand lettering / handwriting / art · ⚡light
> #8 🏷: driver=load/replay · mechanism=a 260% `background-clip:text` gradient swept via `backgroundPosition`, leaving the text lit (wrapped in `@supports`) · carrier=component · content=any short phrase · register=keyword emphasis / cover · ⚡light
> #9 🏷: driver=load/replay · mechanism=`elastic.out(1,0.3)` with y46 + scaleY1.55 stretch-and-settle (duration/easing read from `--tr-*` tokens) · carrier=component · content=any short phrase · register=lively / short-video transition feel · ⚡light
> #10 🏷: driver=scroll-scrub · mechanism=ScrollTrigger with 3 cloned layers at `yPercent ±60/±30/±12` moving at three speeds · carrier=a text block passing through the viewport (`?only` gives it a 340vh runway; `build()` accepts a scroll container) · content=large headline · register=refined opener / cover · ⚡light

| # | Effect | Feel | Suits | GSAP implementation (which skill) |
|---|---|---|---|---|
| 1 | **Typewriter** | Characters appear one by one, as if typed live, with a caret | Notes / demos / an AI-generated feel | `gsap-plugins` SplitText(chars) + stagger, or an object `onUpdate` slicing the substring (`gsap-core`); ✅`material/text-reveal-gallery` `?only=typewriter` 【⚙执行册】 |
| 2 | **Blur In** | Out of focus into focus, like a lens finding it | Suspense reveals, concept openers | `gsap-core` animating `filter:"blur(..)"` + `autoAlpha` (CSSPlugin can animate filter); ✅`material/text-reveal-gallery` `?only=blur-in` 【⚙执行册】 |
| 3 | **Glitch** | A brief displacement / jitter / chromatic split, then recovery | Tech, AI, cyber | `gsap-timeline` sequencing x / `skewX` / clip + RGB separation; short, many keyframes; ✅`material/text-reveal-gallery` `?only=glitch` 【⚙执行册】 |
| 4 | **Scramble** | Random characters first, resolving into the real word | Information decoding, revealing a complex idea | `gsap-plugins` **ScrambleTextPlugin**; ✅`material/text-reveal-gallery` `?only=scramble` 【⚙执行册】 |
| 5 | **Flip** | A card turning over — a distinct sense of switching | Contrast, a reversal of view, feature pages | `gsap-core` `rotationX` + `transformPerspective`; or `gsap-plugins` **Flip** for a layout-state change; ✅`material/text-reveal-gallery` `?only=flip-in` 【⚙执行册】 |
| 6 | **Slice** | Cut into horizontal bands that slide in offset, then align | High-impact headlines, visual packaging pages | `gsap-plugins` SplitText / clip-path banding + `gsap-core` staggered x; ✅`material/text-reveal-gallery` `?only=slice` 【⚙执行册】 |
| 7 | **Stroke Draw** | The outline is drawn stroke by stroke, then fills | Brand lettering, handwritten headlines, art | `gsap-plugins` **DrawSVGPlugin** (needs SVG letter outlines); ✅`material/text-reveal-gallery` `?only=stroke-draw` 【⚙执行册】 |
| 8 | **Highlight Sweep** | A band of light or colour sweeps across and lights the text | Keyword emphasis, cover headlines | `gsap-core` animating `backgroundPosition`, or sweeping a pseudo-element + `gsap-timeline`; ✅`material/text-reveal-gallery` `?only=highlight-sweep` 【⚙执行册】 |
| 9 | **Elastic** | A slight stretch and settle on entry | Lively, a short-video transition feel | `gsap-core` with ease `elastic.out(1,0.3)` / `back.out(1.7)`; ✅`material/text-reveal-gallery` `?only=elastic` 【⚙执行册】 |
| 10 | **Depth Shift** | Front and back layers move at different speeds — depth | Refined openers, personal pages, presentation covers | `gsap-scrolltrigger` with different `y` speeds per element + `scrub` (parallax); ✅`material/text-reveal-gallery` `?only=depth-shift` 【⚙执行册】 |

**Usage note**: the 2-3 Batch 2 variants keep the visual **completely frozen (= the LEAD)** and pull
apart on the motion axis alone — for example "load-in only (1+9) vs scroll-driven depth (10) vs heavy
choreography (3+6+8 combined)". Every one of them must:
- go through the `prefers-reduced-motion` branch of `gsap.matchMedia()` (showing a still),
- read duration and easing from the chassis motion tokens rather than hardcoding them,
- degrade gracefully: the content is visible even if the script never runs.

> Most of these are doable in plain HTML (GSAP is framework-agnostic); SplitText / ScrambleText /
> DrawSVG / Flip are all free now (see `gsap-plugins`).

## Whole-page scroll choreography #11–#20

> This tier governs "**how a whole page is choreographed to scroll**" (pinned scenes / colour
> narrative / stacked cards / layout-state switching) and complements "how a piece of text moves"
> above.
> Added 2026-07-03 (gsap-ecosystem Track B, approved wholesale by the user). The reason: the
> jesus-site rebuild proved the stack covers GSAP/DOM-class effects completely, but the pool had no
> ammunition in this tier, so the "heavy choreography" endpoint of Batch 2 had nothing but the
> model's imagination.
> Provenance: the whole tier is `web-verified` — Codrops/tympanus tutorials (real GitHub source) or
> **official GreenSock CodePen demos**. Learning sources are always mature external code.
> Historical note: the patterns for #11–14 and #20 were first observed on the external site Seamora
> (the blind jesus-site rebuild demonstrated "the stack can do this"),
> and on 2026-07-05, at the user's request, all of them were re-anchored to external real source
> ("a rebuild that has not been through several rounds of refinement is not a learning source"). Only
> #12's full choreographic combination has no tutorial, so it is anchored to an official mechanism
> demo with the combination still marked `seamora-observed`.
> Who looks (the consumer axis, see `reference-sources.md` §0): the whole tier is 🤝 split work — a
> **human** judges how the motion feels from the demo or the result; I read the source and build.
> **All ten graduated 2026-07-11 🎉 (motion-materialize batch B)**: each became its own piece
> (VERIFY/TAGS inside it; two pool rows were corrected against the code evidence — #18's source has
> no SplitText [hand-written spans consuming CSS `calc(var(--progress))`], and #19's source has no
> wave or checkerboard order [it is horizontal blinds / shuffled cells / vertical blinds / column
> sweep]). Five-layer tags per entry (⚡ = costed against the real code):
> #11 🏷: driver=scroll-scrub · mechanism=an explicit fromTo zone table (previous colour → this colour) + `immediateRender:false` + flipping `is-dark` past the halfway point · carrier=a whole-page room sequence (chassis when a zone holds a persistent colour state across sections) / a single-chapter sectional · content=any long segmented page · register=longform narrative · ⚡light (paint-bound but bounded)
> #12 🏷: driver=scroll-scrub · mechanism=a pinned long section with a multi-target timeline (hero scale / yPercent / corner radius → fade out) + a wordmark sweeping the other way via position parameters + the official registerEffect per-character zoom (zoom-in only; the clamped domain scale<1 inversion is verified) · carrier=a pinned hero long section (`+=150%`) · content=a hero card + a giant wordmark slot · register=strong-opener brand site · ⚡light (corner-radius paint called out)
> #13 🏷: driver=scroll-scrub · mechanism=columns at differential speed `yPercent=-pos*10` + per-tile `±depth×vh` drift + slight rotation (the demo2 component) + a caption cross-fading across 4 windows (an authored addition; none of the 10 source variants has a caption) · carrier=a long section tile wall + a fixed caption layer · content=an image wall · register=work wall / case round-up · ⚡light
> #14 🏷: driver=scroll-scrub · mechanism=CSS sticky card stacking + a per-card timeline receding (scale .95 + brightness 50% + corner radius 40); "trigger = the next card" is the source's own `trigger: self + end:'+=100%'` geometry (checked against 15 variants) · carrier=a sequence of cards going sticky in turn · content=step / feature cards · register=methodology walkthrough · ⚡light
> #15 🏷: driver=scroll-scrub · mechanism=a pinned stage + a three-phase master timeline per character (columnar reveal → zoom split → copy floats up, forking by scroll direction with `overwrite:true`) + ScrollSmoother · carrier=a pinned long-section stage · content=an image grid + copy · register=product narrative / capability showcase · ⚡light
> #16 🏷: driver=scroll-scrub · mechanism=a class defines the end state → `Flip.getState` → `Flip.to` + pin + scrub (9 parameter variants: absoluteOnLeave / absolute + 900% long run / scale:false / stagger / 80-item) · carrier=**dual-footprint (user ruling, 2026-07-11)**: a single gallery section = sectional (preferred), a whole-page continuous gallery architecture = chassis deployment · content=an image group + captions · register=portfolio view switching · ⚡medium (scale:false puts it in the reflow tier, and large batches of filter put it in the paint tier)
> #17 🏷: driver=scroll-scrub · mechanism=`Flip.fit` per waypoint fed into one scrubbed timeline (`+=0.5` between legs, clamped at both ends, a full re-capture on resize revert) + a five-part choir of supporting per-value tweens · carrier=a cross-section waypoint sequence (z-index choreography is the key to passing behind and in front) · content=a single protagonist element (image / card / device) · register=a product protagonist that runs through the page · ⚡light
> #18 🏷: driver=scroll-scrub · mechanism=pin + `onUpdate` writing the CSS var `--progress` (double easing via parseEase): 6 layers of the same image on a scale ladder `1/.85/.6/.45/.3/.15` + blur dispersing + a title span yielding the other way with `calc(∓66vw)` + ScrollSmoother `normalizeScroll` · carrier=a pinned hero · content=one image in many layers (changing the image means changing every layer) · register=cinematic opener · ⚡medium (6 full-screen masked layers compositing)
> #19 🏷: driver=scroll-scrub (2.0-2.5 trailing) · mechanism=an SVG `<mask>` rect group staggering open to reveal, with 4 orders switchable per piece via `?pattern=` · carrier=a full-screen image chapter-transition sequence · content=a large image · register=chapter transition / gallery · ⚡medium (the mask rasterises per frame)
> #20 🏷: driver=scroll-scrub · mechanism=`SplitText.create(words,lines+autoSplit+onSplit returning the animation)`, resize-safe (the GggpRoB form) + fromTo from dark .15 to bright 1 + stagger (the JjmMLqo values) · carrier=long paragraphs (each with its own trigger) · content=manifesto / long copy · register=manifesto passage · ⚡light

| # | Effect | Feel | Suits | GSAP implementation (which skill) | provenance |
|---|---|---|---|---|---|
| 11 | **Background colour narrative** bg-morph zones | The page reads as walking through several "rooms": the background colour eases as you scroll and restores exactly on the way back up | Longform narrative / brand story / scrollytelling | `gsap-scrolltrigger` scrub + `gsap-core` with an explicit fromTo zone table (`immediateRender:false`, flipping the `is-dark` class past halfway); ✅`material/bg-morph-zones` | web-verified (official [XWQzYaR](https://codepen.io/GreenSock/pen/XWQzYaR) data-attr version / [PoxvEwK](https://codepen.io/GreenSock/pen/PoxvEwK) sections version) 【⚙执行册】 |
| 12 | **Hero shrink-away exit** | A full-screen hero shrinks into a small receding card as you scroll (scale + corner radius + fade), and a giant wordmark sweeps in to fill the gap | Strong-opener brand sites / portfolios | `gsap-timeline` + `gsap-scrolltrigger` scrub over a long section: hero scale / yPercent / borderRadius → opacity; position parameters send the wordmark drifting the other way; ✅`material/hero-shrink-exit` | web-verified · mechanism (official pin+scale+scrub [YzbPYMx](https://codepen.io/GreenSock/pen/YzbPYMx) / [mdRaRrN](https://codepen.io/GreenSock/pen/mdRaRrN) zoom-by-section); the choreographic combination is seamora-observed, with no full tutorial 【⚙执行册】 |
| 13 | **Pinned depth parallax collage** | Inside a pinned long section, tiles drift vertically at speeds set by a depth coefficient, with slight rotation, while a centre caption cross-fades | Work walls / case round-ups | `gsap-scrolltrigger` long-section scrub + `gsap-core` per-tile fromTo (function-based `y=±depth×vh`); ✅`material/pinned-depth-collage` | web-verified ([OnScrollColumnsRows](https://github.com/codrops/OnScrollColumnsRows), columns/rows scrolling at different speeds) 【⚙执行册】 |
| 14 | **Sticky card deck** | Cards slide up and cover the previous one; the covered card recedes and dims | Methodology steps / feature walkthrough | CSS `position:sticky` stacking + `gsap-scrolltrigger` scrub (trigger = **the next card**, scale + brightness receding); ✅`material/sticky-stack-deck` | web-verified ([StickySections](https://github.com/codrops/StickySections/) sticky stacking/collapsing) 【⚙执行册】 |
| 15 | **Pinned scene stages** scroll-as-time stage | The stage stays fixed and scrolling advances "time": a master timeline in phases (reveal → zoom split → copy floats up), or highlighting switched by progress window | Product narrative / capability showcase long sections | `gsap-scrolltrigger` pin/fixed stage + a scrubbed master timeline (`onUpdate` calling setActive per progress window); for smooth scrolling use `gsap-plugins` ScrollSmoother; ✅`material/pinned-scene-stages` | web-verified ([sticky-grid-scroll](https://github.com/theoplawinski/codrops-sticky-grid-scroll)) 【⚙执行册】 |
| 16 | **Pinned layout-state switch** Flip layout switch | The same set of elements rearranges between two layouts as you scroll (grid → fullscreen, scattered → stacked) | Portfolio view switching / comparison displays | `gsap-scrolltrigger` pin + `gsap-plugins` **Flip** (a class defines the end state, Flip tweens the layout difference); ✅`material/flip-layout-switch` | web-verified ([ScrollBasedLayoutAnimations](https://github.com/codrops/ScrollBasedLayoutAnimations/)) 【⚙执行册】 |
| 17 | **One element across sections** one-element journey | A single element "moves house" between waypoints as you scroll, handing off seamlessly from section to section | A product protagonist running through the page (one device or card telling the story across sections) | `gsap-plugins` **Flip.fit** + `gsap-scrolltrigger` scrub per waypoint; ✅`material/one-element-journey` | web-verified ([OneElementScroll](https://github.com/codrops/OneElementScroll)) 【⚙执行册】 |
| 18 | **Layered zoom reveal** | Many layers of the same image scale up in steps while blur disperses — a trailing zoom, like a lens pushing in | Cinematic openers / image-led heroes | `gsap-plugins` ScrollSmoother + `gsap-scrolltrigger` (a CSS var `--progress` syncs the layer scales; the title span consumes `calc()` to move the other way — **correction 2026-07-11: the source has no SplitText**); ✅`material/layered-zoom-reveal` | web-verified ([telescope-zoom](https://github.com/joffreysp/telescope-zoom)) 【⚙执行册】 |
| 19 | **SVG mask blinds reveal** | A full-screen image is opened by a group of SVG mask rectangles in one of four orders — **horizontal blinds / shuffled cells / vertical blinds / column sweep** (**correction 2026-07-11: the source's 4 variants have no wave or checkerboard**) — scrubbed with a trail | Chapter transitions / image galleries | `gsap-scrolltrigger` (scrub 2.0–2.5) + staggered SVG `<mask>` rect groups (`gsap-core`); ✅`material/svg-mask-blinds` | web-verified ([Scroll-Transition](https://github.com/Hiro-kiii/Scroll-Transition/)) 【⚙执行册】 |
| 20 | **Scrubbed word brighten** paragraph brighten | A long paragraph lights up word by word as you scroll — lit as far as you have read, and reversible (a cross-tier case: a text effect driven by scroll progress) | Manifestos / declarations / long copy | `gsap-plugins` SplitText + `gsap-scrolltrigger` scrub (staggered opacity); ✅`material/scrub-word-brighten` | web-verified (official [JjmMLqo](https://codepen.io/GreenSock/pen/JjmMLqo) scrub+stagger / [GggpRoB](https://codepen.io/GreenSock/pen/GggpRoB) AutoSplit resize-safe form) 【⚙执行册】 |

**Usage note**: the three disciplines from #1–#10 (a matchMedia reduced-motion branch / values from
the chassis motion tokens / graceful degradation) apply to this tier as well. Two more:
- **Hover effects must be interrupt-safe** (the class of bug the user caught in testing on
  2026-07-08: sweep the pointer quickly and the element sticks out instead of returning): give each
  target **one persistent reversible timeline** (built once, `play()` on enter, `reverse()` from the
  current progress on leave), never a one-shot stagger fired on hover; for a simple two-state tween
  use `overwrite:"auto"`.
- **Lift/displacement hovers must not expose what is behind**: put a **motionless twin backdrop** of
  the same colour and shape behind the lifted element (inset:0, never transformed) so the vacated
  pixels always have a floor, instead of depending on the arithmetic of neighbours overlapping
  (proved in R-D v3: 6/6 folders with zero white showing through).
- A pinned / 300vh long section is **heavy choreography**: at most one main choreographed scene per
  page, never pin the whole thing (WHEN and restraint remain `taste-skill` §8's jurisdiction);
- Lenis is not adopted for smooth scrolling: `gsap-plugins` **ScrollSmoother** already covers the
  equivalent capability (lab decision, 2026-07-03).

> Track A note (not in the pool): the scroll→canvas progress bridge (jesus-site's
> `src/scroll/stack.ts` feeding ScrollTrigger progress into a particle field's `setProgress(p)`)
> plus the Codrops article "[How to Build Cinematic 3D Scroll Experiences with GSAP](https://tympanus.net/codrops/2025/11/19/how-to-build-cinematic-3d-scroll-experiences-with-gsap/)"
> = `webgl-readonly-heavy`, saved for Track A (Three.js capability research, see LEDGER).

## Pointer-driven, loading and entrance #21–#22 (added from the 2026-07-08 rebuild wave-1, **the first entries with a compute tier**)

> Both went through a lab rebuild plus live verification plus a human verdict (0 console errors /
> reduced-motion branch / touch degradation); the results were promoted into the **tracked
> `testbed/material/`** (user decision 2026-07-08, same retention logic as the chassis — see its
> README).
> **🏷 Graduated entries carry mechanism tags; the agent consumption contract (filter chain / no two
> pieces with the same mechanism in one batch / write down the reason / enumerate first, with row
> order carrying no priority) is `threed-pool.md` §mechanism tags (canonical at library level), and
> this pool follows it too.**
> #21 🏷: driver=pointer · mechanism=dual-speed quickTo following + a live coordinate readout (◎ ring and ✚ crosshair variants) · carrier=irrelevant (a whole-page overlay) · content=irrelevant · register=instrument / dev-tool / brutalist.
> #22 🏷: driver=load/replay (portable to hover) · mechanism=an SVG goo filter fusing shapes (blur + colorMatrix) · carrier=loader / entrance (portable to nav and micro-interactions) · content=any vector shape · register=organic / playful.

| # | Effect | Feel | Suits | Implementation (source + lab demo) | Compute tier | provenance |
|---|---|---|---|---|---|---|
| 21 | **Coordinate cursor** (two variations: ◎ ring / ✚ crosshair [the user asked for this one on 2026-07-08]) | A dot and a ring follow at two speeds, live XY coordinates read out, and it deforms on hover — the whole page feels like an instrument; the crosshair version draws full-width thin lines crossing at the pointer | dev-tool / instrument / brutalist register | `gsap.quickTo` at two speeds (official docs; the vendored `gsap-performance` has the same pattern); **the matchMedia conditions must be mutually exclusive and exhaustive** (coarse pointer / fine without reduced motion / fine with reduced motion — independent booleans all false means it silently never starts); **centre it with one mechanism only** (a CSS negative margin stacked on GSAP xPercent gives a constant half-size offset — a bug caught in human review); lab demo `testbed/material/cursor-xy/` (probe verified at 0px in both modes) | **light** (pure transform; measured headless at 223fps, which proves the mechanism rather than being a vsync number) | web-verified (GSAP docs) + site anchor Studio Dialect 【⚙执行册】 |
| 22 | **Goo loader entrance** | Metaball blobs fuse while loading → gather and settle → the content is revealed | Loading / section entrance; organic, brand-forward | An SVG goo filter (feGaussianBlur→feColorMatrix, **canonical = the CSS-Tricks Gooey Effect**) + a GSAP timeline (structure follows the Codrops Jump Loader — note that tutorial itself has **no** goo technique; the goo recipe comes from CSS-Tricks); lab demo `testbed/material/goo-loader/` | **light-medium** (an SVG filter rasterises per frame — **only ever cover a small box with the filter, never the page**; fallbacks: fewer blobs / shrink the filter box / drop the filter) | web-verified (CSS-Tricks + Codrops; the user asked for the goo direction on 2026-07-08) 【⚙执行册】 |

## Video / canvas overlay #23 (promoted from arknights-hero, 2026-07-09)

| # | Effect | Feel | Suits | Implementation | Compute tier (initial) | provenance |
|---|---|---|---|---|---|---|
| 23 | **Offline-baked tracking lockbox overlay** | A box, crosshair, leader line and number chase a target across the video; EMA lag gives a deliberate "sensor tracking" feel; colours switch live with page state; **v2 has two tiers**: a primary always-on layer, and a hover tier (kind:'hover') where a temporary lock appears only as the pointer approaches, distinguished by a dashed box and fading out on leave | The "target lock / HUD" layer over a video or canvas hero; military / archival / analysing register; the hover tier gives you "hover to lock a single target" | Offline cv2 (luminance threshold → connected-component centroid → nearest-neighbour association) bakes keyframes into a JS array, so there is **zero CV at runtime**: `video.currentTime` → frame number → linear interpolation → inverse cover-fit mapping → EMA smoothing; DOM elements positioned by transform + `classList.toggle` for state colour; a hover hit is pointer-to-box-centre distance < max(110, box edge · 0.9); lab demo `testbed/material/blueprint-video-wipe/` (the tickOverlay section plus the header note). ⚠ A DOM overlay will collide with text burned into the footage — check what UI the material already carries before overlaying | **light** (DOM transform ×N; the heavy work is all in the offline bake) | **lab-built** (2026-07-09, signed off by the user; the hover tier was approved the same day; the extraction tooling is recorded in that piece's VERIFY.md) 【⚙执行册】 |

## Entrance and scroll narrative #24–#25 (arknights-hero phase two, 2026-07-09, approved item by item)

| # | Effect | Feel | Suits | Implementation | Compute tier (initial) | provenance |
|---|---|---|---|---|---|---|
| 24 | **Light-bar logo reveal** | A curtain of vertical light bars (dense at the centre, sparse at the edges, in two groups top and bottom, flickering fast) parts from the middle to reveal the wordmark; an underline sweeps out and small type follows; at about 3s the bars converge and the whole thing fades away to hand the stage over | Logo / title entrances on brand sites, game sites and launch pages; tech / archival register | 26 gradient light-bar divs (randomised width, height and position, power-law biased toward the centre) + a GSAP timeline: bars scaleY staggered with `from:'random'` + repeatRefresh flicker; the wordmark revealed by `clip-path: inset` with letter-spacing drawing in; on completion `root.remove()` deletes itself; reduced motion shows it statically once and fades opacity; `?logohold` freezes it for debugging; lab demo `testbed/material/blueprint-video-wipe/` (the initLogo section; mechanism referenced from the original footage at t≈10.7–11.3) | **light** (pure DOM/CSS transform + opacity, one-shot, deletes itself with nothing left behind) | **lab-built** (2026-07-09, approved by the user) 【⚙执行册】 |
| 25 | **Scroll-driven exploded view** | Scrolling down explodes the parts apart in a staggered sequence (each one arriving with a leader line and a number appearing), scrolling back reassembles them; the camera eases in as it separates; hovering a part thickens and highlights it; an ASM % counts live | The signature structural display on a hardware or product page; commerce product teardown narrative; archival / engineering register | Parts are a data table of `{shape, explode offset + rotation, callout anchor}`; scroll p → each part interpolated with a stagger of `smoothstep(clamp(p·1.18−i·0.022))`; callouts ride inside the part group and fade in past pi>0.72; `scrollRestoration=manual` guarantees a refresh starts assembled; reduced motion freezes it fully exploded; plain vanilla, zero dependencies; lab demo `testbed/material/exploded-diagram/` (mechanism referenced from the original footage at t≈17). **⚠ Asset slot convention (the user's ruling): the demo art is a placeholder hand drawing that only proves the mechanism, and commercial use must replace it** — ① a designer's layered SVG (replacing the PARTS table) ② cut-out PNGs (swap path for `<image>`) ③ real 3D goes to three (a separate track); a semi-automatic cv2 extraction experiment scored as a 60-point prototype approach (recorded in VERIFY) | **light** (SVG transform ×13, no continuous animation, zero cost at rest) | **lab-built** (2026-07-09, mechanism approved; the art is a placeholder, to be replaced commercially) 【⚙执行册】 |

## Category index interaction #26 (graduated site anchor 2026-07-08, numbered by the user 2026-07-11)

| # | Effect | Feel | Suits | Implementation | Compute tier | provenance |
|---|---|---|---|---|---|---|
| 26 | **Folder drawer index** folder-works spotlight | Hover = spotlight: the others fade back, the folder under the pointer lifts slightly (the drawer stacking order does the rest) and a fanned preview peeks out; click expands | Category / work indexes — any "drawer-style category entrance"; playful editorial / magazine feel | Spotlight fading the others + a slight lift + a fanned preview + a **twin backdrop against show-through** (a motionless same-colour same-shape pad at inset:0; proved in R-D v3, 6/6 with zero white showing); lab demo `testbed/material/folder-works/` (v3) | **light** (pure DOM transform/opacity) | Promoted from the site anchor Wildy Riftian: learn the metaphor, do not copy the implementation (it is a Framer artefact, a different stack from the lab's); rebuilt in the lab + a human verdict over two rounds of screenshot evidence (2026-07-08) 【⚙执行册】 |

## General DOM reveal/dissolve #27 (lab-built, human-approved 2026-07-11 — fed back from the Averonel new-flow evaluation run)

| # | Effect | Feel | Suits | Implementation | Compute tier | provenance |
|---|---|---|---|---|---|---|
| 27 | **CSS grid mask dissolve** grid-mask dissolve | A tile grid in the same colour as the paper goes out tile by tile along a column sweep with per-tile jitter (reveal) or lights up (dissolve), so the content melts into or out of the paper at "pixel block" scale | Entrance reveal / exit dissolve for any HTML component (image, record or plain text) — the general DOM approximation of M-38's pixel-scan language; technical / archival register | Pure DOM: JS builds a ~20px tile grid overlay (doubling the cell size automatically past 2600 tiles) + CSS steps keyframes (45% out → 62% one flash back → 100% out) + a column baseline delay ×0.028s + 0.22s random jitter; triggered by IO on entering the viewport; the whole layer is not rendered under reduced motion; ✅`material/css-grid-mask-reveal` | **light** (pure DOM opacity, with a tile-count backstop) | **lab-built, human-approved** (2026-07-11, produced by the Averonel evaluation run; the user's words were 「这个css可以promote 进素材库，进ledger」; M-38's shader hash flicker is **honestly downgraded** to a steps flash-back) 【⚙执行册】 |

## Register→bento structural component #28 (lab-built, human-approved 2026-07-18 — fed back from the Averonel option-2 run)

| # | Effect | Feel | Suits | Implementation | Compute tier | provenance |
|---|---|---|---|---|---|---|
| 28 | **bento-register card wall disclosure** register→bento card wall | Every row of a flat table or register is promoted into a card with weight: a bento grid span rhythm + click to expand detail (native grid-rows 0fr→1fr transition, singleOpen enforcing "review one at a time"); editorial typography reads as a statement card, civic typography reads as an archive card — **the skin is entirely in the consumer's CSS; the module has no visual of its own** | Structural promotion of a sparse flat table (terms, specifications, service lists) — closer to a hero-grade display than a data row; re-tokenable for register / archival / editorial chassis alike | A structural component, not choreography: `bento-register.js` handles only click/keyboard disclosure coordination + aria (expanded/controls) + mutual exclusion + teardown; **no GSAP**, CSS-first (a `grid-template-rows` transition; reduced motion turns off the transition while disclosure still works); layout is the consumer's CSS grid recipe; ✅`material/bento-register` | **light** (pure DOM, zero RAF) | **lab-built, human-approved** (2026-07-18, produced by the Averonel option-2 run; the lab demo passes 22/22 headless; the `bento-audition` temperament try-out compared two versions on real chassis, and the user's words were 「**同意variation a**」 = the editorial statement-card direction; ⚠ expanding changes the owner's height, so it is a structural piece and **never an atomic candidate** — the component-tier contract is contracts §6) 【⚙执行册】 |

## Text effect · external rebuild #29 (react-bits rebuild 2026-07-19, eyeballed by the user)

| # | Effect | Feel | Suits | Implementation | Compute tier | provenance |
|---|---|---|---|---|---|---|
| 🗑 29 | **Character slide shuffle** char slide shuffle | Each character slides a strip of copies past a clipping window before landing on the real one, odd and even batches staggered; optional scrambled copies + colour gradient / random delay / looping / re-shuffle on hover | Headline and phrase entrances; tech / archival / pixel-arcade register; complements #4 Scramble (characters **slide past** rather than being replaced in place) | Per character an overflow:hidden fixed-width wrap + a translating strip ([copies × rolls + the real character], reordered for right/down with a head pad and tail pad), SplitText chars (smartWrap) + ScrollTrigger entrance (threshold/rootMargin converted) + evenodd (the even batch enters at 0.7 of the odd batch) / random maxDelay; colorFrom→To on the same beat; on completion cleanupToStill restores the static text and armHover re-shuffles; 🗑 withdrawn (was `material/char-slide-shuffle`) (a 4-row parameter-axis demo) | **light** (pure transform; character count × (rolls+1) DOM clones, cleaned up as soon as it finishes) | **web-verified rebuild** (react-bits `Shuffle` real source, React → vanilla line by line, source kept in runs `_src/`; **License = MIT + Commons Clause**: use inside a product ✅ / redistributing the component itself ❌; eyeballed by the user 2026-07-19) · **reason for withdrawal = licence**: upstream react-bits is **MIT + Commons Clause** — the component itself (alone, bundled, or ported) **may not be sold, sublicensed or redistributed**, a constraint this row had already recorded; the manifest separately notes that **SplitText was historically a paid Club GreenSock plugin** (the demo used the public mirror). **The user ruled it out of the library on 2026-08-19** (also noting: quality is unremarkable, and it had 0 production consumers). **The row stays, the badge has been removed, and the registry record has been withdrawn.** |

## Step node axis #30 (lab-built, human-approved 2026-07-18 — fed back from the Averonel option-2 run, registered late 2026-08-01)

| # | Effect | Feel | Suits | Implementation | Compute tier | provenance |
|---|---|---|---|---|---|---|
| 30 | **Step node axis** scroll step axis | A commit-graph-style vertical node axis grows down the left of a numbered step list; natural scrolling (no pin), with a "reading line" at about 40% viewport height sweeping through — a row highlights as it arrives, its node goes from hollow to filled, and the segment fills in; bidirectional by default (scrolling up steps back), with `accumulate` preserving a monotonic commit-log mode | Process / step / timeline sections; craft and archival register; for when you want "order plus visible progress" without pinning the page | The reading line is `innerHeight×opts.line` tested against each row's `getBoundingClientRect`; rows / nodes / segments / line are all consumer DOM, so the module is layout-agnostic and only toggles classes; ✅`material/scroll-step-axis` (M-56) | **light** (no canvas; class and colour switching) | **lab-built, human-approved** (fed back from Averonel option-2 Phase D SPEC v9 §1.2, eyeballed by the user; standard form verified in the B10 batch `ac6ce83`) 【⚙执行册】 |

## Pinned horizontal card rail #31 (lab-built, human-approved 2026-07-18 — fed back from the Averonel option-2 run, registered late 2026-08-01)

| # | Effect | Feel | Suits | Implementation | Compute tier | provenance |
|---|---|---|---|---|---|---|
| 31 | **Pinned horizontal rail** | The section pins and vertical scrolling drives the cards sideways 1:1; a progressBar and counter report progress; the card visuals come entirely from consumer tokens (`--phr-*`) | Service / work card corridors; when you want a horizontal narrative without real horizontal scrolling; ⚠ pin + scroll-jacking monopolises the page's scroll, so at most one main scroll choreography per page (taste §8) | ScrollTrigger pin (scoped to the section, spacer inserted and removed automatically) + scrubbed translateX (transform only); destroys cleanly; ✅`material/pinned-horizontal-rail` (M-57) | **light** (pure transform scrub) | **lab-built, human-approved** (fed back from Averonel option-2 Phase D SPEC v9 §1.1, eyeballed by the user; the B10 pixel gate is an honest exemption [GSAP scrub lag cannot be made deterministic by the harness, the same family as css-grid #11] `ac6ce83`) 【⚙执行册】 |

## Site-level observation anchors (👁 anchor-only — human-admitted 2026-07-07, chosen and judged by the user)

> Unlike the two tiers above, these sites have **no readable tutorial source** (minified production
> code or a Framer platform artefact), so they get **no GSAP implementation column and do not count
> as web-verified implementation exemplars** — they are site-level anchors for "a human looking at
> the feel, to find a direction". Building it still goes through the #1–#20 implementation paths or
> `three/*`. The engine mark is a fact I grepped after curling the page.

| Site | What to learn (the user's own points) | Engine mark | Note |
|---|---|---|---|
| Studio Dialect (https://studiodialect.com) | Elements **tracking the mouse XY coordinates**; the user explicitly judged **the rest not worth learning from** | WebGL+GSAP (same stack) | Take the one point only, do not reference the whole site. **Promoted three tiers → #21** (2026-07-08) 【⚙执行册=anchor-studio-dialect】 |
| Wildy Riftian works page (https://www.wildyriftian.com/works) | The **visual metaphor and interaction of the folders** (work-index composition) | Framer platform | Learn the metaphor, do not copy the implementation (a Framer artefact, a different stack from the lab's HTML+GSAP; the taste red line stands: never mix GSAP/Three with Framer in one tree). **Promoted three tiers → formally numbered #26** (promoted 2026-07-08; numbered by the user 2026-07-11, with the execution record on the #26 row). **🏷**: driver=hover/click · mechanism=spotlight fading the others + a slight lift (the drawer stacking order does the rest) + a fanned preview peeking out + a twin backdrop · carrier=a category / work index (any "drawer-style category entrance") · content=images or abstract file shapes · register=playful editorial / magazine feel 【⚙执行册=anchor-wildy-folder-works】 |
| Orlion Studio contact page (https://www.orlionstudio.com/contact) | The **loading animation** in the "Drop me something" section | webgl | A single-point anchor 【⚙执行册=anchor-orlion-loading】 |
| Studio K95 (https://www.k95.it) | Strong overall (the user's judgement, with no single point named; a communication/graphic agency in Catania, Italy) | webgl | A general site-level anchor; look through it by hand when a brief is similar 【⚙执行册=anchor-studio-k95】 |

> **Compute tier (a dimension added 2026-07-08)**: a newly added effect should carry an initial
> compute tier (light / medium / heavy + a weak-machine fallback; the definition is in
> `threed-pool.md` §compute tier) — a stuttering hero is a hero that failed its job. #1-#20 were
> backfilled against the real code when they graduated on 2026-07-11 (see the ⚡ on each 🏷 line and
> the piece's own TAGS.md).

## Growth (capability honesty, see `reference-sources.md` §5)
**I cannot update this pool by "watching" motion** — I have no direct perception of a running
animation. I can only propose candidates when I get to **read real source** (bucket C: Codrops /
GSAP / vanilla, with a readable implementation), and whether the motion is any good is still judged
by a **human, or by the scorer's `interaction_quality`**. That makes motion-pool the pool most
dependent on "is there code, and did a human look at it", and it is **never written back
automatically**.

**Admission record**: 2026-07-03, the "whole-page scroll choreography" tier #11–#20 was admitted
(approved wholesale by the user; gsap-ecosystem Track B). The web-verified entries come from 6
Codrops/GitHub real-source repos (bucket C process, source read in full); the seamora-observed
entries came from the jesus-site rebuild (pattern observed externally, code produced here), admitted
**after a human verdict** under a one-notch-weaker label — the "self-produced does not auto-enter"
red line was not broken; it went through the human channel.
**Upgrade record**: on 2026-07-05, at the user's request ("seamora 复刻未经多轮微调,不能当可学习的成熟范本"),
every original seamora-observed entry (#11–14 / #20 plus the #15 corroboration) was re-anchored to
external real source — official GreenSock CodePen demos plus codrops repos — and every jesus-site
source pointer was removed. Only #12's full choreographic combination has no external tutorial: the
mechanism is anchored to an official demo (pin+scale+scrub) and the combination honestly keeps its
seamora-observed note.
