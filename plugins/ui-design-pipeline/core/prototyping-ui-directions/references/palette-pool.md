# Palette pool (Batch 1 visual reference · token-level palettes) — optional base cases

> ⚠️ **This is a fallback, not a menu.** Reach for it only when you cannot think of a better palette,
> as a starting point or a comparison — you are **not required** to pick from it. Used at
> `prototyping-ui-directions` **Batch 1 (visual direction)** to settle the palette axis (alongside
> style from `style-pool.md` and type from `font-pool.md`).
> Same origin as font-pool: the hex values in the SaaS rows were **copied out of real brand
> `DESIGN.md` files** (see `reference-sources.md` bucket A). They are not invented.

## Schema (what each palette carries)
`vibe` · a four-part set of **bg / ink (layered) / a single accent / border-rule** (token level, ready
to drop into `--token-color-*`) · **anchor** · **provenance** · `notes`.

**Three provenance marks** (same as font-pool)
- `web-verified` — confirmed from a DESIGN.md or official site that was actually fetched. The
  **spine** of this pool should be this tier: external, credible standards.
- `your-skill` — a real palette this lab ran and locked into `testbed/chassis/`. **An internal
  verification mark, not an external industry standard** — see §Growth.
- `memory-candidate` — a canonical name from memory; re-check before shipping.

## Taste rules (this pool does not exempt you from them)
- **One accent** (`taste-skill` hard rule): a product UI palette carries **exactly one** accent. Do
  not stack colours.
- **No lilac**: avoid lilac/violet as an accent. ⚠️ See the Stripe note in §1.
- **Layer bg/ink** (ink / ink-mid / ink-soft): build hierarchy from a lightness ladder, not from more
  colours.
- **Take the values from the chassis colour tokens**; the page only references
  `var(--token-color-*)`.

---

## §1 · SaaS / developer tools — ★ SEEDED FROM REAL `DESIGN.md` (sample vibe)

**Granularity: 10 brands collapse into 2 sub-vibes; a brand appears as an inline anchor with its real
hex values.**

| sub-vibe | bg / canvas | ink (layered) | single accent (pick one) | anchor (real hex) | provenance |
|---|---|---|---|---|---|
| **Light SaaS** | `#ffffff` / soft `#fafafa`·`#f6f9fc` | near-black `#171717`–`#0d253d` · body `#4d4d4d` | blue `#0070f3` / emerald `#3ecf8e` / mint `#00d4a4` / orange `#ff8800` (e2b, with a black CTA `#000`) | Vercel (blue) · Supabase (emerald) · Mintlify (mint) · e2b (orange / dev-infra; light default bg `#fafafa`, ink `#000`/`#333`/`#666`/`#999`; dark variant `#000`·`#141414`·`#1a1a1a`) | `web-verified` (e2b tokens measured with Playwright) |
| **Dark dev-tool** | near-black `#07080a`–`#010102` · surface one step up | light `#f4f4f6`–`#f7f8f8` | lime `#c2ef4e` / a white pill / warm white `#f7f5f0` | Sentry (lime) · Raycast (white) · Warp (warm white on `#2b2622`) | `web-verified` |

- **Taste tension (violet)**: Stripe `#533afd`, Notion `#5645d4` and Linear `#5e6ad2` all lean
  violet, which collides with the no-lilac rule. **Reverse-engineer their structure and swap in a
  non-violet accent** (blue / green / lime) before using them.
- Vercel's mesh gradient (cyan `#50e3c2` / violet `#7928ca` / pink `#ff0080`) is **marketing only** —
  never a product accent.

---

## §2 · Other vibes — several already confirmed by this lab (`your-skill`, real chassis palettes)

| vibe | bg / surface | ink (layered) | single accent | border/rule | anchor | provenance |
|---|---|---|---|---|---|---|
| **Neo-brutalist / acid·dark** | bg `#14150f` · surface `#1e2016` | paper `#f1efe2` · 2nd `#b7b5a4` · 3rd `#82806f` | acid lime **`#bfe800`** (`#93b300` in dark) | bright edge `#f1efe2` (hard shadow) | this lab's **Northway** | `your-skill` (`chassis/northway-brutalist`) |
| **Organic / linen (quiet luxury)** | linen `#f7f5f0` · warm `#f0ede7` | ink `#1a1a17` · mid `#5c5b57` · soft `#9a9890` | terracotta **`#b06a4f`** (interactive `#8f5133` / hover `#7a4328`) | rule `#d8d5cf` | this lab's **Grove** | `your-skill` (`chassis/grove-linen`) |
| **Dark tech SaaS (neon)** | deep near-black ground | layered paper text | one neon (cyan / green / magenta — pick one) | dark hairline | dark developer-tool sites | `memory-candidate` |
| **Warm AI (AI product)** | cream `#faf9f5` / warm white `#f5f5f5` (or dark ground `#0a0a0a`) | warm near-black `#141413`–`#0c0a09` | warm coral/orange `#cc785c`·`#ff7759`·`#fa520f`·`#ff7a17` (pick one) | warm hairline | Claude · Mistral · xAI · Cohere (Runway has no accent — it is photography-driven) | `web-verified` |
| **Luxury automotive / haute (dark)** | pure black `#000000` / near-black `#181818` | white `#ffffff` · 2nd `#c9c9c9` | **one** metallic: gold `#FFC000` (Lambo) / Rosso red `#da291c` (Ferrari) / ice blue `#c3d9f3` (Bugatti) — **extremely restrained, CTA and mark only** | dark hairline `#2a2a2a` | Lamborghini (gold) · Ferrari (red) · Bugatti (ice blue) | `web-verified` (DESIGN.md) + reverse-eng + `do-not-copy` |
| **Minimal / editorial luxury (light cream)** | cream `#faf9f6` / ivory `#f4f1ea` (or pure white `#ffffff`) | charcoal `#1d1d1f` · body `#4d4d4d` · fine `#8a8a8a` | **pick one**: cool blue `#0066cc` (Apple) / **no accent · pure mono** (Aesop) / warm orange `#f37021` (Hermès) | warm hairline `#e6e2d9` | Apple (blue) · Aesop (no accent) · Hermès (orange) | Apple = `web-verified`; Aesop / Hermès = `memory-candidate` (reverse-engineered from closed source) + `do-not-copy` |
| **Industrial signal / field** (工业信号，light-industrial) | off-white `#ffffff` · inverted charcoal zones `#191919` | charcoal `#191919` · 2nd `#35373c` · soft `#999999` | signal yellow **`#fffa00`** (the site also carries `#00ffa2` green and `#ff1aac` magenta — **pick one, never together**) | hard edges + clip-path diagonal zoning | 👁 Endfield | `web-verified` (production CSS hash-checked) + `do-not-copy` |
| **Cosmic archive / midnight-serif** (宇宙档案) | mostly white `#ffffff` · inverted midnight `#000000` sections | near-black `#000000` · 2nd `#b8b8b8` · soft `#858585` | aqua **`#46f6e6`** (only 4 occurrences site-wide — extremely restrained) | fine hairline + circular orbital strokes | 👁 Ex Astris | `web-verified` (production CSS hash-checked) + `do-not-copy` |
| **Bright collaborative / playful-blue** (明快协作) | white `#ffffff` · blue field `#3994ff` | deep blue `#3a5dad` · deeper `#0050af` · soft `#5a5a5a` | blue **`#3994ff`** (for a warm accent instead, yellow `#ffcc1a` or orange `#f7a120` — **pick one**) | heavy strokes + offset hard shadows | 👁 POPUCOM | `web-verified` (production CSS hash-checked) + `do-not-copy` |

> The luxury tier was seeded 2026-07-01 (same as font-pool): **luxury automotive / haute** (black + a
> single metallic; Ferrari / Lamborghini / Bugatti = `web-verified`) and **minimal / editorial
> luxury** (cream + charcoal; Apple = web-verified, Aesop and Hermès reverse-engineered from closed
> source, `do-not-copy`, marked "interpret, do not copy"). Taste: metallics **stop at a touch**; no
> violet (ice blue `#c3d9f3` is a cool blue, not a violet); cool blue `#0066cc` and warm orange
> `#f37021` are **either/or, never together**. Consumer split: automotive tokens are 🤖 mine to parse;
> Aesop and Hermès are 👁 yours to view live (I only give the URL).

> The game-IP tier was seeded 2026-08-04 (the same three rows as style-pool): **industrial signal /
> field** · **cosmic archive / midnight-serif** · **bright collaborative / playful-blue**.
> Evidence = downloading their **public production stylesheets** and doing a **SHA-256 byte-for-byte
> check** (identical to the upstream 2026-07 snapshot); the hex values are counted, not recalled.
> Rights = `do-not-copy`, marked "interpret, do not copy".
> **Two taste tensions this pool does not exempt**: ① POPUCOM's own site runs blue + yellow + orange
> **together**, colliding with the single-accent hard rule → handle it like Stripe in §1: reverse the
> structure and keep only one accent. ② Ex Astris also carries a violet `#925dff`, colliding with the
> no-lilac rule → **do not take it**; aqua `#46f6e6` is the only accent.
> Consumer split: all three are closed-source commercial game IP; live visuals are 👁 yours to view
> (I only give the URL). Logos, character art and proprietary faces are never taken — only the
> colour grammar.

## Usage notes
- When Batch 1 swaps palettes, what changes is the **lightness temperament plus the accent hue**
  (light linen vs dark acid vs white SaaS) — not the same palette with a different accent.
- Once chosen, write the four-part set into the chassis as `--token-color-*`; the page only
  references the token.
- **Palette tools**: **Coolors** (coolors.co, 🤝) to generate and adjust, then export the hex into
  tokens · **Colorable** (colorable.jxnblk.com, 🤖) to check contrast and a11y (or I compute it in
  code). **Take inspiration from this pool first** rather than browsing an inspiration wall like
  Color Hunt — that is slow.

## Growth (human-gated, see `reference-sources.md` §5)
- **Candidates can be proposed from data**: like typefaces, I can lift **real hex values** off a real
  DESIGN.md or official site and propose them (`web-verified`).
- **Admission stays human**: the value of this pool is that it holds **external credible standards**.
  I surface the candidate (anchor + hex + URL) and **you decide whether it goes in**.
- **Self-produced palettes are not standards**: a page that came out well, or a chosen LEAD, is not
  an industry exemplar. `your-skill` is an internal verification mark and should not lead this pool
  (`Northway` / `Grove` are kept only as "we used this, worth referencing").
