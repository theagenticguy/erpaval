---
name: meta-prompt-optimizer
description: >
  Audit and rewrite prompts against Claude Opus 4.7 instruction-following best practices.
  Produces a scored audit plus a rewritten prompt. Use when the user asks to audit,
  review, critique, rewrite, improve, optimize, tighten, score, fix, migrate, or draft
  a prompt — including system prompts, CLAUDE.md files, Claude Code agent definitions,
  slash commands, SKILL.md files, Jinja2 prompt templates, or tool/parameter descriptions
  in Pydantic v2 or Zod schemas. Trigger on phrases like "is this prompt any good",
  "why isn't Claude following this", "why isn't my agent triggering", "my CLAUDE.md is
  being ignored", "rewrite this for Opus 4.7", "cache hit rate is low on my prompt",
  "the model keeps picking the wrong tool", or on pasted prompt text asking for feedback.
  Also trigger on mentions of prompt engineering, prompt best practices, or
  instruction-following problems. Use this skill whenever the task involves editing,
  reviewing, or writing the text of a prompt — even if the user doesn't say "prompt".
user_facing: true
---

## Contents

| File                                | When to load                                                               |
| ----------------------------------- | -------------------------------------------------------------------------- |
| `references/opus-4-7-principles.md` | Core prompting principles and the 4.7-specific behavior shifts             |
| `references/rubric.md`              | Scoring rubric — shared with the `prompt-critic` agent                     |
| `references/rewriting-patterns.md`  | Before/after transformation patterns with worked examples                  |
| `references/target-types.md`        | Type-specific guidance (CLAUDE.md, agents, commands, Jinja2, Pydantic/Zod) |

The `prompt-critic` agent in this plugin shares the same rubric and is the right tool when the user wants a scored assessment without a rewrite.

# Meta-prompt optimizer

Audit and rewrite prompts so they work well on Claude Opus 4.7. Every run produces two deliverables: a scored audit (what's wrong and why) and a rewritten prompt that applies the fixes.

The guidance is grounded in Anthropic's official prompting best-practices doc for the Claude 4.x family, with emphasis on the Opus 4.7-specific behavior shifts (literal instruction following, adaptive thinking, effort-driven calibration, dialed-back emphasis language, positive framing).

## The three modes

The user's request determines which mode to run.

| Mode                  | Trigger                                                                          | Output                                                      |
| --------------------- | -------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| **Audit only**        | "review this prompt", "critique this", "is this any good?", "score this"         | Structured audit report (pass/fail per rubric item + notes) |
| **Audit + rewrite**   | "improve this", "rewrite for 4.7", "optimize this", "fix this prompt"            | Audit report **+** revised prompt **+** changelog           |
| **Draft from intent** | "write a system prompt that…", "draft an agent for…", "give me a CLAUDE.md for…" | New prompt written against the rubric from the start        |

If the mode is ambiguous, ask once. Default to **audit + rewrite** when the user hands over an existing prompt.

## Workflow

### Step 1 — Identify the target type

Different prompt types need different treatment. Pick the matching section of `references/target-types.md` and load it before proceeding:

- **CLAUDE.md** (project or global memory) — 200-line auto-load ceiling, must stay terse, imports via `@path` are an option.
- **Claude Code agent definition** (`.md` with YAML frontmatter) — description is the triggering mechanism, body is the system prompt.
- **Slash command** (`.md` with YAML frontmatter) — arguments, bash execution, may compose with other skills.
- **SKILL.md** body — description is the triggering mechanism, progressive disclosure via references.
- **System prompt in production code** — usually a multi-line string or Jinja2 template. Often templated with variables.
- **Pydantic v2 or Zod tool / tool-input description** — terse natural-language strings the model reads when deciding whether and how to call a tool.

If you can't tell what type it is from context, ask.

### Step 2 — Read the relevant references

Always load:

- `references/opus-4-7-principles.md` — the principles you're grading against.
- `references/rubric.md` — the scoring rubric.

Load selectively:

- `references/rewriting-patterns.md` — when rewriting (modes 2 and 3).
- `references/target-types.md` — the section matching the detected type.

### Step 3 — Run the audit

For each rubric item, mark it pass / needs work / rethink and note a concrete finding. Cite line numbers or specific phrases in the source prompt when calling out issues. Audits without evidence are not useful.

The rubric has four categories:

1. **Directness and clarity** — is the ask specific, imperative, verifiable?
2. **Framing and tone** — positive statements rather than negative? Emphasis used sparingly? Contrastive phrasing avoided?
3. **Structure** — appropriate use of XML tags, ordered by stability for caching, scope stated explicitly?
4. **Type-specific fitness** — passes the checks for its target type (e.g., CLAUDE.md under 200 lines, agent description describes when to trigger).

A full rubric walkthrough lives in `references/rubric.md`. Use it verbatim — do not improvise new rubric items mid-audit.

### Step 4 — Rewrite (if the mode calls for it)

Apply the transformations from `references/rewriting-patterns.md`. The most common ones:

1. **Flip negatives to positives.** Say what to do, not just what to avoid. Cite source: Anthropic prompt-engineering doc, "Tell Claude what to do instead of what not to do."
2. **Dial back shouting.** Reserve `**IMPORTANT:**` / `**YOU MUST:**` for one or two high-cost rules. Opus 4.x over-triggers on aggressive language that was tuned for older models.
3. **State scope explicitly.** Opus 4.7 interprets prompts literally and won't generalize. "Apply this to every section, every file, every tool call" — not "apply this."
4. **Add motivation after non-obvious rules.** One clause of "because…" turns a rule into a principle the model can generalize from.
5. **Remove hedging.** Replace "likely / probably / maybe" with the specific finding.
6. **Cut self-evident instructions.** If a rule describes behavior the model would already produce, it's filler. Remove it.
7. **Match format to stability.** For cached prompts, put stable content first, volatile content last.
8. **Use XML tags for structure when the prompt mixes content types.** `<instructions>`, `<context>`, `<examples>`, `<frontend_aesthetics>`.

### Step 5 — Produce the deliverable

Output format depends on mode:

**Audit only:**

```markdown
## Audit: [prompt name or summary]

### Scores

| Category              | Score                       | Notes              |
| --------------------- | --------------------------- | ------------------ |
| Directness & clarity  | Pass / Needs work / Rethink | [specific finding] |
| Framing & tone        | …                           | …                  |
| Structure             | …                           | …                  |
| Type-specific fitness | …                           | …                  |

### Findings

1. **[Finding title]** — [what's wrong, with line reference]. Impact: [why it matters].
2. …

### Top priorities to fix

[numbered list of the 2-3 highest-leverage changes]
```

**Audit + rewrite:**

Same audit section, then:

```markdown
### Rewritten prompt

[the full revised prompt]

### Changelog

- [Change 1] — [which rubric item it addresses]
- [Change 2] — …
```

**Draft from intent:**

```markdown
## Drafted prompt: [name]

[the prompt]

### Rationale

- [Decision 1] — [why]
- [Decision 2] — …
```

### Step 6 — Offer to run the critic

After producing the deliverable, offer to run the `prompt-critic` agent on the result for an independent second opinion. The critic uses the same rubric from an unbiased starting point — useful for checking that the rewrite actually improved the scores rather than shuffling them.

Invoke it with the `Agent` tool, `subagent_type: "prompt-critic"`, passing the rewritten prompt and the prompt's target type. Don't auto-run it — ask first, because users iterating quickly may not want the extra round trip. (Note: the `prompt-critic` agent is not bundled in this plugin — it lives in the upstream `personal-plugins` repo. If unavailable, the rewrite is the deliverable.)

## Special cases

### Jinja2 templates

Audit the template skeleton and the rendered output separately. Silent invalidators (per-request timestamps, user IDs, unsorted dict serialization) inside the template will break prompt caching. Flag them. See `references/target-types.md` → "Jinja2 templates".

### Pydantic v2 / Zod tool descriptions

These are terse by nature. The rubric applies differently — short is good here, but the description must answer three questions: what does this tool do, when should the model call it, what do the parameters mean. See `references/target-types.md` → "Tool descriptions".

### Migration tasks

If the user is migrating a prompt from an older model (e.g., Sonnet 3.7 → Opus 4.7), the rewrite should remove obsolete parameter guidance (sampling parameters, `budget_tokens`), dial back the shouting that older models needed, and flip negative framings. Note the migration explicitly in the changelog.

## Anti-patterns to avoid in your own output

This skill is a prompt-optimizer — its output is held to the same standard it grades against.

- Don't pad audits with "Based on our analysis…" or "Overall the prompt has strengths and weaknesses." Lead with the finding.
- Don't hedge scores. If a rubric item fails, say it fails. "Mostly passes" is not useful.
- Don't rewrite for the sake of rewriting. If a section passes the rubric, leave it alone and say so in the changelog.
- Don't invent rubric items that aren't in `references/rubric.md`. The rubric is the contract.
