# Working Backwards — 5-stage customer-first discovery process

Shared reference for the Working Backwards (WB) methodology. This file explains the discipline. The user-facing orchestration lives in `skills/working-backwards/SKILL.md`.

## The principle

Working Backwards is a process for understanding the customer deeply *before* committing to a solution. It applies to products, services, internal tools, external launches, small features, and large bets. The discipline is simple in principle and demanding in practice: set aside assumptions, seek perspectives you might miss, let customer needs drive what you build.

In the AI era the point sharpens: *speed without customer clarity is just a faster way to build the wrong thing.* The artifact speed that LLMs enable raises the bar on the *thinking* upstream of the artifact.

## The five stages

The process is **circular, not linear**. What you learn in Stage 5 feeds back into Stage 1. Working Backwards does not end at launch; it is how you keep improving.

| Stage                 | Key question                                                                                           | What happens                                                                                                                                                                                          | Primary artifact                                                                                              |
| --------------------- | ------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| **1. Listen**         | Who is the customer and what insights do we have?                                                      | Qualitative + quantitative data collection. User research, ethnography, stakeholder interviews, market scans. Focus on a specific primary customer segment.                                           | Raw insights + customer data                                                                                  |
| **2. Define**         | What is the prevailing customer problem or opportunity? What data informed this?                       | Synthesize Listen insights into a specific, data-backed problem statement. Do NOT name the solution.                                                                                                  | Problem statement: *"Today, [customers] have to [problem] when [situation]. Customers need a way to [need]."* |
| **3. Invent**         | What is the solution? Why is it the right one?                                                         | Generate multiple directions. Evaluate alternatives. Be willing to pivot based on feedback.                                                                                                           | 1–2 sentence solution + list of rejected alternatives                                                         |
| **4. Refine**         | How would we describe the end-to-end customer experience? What is the most important customer benefit? | Pin the solution to a customer-visible experience. Identify the single most important benefit. Define the MLP (Minimum Lovable Product).                                                              | First-draft PR/FAQ, Dear Customer Letter, or storyboard + MLP definition                                      |
| **5. Test & Iterate** | How will we define and measure success?                                                                | Validate through testing (usability, A/B, user testing). Consider unintended impacts. Launch is the starting line, not the finish line.                                                                | Success metrics + experiment plan + post-launch quality scorecard + iteration plan                            |

## The artifacts

Three progressively-heavier documents express the WB thinking:

### 5 Customer Questions (5CQ)

The lightest artifact. Answers five foundational questions:

1. **Who is the customer?** — Specific. Behaviors, attributes, context. Not demographics.
2. **What is the customer problem or opportunity?** — The pain, not the feature. Scale it honestly.
3. **What is the most important customer benefit?** — One most-important, not a list.
4. **How do you know what customers want?** — Evidence, or explicit hypothesis + test plan.
5. **What does the customer experience look like?** — Sketch, storyboard, journey map, wireframe.

5CQ is useful on its own for small projects or iterations that do not warrant a full PR/FAQ. For larger work it is the on-ramp: the clarity you develop in 5CQ makes the PR/FAQ faster and sharper to write.

### PR/FAQ

The core artifact. Three sections:

1. **Press Release (PR)** — 1 page maximum, forward-looking, customer-perspective, written as if it were going out on the wire (it never is).
2. **Frequently Asked Questions (FAQs)** — customer-facing questions + internal/stakeholder questions. Anticipates hard questions.
3. **Visuals** — storyboards, wireframes, mocks that make the experience tangible.

Length: PR ≤ 1 page; PR + FAQs ≤ 6 pages. Anyone can write a PR/FAQ — PM, designer, engineer. The composition discipline is `pyramid-principle.md` (the PR is the Pyramid's top; the FAQ is the antagonist test).

### Dear Customer Letter

An alternative to the PR that speaks directly to the customer in 2nd-person letter form. More natural for internal-facing launches; pairs with the same FAQ + Visuals. Five-paragraph template: greeting → announcement → describe the new thing → how it works → call to action → sign off.

## Common pitfalls

- **Skipping Listen.** Jumping to Invent because ideation is fun and customer research is hard. The result is a well-executed wrong solution.
- **Naming the solution in the problem statement.** "Customers need an AI-powered dashboard" pre-commits to the solution and collapses the Invent stage.
- **Writing the PR before thinking.** AI makes polished PR prose easy. The point of the PR is clarity, not polish. If the thinking is soft, the PR is a well-written dead end.
- **Treating launch as the finish line.** Stage 5 loops back to Stage 1. Post-launch iteration is load-bearing, not optional.
- **Executive summary at the top of a PR/FAQ.** Inverts the customer focus. If the exec summary carries the weight, you wrote the wrong document type.

## Principles for PR/FAQ writing

- **Be okay with imperfection.** The first version is rough. Focus on communicating how the idea will delight customers.
- **Keep the PR to one page.** The constraint forces prioritization. Every sentence adds unique value.
- **Customer-centric language.** Write so any customer could read and understand. No hyperbole. No jargon. No weasel words.
- **Evidence over enthusiasm.** Data beats adjectives. "23% of users" beats "a significant proportion of users".

These principles match the discipline in `pyramid-principle.md`. A good PR is a Pyramid expressed as a press release: Purpose (the headline) → Arguments (the body paragraphs) → Evidence (quotes + metrics + customer specifics). The FAQ is the counter-argument test from `pyramid-principle.md` Phase 2, externalized as a Q&A.

## How WB maps to other disciplines

| Stage          | Double Diamond            | Pyramid                                         |
| -------------- | ------------------------- | ----------------------------------------------- |
| Listen         | Discover (diverge)        | Evidence collection                             |
| Define         | Define (converge)         | MECE grouping + problem framing                 |
| Invent         | Develop (diverge)         | Argument construction                           |
| Refine         | Develop (converge)        | Answer derivation + draft in presentation order |
| Test & Iterate | Deliver (converge + loop) | Antagonist test + post-launch feedback          |

See `double-diamond.md` for the UK Design Council framework and `pyramid-principle.md` for the composition discipline. See `methodology-selection.md` for when to pick which.

## Source material

> "Done correctly, the Working Backwards process is a huge amount of work. But, it saves you even more work later. It's not designed to be easy — it's designed to save huge amounts of work on the backend, and to make sure we're actually building the right thing."

Speed without customer clarity is just a faster way to build the wrong thing.
