# Wardley Packet — {{ slug }}

**Status:** IN PROGRESS
**Authored by:** wardley-cartographer
**Framing:** `framing.md`

---

## User Need

[Anchor at the top of the map. Who the user is and what outcome they need. Not a feature. Not a system. The progress they're trying to make. Pull from `framing-design.md` (VP Design) if it ran, otherwise derive from `framing.md`.]

---

## Value Chain

Components that deliver the user need, listed with their dependencies. Dependencies run downward — if X depends on Y, Y sits lower in the chain.

- **[Component 1]** — depends on: [Component A, Component B]
- **[Component 2]** — depends on: [Component C]
- **[Component A]** — depends on: [Component D]
- **[Component B]** — depends on: [none — leaf node]
- ...

---

## Evolution Axis (text-form map)

Coordinates: (evolution stage, visibility where 0.0 = user-need-top, 1.0 = infrastructure-bottom).

| Component | Stage     | Visibility (0.0–1.0) | Evidence for stage                                                |
| --------- | --------- | -------------------- | ----------------------------------------------------------------- |
| [Name]    | Genesis   | 0.2                  | [Novel, no stable category, research-stage]                       |
| [Name]    | Custom    | 0.4                  | [Mostly in-house builds, no dominant product yet]                 |
| [Name]    | Product   | 0.6                  | [2–3 commercial offerings; feature differentiation active; link]  |
| [Name]    | Commodity | 0.9                  | [Multiple providers, pay-per-use pricing, undifferentiated; link] |

---

## Climatic Patterns Identified

External forces acting on this map. Name them concretely.

1. **[Pattern name]** — [Specific claim: "Eval harness category is commoditizing rapidly — 3 commercial providers in 2024, 8 in 2026." Link to evidence.]
2. **[Pattern name]** — [Specific claim with link.]
3. **Red Queen (if applicable)** — [Which components must evolve or die; name them.]

---

## Gameplay Moves

Specific competitive moves available *given this map*. Each move names components and patterns, not generic advice.

1. **[Move name]** — [Description: "Open-source our Custom component X to commoditize it and shift the fight to component Y where we have differentiation."] References: [component X, pattern Z].
2. **[Move name]** — [Description]. References: [...].

---

## Build-vs-Buy Read

Per-component call tied to evolution stage.

| Component | Stage     | Call    | Rationale                                                         |
| --------- | --------- | ------- | ----------------------------------------------------------------- |
| [Name]    | Genesis   | Build   | [Differentiated, core, no product-stage alternative]              |
| [Name]    | Custom    | Build   | [Still defensible; invest now before commoditization]             |
| [Name]    | Product   | Buy     | [2–3 commercial options good enough; building wastes motion]      |
| [Name]    | Commodity | Consume | [Undifferentiated; running our own burns maintenance for no edge] |

### Contradictions flagged

[Any "building a commodity" or "buying a genesis" calls? Name them. These are usually decisions to revisit.]

---

## Map-implied Diagnosis

[One paragraph the Rumelt architect can pull into their diagnosis. What does this map say about the central challenge? Example: "The map shows eval harnesses have entered the Product stage in 2025 (3 providers with mature feature sets). The central challenge is not 'build an eval harness' — it is 'choose a harness and invest our capability budget on guardrails, which remain Genesis.'"]

---

## Attribution Note

[One paragraph the synthesizer drops into the memo verbatim. Example: "The Wardley map contributed the evolution-stage evidence that reframed the build-vs-buy read — components A and B moved from Build to Consume based on commoditization evidence (3→8 providers 2024–2026)."]

---

## Citations

- [5] [Wikipedia, "Wardley map."](https://en.wikipedia.org/wiki/Wardley_map)
- [7] [Learn Wardley Mapping book (CC-BY-SA).](https://learnwardleymapping.com/book/)
- [Additional sources cited inline above — vendor docs, pricing pages, announcements.]

---

When every section has real content, flip `Status:` to `COMPLETE`.
