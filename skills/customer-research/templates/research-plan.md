# Research Plan

Fill-in-the-blank scaffold for structured research design. Based on `${CLAUDE_PLUGIN_ROOT}/skills/product-design-shared/references/research-design.md`.

**Project name**: [FILL]
**Date**: [FILL]
**Author**: [FILL]
**Primary customer segment**: [FILL — specific behaviors + context, not demographics]

---

## 1. Hypothesis

One testable claim in one sentence. Mentions actor + condition + predicted outcome.

> [FILL. Template: "[Actor] [do/experience] [outcome] because [condition]."]

**Example**: "SMB sellers abandon the product-listing flow because the image-requirements step is ambiguous."

## 2. Null hypothesis

The outcome that would disprove the hypothesis. **Pre-commit before gathering.** This is the single most important line in the plan.

> [FILL. Template: "If [predicted evidence] does not appear, the hypothesis is false and [alternate cause] is more likely."]

**Example**: "If listing-completion rates do not improve when image requirements are clarified, the abandonment cause lies elsewhere (likely: pricing input, title-length constraints, or category mapping)."

## 3. MECE sub-questions

3–5 questions that:

- **Cover the hypothesis collectively** (answering all of them tells you whether it holds).
- **Do not overlap** (test: can I answer Q1 without answering Q2?).
- **Are answerable by a method** (each maps to a research technique).

| # | Sub-question | Test it's MECE                |
| - | ------------ | ----------------------------- |
| 1 | [FILL]       | Does not overlap with 2, 3, 4 |
| 2 | [FILL]       | Does not overlap with 1, 3, 4 |
| 3 | [FILL]       | Does not overlap with 1, 2, 4 |
| 4 | [FILL]       | (optional)                    |
| 5 | [FILL]       | (optional)                    |

## 4. Methods per question

Pick by question type, not by personal preference. See `${CLAUDE_PLUGIN_ROOT}/skills/customer-research/references/research-methods.md` for the taxonomy.

| # | Sub-question | Type                                                                    | Method                   | Source / tool                         |
| - | ------------ | ----------------------------------------------------------------------- | ------------------------ | ------------------------------------- |
| 1 | [from above] | [Behavioral / Attitudinal / Pain-point / Segmentation / Scale / Causal] | [e.g., funnel analytics] | [e.g., feedback aggregation, internal dashboard] |
| 2 | ...          | ...                                                                     | ...                      | ...                                   |
| 3 | ...          | ...                                                                     | ...                      | ...                                   |

**Methods mix check**: do you have at least two different methods across the plan? (Single-method plans are brittle.)

## 5. Success criteria for the plan

Pre-commit to what "enough evidence" looks like.

**Volume**: [FILL — e.g., "12 interviews across 3 seller cohorts; 500 tickets coded; funnel data Jan–Mar"]

**Saturation**: [FILL — e.g., "Stop interviews when no new themes emerge in 2 consecutive sessions"]

**Extension trigger**: [FILL — e.g., "If sub-question 3 is inconclusive after N participants, run an A/B test for 2 additional weeks"]

## 6. Evidence gathered

Filled during execution. Keep verbatim quotes and exact numbers. Do not synthesize here.

### For sub-question 1

| What                       | Source                                     | Date         |
| -------------------------- | ------------------------------------------ | ------------ |
| [verbatim quote or metric] | [participant ID, ticket ID, dashboard URL] | [YYYY-MM-DD] |
| ...                        | ...                                        | ...          |

### For sub-question 2

... (repeat per sub-question)

## 7. Findings

**One finding per sub-question**. Each in Pyramid-base shape.

### Finding 1 — [sub-question]

- **Finding**: [one sentence, evidence-backed]
- **Evidence**:
  - [source 1: quote or number]
  - [source 2: quote or number]
- **So what**: [what this implies for the hypothesis]
- **Confidence**: [High / Medium / Low — with reason]

### Finding 2 — [sub-question]

... (repeat)

## 8. Hypothesis outcome

Pick one:

- **[ ] Supported** — evidence across sub-questions is consistent; null did not fire.
- **[ ] Refuted** — null fired. [FILL: what was ruled out + alternate hypothesis]
- **[ ] Inconclusive** — [FILL: why, and what extension is needed]

## 9. Pyramid handoff

Map findings to downstream composition.

**Evidence clusters that share a "so what"** (feed Pyramid-middle arguments):

| Cluster theme | Supporting findings (by #) | Seed argument                                                                                 |
| ------------- | -------------------------- | --------------------------------------------------------------------------------------------- |
| [FILL]        | [1, 3]                     | [e.g., "The image-requirements step is the single biggest driver of SMB seller abandonment."] |
| [FILL]        | [2, 4]                     | [e.g., "Existing guidance is read but not understood by first-time sellers."]                 |

**Next artifact to produce**:

- [ ] Problem statement (`templates/problem-statement.md`)
- [ ] Customer journey map (`templates/customer-journey-map.md`)
- [ ] 5CQ (`${CLAUDE_PLUGIN_ROOT}/skills/working-backwards/templates/5cq-worksheet.md`)
- [ ] PR/FAQ (via `skills/working-backwards/` workflow)
- [ ] PRD (via `skills/product-discovery/`)
- [ ] Hand off to your team's narrative-writing workflow if a long-form doc is the deliverable

## Confidence caveats

- **What was not tested**: [FILL]
- **What could change the result**: [FILL]
- **Saturation status**: [FILL]
- **Recommended next research**: [FILL if inconclusive]
