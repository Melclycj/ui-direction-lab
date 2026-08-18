# IA principles — ratified prior-art distillation (2026-07-03)

Absorbed from the 2026-07-03 prior-art survey (full memo with sources:
`testbed/runs/2026-07-03-ia-mvp-verify/ia-prior-art.md`; shortlist **ratified in full by the
user**). Interpretations of published principles — lineage cited, nothing copied. This file is
Stage-B judgment guidance; the SHAPES stay in `data-contracts.md` (which wins on any conflict).

## Lineage (why this skill's artifacts look the way they do)

- **Priority Guides** (Drew Clemens 2012; Overkamp & den Houting, A List Apart 2018): content +
  elements "sorted by hierarchy from top to bottom and without layout specifications", real
  content only, early-phase tool that hands visual freedom downstream. = our grey-box board.
- **Page Description Diagrams** (Dan Brown, 1999): each component described by the NEED it
  serves, in three priority bands, layout deliberately withheld — because wireframes lock client
  expectations early and cage the designer. = our info-spec + tiers + composition-free rule.

Two independent industry methods arrived at the same shape; this skill is their machine-checkable
descendant (deterministic leak lint + schema), not a new invention.

## Tier semantics (PDD-aligned wording)

- **tier 1** — vital to understanding what this screen fundamentally is and does
- **tier 2** — needed for the screen to function well for the majority of its use
- **tier 3** — useful, but not vital (ambient / meta)

## Stage-B judgment checklist (Dan Brown, 5 of the Eight Principles of IA, 2010)

- **Choices** — fewer, task-focused: each screen serves its ONE `primary_task`; >7±2 top-level
  blocks usually means two screens.
- **Disclosure** — preview first, detail on demand; `within_page_flow` should carry exactly this
  (what surfaces what, what is subordinate).
- **Front doors** — don't assume entry via the hero: every screen must make sense when arrived at
  directly; a `link_map` whose topology only works from one entry point is a smell.
- **Focused navigation** — one nav group carries ONE kind of information; don't mix kinds.
- **Growth** — the structure must survive 10× the content (would the tiers/groups still hold with
  10,000 work items? if not, the hierarchy is undesigned, not just unstyled).

## Object anchoring (OOUX / Sophia Prater — the one rule we take)

Prefer blocks anchored on **domain objects** (transaction, payout, report) over ad-hoc groupings.
The same object appearing on different screens keeps the **same block shape** (same information,
same tier logic), varied only in depth. Cheapest cross-screen-consistency lever, and it directly
feeds round-2: a locked composition generalizes better across screens whose blocks are
object-shaped. (Full 15-step ORCA is deliberately NOT adopted — too heavy for this pipeline.)

## Stage-A note (Priority Guides)

When input material is thin, **co-create the section/block topic list WITH the user** before
designing — don't fill gaps alone. Pairs with the `[ASSUMED]`-marking rule; the user confirms
topics, the skill designs structure.

## Validation upgrades (NN/g — optional, client-shipping products only)

- **Card sorting** — derive grouping from users' mental models (informs `group`);
- **Tree testing** — validate findability of the hierarchy/`link_map` (60–80% success = good,
  >90% excellent).

NOT part of the default pipeline (lab output = review prototypes, human board gate suffices);
recommend to clients when the IA will actually ship.

## Ecosystem note (2026-07-03 survey)

No existing agent skill produces a layout-open info spec that feeds a visual pipeline. Nearest
neighbors: marketing-site sitemap/URL skills (page-level, SEO-oriented) and audit-direction IA
critique (Rosenfeld & Morville four-systems — useful as a completeness lens on a finished spec).
Differentiation to protect: composition-free spec + deterministic leak lint + the two-round wrap
around prototyping.
