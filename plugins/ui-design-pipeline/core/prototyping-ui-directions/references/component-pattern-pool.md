# Component pattern pool (component-pattern-pool) — pointers, not an inventory

> ⚠️ **This is a table of "where to find component code", not a component inventory and not a
> menu.** Used at `prototyping-ui-directions` Stage 1 and when `anchor-prototype-wave` authorises a
> surface: know which **registry** holds reusable code for a class of interaction (action / input /
> navigation / …) instead of hand-rolling it. The organising axis is the **workflow category**
> (borrowing the component taxonomy from the `design-system` companion skill as a structure —
> **not forking it**). Same origin as `reference-sources.md` bucket B (code component libraries) and
> the `shadcn-registry` skill; this table is that material re-cut by workflow category.

## Schema / conventions
- **Organising axis = 6 workflow categories** (not by registry): Actions / Input / Navigation /
  Containment / Data-Display / Feedback.
- Each category gives: **typical components** · **where to get them (registry pointer)** ·
  **engine / consumer**. It does **not** enumerate components — it is an entrance, not a warehouse.
- **Three engine marks** (same as `reference-sources.md` §0):
  - `readable-code` 🤖 — source I can read directly (shadcn / Radix / Ant / Carbon), portable into
    chassis + taste.
  - `tsx-direct` — the Framer Motion registry (bucket B); goes into a **TSX** variant only.
  - `interpret-to-gsap` — an **HTML** variant borrows the technique only and re-authors the motion
    in GSAP (see `motion-pool.md`); **never passed off as a direct copy**.
- **Cap ≈ 2-4 pointers per category** (flood control; this is an entrance, not a repository).

## ⚠️ Iron rule · structure ≠ motion (honesty)
A static registry or DESIGN.md gives you **component structure + token usage** (**no motion**). How a
component *moves* is a separate question, and it always goes to **`motion-pool.md`** (GSAP recipes).
This pool points at where structure comes from and **does not describe motion**. Do not treat a
registry's Framer demo as "HTML motion you can copy" — it is React, and an HTML variant can only
`interpret-to-gsap`.

## 6 categories × registry pointers

| Category | Typical components (examples, not exhaustive) | Where to get them (registry pointer) | engine / consumer |
|---|---|---|---|
| **Actions** | button · icon-button · button-group · dropdown-menu · FAB | shadcn (button / dropdown-menu) · Radix Primitives · Ant / Carbon | `readable-code` 🤖 |
| **Input** | input · textarea · select · combobox · checkbox · radio · switch · slider · date-picker · form | shadcn (form / input / select …) · Radix · React Hook Form (validation logic) · Ant / Carbon | `readable-code` 🤖 |
| **Navigation** | navbar · tabs · breadcrumb · pagination · sidebar · command palette · menubar | shadcn (tabs / navigation-menu / command) · Radix · bucket B (the animated navbars in Aceternity / Magic UI) | `readable-code` 🤖 / bucket B `interpret-to-gsap` 🤝 |
| **Containment** | card · dialog · drawer · sheet · accordion · collapsible · popover · tooltip | shadcn (dialog / drawer / accordion / popover) · Radix · Vaul (drawer) | `readable-code` 🤖 |
| **Data-Display** | table · data-table · list · badge · avatar · stat · chart · tree · calendar | shadcn (table) · TanStack Table (table logic) · Tremor (charts) · Ant / Carbon | `readable-code` 🤖 |
| **Feedback** | toast · alert · progress · spinner · skeleton · empty-state · confirm-modal | shadcn (sonner / alert / progress / skeleton) · Radix | `readable-code` 🤖 |

> **Where motion comes from (shared by every category)**: the table above gives you **structure**.
> For "how does this card / toast / tab **enter or transition**" go to `motion-pool.md` (#1–#20 GSAP
> recipes: text effects plus whole-page scroll choreography). Bucket B (Aceternity / Magic UI /
> React Bits) has flashy motion but it is **Framer/React**: a TSX variant may use `tsx-direct`, an
> HTML variant may only `interpret-to-gsap` (read the technique, re-author in GSAP), **labelled as
> such, never passed off as a direct copy**.

## Usage notes
- At Stage 1 or when a surface is authorised, first ask **which category the interaction you need
  belongs to**, look it up here, take the registry pointer, and install through `shadcn-registry`
  (**not redistributed with this package = nominated**; the lab checkout has it at
  `vendor/shadcn-registry`, and if it cannot be installed, record `companion_skipped: shadcn-registry`
  and go to the registry page by hand). Bucket B installs through the same skill's
  registry path. Do not hand-roll.
- What you get back is **structure**. Put the chassis tokens on it (color / type / space via
  `--token-*`), pass it through the `taste-skill` gate, and take motion from `motion-pool`.
- **Do not fork the `design-system` skill** (it overlaps with prototyping): this table borrows only
  its **workflow taxonomy** as an organising axis; component code still comes from the registry.
- First-party systems (Ant Design / IBM Carbon) have T1-readable component code (🤖) and are more
  authoritative than a community registry. When you need real token values, WebFetch their docs and
  confirm each one — never write a hex or a px from memory.

## Growth (human-gated, see `reference-sources.md` §5)
- **Candidates can be proposed from data**: a registry is an external, credible standard (maintained
  and canonical), so I can lift **real registry pointers** from a real site or repo and propose them
  (`web-verified`).
- **Admission stays human**: I surface the candidate (category + registry + URL + engine mark) and
  **you decide whether it goes in**. The cap (≈2-4 per category) is the flood valve.
- **Self-produced components are not standards**: a good component that came out of a wave is not an
  industry exemplar and is never auto-filed back into this pool (same red line as
  `reference-sources.md` §5).
