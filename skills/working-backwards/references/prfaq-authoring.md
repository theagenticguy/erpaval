# PR/FAQ authoring workflow

Step-by-step workflow for drafting a PR/FAQ the Working Backwards way. The discipline is in the shared reference; this file is the workflow that uses it.

## References to load first

Before drafting, load these:

- **Process** — `${CLAUDE_PLUGIN_ROOT}/skills/product-design-shared/references/working-backwards.md` — the 5 stages, artifacts, principles.
- **Composition** — `${CLAUDE_PLUGIN_ROOT}/skills/product-design-shared/references/pyramid-principle.md` — research bottom-up, present top-down, MECE, SCQA, antagonist test.
- **Research** — `${CLAUDE_PLUGIN_ROOT}/skills/product-design-shared/references/research-design.md` — hypothesis + null + MECE questions that produce Pyramid-base-shaped findings.

The PR/FAQ skeleton, voice rules, and any organization-specific Legal checklist are deliberately not bundled here — they tend to be team-specific. Fork this skill and drop in your team's templates, or compose with a writing-style skill of your choosing.

## The workflow

### 1. Write a 5CQ first

Before the PR, always draft the 5 Customer Questions worksheet (`../templates/5cq-worksheet.md`). The 5CQ is the Pyramid base for the PR:

- Q1 (Who) + Q2 (Problem) + Q4 (Evidence) → the PR's Situation + Complication
- Q3 (Most important benefit) → the PR's headline and most important paragraph
- Q5 (Customer experience) → the PR's body paragraphs

If you cannot answer the 5CQ crisply, the PR will be vague. Go do more research — call `skills/customer-research/` with a research plan.

### 2. Draft the Press Release (PR) top-down

The PR is a mock press release (internal only — never goes on the wire). One page maximum. Structure:

- **Headline** — benefits-first, customer-facing. Derived last. One line.
- **Subheadline** — one sentence that widens the audience-facing claim.
- **Opening paragraph** — city/date/lead. The most important customer benefit in the first two sentences.
- **Customer problem paragraph** — what was hard before. Specific. Data-backed where possible.
- **Solution paragraph** — what is new, how it works, in customer-centric language.
- **Customer quote** — a plausible quote from a named-persona customer articulating the benefit.
- **How to get started paragraph** — discovery + activation + next step.
- **Closing** — a final customer-benefit reinforcement.

Apply the Pyramid discipline: derive the headline *last*, after you know the arguments. Do not start with the headline.

### 3. Draft the FAQ — Customer questions first

The Customer FAQ anticipates the questions a reader of the PR would ask. Examples:

- "How much does this cost?"
- "When will this be available?"
- "How is this different from [existing competitor or adjacent product]?"
- "Is my data private?"

Order by importance. 5-10 questions typical for the customer-facing section.

### 4. Draft the FAQ — Internal/stakeholder questions second

The Internal FAQ pre-empts the skeptical reviewer. This is the Pyramid antagonist test externalized. Write down the 10 hardest questions a leadership reviewer could ask:

- "Why now?"
- "What data supports this customer problem is real at scale?"
- "What happens if [biggest risk] occurs?"
- "Why is this the right team to build this?"
- "What alternatives did you reject and why?"
- "What does success look like at 1 month, 3 months, 1 year?"
- "What are the dependencies on other teams?"
- "What is the plan if [key assumption] is wrong?"
- "What is the monetization/cost model?"
- "What is the operational load post-launch?"

Answer each in 1-3 paragraphs. If you cannot answer one convincingly, that is the signal to do more research or kill the idea — not to bluff.

### 5. Add Visuals

Storyboard panels, mockups, or wireframes. Visuals make the experience tangible; they are not decoration. Each should correspond to a claim in the PR.

### 6. Self-edit against a quality rubric

The critical sentence-level checks (universal, not org-specific):

- No weasel words (significant, many, soon, should, may).
- No passive voice.
- Sentences ≤ 20 words.
- Every claim followed by evidence.

Then the document-level checks:

- PR is one page. No more.
- PR + FAQ + Visuals is six pages or fewer.
- The opening two sentences contain the most important customer benefit.
- The PR stands without the FAQ — a reader who sees only the PR still gets the ask.

### 7. Run the antagonist test

Read the PR + FAQ as the most skeptical person in the room. For every claim: do you believe it? Is it specific? Is hedge language hiding uncertainty? Fix any gap before sharing.

### 8. Legal review (external-facing only)

If the PR/FAQ will leave the organization, apply your team's Legal checklist. Common universal rules:

- No forward-looking statements ("coming soon", "we plan to").
- No superlative claims without approved stats.
- No competitor mentions.
- No "free" outside approved contexts.

## Lengths and conventions

- **PR**: 1 page. ~250-400 words.
- **PR + FAQs**: 6 pages maximum.
- **Visuals**: as many as needed; keep them legible at print size.
- **Headings**: bold. Spell out acronyms on first use.

## Common AI failure modes

| Failure                          | Why it happens                                             | Fix                                                                        |
| -------------------------------- | ---------------------------------------------------------- | -------------------------------------------------------------------------- |
| Vague headline                   | LLM writes the headline first, derives the content from it | Write the headline last, after the FAQs exist                              |
| Polished prose with no substance | LLM optimizes for reading ease over information            | Audit every sentence for load-bearing content; cut fluff                   |
| FAQ that defends the idea        | LLM frames objections it can easily answer                 | Write the 10 hardest questions first, then answer them honestly            |
| Missing or hedged customer quote | LLM is uncertain about what a customer would really say    | Ground the quote in real research or mark as `[NEEDS CUSTOMER VALIDATION]` |
| Hyperbole                        | LLM was rewarded for enthusiastic language in training     | Strip every adjective that does not carry information                      |

## When to use the Dear Customer Letter instead

The Dear Customer Letter is the 2nd-person alternative to the PR. Use it when:

- The product launches via email or internal announcement (no "press release" mock makes sense).
- The primary beneficiary is an internal user (internal tools).
- You want a more natural-feeling empathy exercise.

The letter pairs with the same FAQ + Visuals structure. The PR section becomes a 5-paragraph letter: greeting → announcement → describe the thing → how it works → call to action → thank + sign.
