# Pyramid Principle — Minto composition method

Shared reference for the Pyramid Principle (Barbara Minto, McKinsey). Used across any workflow that composes arguments, synthesizes research, or presents decisions — narratives, PR/FAQs, slide decks, PRDs, reviews, critiques.

The load-bearing idea: **research bottom-up, present top-down.** The reader sees the Purpose first. The writer derives it last.

## Why this reference is shared

Pyramid is a reasoning discipline, not a document type. The same pyramid feeds many artifacts: long-form narratives, PR/FAQs, decks, storyboards, PRDs. Keeping Pyramid as a single citable reference lets every skill compose against it without duplicating the method.

Who consumes this file:

- `skills/working-backwards/` — the PR is the top-down answer; the FAQ is the counter-argument test
- `skills/customer-research/` — findings synthesis produces the Pyramid base
- `skills/product-discovery/` — PRD executive summary derivation
- `skills/product-strategy/` — Minto Pyramid as the strategy memo's structure
- Any orchestrator that needs to synthesize mixed evidence into a defensible recommendation

## The core shape

```text
           Purpose (the ask, 1-2 sentences)
         /          |          \
   Argument 1   Argument 2   Argument 3
  /    |    \   /    |    \  /    |    \
Evidence clusters organized MECE (base)
```

- **Base**: evidence, data, customer signals, metrics. Every item has a source and a one-sentence "so what".
- **Middle**: 3–5 arguments derived from the base. Each argument passes the skeptic test.
- **Top**: one Purpose, one one-sentence summary, one explicit recommendation.

Arguments group evidence; the Purpose summarizes arguments. Every layer reduces to answer a single question the layer above asks.

## Research bottom-up

Build the base first. Do not start writing. Do not start with the headline.

1. Gather data, quotes, metrics, customer signals — everything that might be relevant.
2. For each item write a one-sentence "so what" (what does this prove or suggest?).
3. Group into **MECE** clusters — mutually exclusive, collectively exhaustive. Each cluster points toward one conclusion.
4. Identify gaps. Claims without evidence are deleted or marked `[NEEDS DATA]`. Do not fabricate evidence.

The evidence inventory is the Pyramid base. It is the only artifact produced during research; nothing else exists yet.

See `research-design.md` for the upstream discipline that produces Pyramid-base-shaped output by construction (hypothesis + null hypothesis → MECE questions → findings).

## MECE — the grouping test

**Mutually Exclusive**: no item belongs in two clusters. If it does, the cluster boundaries are wrong.

**Collectively Exhaustive**: everything relevant is in some cluster. If important evidence has no home, a cluster is missing.

MECE failure modes:

| Failure                    | Symptom                                                                  | Fix                                                                                      |
| -------------------------- | ------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------- |
| **Overlapping categories** | "Customer complaints" and "User feedback" — same content in two clusters | Merge, or carve a crisper distinction (e.g., direct support tickets vs. survey comments) |
| **Wrong dimension**        | Grouping by product team when the pattern is by user segment             | Re-cluster on the dimension that predicts the conclusion                                 |
| **Missing category**       | Key evidence gets labeled "other"                                        | Add the category; "other" should never exceed ~10%                                       |
| **Uneven levels**          | One cluster is a root concept; others are sub-concepts                   | Flatten or push down to a consistent depth                                               |

A MECE-clean base reduces composition from improvisation to mechanical translation.

## Present top-down

Draft in presentation order, but **derive in reverse**. The reader needs the Purpose first; the writer needs it last.

1. Restate the Purpose (derived from arguments, not guessed upfront).
2. Lead with the strongest argument.
3. Each argument opens with its claim, followed by evidence.
4. Counter-arguments get pre-empted (inline or as FAQs).

Writing the Purpose first forces you to guess. Writing it last forces you to have evidence.

## SCQA — the Pyramid applied to a narrative

**SCQA** = Situation · Complication · Question · Answer. A sentence-level translation of the Pyramid into a story. The reader's mind is already asking *"so what?"* — SCQA answers it immediately.

| Element          | In a long-form narrative      | On a slide                  | In a PR/FAQ                          |
| ---------------- | ----------------------------- | --------------------------- | ------------------------------------ |
| **Situation**    | Background paragraph          | Opening slide's framing     | "Today, [customers]…"                |
| **Complication** | Problem/Opportunity section   | The tension slide ("…but…") | The pain being solved                |
| **Question**     | Implicit — what should we do? | Implicit — what now?        | Implicit — how should this be fixed? |
| **Answer**       | Recommendation section        | Conclusion slide            | The PR body itself                   |

SCQA is a lens; it works inside any artifact. A deck can use SCQA for the overall arc AND embedded mini-SCQA per section. A PR already is an SCQA structure by construction.

## The antagonist test

Before finalizing, read every sentence as the most skeptical reader in the room:

- Do I believe this? What evidence is missing?
- Is there room for debate? If so, have I addressed it inline or in FAQs?
- Is this specific enough? "A significant proportion of sellers may be affected" fails. "This will affect 23% of sellers" passes.
- Am I hiding uncertainty behind hedge words? State uncertainty explicitly rather than hedging.

Write down the 10 hardest questions a reader could ask. Answer them. Put the answers in FAQs or bake them into the body. Unanswered hard questions at review time kill docs regardless of quality elsewhere.

## Audience calibration

Pyramid rigor is constant; pyramid *depth* varies by reader. Before starting, answer these:

| Question                                                  | Impact                                         |
| --------------------------------------------------------- | ---------------------------------------------- |
| Who is the reader? (peers, skip-level, VP, SVP)           | Detail and context depth                       |
| What does the reader already know?                        | High familiarity = less background             |
| How familiar is the reader with the customer?             | Unfamiliar = more customer framing             |
| Where will the reader disagree?                           | Pre-empt in the recommendation or FAQs         |
| What is the reader's incentive to act?                    | Frame the ask in terms of what matters to them |
| What are you asking for? (decision, resources, alignment) | Make the ask explicit in the Purpose           |

Over-writing for a VP reader who already knows the context wastes their time. Under-writing for a skip-level who does not know the problem leaves the ask ungrounded.

## The composition process (five phases)

Do not write sequentially from Purpose to Appendices. Build, then draft.

### Phase 1 — Evidence assembly (base)

Gather all relevant evidence. One-sentence "so what" per item. Cluster MECE. Mark gaps with `[NEEDS DATA]`. Output: a structured evidence inventory.

### Phase 2 — Argument construction (middle)

Derive 3–5 arguments from the evidence clusters. Each:

- One-sentence claim
- Backed by specific Phase-1 evidence
- Passes the antagonist test
- No weasel words

Order by strength; lead with the strongest. Identify counter-arguments; pre-write responses — these become FAQs.

### Phase 3 — Answer derivation (top)

From the arguments, derive:

1. **Recommendation** — a specific, actionable statement. Not "we should consider improving X" but "we recommend doing X because Y, starting Z."
2. **Purpose statement** — what decision is requested, and why it matters. Derived last; read first.
3. **One-sentence summary** — if the reader remembers one thing, what is it?

### Phase 4 — Draft in presentation order

Now write the document in reading order. Each section draws from the phases above.

### Phase 5 — Self-edit

Apply the writing quality rubric. The antagonist test is the last pass.

## AI-specific anti-patterns

These are failure modes common when an LLM composes a Pyramid document sequentially:

| Anti-pattern              | Fix                                                                                          |
| ------------------------- | -------------------------------------------------------------------------------------------- |
| **Vague purpose**         | Derive Purpose last, after arguments                                                         |
| **Background dump**       | Include only context needed to understand the problem; appendix the rest                     |
| **Symmetric treatment**   | Not all points deserve equal space; lead with the strongest                                  |
| **Hedge cascade**         | "This could potentially help to somewhat improve…" — pick a position                         |
| **Missing the ask**       | Every narrative requests something; if you cannot state the ask, the document has no purpose |
| **Filler transitions**    | "Now let's turn to…" — delete; headings do the transition                                    |
| **Decorative adjectives** | "Incredibly important strategic initiative" — state why with data                            |
| **Restating the heading** | First sentence after a heading should not repeat the heading                                 |

## Long-form narrative structure

For long-form narrative documents (executive memos, multi-page narratives, ADRs), a typical section layout:

| Section                   | Purpose                                      | Required  |
| ------------------------- | -------------------------------------------- | --------- |
| **Title + Date**          | Document name and review date                | Yes       |
| **Purpose**               | What decision is needed; state it plainly    | Yes       |
| **Tenets**                | Team principles relevant to this decision    | Optional  |
| **Background**            | Context the reader needs                     | Yes       |
| **Problem / Opportunity** | The customer problem. Data-backed            | Yes       |
| **Recommendation**        | Proposed solution with supporting arguments  | Yes       |
| **Next steps**            | Who does what, when                          | Yes       |
| **Summary**               | Recap for docs over 4 pages; restate the ask | Optional  |
| **FAQs**                  | Anticipated objections, answered             | Optional  |
| **Appendices**            | Full datasets, supporting material           | As needed |

### Formatting constraints (typical)

- Cap page length up front. If longer, cut.
- Single-spaced, left-aligned, print-friendly.
- Number every page; consistent header.
- Headings bold; sub-headings styled consistently.
- Spell out acronyms on first use.

## Mechanisms in recommendations

A recommendation without a mechanism is a wish. A mechanism is a repeatable system with four components:

- **Flywheel** — the virtuous cycle being accelerated
- **Metric** — the measurable output
- **Process** — the repeatable action
- **Audit** — the inspection cadence

When writing the Recommendation section, each line of effort should specify what process drives what metric, who owns it, and when it is audited.

## Upstream and downstream

- **Upstream** — `research-design.md` produces Pyramid-base-shaped evidence by construction.
- **Downstream** — the Pyramid feeds many artifacts:
  - PR/FAQs (`skills/working-backwards/`)
  - PRDs with executive summaries (`skills/product-discovery/`)
  - Strategy memos (`skills/product-strategy/`)
  - Long-form narratives — hand the Minto-shaped pyramid to whatever narrative-writing workflow your team uses
  - Slide decks via SCQA
