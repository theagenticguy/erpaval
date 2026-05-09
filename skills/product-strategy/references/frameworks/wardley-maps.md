# Wardley Maps

## Canonical structure

A Wardley Map has two axes plus dependencies, and everything else layers on top [5, 6, 7].

- **Vertical axis — value chain (visibility)**: anchored at the top by **user need**. Components hang below by dependency, with infrastructure at the bottom. Lines connect components to show dependency. Higher = more visible to the user.
- **Horizontal axis — evolution**: four stages, left to right.
  1. **Genesis** — novel, uncertain, high-risk, hand-built.
  2. **Custom-built** — bespoke, differentiated, teams still reinventing.
  3. **Product (+rental)** — standardized, multiple providers, commercial offerings.
  4. **Commodity / utility** — undifferentiated, interchangeable, pay-as-you-go.

The build-vs-buy decision is *literally* the x-axis position. Build in Genesis/Custom where differentiation lives; buy/rent in Product; consume in Commodity. Reinventing commodity wastes motion; buying Genesis locks you into a vendor's experiment.

**Layered concepts**:

- **Climatic patterns** — external forces that shape evolution. Examples: supply/demand drives commoditization; Red Queen (components must evolve or die); everything evolves due to competition. These are not your choices — they're the weather [5, 42].
- **Doctrine** — 44 universal principles grouped into phases. Phase I "Stop self-harm" (know your users, challenge assumptions). Phase II "Development" (focus on users, avoid duplication). Phase III "Learning" (embrace failure, share knowledge). Doctrine is context-independent — always-true [7, 43].
- **Gameplay** — competitive moves available *given this specific map*. Examples: pre-empt a competitor by moving a component leftward; open-source to accelerate commoditization of a dependency; industrialize to drive out a high-margin incumbent.

Wardley's book is CC-BY-SA 4.0; the vocabulary is freely reusable [43, 44].

## When to use

Build-vs-buy decisions, platform strategy, "what should we open-source," competitive positioning, third-party dependency evaluation. Pair with Rumelt — the map surfaces facts the diagnosis needs. Especially sharp when a team is about to reinvent something that's already commoditized, or assumes a Genesis component will stay differentiated.

## When to skip

Skip for pure UX/discovery work (use Double Diamond / JTBD in `product-discovery`). Skip when the team already agrees on build-vs-buy and is arguing about implementation. Skip when the problem is organizational (reorg, hiring, culture) — Wardley doesn't speak about people. Skip when the decision has no physical-or-digital components to arrange on an axis — pure financial choices don't map.

## Template / worked example

Text-form Wardley map. Coordinates are (evolution, visibility) where evolution ∈ {Genesis, Custom, Product, Commodity} and visibility ∈ {0.0 user-need-top to 1.0 infrastructure-bottom}.

```markdown
## User need (top of map)

[Who the user is and what outcome they need. Not a feature. Not a system. The progress they're trying to make.]

## Value chain

- [Component 1] — depends on: [Component 2, Component 3]
- [Component 2] — depends on: [Component 4]
- ...

## Evolution positioning

| Component | Stage     | Evidence for stage                                          |
| --------- | --------- | ----------------------------------------------------------- |
| [Name]    | Commodity | [Multiple providers, pay-per-use pricing, undifferentiated] |
| [Name]    | Product   | [2-3 commercial offerings, feature differentiation active]  |
| [Name]    | Custom    | [Mostly in-house builds, no dominant product yet]           |
| [Name]    | Genesis   | [Novel, no stable category, research-stage]                 |

## Climatic patterns in play

- [Pattern — "commoditization of X is accelerating because Y"]
- [Pattern — "Red Queen: if we don't evolve Z, competitors will"]

## Gameplay moves considered

- [Move — "open-source our Custom component to commoditize it and shift the fight upstream"]
- [Move — "industrialize the adjacent Product-stage component to squeeze incumbent margins"]

## Build-vs-buy read

- [Component] → build (Genesis, differentiated, core)
- [Component] → buy (Product, commercial options good enough)
- [Component] → consume (Commodity, no reason to run our own)
```

**Worked example excerpt**:

> User need: "spin up a reliable internal agent without reinventing plumbing."
> Key components: prompt store (Product), eval harness (Custom → moving to Product), model serving (Commodity — Bedrock, Azure, others), guardrails (Genesis).
> Climatic pattern: eval harnesses are commoditizing fast (2024-2026). Building custom now buys short-term flexibility at long-term maintenance cost.
> Gameplay: consume model serving, buy an eval harness, invest internal headcount on guardrails where the map is still Genesis.

## Validation checks

- User need is at the top and is stated as user outcome, not system feature.
- Every component has an evolution stage and evidence for it. "It feels Custom" fails.
- Dependencies run downward — no component depends on one above it.
- Gameplay moves reference specific components and specific climatic patterns, not generic advice.
- Build-vs-buy reads correspond to evolution stages — building Commodity or buying Genesis is always flagged.
- Claims about competitor positioning are verifiable (public products, prices, announcements) — not "I heard from a friend."

## Citations

- [5] [Wikipedia, "Wardley map."](https://en.wikipedia.org/wiki/Wardley_map) — canonical glossary.
- [7] [Learn Wardley Mapping — Simon Wardley's open book (CC-BY-SA).](https://learnwardleymapping.com/book/)
- [42] [Learn Wardley Mapping — Climate.](https://learnwardleymapping.com/climate/) (2020+, CC-BY-SA).
- [43] [Tristan Lamonica, "Microdoctrine: Wardley Doctrine Piece by Piece."](https://tristanls.medium.com/microdoctrine-wardley-doctrine-piece-by-piece-f1f9e8657e5) (2023).
- [6] [Stratrix, "Wardley Mapping."](https://www.stratrix.com/learn/frameworks/wardley-mapping) (2024).
