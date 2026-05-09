# Product-Strategy Frameworks — Routing Guide

First thing a product-strategy orchestrator or role reads when deciding which framework(s) to run. This file routes to per-framework files in the same directory; it does not restate their canonical structures. When a role already knows it needs one specific framework, it should read that framework's file directly and skip this index.

## When to use this family

Reach for this family when the user needs to figure out the *why* and the *where-to-play* of a product bet before any backlog, design, or code gets written. Signals: "fluffy strategy," "we need to decide build vs buy," "our roadmap is a wishlist," "how do we explain this to the exec team," "what's the real challenge here." The output of this family is a strategy memo, a kernel, a map, or a PR-FAQ — not a PRD, not a spec, not a slide deck.

## Decision table

Pick one or more frameworks. When multiple rows match, compose — see the next section.

| User signal / ask                                           | Framework file         | One-line why                                                                                        |
| ----------------------------------------------------------- | ---------------------- | --------------------------------------------------------------------------------------------------- |
| "our strategy feels fluffy / we have a list of goals"       | `rumelt-kernel.md`     | Diagnosis forces a concrete challenge statement and exposes "bad strategy."                         |
| "what is the single most important thing to solve"          | `rumelt-kernel.md`     | The Crux refinement names the one surmountable, high-impact challenge.                              |
| "should we build or buy / is this component a commodity"    | `wardley-maps.md`      | Evolution axis (Genesis → Custom → Product → Commodity) literally answers build-vs-buy.             |
| "what's the competitive landscape / where's the play"       | `wardley-maps.md`      | Value chain + evolution + climatic patterns give positioning beyond SWOT.                           |
| "draft a PR-FAQ for a new product idea / working backwards" | `working-backwards.md` | Press release + 5 customer questions + internal FAQ forces customer-value clarity before any build. |
| "we have the strategy, now write the memo for leadership"   | `minto-pyramid.md`     | SCQA at top + MECE support below gives executives a top-down reading path.                          |
| "structure this argument / help me explain this decision"   | `minto-pyramid.md`     | Thinking structure that orders a case by importance, not chronology.                                |
| "full strategy memo from scratch for exec review"           | Compose (see below)    | Rumelt → Wardley → Minto for the write-up → Working Backwards as the customer-facing output.        |

## Compose more than one framework

The four frameworks earn their keep together. Common combinations:

- **Rumelt + Wardley** — diagnosis plus positioning. When the kernel's diagnosis depends on "what's commoditizing," run Wardley first, then feed the map into the diagnosis. When the kernel is about competitive response, Wardley is almost always an input.
- **Rumelt + Working Backwards** — kernel names the challenge and guiding policy; the PR-FAQ makes the customer-facing solution concrete. Run the kernel first when the diagnosis is contested; run PR-FAQ first when customer value is the thing in doubt.
- **Minto as the output structure of either.** A strategy memo composed from a kernel + PR-FAQ reads cleanly as SCQA — Situation (diagnosis's context), Complication (the crux), Question (implicit), Answer (guiding policy + coherent actions). Minto structures the *output* of strategy, not the strategy itself.
- **Long-form narratives are Minto serialized into prose.** If the deliverable is a long-form document, the kernel + map + PR-FAQ thinking is the input; hand the Minto-shaped artifacts to whatever narrative-writing workflow your team uses.

## When to skip the whole family

- **The ask is "write a PRD / spec / requirements."** Route to `product-discovery` — PRDs, user stories, HMW, EARS, Gherkin, JTBD job stories.
- **The ask is "write a long-form narrative."** Strategy frameworks here produce the thinking; hand the memo and PR-FAQ to your team's writing workflow for prose composition.
- **The ask is "do design thinking / brainstorm UX."** Route to `product-discovery` — discovery rounds, agent UX patterns, Double Diamond.
- **The problem is execution-shaped.** A team already knows the challenge and is building — strategy frameworks here are overhead.

## Framework file index

- `rumelt-kernel.md` — Rumelt Kernel (diagnosis / guiding policy / coherent actions) and the Crux refinement. Use when the strategy reads as aspiration, not direction.
- `wardley-maps.md` — Value chain on visibility × evolution axes, plus climatic patterns, doctrine, and gameplay. Use for build-vs-buy and competitive positioning.
- `minto-pyramid.md` — SCQA + MECE thinking structure for top-down executive communication. Use for memos, decks, PR-FAQs, any document where the reader is time-poor.
- `working-backwards.md` — PR-FAQ (press release + internal/external FAQ) as a discovery artifact. Use when customer value is in doubt and the team needs a forcing function before build.
