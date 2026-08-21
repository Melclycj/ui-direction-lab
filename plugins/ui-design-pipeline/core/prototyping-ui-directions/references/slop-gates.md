# Slop Gates — a pre-ship negative checklist + a six-axis pre-emit self-score (hallmark adaptation)

> Source: [Nutlope/hallmark](https://github.com/Nutlope/hallmark) `slop-test.md` (58 gates, MIT); the verbatim archive is [`_vendor/hallmark-slop-test.md`](_vendor/hallmark-slop-test.md) (with commit hash and pull date).
> This file is **our adaptation**: bucket (a) = lab core gates (chosen because this repo has actually failed them, or because they are the commonest AI default); bucket (b) = conditional gates; bucket (c) = gates not adopted. All 58 (1-57 plus 38a) are accounted for, and anything cut can be traced back to the vendor original.
> **How to use it**: on a PUD batch, run a gate sweep **once per batch** (against what the batch has in common) plus a per-variant six-axis stamp; on an APW Base Wave, sweep bucket (a) **once per wave** plus a per-surface stamp. This is an instruction-layer self-check, **not a machine gate** — it never enters the registry, the sync check, or a hook.

## (a) Lab core gates — every answer must be no (24 gates)

Gate numbers follow hallmark's originals so you can trace them back.

1. Is the display face Inter / Roboto / Open Sans / Poppins / Lato / a system default? (the wider form of font-pool's "no Inter as primary")
2. Is there a violet→blue (or cyan→magenta) gradient anywhere — including a `background-clip: text` gradient headline?
3. A grid of 3 equal-width cards with icon-above-heading tiles?
4. Cards inside cards?
6. Fully centred hero, auto-fail: `min-height:100vh` with everything centred, or eyebrow / headline / lede / CTA all on the same centred vertical axis? (at most two centred elements; the eyebrow or the CTA must leave the axis)
8. Reusing structure that should not be reused — the generic AI template (Hero → 3 features → CTA → footer), or the same structural fingerprint as this project's previous output?
9. Sections separated by equal whitespace alone: no rule, no ornament, no colour shift, every section at the same rhythm?
10. `transition: all` anywhere? (name the properties)
11. `hover:scale-105` (or any uniform hover-scale) applied across unrelated elements?
13. Any element carrying more than one hover effect at once (translate + scale + shadow + colour + rotate)?
14. Animating `width` / `height` / `top` / `left` / `margin` / `padding`? (transform and opacity only)
15. Does the focus ring fade in? (it must appear instantly — keyboard users need an immediate indication)
19. Placeholder names (Jane Doe / John Smith) or startup clichés (Acme / Nexus / Seamless / Unleash)?
24. Any padding / gap / margin off the named spacing scale (multiples of 4px)? `padding: 17px` is the tell.
26. Any interactive element missing `:focus-visible` / `:active` / `:disabled`?
30. More than one icon library mixed, or emoji (✨🚀⚡🔥🎯✅) used as feature / step / pricing icons?
37. More than 3 `font-family` families on the page? (display + body + at most 1 outlier; different weights of one family count as one)
38a. Any headline or display text in italic? (italic is for emphasis inside body copy only; emphasise a headline with weight, accent colour, or a rule)
40. Does any (color, background) pair fail its contrast threshold? Body 4.5:1 (APCA Lc≥60); large text / icons / focus rings 3:1 (Lc≥45)
41. The three most-failed contrast cases: button text ≈ its fill (black on black); a missing `--color-accent-ink` on an accent surface; a dark-ground section that never flipped its text colour (ink on ink)?
42. Is the nav the AI default fingerprint (wordmark left + 4-5 inline links + button right + 1px hairline + white ground)?
45. Hero decoration with no semantic anchor (a floating cursor, an unexplained numeric corner tag, random ornament)? Decoration must have a reason.
46. Invented data ("10× faster" / "trusted by 50,000+") filling a stat slot? Any number the user did not supply is a `—` placeholder or a question back; a bare number may never carry the hero alone.
54. Eyebrow or number on the same line as the headline (tag-left, header-right)? Auto-fail — an eyebrow may only stack directly above the headline in the same column.

## (b) Conditional gates — checked when the condition applies (28 gates, compact table)

| Gate | Condition / how we recalibrated it |
|---|---|
| 5 | When using a card list: no heavy coloured side borders |
| 7 | Pure `#000` / `#fff` as a base colour — **exempt for a brutalist chassis**; pure white paper is also fine for the modern-minimal school; banned elsewhere |
| 12 | Overshoot / bouncy easing — allowed only where the interaction is a physical metaphor; banned for UI state changes such as buttons, modals and tooltips |
| 16·17·18 | When a toast / tooltip / carousel is present: never fire a success toast for a visible effect; tooltip hover 800-1000ms, focus 0ms; a carousel must pause on hover **and** focus (WCAG 2.2.2) |
| 22 | Zero-chroma neutrals — **exempt for Editorial Monochrome and the Stripe school**; elsewhere neutrals carry at least 0.005 chroma biased toward the anchor hue |
| 23 | Accent covering more than ~5% of the viewport — **recalibrated for acid / atmospheric styles** (where the bloom is the design itself, up to ~20%) |
| 25 | When there is running body copy: prose measure 45-75ch |
| 28·29·31 | When the hero is enriched: video never autoplays with sound and must carry a poster + `fetchpriority="high"`; an abstract background keeps a single accent ≤5% and does not animate; illustration prefers hand SVG or pure CSS over Lottie |
| 33 | When there is a decorative hand-drawn SVG or canvas: it must carry `aria-hidden="true"` or an `aria-label` |
| 34·44·49 | Browser-verified round (needs a real render): no horizontal scroll from 320-1920 (fix = `overflow-x: clip` on html+body); the hero is complete above the fold at 1280×800; clickable copy never wraps to two lines at any width |
| 35 | When using text decoration (highlighter / underline), check placement visually: a highlighter sits on the x-height, not the baseline; an underline is 1-2px with a 1-2px offset |
| 36 | A flex row of mixed heights (button + text, icon + text) needs `align-items: center` plus `line-height: 1` on the inner items |
| 38 | When using a third outlier face: ≤2 slots (wordmark + hero stat is the canonical pair) |
| 39 | When a form is present, check the five input states: border-width constant at 1px / focus uses outline not border / input height = button height (44px floor) / helper slot `min-height:1lh` / disabled across all three channels |
| 43 | When there is a real footer: no AI default fingerprint (4 link columns + a social row + small copyright at the bottom + a grey ground) |
| 47 | When showing a product screenshot or a device frame: no hand-drawn fake chrome (browser bars, phone frames, terminal frames) — use a real screenshot or bare content |
| 48 | When a variant uses a `:root` token system: colour and type may not drop out of tokens mid-page (an inline hex or a one-off font-family is a fail) |
| 50·51·53·55·56 | When the matching pattern appears: image grid tracks use `minmax(0,1fr)`; long display words get `overflow-wrap:anywhere`; CSS radio tabs guard against scroll-jump; all-caps display keeps `line-height ≥1.0`; two stacked stickies at top:0 offset by `--banner-height` |

## (c) Gates not adopted — one-word reason (6 gates, compact table)

| Gate | Reason |
|---|---|
| 20 | hallmark-specific (its macrostructure stamp mechanism) — our stamp is the six-axis stamp at the end of this file |
| 21 | hallmark-specific (Specimen theme-directory fall-through) |
| 27 | Duplicate → pointer to [the three motion-pool disciplines](motion-pool.md) (the reduced-motion branch is already a hard rule here) |
| 32 | hallmark-specific (component-cookbook variation knobs) — the concept is taken over by the Variety axis |
| 52 | hallmark-specific (its theme section-head override system) |
| 57 | hallmark-specific (the study verb / studied-DNA, outside what we absorbed this time) |

## (d) Archetype gates — the surface's KIND adds its own, and they are not optional

Everything above applies to every surface. A surface also owes whatever its **kind** owes: a
dashboard owes tabular figures and three async states, a scrollytelling section owes a readable
story with JS off, a game-style surface owes honest progress. Those live in
[`archetype-rules.md`](archetype-rules.md), assigned per screen by IA Stage B and visible on the
review board.

- **Where it comes from**: `info-spec.json` → `screens[].archetype`. **No IA spec, or no archetype
  on this screen → this section adds nothing**, and that is the designed degrade, not a gap to
  paper over by guessing a kind.
- **Style conflicts**: the locked L3 style wins the skin, the archetype wins the skeleton. A
  brutalist dashboard is still `tabular-nums`.
- **Two of the seven carry ethics rules with an absolute veto** — `game-style`'s honest-progress /
  no-dark-pattern / no-streak-hostage rules, and `creative-eye`'s never-block-access rule. There
  is no visual-direction exception to those; a variant that trips one is rejected, not scored.

Check them at the same moment as the gates above, and note in the report which archetype was
applied — or that none was, which is a fact about the run and not an omission to hide.

## Six-axis pre-emit self-score (run it before shipping, not after)

**Before** shipping, score the planned output 1-5 on each axis. **Any axis below 3 forces one more
pass before it goes to a human** — do not carry a known weakness into the gate sweep.
The original wording, kept: "Two passes is normal. Three is a sign the brief is wrong, not the
design — re-read the brief."

| Axis | What you are scoring | Note in our context |
|---|---|---|
| **P** Philosophy | Does the page have a clear *why* — a position? Or is it just a layout? | Corresponds to the variant's one-line thesis |
| **H** Hierarchy | Can you separate primary / secondary / tertiary within 2 seconds? | |
| **E** Execution | Are all the details inside spec (rule weights / accent footprint / text-wrap / focus ring / contrast)? | Corresponds to the implementation gates in bucket (a) |
| **S** Specificity | Does it look like *this brief*, or like a page anyone could use? | |
| **R** Restraint | Has every ornament, redundancy and filler padding that did not earn its place been deleted? | |
| **V** Variety | Does it share a structural fingerprint with this project's earlier output? **Score by structural distance, not visual distance — a colour swap is not variety** ("colour-swaps don't count as variety") | Aimed straight at the reskin failure in batched exploration: variants in one batch must have different structural fingerprints |

**Stamp format** (one comment line at the top of each variant / surface file, travelling with it):
`/* pre-emit critique: P5 H4 E5 S4 R5 V5 */`
A later run should be able to find that line and avoid repeating the same weakness. Gate sweep
results go in run-notes, one line per batch or per wave: `slop sweep: pass` or `FAIL: <gate numbers>`.
