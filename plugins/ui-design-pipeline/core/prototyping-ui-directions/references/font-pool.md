# Typeface pairing pool (Batch 1 visual reference · typeface pairings) — optional base cases

> ⚠️ **This is a fallback, not a menu.** Reach for it only when you cannot think of a better
> typographic direction, as a starting point or a comparison — you are **not required** to pick from
> it. Used at `prototyping-ui-directions` **Batch 1 (visual direction)** to settle the typography
> axis (alongside palette and layout from `style-pool.md`).
> Naming: this is a **typeface** pairing pool. How text *moves* is a different question — see
> `motion-pool.md`.

## Schema (what each pairing carries)
`vibe` · a **display + body + mono** set · per face a `family` + `source` + `free/commercial` ·
an **exemplar anchor** (who uses it best — the taste anchor) · **provenance** (where the row came
from, honestly) · `notes` (including taste rules).

**Three provenance marks (honest sourcing)**
- `web-verified` — confirmed from a file or page actually fetched (a DESIGN.md corpus, a foundry
  site).
- `your-skill` — a real choice this lab made, verified live, and locked into `testbed/chassis/`
  (highest confidence).
- `memory-candidate` — a canonical name from model memory: reliable, but the URL and details were
  not re-searched one by one. Verify before shipping it.

## Taste rules (this pool does not exempt you from them)
- **Inter is banned as a primary face** (`taste-skill` hard rule). Vercel and others keep Inter as a
  fallback in their stack — we **do not follow that**. Use a non-Inter grotesk such as Geist for the
  primary, and let `system-ui` be the fallback.
- **Numerals go mono** (tabular), which is why every row carries a mono face.
- **Take the values from the chassis type tokens** (family / size / weight / tracking). Never
  hardcode them in the page.
- **Free first**: if a free face gets the effect, do not reach for a commercial one. Commercial faces
  are listed as exemplar anchors only — nobody is asked to buy them.

---

## §1 · SaaS / developer tools — ★ SEEDED FROM REAL `DESIGN.md` (sample vibe, verified rather than remembered)

This tier is the worked example: the data comes from 10 brand DESIGN.md files that were actually
fetched (see `reference-sources.md` bucket A).
**Granularity: 10 SaaS/dev brands collapse into 3 tiers; a brand appears as an inline exemplar
anchor, never as a row of its own.**

| Pairing tier | family | Anchor (real) | Source / free vs commercial | Real tokens / notes | provenance |
|---|---|---|---|---|---|
| **Free first choice** | **Geist** + **Geist Mono** | Vercel | Google Fonts · Fontshare · npm `geist` · **free, OFL** | stack `Geist, system-ui`; Display XL 48/600/-2.4px; Body 16/400 | `web-verified` |
| **Refined grotesk (commercial)** | Söhne / Circular / Linear's own | Stripe · Supabase · Linear | commercial/proprietary ↔ free stand-ins **General Sans** (Fontshare) / **Hanken Grotesk** (Google) | Stripe runs light headlines at weight 300 + `ss01`; Linear only in dark | `web-verified` |
| **Supporting face (optional)** | Rubik / Instrument Serif | Sentry (Rubik) · Warp (Instrument Serif) | Google · **free** | Rubik is friendly and rounded; Instrument Serif adds a touch of editorial to a dev product | `web-verified` |

**Recommended landing (free first, taste-clean)**: Display + Body = **Geist** (what Vercel uses; one
family covers both) · Mono = **Geist Mono / JetBrains Mono**.
- ⚠️ **The Inter trap**: half of the SaaS/dev set (Raycast / Notion = Notion Sans / Warp / Resend-UI
  / Mintlify / the Supabase stand-in) runs **Inter** as its primary, which taste bans. **Borrow their
  structure, not their face**: primary goes to Geist, fallback `system-ui`.
- **The IBM Plex pairing** (what e2b uses; free OFL; the other taste-clean dev-tool route): body
  **IBM Plex Sans** + **IBM Plex Mono as the display face** (monospace as a headline reads as
  technical/terminal, not just as numerals) + mono also IBM Plex Mono. A free non-Inter alternative
  to Geist; for the accent see the orange `#ff8800` in `palette-pool`. `web-verified` (e2b measured
  with Playwright).

---

## §2 · Other vibes — seed rows (some already confirmed by this lab = `your-skill`)

| vibe | display | body | mono | source/free | anchor | provenance |
|---|---|---|---|---|---|---|
| **Neo-brutalist / acid** | **Archivo Black** | **Archivo** | **Space Mono** | Google · all free | this lab's **Northway** fixture (acid·dark, live) | `your-skill` (`chassis/northway-brutalist`) |
| **Organic / editorial Didone (quiet luxury)** | **Playfair Display** (high-contrast Didone; the italic can carry drama) | **Manrope** (a quiet grotesk) | **DM Mono** | Google · all free | this lab's **Grove** fixture (linen, live) | `your-skill` (`chassis/grove-linen`) |
| **Magazine / luxury editorial (commercial tier)** | Canela / Tiempos Headline / GT Sectra | Tiempos Text / the matching body | (none, or mono numerals) | commercial (Klim / Commercial Type / GT) ↔ free stand-ins **Fraunces** / **Playfair** / **Instrument Serif** + body **Newsreader** / **Source Serif 4** | Hermès · Aesop · Vogue-class editorial luxury (closed-source majors → **interpret, do not copy**, `do-not-copy`) | `memory-candidate` (reverse-engineered from closed source) |
| **Luxury automotive / haute (dark, dramatic)** | **Saira / Saira Condensed** (refined condensed grotesk; Bugatti ships it as a fallback) ↔ commercial Bugatti Display / FerrariSans / LamboType | **Saira** / **Cormorant Garamond** (an editorial serif voice; Bugatti's serif fallback) | **JetBrains Mono** | Google · all free (the commercial faces are anchors only) | Ferrari · Lamborghini · Bugatti (black ground + a single metallic accent) | `web-verified` (DESIGN.md) + reverse-eng + `do-not-copy` |
| **Minimal / geometric** | General Sans / Space Grotesk | General Sans / Hanken Grotesk | IBM Plex Mono | Fontshare / Google · free | minimal product sites | `memory-candidate` |
| **Dark tech SaaS (neon accent)** | Geist / Space Grotesk | Geist / Hanken Grotesk | Geist Mono / JetBrains Mono | free | developer-tool sites (same as §1) | `memory-candidate` (partly confirmed in §1) |
| **Editorial AI (AI product)** | serif display: Fraunces / Newsreader (free) ↔ Tiempos / PP Editorial (commercial) | geometric sans: Geist / General Sans / DM Sans | JetBrains Mono / Geist Mono | Google · Fontshare · free | Claude · Mistral · xAI (warm coral accent, see palette); ⚠️ 5 of the 6 use Inter → borrow the structure, not the face | `web-verified` |

> **The luxury tier (seeded 2026-07-01)** was confirmed by parsing real sources: the **luxury
> automotive / haute** row comes from Ferrari / Lamborghini / Bugatti's own DESIGN.md
> (`web-verified`); the **editorial luxury** row is anchored on Hermès / Aesop / Vogue, which are
> closed-source majors, so it is reverse-engineered (`memory-candidate` + `do-not-copy`, marked
> "interpret, do not copy"). ⚠️ **Ferrari's official fallback is Inter** (taste bans it) → borrow the
> structure, not the face; take display from Saira / Cormorant. Dark-luxe type is "large, restrained,
> refined condensed" — **not** the heavy brutalism of Archivo Black. Consumer split: DESIGN.md tokens
> are 🤖 mine to parse; closed-source majors are 👁 yours to look at live (I only give the URL).

## Usage notes
- When Batch 1 variants pull apart on the typography axis, what should change is the **temperament of
  the family** (grotesk vs Didone vs geometric) — not the same family at a different weight.
- Once a tier is chosen, write the families into the chassis as
  `--token-font-display/body/mono`; the page only ever references the token.
- **Free sources**: **Fontshare** / **Google Fonts** / **Fontsource (npm)** + **The League of
  Moveable Type** (theleagueofmoveabletype.com, an open-source foundry, 🤝).
- Commercial faces (Söhne / Canela / Tiempos) are anchors, not purchases. Their foundry **Klim**
  (klim.co.nz) is 👁 yours to browse — **expensive → browse-later**, kept for reference.
- **To see how a given face is actually paired in the wild** → **search Typ.io** (👁, **go in with a
  specific family name and filter**; do not wander an infinite inspiration wall — that is slow).

## Growth (human-gated, see `reference-sources.md` §5)
Typefaces **can be proposed from data**: I can lift a real family off a real site or a DESIGN.md and
propose it (`web-verified`). **Admission stays human** — I surface the candidate (family + source +
anchor + URL) and **you decide whether it goes in**. The spine of this pool should be the
`web-verified` / canonical tier, which is an external credible standard; `your-skill` rows (such as
`Northway` / `Grove`) are an **internal verification mark, one notch weaker than a standard**, kept
only as "we used this, worth referencing" — they **do not lead this pool**. Output we produced does
not become an exemplar just because it went well.
