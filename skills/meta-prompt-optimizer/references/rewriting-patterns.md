# Rewriting patterns

Before/after transformations for common prompt issues. Each pattern maps to one or more rubric items.

---

## Pattern 1: Flip negatives to positives

**Rubric:** 2.1 Positive framing.

**Why:** Anthropic's direct recommendation — "Tell Claude what to do instead of what not to do." Positive framing gives the model a concrete behavior to exhibit rather than a category to avoid.

**Before:**

```text
Do not use markdown in your response.
```

**After:**

```text
Your response should be composed of smoothly flowing prose paragraphs.
```

---

**Before:**

```text
NEVER use ellipses.
```

**After:**

```text
Your response will be read aloud by a text-to-speech engine, so never use ellipses since the text-to-speech engine will not know how to pronounce them.
```

Note: this second example keeps the "never" but adds motivation. Negative constructions are sometimes the right shape — the point is that the *rule* should give the model something concrete to do.

---

**Before (negative ladder):**

```text
- Avoid contrastive statements
- Don't hedge
- NEVER use ellipses
- Avoid passive voice
- Don't use buzzwords
```

**After (positive statements):**

```text
- Write assertions as single positive claims.
- State conclusions directly.
- End sentences with periods.
- Use active voice — "we shipped X," not "X was shipped."
- Name specifics — "23% of users" beats "many users."
```

---

## Pattern 2: State scope explicitly

**Rubric:** 3.1 Explicit scope.

**Why:** Opus 4.7 interprets prompts literally and won't generalize from one example to other cases.

**Before:**

```text
Format this section with bullet points.
```

**After:**

```text
Format every section with bullet points, including the summary and the conclusion.
```

---

**Before:**

```text
Don't claim the code is fixed without running the tests.
```

**After:**

```text
Before reporting any bug fix, refactor, or feature as complete, run the full test suite and confirm it passes. This applies to single-line changes as well as larger refactors.
```

---

## Pattern 3: Dial back shouting

**Rubric:** 2.3 Emphasis used sparingly.

**Why:** Opus 4.x over-triggers on aggressive emphasis tuned for older models. "CRITICAL: YOU MUST..." was the right intensity in 2024. In 2026 it's noise.

**Before:**

```text
CRITICAL: You MUST always run tests. NEVER skip this step. This is ABSOLUTELY REQUIRED.
```

**After:**

```text
Run the test suite before declaring work complete. If tests fail, fix them in the same change; don't move on.
```

Reserve bold `**IMPORTANT:**` for one or two rules in a prompt — the ones where skipping would cause real harm. Everything else uses plain imperatives.

---

## Pattern 4: Add motivation after non-obvious rules

**Rubric:** 2.2 Motivation after non-obvious rules.

**Why:** Motivation gives the model grounds to generalize and judge edge cases.

**Before:**

```text
Use TaskCreate for multi-step work.
```

**After:**

```text
Use TaskCreate for multi-step work (3+ discrete steps or multiple files), because it makes progress visible to the user and prevents steps from being dropped when you switch context.
```

---

**Before:**

```text
Don't interpolate timestamps into the system prompt.
```

**After:**

```text
Don't interpolate timestamps into the system prompt — a changing timestamp at the start of the prefix invalidates the prompt cache for every downstream block, which can silently turn a cache-hit path into a cache-miss path.
```

---

## Pattern 5: Cut self-evident content

**Rubric:** 3.5 Self-evident content.

**Why:** Rules that describe default model behavior add noise. If removing the rule wouldn't change anything, remove it.

**Before (all filler):**

```text
- Be helpful.
- Be accurate.
- Think before you respond.
- Don't make things up.
- Write clean code.
```

**After:**

```text
(delete the section)
```

Model already defaults to being helpful, accurate, and thoughtful. These rules only become useful if they're specific ("accurate — cite line numbers when referencing code") or counter-default ("when uncertain, ask rather than guess — default is to guess").

---

## Pattern 6: Replace blanket defaults with targeted triggers

**Rubric:** Anti-pattern — "anti-laziness prompts tuned for older models."

**Why:** Anthropic's direct recommendation — "Instead of 'Default to using [tool],' add guidance like 'Use [tool] when it would enhance your understanding of the problem.'"

**Before:**

```text
Always use Context7 for any library question.
```

**After:**

```text
Use Context7 when writing code that calls a library API, because training-data recall of specific function signatures is often stale. Skip it for general concepts the docs wouldn't change (e.g., "what is recursion").
```

---

## Pattern 7: Structure with XML tags

**Rubric:** 3.2 XML tags when mixing content types.

**Why:** When a prompt bundles instructions + context + examples + inputs, delimiting each type with XML tags reduces misinterpretation.

**Before (unstructured):**

```text
You are a code reviewer. Here are the style rules we follow: 2-space indent, no semicolons, arrow functions for callbacks. Review this code and flag any issues: function foo() { return 1; }. Respond with a list of findings.
```

**After (XML-structured):**

```text
You are a code reviewer.

<style_rules>
- 2-space indent
- No semicolons
- Arrow functions for callbacks
</style_rules>

<code_to_review>
function foo() { return 1; }
</code_to_review>

Respond with a list of findings in <findings> tags.
```

---

## Pattern 8: Long-context ordering

**Rubric:** 3.3 Stable-first ordering.

**Why:** Anthropic's guidance — "Put longform data at the top. Queries at the end can improve response quality by up to 30% in tests, especially with complex, multi-document inputs."

**Before:**

```text
Summarize the key points from this document:

<document>
{{50_pages_of_content}}
</document>

Include specific numbers and cite the section name for each point.
```

**After:**

```text
<document>
{{50_pages_of_content}}
</document>

Summarize the key points from the document above. Include specific numbers and cite the section name for each point.
```

Also: for prompt caching, stable content (role, fixed instructions) goes before volatile content (per-request inputs).

---

## Pattern 9: Migrate deprecated parameters and patterns

**Rubric:** 3.4 Deprecated parameter references.

**Why:** Prompts written for older models reference parameters that fail or silently misbehave on Opus 4.7.

**Before:**

```text
Use extended thinking with a budget of 32000 tokens. Set temperature to 0 for determinism.
```

**After:**

```text
Use adaptive thinking with `effort: "xhigh"` (for coding/agentic work) or `effort: "high"` (intelligence-sensitive). Opus 4.7 no longer exposes `temperature`, `top_p`, or `top_k` — steer behavior through prompting only.
```

---

**Before (prefill pattern):**

```python
messages = [
    {"role": "user", "content": "Generate JSON with name, age"},
    {"role": "assistant", "content": "{"}  # prefill
]
```

**After (structured outputs):**

```python
response = client.messages.parse(
    model="claude-opus-4-7",
    messages=[{"role": "user", "content": "Generate name and age"}],
    output_format=PersonSchema,  # Pydantic class
)
```

---

## Pattern 10: Remove hedging from the prompt itself

**Rubric:** 2.5 No hedging.

**Why:** Prompts that hedge teach the model to hedge.

**Before:**

```text
If you think it might be a good idea, you could probably try to maybe add some error handling.
```

**After:**

```text
Add error handling at system boundaries (user input, external APIs).
```

---

## Pattern 11: The overengineering snippet (verbatim)

When a prompt addresses agentic coding with a model that tends to overengineer, Anthropic's recommended snippet is worth using verbatim. Don't paraphrase — the exact phrasing has been tuned.

```text
Avoid over-engineering. Only make changes that are directly requested or clearly necessary. Keep solutions simple and focused:

- Scope: Don't add features, refactor code, or make "improvements" beyond what was asked. A bug fix doesn't need surrounding code cleaned up. A simple feature doesn't need extra configurability.

- Documentation: Don't add docstrings, comments, or type annotations to code you didn't change. Only add comments where the logic isn't self-evident.

- Defensive coding: Don't add error handling, fallbacks, or validation for scenarios that can't happen. Trust internal code and framework guarantees. Only validate at system boundaries (user input, external APIs).

- Abstractions: Don't create helpers, utilities, or abstractions for one-time operations. Don't design for hypothetical future requirements. The right amount of complexity is the minimum needed for the current task.
```

Note this uses negative framing ("Don't add features…"). In this case the negatives are specific and verifiable, which passes the rubric. Negative framing fails when it's vague ("don't be lazy") — not when it's concrete.

---

## Pattern 12: Parallel tool calls (verbatim)

When a prompt needs reliable parallel tool execution, Anthropic's snippet pushes it to ~100%:

```text
<use_parallel_tool_calls>
If you intend to call multiple tools and there are no dependencies between the tool calls, make all of the independent tool calls in parallel. Prioritize calling tools simultaneously whenever the actions can be done in parallel rather than sequentially. For example, when reading 3 files, run 3 tool calls in parallel to read all 3 files into context at the same time. Maximize use of parallel tool calls where possible to increase speed and efficiency. However, if some tool calls depend on previous calls to inform dependent values like the parameters, do NOT call these tools in parallel and instead call them sequentially. Never use placeholders or guess missing parameters in tool calls.
</use_parallel_tool_calls>
```

---

## Pattern 13: Investigation before answering (verbatim)

For code-aware agents that tend to speculate:

```text
<investigate_before_answering>
Never speculate about code you have not opened. If the user references a specific file, you MUST read the file before answering. Make sure to investigate and read relevant files BEFORE answering questions about the codebase. Never make any claims about code before investigating unless you are certain of the correct answer — give grounded and hallucination-free answers.
</investigate_before_answering>
```

This one intentionally uses "MUST" — Anthropic's own snippet does. When an emphasized rule is high-stakes (grounding in code), the emphasis earns its place.

---

## Pattern 14: Uncertainty handling — ground, propose, confirm

**Rubric:** 2.6 Uncertainty handling.

**Why:** Prompts often fall into one of two failure modes for "when the model is unsure." The first — "just make your best guess and move on" — licenses hallucination. The second — "always ask the user before doing anything" — blocks the model from using tools and knowledge it has, producing low-value back-and-forth. Both hand off work the model could have done.

The right shape is a three-step escalation: **ground → propose → confirm.** Use tools, web search, and code reading to resolve the uncertainty yourself; if you still can't, state the specific call you're making and why; ask the user to verify the call — not to make it for you.

**Before (hallucination license):**

```text
If you don't know the answer to something, just make your best guess.
```

**Before (escalation without attempt):**

```text
If you are unsure about anything, always ask the user before proceeding.
```

**After:**

```text
When you're uncertain:
1. Ground first — search docs, read the relevant code, run a quick check. Most uncertainty is resolvable this way.
2. If ground-first doesn't resolve it, state your best call and the evidence behind it. Don't hide the uncertainty, but don't escalate it either.
3. Ask the user to verify your call when the action is irreversible, affects shared systems, or the evidence is thin. For reversible work within scope, proceed with your call and flag it in the summary.
```

This pattern generalizes: it keeps the model productive on reversible work while preserving a confirmation gate for destructive or hard-to-verify actions. Pair it with Pattern 13 (investigation before answering) for code-aware agents.

---

## What doesn't need rewriting

Not every section of a prompt needs changes. The rewriter's job is to fix what's broken, not to regenerate the whole thing. Examples of sections to leave alone:

- Concrete, verifiable rules already in imperative voice.
- Well-structured tables of commands or configuration.
- Examples that cover diverse edge cases (Anthropic recommends 3–5).
- Motivation clauses that explain why a rule exists.

If a section passes the rubric, the changelog should say so: "Left Section X unchanged — already passes rubric on all items."
