---
name: design-system
description: >
  Curated catalog of ~165 public design systems with tags for component
  availability, voice/tone guidance, designer assets (Sketch/Figma), and
  open-source source code. Use to shortlist reference systems for UI
  direction exploration (Stage 1 of `prototyping-ui-directions`), to find
  anchor candidates before locking a chassis in `anchor-prototype-wave`,
  or when the user asks for design-system recommendations matching a
  specific stance ("neutral enterprise", "government clarity", "playful
  consumer", "developer tooling", "data-dense").
  Trigger phrases: "what design systems should I look at", "shortlist
  design systems for X", "give me 3 references for [stance]",
  "find me design systems with open-source code", "pull design-system
  candidates".
  This skill provides LINKS, not extracted token values — verifying
  actual palette/typography requires WebFetch on the linked docs.
allowed-tools: Read, WebFetch
---

# design-system

## What this is

An index of ~165 public design systems (corporate, government,
open-source frameworks). **This SKILL.md is the single source of truth for
the catalog — the sibling `README.md` is provenance only and does not
duplicate the table.** Each row is tagged with:

| Tag | Meaning |
|---|---|
| **Components** | Has coded UI components |
| **Voice & Tone** | Has writing / voice guidance |
| **Designers Kit** | Has Sketch / Figma / Photoshop assets |
| **Source code** | Publicly viewable source (GitHub / GitLab / Bitbucket) |

The catalog does **not** contain extracted palette, typography, or
spacing values. For actual token values, follow the link and `WebFetch`
the system's docs site.

## When to use this skill

- **Stage 1 reference acquisition** in `prototyping-ui-directions`:
  shortlist 3-5 reference systems matching the user's brief.
- **Pre-anchor lock** in `anchor-prototype-wave`: when the user wants
  the chassis to echo an existing system's stance, find candidates here
  first.
- **Standalone**: user asks "what design systems should I look at for
  [X]" or "give me 3 references for [stance]".

## How to use this skill

1. **Read the catalog** below.
2. **Filter to a focused shortlist of 3-5** matching the user's brief.
   Use the tags plus heuristic stance mapping:
   - Neutral enterprise / B2B SaaS → Atlassian, IBM Carbon, Microsoft
     Fluent, Salesforce Lightning, Shopify Polaris, AWS Cloudscape
   - Government clarity → GOV.UK, U.S. Web, Singapore SGDS, French DSFR,
     Italia, Estonia, Ontario
   - Developer tooling → GitHub Primer, Mantine, Shadcn/ui, Radix,
     JetBrains Ring UI, HashiCorp Helios, Vercel Geist
   - Data-dense / dashboard → AWS Cloudscape, IBM Carbon, Elastic EUI,
     Salesforce Lightning, Morningstar
   - Playful / consumer → Duolingo (tone), Skyscanner Backpack,
     Pinterest Gestalt, Material Minimal
   - Editorial / publishing → FT Origami, BBC GEL, Mailchimp tone,
     Artsy Palette
   - Component-library-as-product → Chakra, Mantine, Radix, Shoelace,
     Reshaped, Bumbag, Evergreen
3. **Cite each candidate by name + link.** Never invent token values.
4. **If the downstream skill needs actual palette / typography / spacing**,
   announce which 1-3 sites you intend to `WebFetch`, then fetch and
   quote the values verbatim with the URL.

## Anti-patterns

- Inventing token values ("Carbon uses #0F62FE", "Polaris radius is
  8px") without `WebFetch` — values drift between versions.
- Returning the whole catalog instead of a focused shortlist of 3-5.
- Treating the tags as exhaustive — a system without a "Designers Kit"
  tag here may still publish one on its docs site; the catalog reflects
  what was indexed, not what currently exists.
- Recommending a system whose link is dead. If a fetch fails, note it
  and substitute another candidate from the same stance group.

---

## Catalog

> Source: [alexpate/awesome-design-systems](https://github.com/alexpate/awesome-design-systems).
> Open-source projects may have varying licenses — always check before
> reusing assets or code.

|                                                                                    | Components | Voice & Tone | Designers Kit |                                             Source code \*                                             |
| ---------------------------------------------------------------------------------- | :--------: | :----------: | :-----------: | :----------------------------------------------------------------------------------------------------: |
| [Aalto University](https://brand.aalto.fi/)                                        |     👍     |      👍      |      👍       |                                                                                                        |
| [Adobe Spectrum](https://spectrum.adobe.com)                                       |     👍     |      👍      |      👍       |                          [:octocat:](https://github.com/adobe/react-spectrum)                          |
| [Adjust Atlas](https://atlas.adeven.com)                                           |     👍     |      👍      |      👍       |                                                                                                        |
| [Alaska Airlines](https://auro.alaskaair.com/)                                     |     👍     |      👍      |      👍       |                             [:octocat:](https://github.com/AlaskaAirlines)                             |
| [Alibaba Ant Design](https://ant.design)                                           |     👍     |      👍      |      👍       |                         [:octocat:](https://github.com/ant-design/ant-design/)                         |
| [Amplify UI](https://ui.docs.amplify.aws/)                                         |     👍     |      👍      |      👍       |                        [:octocat:](https://github.com/aws-amplify/amplify-ui/)                         |
| [Appear Here Styleguide](https://bloom.appearhere.co.uk/)                          |     👍     |              |               |                            [:octocat:](https://github.com/appearhere/bloom)                            |
| [Apple Developer Design Guidelines](https://developer.apple.com/design/)           |            |              |      👍       |                                                                                                        |
| [Aragon UI](https://ui.aragon.org/)                                                |     👍     |              |               |                               [:octocat:](https://github.com/aragon/ui)                                |
| [Artsy Palette](https://palette.artsy.net/)                                        |     👍     |              |               |                             [:octocat:](https://github.com/artsy/palette)                              |
| [Astro UXDS](https://astrouxds.com/)                                               |     👍     |              |      👍       |                [:octocat:](https://github.com/RocketCommunicationsInc/astro-components)                |
| [AT UIKIT](https://at-ui.github.io/at-ui/#/en)                                     |     👍     |              |               |                              [:octocat:](https://github.com/at-ui/at-ui)                               |
| [Atlassian Design System](https://atlassian.design)                                |     👍     |      👍      |      👍       |             [:space_invader:](https://bitbucket.org/atlassian/atlassian-frontend-mirror/)              |
| [Audi UI Kit](https://www.audi.com/ci/en/guides/user-interface/introduction.html)  |     👍     |              |      👍       |                              [:octocat:](https://github.com/audi/audi-ui)                              |
| [Aurora (Government of Canada)](https://design.gccollab.ca/)                       |     👍     |      👍      |      👍       |                     [:octocat:](https://github.com/gctools-outilsgc/design-system)                     |
| [AutoGuru Overdrive](http://overdrive.autoguru.io/)                                |     👍     |              |               |                         [:octocat:](https://github.com/autoguru-au/overdrive)                          |
| [AWS Cloudscape Design System](https://cloudscape.design/)                         |     👍     |      👍      |      👍       |                      [:octocat:](https://github.com/cloudscape-design/components)                      |
| [Backpack (Skyscanner)](https://skyscanner.design/)                                |     👍     |      👍      |      👍       |                          [:octocat:](https://github.com/skyscanner/backpack)                           |
| [Basis Design System](https://basis.now.sh)                                        |     👍     |              |               |                             [:octocat:](https://github.com/moroshko/basis)                             |
| [BBC GEL (Global Experience Language)](https://www.bbc.co.uk/gel)                  |     👍     |      👍      |      👍       |                                                                                                        |
| [Bento DS](https://bento-ds.com)                                                   |     👍     |              |      👍       |                       [:octocat:](https://github.com/buildo/bento-design-system)                       |
| [BLiP](https://design.take.net/)                                                   |     👍     |              |               |                          [:octocat:](https://github.com/takenet/blip-toolkit)                          |
| [Blueprint](https://blueprintjs.com/)                                              |     👍     |              |      👍       |                           [:octocat:](https://github.com/palantir/blueprint)                           |
| [Bold (Bridge Design System)](https://bold.bridge.ufsc.br/)                        |     👍     |              |      👍       |                         [:octocat:](https://github.com/laboratoriobridge/bold)                         |
| [Bolt Design System](https://boltdesignsystem.com/)                                |     👍     |              |               |                         [:octocat:](https://github.com/boltdesignsystem/bolt)                          |
| [Braid Design System](https://seek-oss.github.io/braid-design-system/)             |     👍     |              |               |                      [:octocat:](https://github.com/seek-oss/braid-design-system)                      |
| [British Gas Nucleus](https://britishgas.design/)                                  |     👍     |      👍      |               |                                                                                                        |
| [Buildit Gravity](http://style.buildit.digital/)                                   |     👍     |              |               |                         [:octocat:](https://github.com/buildit/gravity-ui-web)                         |
| [Bumbag UI](https://bumbag.style/)                                                 |     👍     |              |               |                            [:octocat:](https://github.com/bumbag/bumbag-ui)                            |
| [BuzzFeed Solid](https://solid.buzzfeed.com/)                                      |     👍     |              |      👍       |                             [:octocat:](https://github.com/buzzfeed/solid)                             |
| [Buzzvil Design System](https://design.buzzvil.com/)                               |     👍     |      👍      |               |                                                                                                        |
| [CA Technologies Mineral UI](https://mineral-ui.netlify.app/)                      |     👍     |              |               |                         [:octocat:](https://github.com/mineral-ui/mineral-ui)                          |
| [CBRE Blocks](https://blocks.cbrebuild.com/)                                       |     👍     |      👍      |               |                                                                                                        |
| [Cedar](https://rei.github.io/rei-cedar-docs/)                                     |     👍     |              |      👍       |                             [:octocat:](https://github.com/rei/rei-cedar)                              |
| [Chakra UI](https://chakra-ui.com/)                                                |     👍     |              |               |                          [:octocat:](https://github.com/chakra-ui/chakra-ui)                           |
| [City of Boston Fleet](https://patterns.boston.gov/)                               |     👍     |      👍      |               |                          [:octocat:](https://github.com/CityOfBoston/digital)                          |
| [Cloudflare](https://cloudflare.github.io/cf-ui/)                                  |     👍     |              |               |                            [:octocat:](https://github.com/cloudflare/cf-ui)                            |
| [Co-op Experience Library](https://www.coop.co.uk/experience-library/)             |     👍     |      👍      |      👍       |                     [:octocat:](https://github.com/coopdigital/experience-library)                     |
| [Contentful Forma 36](https://f36.contentful.com/)                                 |     👍     |      👍      |      👍       |                          [:octocat:](https://github.com/contentful/forma-36)                           |
| [Decathlon Design System - Vitamin](https://decathlon.design/)                     |     👍     |              |      👍       |                         [:octocat:](https://github.com/decathlon/vitamin-web)                          |
| [Decentraland UI](https://ui.decentraland.org/)                                    |     👍     |              |               |                            [:octocat:](https://github.com/decentraland/ui)                             |
| [Duet](https://www.duetds.com)                                                     |     👍     |              |      👍       |                                                                                                        |
| [Duolingo](https://design.duolingo.com/)                                           |            |      👍      |               |                                                                                                        |
| [eBay Skin](https://ebay.github.io/skin/)                                          |     👍     |              |               |                               [:octocat:](https://github.com/eBay/skin)                                |
| [Elastic UI Framework](https://elastic.github.io/eui/)                             |     👍     |      👍      |      👍       |                              [:octocat:](https://github.com/elastic/eui)                               |
| [ENGIE Fluid Design System](https://www.engie.design)                              |     👍     |              |      👍       |                                                                                                        |
| [Enel](https://dsyui.enelx.com/)                                                   |     👍     |              |               |                                                                                                        |
| [Enigma Boundless](https://boundless.js.org/)                                      |     👍     |              |               |                          [:octocat:](https://github.com/enigma-io/boundless)                           |
| [Estonia Country Design Guidelines](https://brand.estonia.ee)                      |     👍     |      👍      |      👍       |                                                                                                        |
| [Evergreen](https://evergreen.surge.sh)                                            |     👍     |              |               |                          [:octocat:](https://github.com/segmentio/evergreen)                           |
| [Financial Times Origami](https://origami.ft.com/)                                 |     👍     |              |               |                        [:octocat:](https://github.com/Financial-Times/origami)                         |
| [Finland Toolbox](https://toolbox.finland.fi/)                                     |            |      👍      |      👍       |                                                                                                        |
| [Firefox Photon Design System](https://design.firefox.com/photon)                  |     👍     |      👍      |      👍       |                            [:octocat:](https://github.com/FirefoxUX/photon)                            |
| [Flowbite Design System](https://www.figma.com/community/file/1179442320711977498) |     👍     |              |      👍       |                          [:octocat:](https://github.com/themesberg/flowbite)                           |
| [Fluent UI](https://developer.microsoft.com/en-us/fluentui#/)                      |     👍     |      👍      |      👍       |                           [:octocat:](https://github.com/microsoft/fluentui)                           |
| [Foundation](https://get.foundation/)                                              |     👍     |      👍      |      👍       |                      [:octocat:](https://github.com/foundation/foundation-sites)                       |
| [Foyer Design System](https://design.foyer.lu/)                                    |     👍     |              |      👍       |                                         :closed_lock_with_key:                                         |
| [French Government Design System](https://www.systeme-de-design.gouv.fr/)          |     👍     |      👍      |      👍       |                          [:octocat:](https://github.com/GouvernementFR/dsfr)                           |
| [FutureLearn Pattern Library](https://www.futurelearn.com/pattern-library)         |     👍     |              |               |                                                                                                        |
| [GitHub Primer](https://primer.style/)                                             |     👍     |              |      👍       |                                [:octocat:](https://github.com/primer/)                                 |
| [GitLab Design System - Pajamas](https://design.gitlab.com/)                       |     👍     |      👍      |      👍       |                     [:fox_face:](https://gitlab.com/gitlab-org/design.gitlab.com)                      |
| [GoodBarber Design System](https://www.goodbarber.com/uxdesign/)                   |     👍     |              |               |                                                                                                        |
| [Google Material Design](https://material.io/guidelines/#introduction-goals)       |     👍     |      👍      |      👍       |                [:octocat:](https://github.com/material-components/material-components)                 |
| [GOV.UK Design System](https://www.gov.uk/design-system)                           |     👍     |              |               |                      [:octocat:](https://github.com/alphagov/govuk-design-system)                      |
| [Gympass Yoga](https://gympass.github.io/yoga/)                                    |     👍     |      👍      |               |                              [:octocat:](https://github.com/gympass/yoga)                              |
| [HashiCorp Helios](https://helios.hashicorp.design)                                |     👍     |      👍      |      👍       |                        [:octocat:](https://github.com/hashicorp/design-system)                         |
| [Help Scout](https://style.helpscout.com/)                                         |     👍     |      👍      |               |                        [:octocat:](https://github.com/helpscout/seed-framework)                        |
| [Heroku Purple3](https://design.herokai.com/)                                      |     👍     |              |               |                                                                                                        |
| [Hewlett Packard grommet](https://grommet.github.io)                               |     👍     |              |               |                            [:octocat:](https://github.com/grommet/grommet)                             |
| [HubSpot Canvas](https://canvas.hubspot.com/)                                      |     👍     |      👍      |               |                             [:octocat:](https://github.com/HubSpot/canvas)                             |
| [Hudl Design System](https://uniform.hudl.com/)                                    |     👍     |      👍      |               |                                                                                                        |
| [IBM Carbon](https://www.carbondesignsystem.com/)                                  |     👍     |      👍      |      👍       |                         [:octocat:](https://github.com/ibm/carbon-components)                          |
| [IBM Design Language](https://www.ibm.com/design/language/)                        |     👍     |      👍      |               |                                                                                                        |
| [IBM Northstar](https://www.ibm.com/standards/web/)                                |     👍     |      👍      |               |                                                                                                        |
| [Intuit Harmony](https://designsystem.quickbooks.com/)                             |     👍     |      👍      |      👍       |                                                                                                        |
| [Italia Design System](https://designers.italia.it/design-system/)                 |     👍     |      👍      |      👍       |                                 [:octocat:](https://github.com/italia)                                 |
| [JB Design System](https://javadbat.github.io/design-system)                       |     👍     |      👍      |               |                         [:octocat:](https://javadbat.github.io/design-system)                          |
| [JetBrains Ring UI](https://jetbrains.github.io/ring-ui)                           |     👍     |              |               |                           [:octocat:](https://github.com/JetBrains/ring-ui)                            |
| [Jobber](https://atlantis.getjobber.com) (🔱 Atlantis)                             |     👍     |              |               |                           [:octocat:](https://github.com/GetJobber/atlantis)                           |
| [Just Eat Takeaway.com PIE Design System](https://pie.design/)                     |     👍     |              |      👍       |                          [:octocat:](https://github.com/justeattakeaway/pie)                           |
| [Kaizen](https://cultureamp.design/)                                               |     👍     |      👍      |               |                    [:octocat:](https://github.com/cultureamp/kaizen-design-system)                     |
| [KoliBri](https://public-ui.github.io/) (Public-UI)                                |     👍     |              |               |                           [:octocat:](https://github.com/public-ui/kolibri/)                           |
| [Kontur](https://guides.kontur.ru/)                                                |     👍     |              |      👍       |                          [:octocat:](https://github.com/skbkontur/retail-ui/)                          |
| [Korea Design System](https://www.krds.go.kr)                                      |     👍     |      👍      |      👍       |                          [:octocat:](https://github.com/KRDS-uiux/krds-uiux)                           |
| [Lexicon](https://lexicondesign.io/)                                               |     👍     |      👍      |               |                                                                                                        |
| [Louder Than Ten Manual](https://www.louderthanten.com/manual)                     |     👍     |      👍      |               |                                                                                                        |
| [Mail.ru Group Paradigm](https://design.mail.ru/)                                  |     👍     |      👍      |      👍       |                                                                                                        |
| [Mailchimp Content Styleguide](https://styleguide.mailchimp.com/)                  |            |      👍      |               |                                                                                                        |
| [Mantine](https://mantine.dev/)                                                    |     👍     |              |               |                           [:octocat:](https://github.com/mantinedev/mantine)                           |
| [Marvel Styleguide](https://marvelapp.com/styleguide)                              |     👍     |              |               |                                                                                                        |
| [Material Minimal](https://material-minimal.com/)                                  |     👍     |      👍      |      👍       |                         [:octocat:](https://github.com/mdbootstrap/mdb-ui-kit)                         |
| [Materialize CSS](https://materializecss.com/)                                     |     👍     |              |      👍       |                          [:octocat:](https://github.com/Dogfalo/materialize)                           |
| [Mesh Design System](https://www.meshdesignsystem.com/)                            |     👍     |              |      👍       |                                                                                                        |
| [Microsoft Fluent](https://www.microsoft.com/design/fluent/)                       |     👍     |              |      👍       |                           [:octocat:](https://github.com/microsoft/fluentui)                           |
| [Mixpanel Design System](https://design.mixpanel.com)                              |     👍     |      👍      |               |                                                                                                        |
| [MongoDB Design System](http://mongodb.design)                                     |     👍     |              |      👍       |                             [:octocat:](https://github.com/mongodb/design)                             |
| [Monzo Tone of Voice](https://monzo.com/tone-of-voice/)                            |            |      👍      |               |                                                                                                        |
| [Morningstar Design System](http://designsystem.morningstar.com/)                  |     👍     |      👍      |      👍       |                                                                                                        |
| [Mozilla Protocol](https://protocol.mozilla.org/)                                  |     👍     |              |               |                            [:octocat:](https://github.com/mozilla/protocol)                            |
| [NASA Web Design System](https://nasa.github.io/nasawds-site/)                     |     👍     |              |               |                              [:octocat:](https://github.com/nasa/nasawds)                              |
| [NationBuilder Radius](https://www.nationbuilder.design/)                          |     👍     |              |               |                                                                                                        |
| [NHS.UK Service Manual](https://service-manual.nhs.uk/)                            |     👍     |      👍      |               |                                                                                                        |
| [Nordhealth](https://nordhealth.design/)                                           |     👍     |              |      👍       |                                                                                                        |
| [New York State Design System](https://designsystem.ny.gov/components/)            |     👍     |              |      👍       |                             [:octocat:](https://github.com/ITS-HCD/nysds)                              |
| [Nordnet](https://brand.nordnet.se/)                                               |     👍     |      👍      |               |                                                                                                        |
| [Okta Odyssey Design System](https://odyssey.okta.design)                          |     👍     |              |      👍       |                              [:octocat:](https://github.com/okta/odyssey)                              |
| [Ontario Design System](https://designsystem.ontario.ca/)                          |     👍     |              |      👍       | [:globe_with_meridians:](https://designsystem.ontario.ca/docs/documentation/release-notes.html#latest) |
| [Oracle Redwood](https://redwood.oracle.com)                                       |     👍     |              |      👍       |                                                                                                        |
| [Persona Design System](https://privy-open-source.github.io/design-system/)        |     👍     |      👍      |               |                    [:octocat:](https://github.com/privy-open-source/design-system)                     |
| [Pharos: JSTOR's Design System](https://pharos.jstor.org)                          |     👍     |      👍      |               |                             [:octocat:](https://github.com/ithaka/pharos)                              |
| [Pinterest Gestalt](https://pinterest.github.io/gestalt/#/)                        |     👍     |              |               |                           [:octocat:](https://github.com/pinterest/gestalt)                            |
| [Pivotal](https://styleguide.pivotal.io/)                                          |     👍     |              |               |                         [:octocat:](https://github.com/pivotal-cf/pivotal-ui)                          |
| [Pluralsight Design System](https://design-system.pluralsight.com/)                |     👍     |              |               |                       [:octocat:](https://github.com/pluralsight/design-system)                        |
| [Porsche Design System](https://designsystem.porsche.com)                          |     👍     |              |      👍       |              [:octocat:](https://github.com/porsche-design-system/porsche-design-system)               |
| [Priceline Design System](https://priceline.github.io/design-system/)              |     👍     |      👍      |               |                        [:octocat:](https://github.com/priceline/design-system)                         |
| [Pusher Chameleon](https://pusher.github.io/chameleon/)                            |     👍     |              |               |                            [:octocat:](https://github.com/pusher/chameleon)                            |
| [Radix](https://www.radix-ui.com/)                                                 |     👍     |              |               |                                [:octocat:](https://github.com/radix-ui)                                |
| [Rambler](https://rambler-digital-solutions.github.io/rambler-ui/)                 |     👍     |              |               |                  [:octocat:](https://github.com/rambler-digital-solutions/rambler-ui)                  |
| [Rendition](https://balena-io-modules.github.io/rendition/)                        |     👍     |              |               |                      [:octocat:](https://github.com/balena-io-modules/rendition/)                      |
| [Reshaped](https://reshaped.so)                                                    |     👍     |              |      👍       |                                                                                                        |
| [Salesforce Lightning Design System](https://www.lightningdesignsystem.com)        |     👍     |      👍      |      👍       |                      [:octocat:](https://github.com/salesforce-ux/design-system)                       |
| [Sage by Kajabi](https://sage.kajabi.com)                                          |     👍     |              |               |                            [:octocat:](https://github.com/Kajabi/sage-lib)                             |
| [SAP Fiori](https://experience.sap.com/fiori-design/)                              |     👍     |              |               |                                                                                                        |
| [SAP Fundamental](https://github.com/SAP/fundamental)                              |     👍     |              |               |                            [:octocat:](https://github.com/SAP/fundamental)                             |
| [SAP OpenUI](https://github.com/SAP/openui5)                                       |     👍     |              |               |                              [:octocat:](https://github.com/SAP/openui5)                               |
| [Scania Digital Design System](https://digitaldesign.scania.com/home)              |     👍     |              |      👍       |                   [:octocat:](https://github.com/scania-digital-design-system/sdds)                    |
| [Seeds](https://sproutsocial.com/seeds)                                            |     👍     |      👍      |      👍       |                                                                                                        |
| [SEEK Style Guide](https://seek-oss.github.io/seek-style-guide/)                   |     👍     |              |               |                       [:octocat:](https://github.com/seek-oss/seek-style-guide)                        |
| [Semi Design](https://semi.design/en-US)                                           |     👍     |              |      👍       |                          [:octocat:](https://github.com/DouyinFE/semi-design)                          |
| [Semrush Intergalactic Design System](https://i.semrush.com/)                      |     👍     |              |      👍       |                         [:octocat:](https://github.com/semrush/intergalactic)                          |
| [Shoelace](https://shoelace.style)                                                 |     👍     |      👍      |               |                        [:octocat:](https://github.com/shoelace-style/shoelace)                         |
| [Shopify Polaris](https://polaris.shopify.com)                                     |     👍     |      👍      |      👍       |                            [:octocat:](https://github.com/Shopify/polaris)                             |
| [Shadcn/ui](https://ui.shadcn.com/)                                                |     👍     |              |               |                               [:octocat:](https://github.com/shadcn-ui)                                |
| [Siemens iX](https://ix.siemens.io/)                                               |     👍     |      👍      |      👍       |                               [:octocat:](https://github.com/siemens/ix)                               |
| [Singapore Government Design System](https://www.designsystem.tech.gov.sg/)        |     👍     |      👍      |      👍       |                             [:octocat:](https://github.com/govtechsg/sgds)                             |
| [Stacks – Stack Overflow](https://stackoverflow.design/)                           |     👍     |      👍      |               |                          [:octocat:](https://github.com/StackExchange/Stacks)                          |
| [Starbucks Style Guide](https://creative.starbucks.com)                            |     👍     |      👍      |               |                                                                                                        |
| [Strapi Design System](https://design-system.strapi.io/)                           |     👍     |              |               |                          [:octocat:](https://github.com/strapi/design-system)                          |
| [Teambition Clarity Design](https://design.teambition.com/)                        |     👍     |              |               |                                                                                                        |
| [Telefónica Mística](https://brandfactory.telefonica.com/mistica)                  |     👍     |              |      👍       |                           [:octocat:](https://github.com/Telefonica/mistica)                           |
| [Thumbprint](https://thumbprint.design/)                                           |     👍     |              |               |                          [:octocat:](https://github.com/thumbtack/thumbprint)                          |
| [Tizen CircularUI](https://developer.samsung.com/one-ui-watch-tizen)               |     👍     |              |      👍       |                        [:octocat:](https://github.com/Samsung/Tizen.CircularUI)                        |
| [Twilio Paste](https://paste.twilio.design/)                                       |     👍     |      👍      |      👍       |                           [:octocat:](https://github.com/twilio-labs/paste)                            |
| [Uber's Base Web](https://baseweb.design/)                                         |     👍     |              |               |                            [:octocat:](https://github.com/uber-web/baseui)                             |
| [Ubuntu Vanilla framework](https://vanillaframework.io/)                           |     👍     |      👍      |      👍       |               [:octocat:](https://github.com/canonical-web-and-design/vanilla-framework)               |
| [Uiverse](https://uiverse.io)                                                      |     👍     |      👍      |      👍       |                           [:octocat:](https://github.com/uiverse-io/galaxy)                            |
| [Untitled UI](https://www.untitledui.com/react/)                                   |     👍     |              |      👍       |                          [:octocat:](https://github.com/untitleduico/react/)                           |
| [uSwitch style guide](https://ustyle.guide/)                                       |     👍     |      👍      |               |                             [:octocat:](https://github.com/uswitch/ustyle)                             |
| [U.S. Web Design Standards](https://designsystem.digital.gov/)                     |     👍     |      👍      |      👍       |                              [:octocat:](https://github.com/uswds/uswds)                               |
| [U.S. CMS.gov Design System](https://design.cms.gov/)                              |     👍     |              |               |                                                                                                        |
| [Vibe](https://style.monday.com/)                                                  |     👍     |              |      👍       |                             [:octocat:](https://github.com/mondaycom/vibe)                             |
| [Vimeo Design System](https://vimeo.github.io/iris/)                               |     👍     |              |               |                               [:octocat:](https://github.com/vimeo/iris)                               |
| [VMware Clarity Design System](https://clarity.design/)                            |     👍     |      👍      |      👍       |                             [:octocat:](https://github.com/vmware/clarity)                             |
| [VTEX Styleguide](https://styleguide.vtex.com/)                                    |     👍     |              |      👍       |                            [:octocat:](https://github.com/vtex/styleguide)                             |
| [Vue Design System](https://vueds.com/)                                            |     👍     |              |               |                       [:octocat:](https://github.com/viljamis/vue-design-system)                       |
| [Ray by WeWork](https://ray.wework.com)                                            |     👍     |              |               |                               [:octocat:](https://github.com/wework/ray)                               |
| [Welcome UI](http://www.welcome-ui.com/)                                           |     👍     |              |               |                            [:octocat:](https://github.com/WTTJ/welcome-ui)                             |
| [West Midlands Network Design System](https://designsystem.wmnetwork.co.uk/)       |     👍     |      👍      |               |                     [:octocat:](https://github.com/wmcadigital/wmn-design-system)                      |
| [Wix Style React](https://www.wix-style-react.com/storybook/)                      |     👍     |              |               |                                                                                                        |
| [Vercel](https://vercel.com/geist)                                                 |     👍     |              |               |                                                                                                        |
| [Workday Canvas](https://design.workday.com/)                                      |     👍     |      👍      |               |                           [:octocat:](https://github.com/Workday/canvas-kit)                           |
| [Yelp Styleguide](https://www.yelp.com/styleguide)                                 |     👍     |      👍      |               |                                                                                                        |
| [Zendesk Garden](https://garden.zendesk.com/)                                      |     👍     |              |               |                             [:octocat:](https://github.com/zendeskgarden)                              |

\* _Open-source projects may have varying licenses — always check before using._

> 'Design systems', 'UI libraries', and 'pattern libraries' are technically different things but often used interchangeably; this catalog includes all three.
