---
name: customer-research
description: >
  Customer research and problem framing using the research-design discipline: hypothesis,
  null hypothesis, MECE questions, methods, findings. Produces Pyramid-base-shaped output
  ready for downstream composition into PR/FAQs, long-form narratives, or PRDs. Use when
  the user asks to design user research, run customer interviews, synthesize research
  findings, frame a problem statement, build a customer journey map, plan a VoC study, or
  mentions pain-point analysis, research plan, hypothesis testing, customer insights,
  jobs-to-be-done, or voice of customer.
---

## Contents

| File                                  | Path                                                                                   | When to load                                                  |
| ------------------------------------- | -------------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| Research design method                | `${CLAUDE_PLUGIN_ROOT}/skills/product-design-shared/references/research-design.md`     | Hypothesis + null + MECE + findings                           |
| Pyramid composition                   | `${CLAUDE_PLUGIN_ROOT}/skills/product-design-shared/references/pyramid-principle.md`   | Where findings get composed into arguments                    |
| Canonical Working Backwards reference | `${CLAUDE_PLUGIN_ROOT}/skills/product-design-shared/references/working-backwards.md`   | Listen + Define stage context                                 |
| Research methods                      | `references/research-methods.md`                                                       | Interview protocols, affinity clustering, qual/quant taxonomy |
| Customer-insights role                | `${CLAUDE_PLUGIN_ROOT}/skills/working-backwards/references/roles/customer-insights.md` | Researcher agent for Listen-stage execution                   |
| Research plan template                | `templates/research-plan.md`                                                           | Hypothesis, null, MECE questions, methods, findings (fill-in) |
| Problem statement template            | `templates/problem-statement.md`                                                       | "Today [customers] have to..."                                |
| Customer journey map template         | `templates/customer-journey-map.md`                                                    | Phase / action / touchpoint / thought / feeling / opportunity |

# Customer Research

The discipline of framing a testable hypothesis, gathering evidence via MECE sub-questions, and synthesizing findings into a shape the Pyramid Principle can compose. This is the *research bottom-up* half of Minto's core instruction — the upstream of `working-backwards` and any narrative composition.

## When to Use

- You have a vague customer pain and need to know if it's real, at scale, and root-caused correctly.
- You need to produce a problem statement for a PR/FAQ or long-form narrative.
- You need to build a customer journey map for a design review.
- You have interview transcripts or survey data and need to synthesize them into decision-ready findings.
- You need to design a research plan before committing to a study (interviews, A/B test, survey).

When NOT to use:

- The customer problem is already well-framed and data-backed → go straight to `skills/working-backwards/` or `skills/product-discovery/`.
- You need writing critique for an existing prompt or document → `skills/meta-prompt-optimizer/`.

## Core Concepts

### The method: research-design

The load-bearing reference is `${CLAUDE_PLUGIN_ROOT}/skills/product-design-shared/references/research-design.md`. Five steps:

1. **Hypothesis** — one testable claim in one sentence.
2. **Null hypothesis** — the outcome that would disprove it. Pre-commit before gathering.
3. **MECE sub-questions** — 3–5 questions that collectively test the hypothesis without overlap.
4. **Methods per question** — behavioral, attitudinal, pain-point texture, segmentation, scale, causal.
5. **Findings in Pyramid-base shape** — per sub-question: Finding + Evidence + So what + Confidence.

The shape of your output is not optional. Pyramid-base-shaped findings feed `pyramid-principle.md` Phase 1 by construction.

### Pyramid connection

This skill *produces* the Pyramid base. Downstream skills *compose* it:

- `working-backwards` uses the findings for the 5CQ's Q1, Q2, Q4 and the PR's Situation + Complication.
- `product-discovery` uses the findings for its research-scout role.
- A narrative-writing workflow of your choice composes a long-form document or one-pager from the findings.

Keeping findings in a structured shape means downstream composition becomes mechanical translation, not improvisation.

### Three artifacts ship from this skill

| Artifact             | Template                            | When                                                               |
| -------------------- | ----------------------------------- | ------------------------------------------------------------------ |
| Research plan        | `templates/research-plan.md`        | Before gathering — pre-commit the hypothesis and null              |
| Problem statement    | `templates/problem-statement.md`    | After Define — the Listen output used by WB Stage 2                |
| Customer journey map | `templates/customer-journey-map.md` | When you need to visualize current-state pain points across a flow |

## Quick Reference

A typical customer-research run:

1. **Capture intent.** What is the fuzzy question? Who is the primary customer segment?
2. **Frame the hypothesis + null.** Use `templates/research-plan.md`. Pre-commit in writing.
3. **Decompose MECE.** 3–5 sub-questions. Test: "Can I answer Q1 without answering Q2?"
4. **Pick methods per question** (see `references/research-methods.md` for the taxonomy).
5. **Execute** — either yourself for small corpora (synthesize from support tickets, survey data, past research) or via the `customer-insights` role of the `researcher` agent.
6. **Synthesize** per `research-design.md` step 7 — one finding per sub-question, each with Evidence + So what + Confidence.
7. **Evaluate the hypothesis** — Supported / Refuted / Inconclusive. Report honestly.
8. **Produce the downstream artifact** — problem statement, journey map, or hand off to working-backwards.

### Composition with other skills

| Upstream                                                    | Downstream                                                |
| ----------------------------------------------------------- | --------------------------------------------------------- |
| Raw customer data (tickets, interviews, surveys, analytics) | `skills/working-backwards/` (Listen + Define + Invent)    |
| User-research transcripts                                   | `skills/product-discovery/` (PRD personas + user stories) |

## Anti-Patterns

- **Skipping the null hypothesis.** Research becomes confirmation-gathering without it. Write it down *before* you gather.
- **Non-MECE sub-questions.** Overlapping questions muddle the findings. Re-decompose before executing.
- **Using interviews to prove causation.** Pick methods by question type — causal claims need experiments, not stories.
- **Synthesizing during gathering.** Forces confirmation bias into the evidence. Separate execution and synthesis in time.
- **Reporting only supporting evidence.** The antagonist test downstream depends on you seeing the counter-evidence.
- **Moving goalposts when the null fires.** When the null fires, document it — don't redefine the hypothesis to rescue the conclusion.

## References

- `references/research-methods.md` — interview protocols, affinity clustering, qual/quant/subjective metric taxonomy, common VoC resource categories
- Shared methodology refs in `${CLAUDE_PLUGIN_ROOT}/skills/product-design-shared/references/`:
  - `research-design.md` — the method
  - `pyramid-principle.md` — the downstream composition discipline
  - `working-backwards.md` — the end-to-end product-discovery process this skill plugs into
  - `methodology-selection.md` — when to use this skill vs. others
