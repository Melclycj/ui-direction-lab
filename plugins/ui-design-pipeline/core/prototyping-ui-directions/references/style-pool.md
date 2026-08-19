# Visual style pool (Batch 1 visual reference) — optional base cases

> ⚠️ **This is a fallback, not a menu.** Reach for it only when you cannot think of a better
> direction, as a starting point or a comparison — you are **not required** to pick from it. Propose
> an original direction first and treat these as a springboard to push past. Used at
> `prototyping-ui-directions` **Batch 1 (visual direction)** — the axis that settles palette / type /
> layout / density.

| Family | Style | In a sentence | Suits / leans | Exemplar anchor |
|---|---|---|---|---|
| Classic refined | Minimal luxury (极简高级风) | Generous whitespace, restraint, less is more | Premium brands, consultancies, luxury goods; mostly light, low density | Vercel · ElevenLabs · Apple · Aesop |
| Classic refined | Apple-style product page | Centred hero imagery + short lines + progressive reveal | Product launch pages; light or dark, strong hero | Apple |
| Classic refined | Swiss International | Strict grid, sans-serif, left-aligned, red and black | Editorial / institutional / portfolio; high order, low ornament | — |
| Product tooling | Bento cards | Irregular tiled grid (Apple's Control Centre) | SaaS feature sections, dashboards; medium density | Apple Control Centre |
| Product tooling | Dark tech SaaS | Dark ground + a single neon accent + mono numerals | Developer tools, AI products; dark, medium-high density | Linear · Raycast · Sentry · xAI · Warp · **e2b** (dev-infra; **light marketing pages / dark app console** [confirmed by screenshot], orange `#ff8800` = active and green = LIVE status, large IBM Plex Mono numerals rather than neon — this widens the row rather than being typical dark-neon; the console's **composition** exemplar has moved to `ia-companion.plan.md` as a seed) |
| Product tooling | Design-system look | Tokenised, tidy components, a reusable feel | Platforms / B2B; neutral, strongly consistent | Stripe · Supabase · Vercel |
| Product tooling | Field engineering (现场工程风) | Light industrial instrumentation: zoned stages, long leader lines, calibration tick rails, oversized numerals | Construction / logistics / data tools / industrial products; off-white + charcoal, medium-high density, a single signal yellow | 👁 **Endfield** (https://endfield.hypergryph.com/ · confirmed from production CSS: `#191919`/`#fff`/signal yellow `#fffa00`, Novecento Sans Wide + clip-path zoning · closed-source game IP, **interpret, do not copy**) |
| Future tech | Glassmorphism | Frosted glass, inner-glow edges, stacked transparency | Tech / fintech; pairs with a dark ground | — |
| Future tech | 3D immersive | WebGL/3D scenes, spatial depth | Launch events, concept sites; heavy assets, needs perf control | 👁 igloo.inc (https://igloo.inc · Awwwards SOTY 2024 · fully WebGL: Three.js + GSAP) · Bruno Simon portfolio (https://bruno-simon.com · Awwwards SOTD · a drivable Three.js open world) · landonorris.com (https://landonorris.com) · Shopify Editions Winter'26 (https://www.shopify.com/au/editions/winter2026 · seasonal URLs expire; swap in the current Editions when it does) — the last two were picked by the user on 2026-07-07, whose verdict was: "非常优秀的向下翻滚式作品,超前 3D 效果" (replacing Seamora; curl 200 confirmed). The HOW layer is in `three/` (threejs-scroll-stage) |
| Future tech | Cosmic archive (宇宙档案风) | Midnight ground + serif narrative headlines + circular orbital instruments, star-map nodes | Narrative archives, cultural editorial, astronomy tools, character dossiers; dark, low density, generous whitespace | 👁 **Ex Astris** (https://exa.hypergryph.com/ · confirmed from production CSS: white / near-black + an extremely restrained aqua `#46f6e6`, Source Han Serif + Sumerhan, 44 masks and orbital keyframes · closed-source game IP, **interpret, do not copy**) |
| Future tech | Data visualisation | The chart is the hero, information-dense | Analytics / monitoring products; high density, mono | — |
| Typographic | Magazine editorial | Large serif headlines, column measure, pull quotes | Content sites, brand narrative; editorial | Claude · Mistral (editorial-serif AI) · Hermès·Aesop (editorial luxury, interpret don't copy) |
| Typographic | Kinetic type | The text itself moves or deforms | Creative sites, event pages; motion-heavy (hands off to Batch 2) | — |
| Typographic | Full-bleed visual | Full-screen imagery or type, one idea per screen | Marketing landings, portfolios | Runway (photo/video driven) · Ferrari·Lamborghini·Bugatti (luxury automotive: black ground, full bleed, a single metallic accent, interpret don't copy) |
| Character | Neo-brutalist | Heavy borders, hard shadows, a raw-HTML feel, high contrast | Personality brands, streetwear; unafraid of "ugly" | this lab's Northway (lab) |
| Character | Retro-futurism | 80s/90s sci-fi, grid horizons, neon | Music / games / events | — |
| Character | Y2K digital | Millennial chrome, bubbles, pixels, bright colour | Youth-facing, trend commerce | — |
| Emotional brand | Illustration-led | Custom illustration leads, warm, personified | Consumer brands, education, children | — |
| Emotional brand | Hand-drawn | Hand strokes, casual, irregular | Creative studios, personal sites | — |
| Emotional brand | Organic natural | Soft colour, rounded corners, natural texture, slow pacing | Wellness, food, sustainability brands | this lab's Grove (lab) |
| Emotional brand | Bright collaborative (明快协作风) | Rounded pills, heavy strokes, offset hard shadows, floating layers and bouncy feedback | Collaboration tools, playful onboarding, family-facing, event pages; light ground, medium density | 👁 **POPUCOM** (https://popucom.hypergryph.com/ · confirmed from production CSS: blue `#3994ff` carries the structure, yellow and orange act only as action signals · ⚠ the original site runs all three together; before entering a product UI it must be reduced to a **single accent** (see `palette-pool.md` §2) · closed-source game IP, **interpret, do not copy**) |

> **Anchor provenance**: a named brand = `web-verified` (confirmed from its DESIGN.md, including the
> luxury automotive trio Ferrari/Lamborghini/Bugatti); `this lab's X (lab)` = `your-skill`; Apple =
> canonical memory; **closed-source majors (Hermès / Aesop and the like) = reverse-engineered
> `memory-candidate` + `do-not-copy`, marked "interpret, do not copy"** (the visuals are 👁 yours to
> view, I only give the URL); `—` = still waiting to be surfaced by a human (judging visuals is human
> work, see §Growth).
>
> **The game-IP sites (Endfield / Ex Astris / POPUCOM, added 2026-08-04) = evidence `web-verified`
> plus rights `do-not-copy`, marked "interpret, do not copy".**
> The evidence is harder than a DESIGN.md: their **public production stylesheets** were downloaded and
> **SHA-256 byte-checked** (4 files, 353KB total, identical to the upstream 2026-07 snapshot), so the
> colour and type values are counted rather than recalled.
> **But strength of evidence is not permission to copy** — these are commercial game IP. Logos,
> character art and proprietary faces are never taken; only the composition, hierarchy, geometry and
> colour **grammar**.
> The second-hand source `ark-ui-skill` (github.com/Brandon030722/ark-ui-skill, a clean-room
> distillation) is **not used as an anchor**, only as corroboration that someone has distilled this
> once already.

**Usage note**: the 3-4 Batch 1 variants should pull apart across **several facets of this axis**
(for example "Swiss International (light / high order) vs dark tech SaaS (dark / medium density) vs
magazine editorial (serif / narrative)") rather than one style in three accent colours. Motion is
held at a plain default for this batch (load-in only, or nothing) and belongs to Batch 2.

> The `taste-skill` hard rules are unaffected by this pool: no lilac, one accent, mono numerals, no
> Inter, no three equal-width card columns, and so on. A style pool decides *which direction to walk
> in*; it does not exempt you from the taste gate.

## Growth (human-gated, see `reference-sources.md` §5)
Judging whether a visual style is any good is **human work** (I can read a static page, which is not
the same as having taste). So when a style shows up that this pool does not have, I **do not add it
myself** — I **surface it to you** (style name + URL + why), and **you go look at that site yourself**
before deciding. However well a page we produced turned out, it does not enter as a standard.
