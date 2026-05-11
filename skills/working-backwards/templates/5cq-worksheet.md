# 5 Customer Questions (5CQ) Worksheet

Fill-in-the-blank worksheet for the 5 Customer Questions. The lightest Working Backwards artifact — useful as a standalone for small projects, or as the on-ramp to a full PR/FAQ.

**Project name**: [FILL]
**Date**: [FILL]
**Author**: [FILL]
**Status**: [Draft / Reviewed / Approved]

---

## Question 1 — Who is the customer?

Be specific. A label like "user" or "shopper" is not specific enough. Think about the behaviors, attributes, and context that define your target customer. What are they doing when they encounter the problem? What is their relationship to your product or service? What makes them unique?

Everything that follows depends on this answer. Vague here = vague everywhere. Avoid demographics-only descriptions. Focus on behavior, context, and need.

**Your answer:**

> [FILL: 2–4 sentences. Name one primary customer segment. Describe what they do, where, when, and why.]

**Evidence / data that grounds this segment:**

- [FILL: source 1]
- [FILL: source 2]

---

## Question 2 — What is the customer problem or opportunity?

Describe the specific problem you are solving or opportunity you are creating. Put yourself in the customer's situation. When do they experience this problem? How does it present itself?

**A need is not a feature.** No one needs an app to organize their shopping list. They need to save time, save money, or make a better decision. Focus on what the customer is *feeling*, not what you are building.

Be honest about the scale. A small frustration felt by many customers can still be a significant opportunity. You do not need to exaggerate.

**Your answer:**

> [FILL: 2–4 sentences. Describe the problem from the customer's perspective. Do NOT name the solution.]

**Problem statement (formal):**

> Today, [customer segment from Q1] have to [specific problem] when [situation]. Customers need a way to [what they need, not what you're building].

**Evidence of the problem:**

- Behavioral: [FILL — what customers are observably doing]
- Attitudinal: [FILL — what customers say]
- Scale: [FILL — how many customers, how often]

---

## Question 3 — What is the most important customer benefit?

Describe your proposed solution and the **single most important benefit** it delivers to the customer. There may be many benefits, but identifying the one-most-important forces you to prioritize and clarify your thinking.

Walk through the solution from the customer's perspective. You do not need final designs. Paint a plausible picture of how the customer's experience improves. Then ask: what does the customer *actually get*? How does it make their life better? Be specific. If you say it saves them time, say how much. If you say it makes something simpler, explain what you removed or changed.

**Your answer:**

> [FILL: 1–2 sentences describing the solution. Then one sentence stating the single most important benefit.]

**Why this benefit, not a different one:**

> [FILL: Why is this the top benefit? What would you give up if a reviewer said "pick one — time saved or money saved"?]

---

## Question 4 — How do you know what customers want?

Bring whatever evidence you have. Analytics, research, customer service data, anecdotes, qualitative studies. If you do not have evidence yet, articulate your hypothesis clearly and describe how you would test it.

Not having evidence should not stop you from starting. Writing down your hypothesis often helps you identify what evidence you need, and sharing the document frequently surfaces data you did not know existed.

**Evidence you already have:**

- [FILL: quantitative source 1]
- [FILL: qualitative source 1]
- [FILL: existing customer research]

**What you do not yet know (research gaps):**

- [FILL: open question 1]
- [FILL: open question 2]

**If you have a hypothesis but no evidence yet:**

- Hypothesis: [FILL]
- Null hypothesis (what would disprove it): [FILL]
- How you would test: [FILL — method + success criteria]

(See `${CLAUDE_PLUGIN_ROOT}/skills/product-design-shared/references/research-design.md` for the full research-design method, or delegate to `skills/customer-research/` to build a plan.)

---

## Question 5 — What does the customer experience look like?

Describe how customers would discover and use your solution. Sketch the experience, literally if it helps. A whiteboard drawing, storyboard, user journey map, or wireframe all work. The goal is to make the experience tangible enough that others can react to it and help improve it.

**Narrative walkthrough (2–3 paragraphs):**

> [FILL: Start with the moment the customer encounters the problem or the entry point. Walk through discovery → first use → ongoing use. Use 2nd person "you" if that helps. Describe the customer's emotional arc.]

**Supporting visuals:**

- Storyboard: [FILL — link or inline reference]
- Journey map: [FILL — link or inline reference; see `skills/customer-research/templates/customer-journey-map.md`]
- Wireframes / mocks: [FILL]

---

## What happens next

Once the 5CQ is filled in and feels tight, decide:

| Confidence in answers                                   | Next step                                                                                 |
| ------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| All five answers are strong and you need wide alignment | Escalate to a full PR/FAQ — use `skills/working-backwards/references/prfaq-authoring.md`  |
| All five answers are strong and the work is small       | Ship the 5CQ as-is; skip the PR/FAQ                                                       |
| Q4 is weak (evidence gap)                               | Run `skills/customer-research/` with the hypothesis from Q4 before continuing             |
| Q1 or Q2 feels vague                                    | Go back to Listen — interview more customers before naming benefits                       |
| Q3 keeps shifting                                       | That is the signal the solution is not yet clear — try a storyboard to force concreteness |

## Anti-patterns

- **Q1 too broad.** "All customers" fails. Narrow to a specific primary segment.
- **Q2 names the solution.** "Customers need an AI-powered dashboard" is a solution masquerading as a problem. Rewrite around the *pain* or *job-to-be-done*.
- **Q3 is a feature list.** The prompt asks for the single most important benefit. Force yourself to pick one.
- **Q4 is aspirational.** "We believe customers will love this" is not evidence. If you have no evidence, mark it as a hypothesis and plan the test.
- **Q5 is a feature-tour.** The prompt asks what the customer experiences, not what the product does. Frame it around customer actions and emotions, not UI elements.
