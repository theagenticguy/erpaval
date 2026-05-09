# Problem statement

A specific, data-backed articulation of a customer problem. The output of the Working Backwards Define stage. The input to Invent (and to any PR/FAQ, long-form narrative, or PRD downstream).

## The formal template

> Today, **[customer segment]** have to **[specific problem]** when **[situation]**. Customers need a way to **[insert need — not a solution]**.

## Fill-in

**Project / product name**: [FILL]
**Date**: [FILL]
**Author**: [FILL]
**Source research**: [link to `research-plan.md` or interview notes]

### Customer segment (who)

Specific. Behaviors + context, not demographics. Matches the primary segment from the research plan.

> [FILL]

**Evidence grounding this segment**:

- [source 1]
- [source 2]

### Specific problem (what)

The *pain*, not the *feature*. A need, not a solution.

> [FILL]

**Do NOT name the solution here.** "Customers need an AI-powered dashboard" is a solution. "Customers need a way to know at a glance whether their listings are healthy" is a need.

### Situation (when)

When does this problem happen? What is the customer doing? What triggered the friction?

> [FILL]

### Need (what the customer needs, not what you'll build)

> [FILL — start with "a way to" or "the ability to"]

---

## Assembled statement

After filling the pieces above, assemble into the canonical form:

> Today, **[customer segment]** have to **[specific problem]** when **[situation]**. Customers need a way to **[need]**.

### Example — Food Desert grocery access

> Today, **17.2MM low-income US households living more than 0.5 miles from a supermarket** have to **make large monthly grocery trips with limited fresh-food selection** when **benefits arrive at the start of the month**. Customers need a way to **access affordable fresh-food selection without traveling far from home**.

## Evidence backing the statement

List the data points that ground each element. Source from `research-plan.md` findings.

| Element                        | Evidence                                         | Source                       |
| ------------------------------ | ------------------------------------------------ | ---------------------------- |
| Customer segment is real       | [e.g., 17.2MM households per USDA 2019]          | [USDA Food Desert study]     |
| Problem is widespread          | [e.g., 42% funnel drop at the image step]        | [feedback dashboard, Q1 data] |
| Problem is felt                | [e.g., 7 of 12 interviewed volunteered the pain] | [Interviews P01-P12]         |
| Current workarounds are costly | [e.g., average detour = 12 miles round trip]     | [Census geo + seller survey] |

Cite specific sources. Mark `[NEEDS DATA]` where evidence is missing — do not fabricate.

## Antagonist test

Read the statement as the most skeptical reviewer. Answer honestly:

- Is the segment specific enough that a reader could identify one?
- Is the problem separate from the solution?
- Is the scale backed by data or is it aspirational?
- If a reader said "I don't think this is a real problem", what specific evidence would you point at?

If any answer is weak, return to the research plan before proceeding.

## Common failure modes

| Failure                                                             | Fix                                                                                      |
| ------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| **Segment too broad** ("all our customers")                         | Narrow to one primary segment; secondary beneficiaries go in the Customer FAQ downstream |
| **Solution in the problem** ("customers need a dashboard")          | Rewrite around the pain or job-to-be-done                                                |
| **No data** ("customers are frustrated")                            | Cite specific data. If absent, mark `[NEEDS DATA]` and plan the research                 |
| **Features described** ("the listing flow is confusing")            | Reframe around customer impact ("sellers abandon listings")                              |
| **Mixed time horizon** ("today and in the future, customers will…") | Stick to present-tense. Future is the PR's job, not the problem statement's              |

## What happens next

Once the problem statement is tight:

- Feed to `skills/working-backwards/` Stage 3 (Invent) to generate solution directions.
- Feed to `skills/product-discovery/` as the PRD's problem framing.
- Use as the seed for the 5CQ's Q2 in `skills/working-backwards/templates/5cq-worksheet.md`.
