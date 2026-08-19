# Reference source register + the reference-first workflow (reference-sources)

> Used at `prototyping-ui-directions` **Stage 1 (reference acquisition)**: when the user names a
> specific complex effect or asks for inspiration, **come here first to find out where to look**
> instead of writing it blind from a paragraph of description. Pairs with `style-pool.md` (style) /
> `font-pool.md` (type) / `motion-pool.md` (motion: text #1–#10 + whole-page scroll choreography
> #11–#20).
> Deployed with the skill (it travels inside `references/`).

## 0 · Capability honesty (the crux — it decides every tier below)
**I am strong at reading code, but I cannot "see" a running animation.** So every source is scored
on **two independent axes**, not one ladder:

- **VISUAL fidelity**: can this *look* be built? (real tokens / type / layout / component specs =
  high; a screenshot only = low)
- **MOTION fidelity**: is there **real animation code**, and **on what engine**?
  - `gsap` / vanilla → **goes straight into our HTML output** (highest; my strength)
  - Framer/React → only into a **TSX** variant; an HTML variant can only **borrow the technique and
    re-author in GSAP** (`interpret-to-gsap`, never passed off as directly copyable)
  - WebGL/canvas → I can read the code but **cannot see the output**, and it is heavy →
    `webgl-readonly-heavy`, flagged
  - Closed-source majors (Hermès / Linear class, minified and bundled) → **the real implementation
    is not obtainable** → only a "**looks like it**" reverse-engineered version, **marked "interpret,
    do not copy"**

A source can be high-visual and zero-motion (a DESIGN.md is exactly that), which is why the two axes
stay separate.
`WebFetch` only returns text/HTML (no JS execution, no motion); Playwright can get the rendered DOM,
the (minified) scripts, and state samples.

### A third axis · who looks (consumer) — orthogonal to fidelity, it sets the **division of labour**
Sources also differ in *who should look at them*, and that axis decides the call contract:
- 🤖 **AI reads**: I fetch and extract (tokens / code / structure) and **you only review the result**
  (bucket A, Ant/Carbon code).
- 👁 **A human looks**: the value is visual or motion, which I cannot see or would read inefficiently
  → **you look and you pick**, then hand me the screenshot or the choice (bucket E galleries, motion
  inspiration walls).
- 🤝 **Split**: you watch the live demo and **pick**, I read the code and **build** (buckets B and C —
  you judge motion far faster, I read the GSAP source).

Iron rule: for a 👁 source I **only give you the URL to look at**, and never pretend I can fetch the
visuals or the motion.

---

## 1 · Buckets — a source the user names is bucket #1 (public resources, not private skills)

> Each bucket is organised around "what can I actually obtain"; `engine` / `provenance` /
> `do-not-copy` / `cap` are marked on the bucket.
> **Cap ≈ 3-5 entries per class** (to prevent the 400-link flood of `awesome-design`) — it grows
> slowly through the promotion loop and human curation.

### Bucket A · DESIGN.md corpus — ★ highest visual value (static)
- **Sources**: `voltagent/awesome-design-md` (73+ major brands) · `VoltAgent/awesome-claude-design`
  (68) · `zephyrwang6/brand-design-md` (62) · `bergside/awesome-design-skills`.
- **VISUAL high / MOTION none**: each brand has a `DESIGN.md` = directly buildable static tokens
  (role-tagged hex + type scale + spacing/radius/shadow + component specs). **No motion code.**
- **How to get it**: fetch
  `raw.githubusercontent.com/VoltAgent/awesome-design-md/main/design-md/<brand>/DESIGN.md` → map its
  9 sections into our pools (palette → style/palette; typography → `font-pool`; guardrails → taste
  checks).
- **provenance** `web-verified` + `community-reverse-eng` (community reverse-engineering, which may
  have drifted from the real brand → mark a confidence level) + **`do-not-copy`** (reverse the
  system only, never take the assets).
- **Already confirmed (the SaaS worked example)**: `stripe` (Söhne / commercial, light large
  headlines) · `vercel` (Geist / free) → see `font-pool.md §1`. SaaS/dev also has linear* /
  supabase / sentry / raycast / warp / cursor / notion (*linear uses Inter, which taste bans — not
  recommended).
- **cap**: do not ingest everything; parse a single brand on demand as a "reference card".
- **First-party official design systems** (also in this bucket, and more authoritative than a
  community DESIGN.md because they are the source): **Ant Design** (ant.design) / **IBM Carbon**
  (carbondesignsystem.com) = **real component code, T1, directly readable by me**; **Material
  Design** (m3.material.io) / **Apple HIG** (developer.apple.com/design) = spec and token anchors.
- **Interaction-detail spec anchor (added 2026-08-05)**: **detail.design** — a curated collection of
  "small design decisions", in **6 categories** (Design / Copywriting / Accessibility / Motion /
  Optimization / Feedback), each entry = a title + **a one-line technique** + a category + a
  screenshot or video demo (**not a long analysis**). **Server-rendered, so I can read the text
  layer directly**; verbatim examples: *"Clicking the Input Label Focuses the Input Field"*
  [Accessibility] · *"Screen Shaking Feedback — Feedback for the dead end."* [Motion] · *"'Follow Us'
  Text Trick — You don't have to say Follow us on X."* [Copywriting].
  ⚠️ **On the two axes of §0 it scores low on both** (no tokens, no animation code) — **do not throw
  it out over the score**: its value is in "**executable interaction rules**", a third dimension the
  two axes cannot measure, and it is the only source here that feeds a checklist directly
  (taste-skill states the taste policy on *which kind* of micro-interaction to use and carries **no
  list of techniques** — they do not overlap).
  **Who looks** 🤝 split: **I read the text layer, you watch the video demos**. `web-verified` ·
  ⚠ **community-curated, not first-party** (one notch below Ant/Carbon) · the demo material is
  `do-not-copy`.
- **Who looks** 🤖 AI reads — I fetch and parse the tokens; a human does not need to visit
  (first-party systems are also 🤖, and for Ant/Carbon even the component code is readable;
  **detail.design is the exception = 🤝**, see its entry).

### Bucket B · Code component libraries (React + Framer)
- **Sources**: Aceternity UI · Magic UI · 21st.dev (has Magic MCP; ⚠ **`21st.com` is a typo for it,
  not a separate product** — it 403s and no evidence of a separate product exists, so **stop
  admitting it as a new source**) · React Bits · motion-primitives · Hover.dev.
- ⚠️ **This bucket is at 6 entries against a cap of ≤3-5 = overloaded**, and as of **2026-08-05 it
  has zero measured usage** (all 6 library names hit nothing in the repo except this register and
  planning documents; 0 hits under `testbed/`, and not one of the 57 material pieces came from
  them). **Nothing new is admitted until the open question of "how do we actually use an external
  component library" is settled** (bucket B ↔ bucket C positioning and priority / install directly
  vs read and rewrite / how far `tsx-direct` goes) — otherwise this is just welding the flood valve
  open.
  **Candidate on hold**: `eldoraui.site` (150+ React/TS/Tailwind/Motion components, a
  shadcn-compatible registry + an official MCP, **LICENSE confirmed MIT** — an extremely rare
  **directly copyable** source in this register) = **🔒 BLOCKED pending that decision**, which is not
  the same as "rejected".
- **VISUAL high / MOTION high, but engine = Framer Motion (React only)**.
- **Engine marks**: `tsx-direct` (a TSX variant uses it directly) / `interpret-to-gsap` (an HTML
  variant borrows the technique and re-authors in GSAP, and is **never** listed as directly
  copyable).
- **How to get it**: most are shadcn-compatible registries → reuse this harness's `shadcn-registry`
  skill for the install path (reuse; do not rebuild).
- **provenance** `web-verified` (the sites are maintained). **cap ≤ 3-5** (do not collect 5 Framer
  libraries).
- **Who looks** 🤝 split — you watch the live demo and pick, I read the code and port it.
- **The entrance organised by workflow category** → `component-pattern-pool.md` (which re-cuts this
  bucket plus shadcn/Radix/Ant/Carbon into a pointer table of "where to get code for this class of
  interaction", across Actions / Input / Nav / Containment / Data-Display / Feedback; structure ≠
  motion, and motion still goes through `motion-pool.md`).

### Bucket C · Tutorial / demo code (vanilla + GSAP/WebGL) — ★ highest motion value
- **Sources**: **Codrops / tympanus** · GSAP Showcase + CodePen GreenSock · GitHub demo repos.
- **VISUAL medium / MOTION high, and engine = GSAP/vanilla → goes straight into our HTML**. A
  WebGL/canvas demo is `webgl-readonly-heavy`.
- **How to get it**: per demo → name + effect + source repo URL + library (GSAP/Three) + a one-line
  technique + portability. **Complex motion comes here first** (I read the real
  `gsap.to(...{duration,ease,stagger})`, timelines, and ScrollTrigger parameters).
- **provenance** `web-verified`. Feeds `motion-pool.md`.
- **Who looks** 🤝 split (motion) — **you judge the demo far faster**, I read the GSAP source and
  build.

### Bucket D · Meta indexes (source-of-sources) — a mine, not the ore
- **Sources**: **`gztchan/awesome-design`** (400+ links in two families, "Get things done" /
  "Concepts": Color/Typography/Toolkit/Prototyping/Styleguide…) · **bentogrids.com** (a bento-layout
  collection, detailed below) · GitHub topic lists.
- **Never ingest wholesale**: run the §2 selection process, pick a small high-signal handful per
  class, fetch-verify each one, and admit only the **verified leaves** into their proper bucket. The
  index itself gets **one line**: "come back and mine this periodically".
- **Who looks** 🤝 — either of us can scan the list; verification splits by type (I read the 🤖 ones,
  you look at the 👁 ones).
- **bentogrids.com (added 2026-08-05, a single-layout collection mine)**: **it has not one line of
  its own source code**; all of its value is in **the origin URL each entry links back to** — which
  is exactly "the mine, not the ore", so it belongs here and **not in bucket E** (an inspiration
  gallery is a terminus; this bucket is an entrance).
  **Measured index** (parsed from its `__NEXT_DATA__`, not estimated): **285 entries, 0 missing a
  `sourceLink`**; of those, **226 link back to a real live product site** (trychroma / neon.tech /
  dovetail / tuple.app / huly.io / pixelmator / june.so / novu.co / useparagon / kentcdodds /
  taipy.io … **all 10 named here were re-curled live on 2026-08-05**) ⇒ **their production CSS can be
  downloaded and taken apart**.
  ⚠ The index also contains **sites this machine cannot reach** (`alfabank.ru`, for instance: curl
  times out / regionally unreachable) — **probe before mining**, and do not mistake unreachable for
  gone. There are also 50 Dribbble images + 7 Framer template sites + 2 Behance entries ⇒ **no CSS to
  take apart, forever human-only**. Categories are `ui` 203 / `graphic` 82 (the latter is print plus
  Figma community templates, **not web**); an `isDark` field (dark 156 / light 129) lets you filter
  by lightness directly; 59 of the 558 assets are video.
  **Mining in four steps**: ① I read the index (already read in full) and filter by keyword / `ui` vs
  `graphic` / lightness → ② pick (I cannot see the images ⇒ you flip through and choose, or I
  pre-filter by the calibre of the site) → ③ take the chosen **origin sites** through
  `vendor/competitive-teardown` **Visual Mode** to dismantle the **production CSS** (download the
  stylesheets + SHA-256 byte-check + count the real hex / faces / grid parameters — the same method
  as the 2026-08-04 game-IP batch, **producing hard evidence rather than "looks like"**) → ④ land it
  on `style-pool.md` as an anchor for "Bento cards"; if a runnable piece is wanted, the bento
  mechanism is CSS Grid `grid-template-areas`/span, **which I write myself without depending on
  their code**.
  **Who looks** 🤝 split (**you look at the images / I read the index and the 226 origin links**).
  `web-verified` · it catalogues other people's sites → `do-not-copy`.
  ⚠️ **Honest boundary**: the 50 Dribbble entries and the 82 `graphic` ones **cannot be dismantled**
  (images / Figma templates, no CSS online); what is genuinely minable is the part of the 203 `ui`
  entries that links to a real site.

### Bucket E · Inspiration galleries (static look + one motion-inspiration exception)
- **Sources**: Awwwards · Godly · SiteInspire · Land-book · Mobbin (login wall) · Savee · Cosmos ·
  **Typewolf** · Fonts In Use · **Design Spells** (designspells.com; the motion exception, below).
- **VISUAL low-medium (static) / MOTION none** (motion sources are bucket C; the only motion
  **inspiration** exception here is Design Spells): they give you layout, colour and type only.
- ⚠️ **This bucket is at 10 entries against a cap of ≈3-5 = chronically overloaded** (counted
  2026-08-05). **Anything new must be a net-zero replacement**; adding without removing is not
  allowed. Removal, like admission, is **a human decision** (the mirror of red line 2 in §5) — I do
  not delete on my own.
- **How to get it**: URL + what to extract + a login-wall flag. For a login wall like Mobbin → ask
  the user for a screenshot → run `image-to-code-skill`. Typewolf / Fonts In Use → anchors for
  `font-pool`.
- **Who looks** 👁 human — purely visual, and a fetch gets me nothing; **you look and you pick** →
  hand me a screenshot for image-to-code.
- **The Design Spells exception (designspells.com, added 2026-08-05, 👁 you look and you pick)**: a
  collection of micro-interactions and easter eggs — hidden animations and playful feedback inside
  **real commercial products** (Monzo's unlock animation · the jumping mini-game hidden in GitHub
  Copilot · Claude Code's effort-selection motion …).
  **Measured shape** (parsed from its `sitemap.xml`): **322 `/spells/` entries, each with one
  `<video:video>` block** (`video:content_loc` → an `.mp4`, `video:thumbnail_loc` → a first-frame
  jpg), and **zero `<video:description>`** ⇒ **each entry = a screen recording plus a title, with no
  explanatory text and no implementation code**. There are also 155 `/apps/` pages aggregating by
  product.
  ⚠️ **I cannot see a single frame**: all I can obtain is **the list of titles** ("Unlock animation in
  Monzo"). Writing "I looked at Design Spells and thought…" **is a violation** (the §0 iron rule).
  **You browse and pick the feel → I interpret it into GSAP under taste (never a copy)**.
  **❌ Does not enter `motion-pool`** — §5 red line: that pool only admits candidates whose **real
  source I have read**, and a recording is not source. Cross-ref `motion-pool.md`.
  `web-verified` (322 entries + a newsletter up to #73) · everything is a recording of **someone
  else's commercial product** → **`do-not-copy`, absolutely**.
  > ⚠ **Note the UA**: a default WebFetch eats a **403** (Cloudflare); curl with a browser UA gets
  > 200. `/rss.xml` is a 404 — the real feed is **`/feed`** (a newsletter digest only, without the
  > entries).
- **🗑 Withdrawn: MotionSites (motionsites.ai)** — net-zero replaced by Design Spells on 2026-08-05
  (bucket E was overloaded, so anything new had to replace something). The two are the same type
  (👁 motion inspiration walls, not portable, never entering motion-pool), but MotionSites is
  **AI-prompt templates** (aimed at Lovable/Cursor generation) rather than real product
  implementations, and its signature Neon Pulse / Crystal Wave / Cosmic Ripple / big gradient heroes
  **collide with `taste-skill` hard rules** (no neon · no gradient headlines · one accent). Its own
  creator's warning acts as **external corroboration** — pages generated straight from the original
  prompts come out nearly identical to the original site and even share its assets (**homogenisation
  risk**, pointing the same way as this register's existing rulings).
  **⇒ It was not thrown away; it moved to the maintainer's private ledger under "📌 standing ·
  cultivating taste"** (the user's personal viewing list: it does not pass the 6 gates, does not
  occupy a cap slot, and does not ship with the skill). **Do not re-admit it as a new source.**

### ⚠️ Domain correction record (measured 2026-08-05 — mistakes already made, do not repeat)

A mistyped domain **fails silently** (DNS does not exist / a redirect / a parking page / a 403) and
leaves no trace, so it is recorded here to prevent a second trip.

| Common spelling | Reality | The correct one |
|---|---|---|
| `bestdesignonx.com` | **DNS does not exist** (one s short) | `bestdesignsonx.com` |
| `bentogrid.com` | 308 permanent redirect (one s short) | **`bentogrids.com`** |
| `designeverywhere.com` | **A GoDaddy parking/for-sale page** (not the site) | `designeverywhere.co` |
| `21st.com` | 403, no evidence of a separate product | A typo for **`21st.dev`**, **not a new source** |

### 🚫 Already rejected (they ran the §2 six gates — do not re-evaluate)

| Source | Which gate it fails | Reason |
|---|---|---|
| **variant.com** | ① fidelity + ③ non-overlap + the §5 first principle | **It is an AI design generator, not a reference source.** Its `meta description`, verbatim: *"Enter an idea for an app or site and see endless design options just by scrolling."* ⇒ what it emits is **design a machine just generated**, not "an external exemplar that already exists and is respected". The value of this library is pointing at **external credible standards**; admitting this welds an echo-chamber entrance onto it (the echo just happens to be someone else's model). **It belongs to none of buckets A–E.** ⚠ "One-click import to Figma" is hearsay, unevidenced on the site, and **unverified** — but even if true, it is still a generator and the ruling stands |
| **bestdesignsonx.com** | ③ non-overlap + ⑥ cap | Hourly-curated X/Twitter design posts. **The same type as Savee / Cosmos already in bucket E** (general visual moodboards) and **weaker** — purely second-hand reposting with no judgement of its own, and copyright sits with the original poster. Bucket E is already 10/5, so **it does not even qualify to replace something** |
| **designeverywhere.co** | ① fidelity | Measured entries are `WK-number + work name by studio` (Nudo Noodle by Workbyworks …), tagged Typography / Logo Design / Identity ⇒ **print / brand identity / packaging, not web UI**, and this repo cannot produce it; some content requires a log-in. **⇒ Moved to the maintainer's private "cultivating taste" list** (the user, 2026-08-05: "可以作为人的审美修养,定期去看") — **not admitted ≠ without value**, precisely because it steps outside the web and supplies taste that looking only at web pages will not build |

---

## 2 · Selection process (how to choose — run this when the user drops "a lot of them", operational)

> This turns "I could recommend many, so how do I choose" into an executable gate. **It is a process,
> not a description.**

```
user drops a batch of sources
   │
   ▼
① bucket them (judge the type against buckets A-E)
   │
   ▼
② run each through the 6-gate rubric (below) ── fails → discard or downgrade
   │
   ▼
③ produce a candidate shortlist: capped + deduplicated + tiered (visual/motion) + engine + provenance labels
   │
   ▼
④ show the user → the user approves (the Stage-1 iron rule: lock the reference list with the user before any fetch or clone)
   │
   ▼
⑤ only once approved, fetch/parse → admit into the right bucket / feed the pool
```

### The 6-gate rubric (all must pass)
1. **Fidelity gate** — score both axes honestly; prefer sources that yield something buildable
   (A/B/C); purely static ones (D/E) are admitted only when they are a **recognised taste anchor**.
2. **Engine-match gate** — GSAP/vanilla goes straight into HTML; Framer/React goes into TSX, and in
   HTML it is `interpret-only` **and must be marked as such**, never dressed up as directly
   copyable.
3. **Non-overlap gate** — what you are adding must be a capability the register and existing buckets
   do not already have (do not collect 5 Framer libraries); if the user later names a private
   collection skill, run it through this gate before adding it.
4. **Source / freshness gate** — maintained and canonical (stars, recent commits); community
   reverse-engineering (a DESIGN.md) gets a confidence label.
5. **Copyright / do-not-copy gate** — for a major brand's assets, reverse the system only → mark
   `do-not-copy`.
6. **Per-class cap gate** — ≈3-5 per class. Keep it a **springboard, not a dumping ground**. This is
   the flood valve.

> **Default disposition** (once a shortlist has passed the 6 gates above and you have reviewed it):
> anything **you did not explicitly reject is promoted** (admitted by default) — there is no need to
> nod at each one; only what you explicitly drop is dropped. The flood valve is held at the
> "getting onto the shortlist" gate; **once on the shortlist, the default is to keep**.

---

## 3 · Call contract (how the user opens → where I go → what I return)

| The user says | I go to | I return |
|---|---|---|
| **"inspiration / reference: \<vibe or feel\>"** (taste) | Bucket E galleries + bucket A anchors + Typewolf | A curated **URL shortlist** + one line per entry on "why, and what to extract" (reverse-engineer, do not copy) |
| **"find me code that can do X"** (implementation, especially complex motion) | Bucket C (GSAP/vanilla, first choice) → bucket B (React/Framer) | **Portable source + a plan to port it** into our chassis + GSAP + taste (code + source URL + engine mark) |
| **"make it like \<brand\>"** (brand style) | Bucket A: pull that brand's `DESIGN.md` as a reference card | Real tokens (high visual) + the honest reminder that it **gives you the look and not the motion**, and the assets are `do-not-copy` |

- Inspiration → URLs; implementation → portable code + URLs. **A live, verified URL needs WebSearch /
  WebFetch or the user to supply it**; from memory alone I can only give a canonical name, with no
  guarantee of freshness.
- **Who-looks mapping**: row 1, inspiration = 👁 **you look** (I only give URLs and do not pretend I
  can read them); row 2, find code = 🤝/🤖 **I read**; row 3, brand = 🤖 **I parse**. The consumer
  axis (§0) is the underlying logic of this contract.

## 4 · Reuse existing skills (do not rebuild)
**They are all in this repo's `vendor/`** (vendored from global, so a clone is complete; upstream
still lives in `~/.claude/skills/`):
`vendor/competitive-teardown` (dismantling a reference site — the lab copy has **only** the
Design-Reference Visual Mode, which produces a visual extraction card; the commercial-scorecard half
was not copied) ·
`vendor/image-to-code-skill` (screenshot → code, serving bucket E and login-walled galleries) ·
`vendor/shadcn-registry` (bucket B installs) ·
`vendor/imagegen-frontend-web` (generating reference images).
Motion taste is not outsourced: the lab canonical is `authoring/taste-skill` §8.
There is also the global `development-workflow.md §0 Research & Reuse` (harness level; it does not
travel with this repo).

## 5 · Growth governance (how the library grows — human-gated, against a self-produced echo chamber)

> **First principle: the value of this library is that it points at "external credible standards".**
> Once it fills up with our own output it degenerates into a self-referential echo chamber and loses
> any meaning as a set of credible exemplars. So growth has red lines.

**Red line 1 · Our own output never enters as a standard automatically.** A page that came out well,
a LEAD the user picked, a surface that cleared the scorer — each of those only means "**it suited
this project**", **not "it is an industry exemplar"**. Winning does not admit it.

**Red line 2 · The only thing that flows back is "external" material discovered during a run**, and
it must be **human-gated**:
- I **do not add it myself**; I **surface the candidate to the user** (anchor + URL/source + one line
  on why + provenance + the result of the §2 six gates), and **the user decides whether it goes in**
  (an extension of the Stage-1 iron rule: admission is a human decision).

**How much I can help, pool by pool (capability honesty):**
| pool | What I can do | What needs a human |
|---|---|---|
| **style-pool** | When a style shows up that the pool lacks → report it: name + URL + why | **You go and look at that site yourself before deciding** (taste is human work; my reading a static page is not the same as judging whether it is good) |
| **font / palette** | Lift **real families and hex values off a real DESIGN.md or official site** as candidates (it can be done from data) | Whether it is "externally credible" enough, and admission — you nod |
| **motion** | Propose candidates **only where I have read real source** (bucket C, GSAP/vanilla) | I **cannot judge motion by "watching" it** → a human, or the scorer's `interaction_quality`, judges; **I may not update motion-pool automatically** |

**Provenance tiering (the library's constitution)**: `web-verified` / canonical = the **spine** (the
library should be mostly this tier); `your-skill` = an **internal verification mark, one notch
weaker than a standard**, and it should not lead any pool (the `Northway` / `Grove` rows are kept
only as "we used this, worth referencing", not as industry exemplars).
