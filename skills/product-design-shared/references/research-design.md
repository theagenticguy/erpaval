# Research design — hypothesis, null, MECE questions, findings

Shared reference for structured research design. Applies to customer research, user studies, competitive analysis, technical investigations, incident post-mortems, and agent evals — anywhere you need to go from "vague question" to "Pyramid-ready evidence" without motivated reasoning.

This file is the upstream for `pyramid-principle.md`. It produces evidence in the shape the Pyramid base expects by construction.

## Why research needs design

Research without a plan becomes evidence-gathering for a preferred conclusion. A well-designed plan forces you to pre-commit to:

- What claim you are testing (hypothesis)
- What would change your mind (null hypothesis)
- What you need to learn to test it (MECE sub-questions)
- How you will learn it (methods per question)
- What "enough evidence" looks like (success criteria)

Without these, any amount of data can feel like confirmation. With them, you either have enough evidence or you know what is missing.

## Who uses this reference

- `skills/customer-research/` — primary consumer; templates execute this method
- `skills/working-backwards/` — the Listen stage
- `skills/product-discovery/` — research-scout role framing
- `agents/researcher` — upstream role framing for deep research
- Any skill that needs to produce Pyramid-base-shaped output

## The method

### Step 1 — Frame a single hypothesis

One testable claim. One sentence. Mentions the actor, the condition, and the predicted outcome.

**Template:** *"[Actor] [do/experience] [outcome] because [condition]."*

**Examples**

- Good: "SMB sellers abandon the product-listing flow because the image-requirements step is ambiguous."
- Good: "Opus-4.7 handles multi-file refactors more accurately than Sonnet-4.6 because its longer reasoning chains catch cross-file constraint violations."
- Bad: "Sellers struggle with listings." — no condition, no predicted outcome, untestable.
- Bad: "The UI should be better." — no actor, no claim, no evidence could refute it.

If you cannot write the hypothesis in one sentence, you have more than one hypothesis. Split them.

### Step 2 — Frame the null hypothesis

The outcome that would disprove the hypothesis. Pre-commit to it *before* gathering evidence. This is the single most important step.

**Template:** *"If [predicted evidence] does not appear, the hypothesis is false and [alternate cause] is more likely."*

**Examples**

- Hypothesis: SMB sellers abandon listings because image requirements are ambiguous.
- Null: If listing-completion rates do not improve when image requirements are clarified, the abandonment cause lies elsewhere (likely: pricing input, title-length constraints, or category mapping).

- Hypothesis: Opus-4.7 is better at multi-file refactors.
- Null: If Opus-4.7 does not exceed Sonnet-4.6 by more than 5pp on multi-file refactor accuracy in matched tasks, the advantage is not material for this use case.

**Why the null matters.** Without it, you will find evidence for the hypothesis because you were looking for it. With it, you have a falsifiable commitment. When the null fires, you have learned something — not failed.

### Step 3 — Decompose into MECE sub-questions

Break the hypothesis into 3–5 sub-questions that:

- **Cover the hypothesis collectively** — answering all of them tells you whether the hypothesis holds.
- **Do not overlap** — no question's answer is a subset of another question's answer.
- **Are answerable by a method** — each question maps to a research technique.

**Example decomposition** for *"SMB sellers abandon listings because image requirements are ambiguous"*:

1. **Where in the flow do sellers abandon?** (behavioral — funnel analytics)
2. **What do sellers say about the image step?** (attitudinal — interviews, support tickets)
3. **How many sellers complete listings when image requirements are restated more clearly?** (experimental — A/B test with a clarified variant)
4. **Do abandonment rates differ by seller size, category, or first-time vs returning?** (segmentation — cohort analysis)

These four are MECE: you can answer (1) without answering (2); (3) tests the causal claim directly; (4) rules out confounds.

### Step 4 — Select methods per sub-question

Different question types want different methods. Pick by question type, not by personal preference.

| Question type          | What it asks                                               | Best methods                                                              |
| ---------------------- | ---------------------------------------------------------- | ------------------------------------------------------------------------- |
| **Behavioral**         | What are people doing?                                     | Funnel analytics, session replay, A/B test, event logs                    |
| **Attitudinal**        | Why are they doing it? What do they feel?                  | Interviews, open-ended surveys, support ticket review                     |
| **Pain-point texture** | What is the emotional weight? What does "fixed" feel like? | Ethnography, diary studies, Gemba walks, empathy maps                     |
| **Segmentation**       | Who is affected? How does behavior differ across groups?   | Cohort analysis, persona-based research                                   |
| **Scale**              | How common is this?                                        | Quantitative survey, site-wide analytics, industry benchmarks             |
| **Causal**             | Does changing X move Y?                                    | Controlled experiment (A/B), quasi-experiment, before/after with controls |

Mix at least two methods across the plan. A plan that relies only on interviews can produce beautiful stories that do not scale; a plan that relies only on analytics can miss the human texture that explains the numbers.

### Step 5 — Define success criteria for the plan

Before gathering, pre-commit to what "enough evidence" looks like. Two dimensions:

- **Volume** — how many interviews, sessions, or events constitute sufficient data?
- **Saturation** — at what point do new interviews stop yielding new themes?

Also pre-commit to what would make you extend the plan (e.g., "if sub-question 3 is inconclusive after N participants, we run the A/B for another two weeks").

### Step 6 — Gather and record

Execute the plan. Record evidence verbatim where possible: direct customer quotes, raw metric values, specific observations. Do not synthesize during gathering — synthesis comes next.

For each item captured, record:

- **What** — the observation, quote, or metric
- **Source** — where it came from (participant ID, ticket, experiment, etc.)
- **Which sub-question** — the one this evidence bears on

### Step 7 — Synthesize into findings (Pyramid-base-shaped)

For each sub-question, synthesize the evidence into a **finding** with a **so-what**.

**Finding template:**

```text
Sub-question: [the MECE question from Step 3]
Finding: [the evidence-backed answer, one sentence]
Evidence: [specific sources with quotes or numbers]
So what: [what this implies for the hypothesis]
Confidence: [high / medium / low, with reason]
```

**Example:**

```text
Sub-question: What do sellers say about the image step?
Finding: 7 of 12 SMB sellers interviewed reported confusion about image background requirements, and 4 of those 7 abandoned during the image upload.
Evidence:
  - Interview P04: "I didn't know if 'plain white' meant literally #FFFFFF or any light background."
  - Interview P11: "I gave up and came back two days later with help from a friend."
  - Support ticket analysis: 23% of listing-abandonment-related tickets mention images.
So what: Ambiguity in image requirements is a live, verbalized pain; supports the hypothesis.
Confidence: Medium — sample size is small; should be triangulated with analytics (sub-question 1) and the A/B test (sub-question 3).
```

Each finding is a row in the Pyramid base. Each "so-what" is the seed of an argument in the Pyramid middle.

### Step 8 — Evaluate the hypothesis

Collect findings across all sub-questions. Three possible outcomes:

1. **Hypothesis supported** — evidence across sub-questions is consistent with the predicted outcome; the null did not fire. Proceed to Pyramid composition.
2. **Hypothesis refuted** — the null fired. Document what was ruled out (this is useful research, not failed research) and reframe around the alternate cause.
3. **Inconclusive** — evidence is mixed or incomplete. Either extend the plan per the success criteria or mark the hypothesis as not yet testable and document why.

Do not massage ambiguous evidence into support. The null firing is often the most valuable outcome because it eliminates a bad bet.

## Pyramid handoff

The output of this method slots directly into `pyramid-principle.md` Phase 1:

| Research design output                          | Pyramid Phase 1 input                     |
| ----------------------------------------------- | ----------------------------------------- |
| Finding + evidence + so-what (per sub-question) | Evidence-inventory item                   |
| Sub-questions that share a so-what              | MECE evidence cluster                     |
| Overall hypothesis outcome                      | Seed for the Pyramid's top-level argument |

The Pyramid's Phase 2 (argument construction) now becomes mechanical: the clusters *are* the arguments. The antagonist test (Pyramid Phase 5) inherits the null hypothesis — a skeptic asking "what would disprove this?" has their answer pre-written.

## Anti-patterns

| Anti-pattern                      | Why it hurts                                                         | Fix                                                                             |
| --------------------------------- | -------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| **Hypothesis with no null**       | Research becomes confirmation-gathering                              | Write the null first; require it before Step 3                                  |
| **Non-MECE sub-questions**        | Evidence clusters leak into each other; arguments muddle             | Re-decompose; test with "can I answer Q1 without answering Q2?"                 |
| **Method mismatch**               | Using interviews to prove causation, analytics to explain feelings   | Pick methods by question type, not by what's easiest                            |
| **Synthesizing during gathering** | Confirmation bias as you go                                          | Hard-separate Steps 6 and 7 in time                                             |
| **Skipping so-what**              | Raw data without interpretation; Pyramid base cannot cluster         | Every finding gets a one-sentence so-what before it counts as recorded          |
| **Moving goalposts**              | When the null is about to fire, redefining the hypothesis mid-stream | Make the null commitments visible in the plan doc; freeze them before gathering |

## Template

A fill-in-the-blank scaffold ships at `skills/customer-research/templates/research-plan.md`. It instantiates this method for a specific research effort.

## Upstream and downstream

- **Upstream** — a vague question, a customer pain, a strategic hypothesis, an agent-eval design.
- **Downstream** — `pyramid-principle.md` composes the findings into a document, deck, or storyboard. In the WB pipeline, this sits at Stage 1 (Listen) and Stage 2 (Define).
