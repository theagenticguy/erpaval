# Working Backwards (PR-FAQ as strategy thinking-tool)

Within `product-strategy`, the PR-FAQ is used as a **strategy-framework thinking tool** — a forcing function for customer-value clarity during the Phase 2 fan-out. The canonical 5-stage discovery orchestrator (Listen → Define → Invent → Refine → Test) and any publishable PR-FAQ format live elsewhere.

## Canonical references

- `${CLAUDE_PLUGIN_ROOT}/skills/product-design-shared/references/working-backwards.md` — full 5-stage methodology, artifacts, principles, common pitfalls.
- `${CLAUDE_PLUGIN_ROOT}/skills/working-backwards/` — the user-facing orchestrator when the deliverable is a PR/FAQ or 5CQ end-to-end.

## When to use within `product-strategy`

New product or major feature where customer value is genuinely ambiguous. Executive-gate discovery where the leadership audience needs a customer-facing story, not a feature spec. Teams that want to catch "wrong product" before a kernel commits to action. Especially useful upstream of the Phase 3 synthesizer: the PR-FAQ becomes the customer-value spine the memo builds from.

## When to skip

Skip for iteration on an existing product with known customer fit. Skip for infrastructure, refactors, and internal tooling where "customer" is a stretched term. Skip for teams without leadership-review culture — a PR-FAQ without a critical reader is a hallucination with a byline. Skip when the work is really a kernel (diagnosis-first) — PR-FAQs don't diagnose, they describe.

## Strategy-specific validation checks

- Headline is a customer benefit, not a feature name.
- The five customer questions (McAllister) are answered specifically, not generically.
- Customer quote is realistic — named archetype, specific situation, past-tense success.
- Internal FAQ includes honest kill criteria and real risks — not "risks we already handled."
- "How do we know the customer wants this?" cites research or real signal, not gut feel.
- External FAQ answers objections a competitor would raise.

For the full structure, five customer questions, template, and worked example, load the shared canonical reference. This file exists to mark the framework-routing boundary — the synthesizer sees the PR-FAQ as one of four Phase 2 inputs, not as the deliverable.

## Citations

- [30] Bryar, C. & Carr, B. *Working Backwards: Insights, Stories, and Secrets from Inside Amazon.* St. Martin's Press, 2020.
- [31] [Product School, "PR/FAQ: The Working Backwards Document."](https://productschool.com/blog/product-fundamentals/prfaq) (updated 2024).
- [58] [Ian McAllister on Working Backwards, Medium summary.](https://medium.com/fact-of-the-day-1/working-backwards-at-amazon-a303c3680aa3) (2021).
