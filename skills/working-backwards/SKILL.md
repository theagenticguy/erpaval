---
name: working-backwards
description: >
  Working Backwards 5-stage customer-first product discovery. Orchestrates
  Listen, Define, Invent, Refine, Test & Iterate to produce a 5CQ, PR/FAQ, or
  Dear Customer Letter. Use when the user asks to work backwards, write a PR/FAQ,
  draft 5 customer questions, do customer-first product definition, or mentions
  Working Backwards, press release FAQ, 5CQ, MLP, or customer obsession. Do NOT
  use for strategy kernel, Rumelt diagnosis, or Wardley mapping — use
  product-strategy. Do NOT use for PRD drafting or HMW/EARS specs — use
  product-discovery.
---

## Contents

| File                      | Path                                                                                   | When to load                                            |
| ------------------------- | -------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| Canonical WB reference    | `${CLAUDE_PLUGIN_ROOT}/skills/product-design-shared/references/working-backwards.md`   | 5-stage process, artifacts, principles, common pitfalls |
| Pyramid composition       | `${CLAUDE_PLUGIN_ROOT}/skills/product-design-shared/references/pyramid-principle.md`   | PR as Pyramid top, FAQ as antagonist test               |
| Research design           | `${CLAUDE_PLUGIN_ROOT}/skills/product-design-shared/references/research-design.md`     | Listen-stage hypothesis + MECE sub-questions            |
| PR/FAQ authoring workflow | `references/prfaq-authoring.md`                                                        | Drafting workflow: 5CQ → PR → FAQ → visuals             |
| Customer-insights role    | `references/roles/customer-insights.md`                                                | Researcher-agent role for Listen synthesis              |
| 5CQ worksheet             | `templates/5cq-worksheet.md`                                                           | Fill-in-the-blank for the 5 Customer Questions          |

# Working Backwards

Orchestrate the 5-stage Working Backwards process end-to-end to produce a 5CQ, PR/FAQ, or Dear Customer Letter. This skill is the user-facing runner; the canonical discipline lives in the shared reference at `${CLAUDE_PLUGIN_ROOT}/skills/product-design-shared/references/working-backwards.md`.

## When to Use

- You have a product idea and need to pressure-test it customer-first before building.
- You need to produce a PR/FAQ for an annual planning cycle or leadership review.
- You need a 5CQ to align a small team on a feature idea without the full PR/FAQ overhead.
- The real customer problem is fuzzy and you want the discipline to force clarity.

When NOT to use:

- The customer problem is already well-framed and you just need an engineering PRD → use `skills/product-discovery/` directly.
- You need a strategic argument (Rumelt kernel, Wardley map) → use `skills/product-strategy/` directly.

## Core Concepts

### The 5 stages

Load the canonical shared reference for full per-stage detail: `${CLAUDE_PLUGIN_ROOT}/skills/product-design-shared/references/working-backwards.md`. Summary:

| Stage                 | Key question                                                    | Primary artifact                                   | Upstream / downstream                                     |
| --------------------- | --------------------------------------------------------------- | -------------------------------------------------- | --------------------------------------------------------- |
| **1. Listen**         | Who is the customer and what insights do we have?               | Raw insights + customer data                       | `skills/customer-research/` + `customer-insights` role    |
| **2. Define**         | What is the prevailing customer problem / opportunity?          | Problem statement (data-backed, no solution named) | `skills/customer-research/templates/problem-statement.md` |
| **3. Invent**         | What is the solution? Why is it the right one vs. alternatives? | 1-2 sentence solution + rejected alternatives      | Brainstorm multiple directions; evaluate                  |
| **4. Refine**         | End-to-end CX? Most important customer benefit?                 | PR/FAQ draft + storyboard + MLP                    | `references/prfaq-authoring.md`                           |
| **5. Test & Iterate** | How do we measure success? Unintended impacts?                  | Success metrics + experiment plan                  | Launch is the starting line                               |

The process is **circular, not linear**. What you learn in Stage 5 feeds Stage 1.

### Artifact progression

The three WB artifacts stack from lightest to heaviest:

1. **5 Customer Questions (5CQ)** — `templates/5cq-worksheet.md`. The on-ramp. Useful on its own for smaller work.
2. **PR/FAQ** — the Press Release (≤1 page) + FAQs + Visuals (combined ≤6 pages). Workflow at `references/prfaq-authoring.md` covers the structural skeleton (headline, sub-headline, summary paragraph, problem, solution, customer quote, getting-started, leader quote, then internal/external FAQs).
3. **Dear Customer Letter** — alternative to the PR in 2nd-person letter form. Five-paragraph template.

### Pyramid connection

Working Backwards maps cleanly onto the Pyramid Principle:

- **5CQ** is a mini-Pyramid. Q1–Q4 are the base (evidence: who, what, most important benefit, how we know). Q5 is the customer-facing answer (the experience).
- **PR** is the Pyramid top-down: headline (Purpose) → body (arguments) → customer quotes + specifics (evidence).
- **FAQ** is the antagonist test from Pyramid Phase 2 externalized — pre-writing responses to the 10 hardest questions a skeptic could ask.

See `${CLAUDE_PLUGIN_ROOT}/skills/product-design-shared/references/pyramid-principle.md` for the composition discipline.

## Quick Reference

A typical end-to-end run:

1. **Capture intent.** What is the idea? Who is the primary customer segment?
2. **Listen.** Delegate to `skills/customer-research/` or use the `customer-insights` role directly. Gather raw insights; return Pyramid-base-shaped findings (per `research-design.md`).
3. **Define.** Write the problem statement using `skills/customer-research/templates/problem-statement.md`. Pressure-test with the antagonist lens.
4. **Invent.** Generate 4-6 distinct directions with tradeoffs. Do not fall in love early. Use `skills/agent-ux-patterns/` if this is an agent-UX problem.
5. **Refine.** Draft the 5CQ (`templates/5cq-worksheet.md`). Build a storyboard for the customer experience. Draft the PR/FAQ following `references/prfaq-authoring.md`.
6. **Test & Iterate.** Define success metrics. Plan the experiment. Launch. Feed learnings back to Stage 1.

### Composition with other skills

| Role                       | Skill                           | What it does                                           |
| -------------------------- | ------------------------------- | ------------------------------------------------------ |
| Upstream (Listen + Define) | `skills/customer-research/`     | Research-design method → Pyramid-base-shaped findings  |
| Downstream (engineering)   | `skills/product-discovery/`     | Translate a defined idea into engineering requirements |
| Strategic framing          | `skills/product-strategy/`      | Rumelt kernel, Wardley map, Minto-shaped argument      |
| The methodology reference  | `skills/product-design-shared/` | Canonical WB + Pyramid + research-design content       |

## Anti-Patterns

- **Skipping Listen.** Jumping to Invent because it's more fun. Produces well-executed wrong solutions.
- **Naming the solution in the problem statement.** "Customers need an AI dashboard" pre-commits the answer.
- **Writing a polished PR without the thinking.** LLMs make polish easy. Polish without clarity is a faster path to the wrong build.
- **Executive summary at the top of a PR/FAQ.** Inverts customer focus. If exec summary carries weight, wrong document type.
- **Treating launch as the finish line.** Stage 5 loops back to Stage 1.

## References

- `references/prfaq-authoring.md` — step-by-step drafting workflow (5CQ → PR → FAQ → Visuals)
- `references/roles/customer-insights.md` — researcher-agent role for Listen-stage synthesis

### Why the work is worth it

> "Done correctly, the Working Backwards process is a huge amount of work. But, it saves you even more work later. It's not designed to be easy — it's designed to save huge amounts of work on the backend, and to make sure we're actually building the right thing."
