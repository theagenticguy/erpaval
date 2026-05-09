# Opus 4.7 prompting principles

Source: Anthropic, *Prompting best practices* (platform.claude.com), plus the Opus 4.7 migration guide. This file is the authoritative list of principles used by the audit rubric and the rewriting patterns. If you disagree with something here, check the source doc first — this file quotes and paraphrases Anthropic's own guidance.

## What changed in Opus 4.7 (vs Opus 4.6)

Five shifts directly affect prompt authoring:

### 1. More literal instruction following

> "Claude Opus 4.7 interprets prompts more literally and explicitly than Claude Opus 4.6, particularly at lower effort levels. It will not silently generalize an instruction from one item to another, and it will not infer requests you didn't make."

**Authoring implication:** State scope explicitly. "Apply this to every section, not just the first one." Prompts that rely on the model generalizing from one example to other cases will underperform.

### 2. Response length calibrates to judged complexity

Opus 4.7 calibrates length to how complex it judges the task to be, not to a fixed verbosity baseline. Prompts that tried to impose a specific length (written for 4.6) often over- or under-correct.

**Authoring implication:** If length matters, describe it positively ("Provide concise, focused responses. Skip non-essential context.") rather than imposing token caps via language.

### 3. Tone is more direct and opinionated

Less validation-forward phrasing, fewer emoji, more direct. If a product relies on a warmer voice, prompts need to ask for it explicitly.

### 4. Fewer tool calls, fewer subagents by default

Opus 4.7 reasons more and delegates less. To get more tool use or more subagent spawning, either raise `effort` to `xhigh` or state the trigger explicitly in the prompt.

### 5. Aggressive emphasis language over-triggers

This isn't new in 4.7 — it was true from 4.5 onward — but it still causes real problems in migrated prompts. Anthropic's direct quote:

> "Where you might have said 'CRITICAL: You MUST use this tool when...', you can use more normal prompting like 'Use this tool when...'."

**Authoring implication:** Reserve `**IMPORTANT:**` / `**YOU MUST:**` for one or two high-cost rules. Blanket shouting is counterproductive.

## Foundational principles (all Claude 4.x models)

### Be clear and direct

> "Think of Claude as a brilliant but new employee who lacks context on your norms and workflows. The more precisely you explain what you want, the better the result."

**Golden rule (Anthropic's own phrasing):** Show your prompt to a colleague with minimal context. If they'd be confused, Claude will be too.

### Tell Claude what to do, not just what to avoid

Positive framing outperforms negative. Anthropic's before/after:

- **Less effective:** "Do not use markdown in your response"
- **More effective:** "Your response should be composed of smoothly flowing prose paragraphs."

And:

- **Less effective:** "NEVER use ellipses"
- **More effective:** "Your response will be read aloud by a text-to-speech engine, so never use ellipses since the text-to-speech engine will not know how to pronounce them."

Note how the second adds motivation — Claude generalizes from the explanation.

### Add context and motivation

> "Providing context or motivation behind your instructions, such as explaining to Claude why such behavior is important, can help Claude better understand your goals and deliver more targeted responses."

Rules with a "because…" clause are stickier and let the model judge edge cases correctly.

### Use examples (few-shot)

Wrap examples in `<example>` tags (multiple in `<examples>`). Aim for 3–5 examples that are relevant, diverse, and cover edge cases. Anthropic explicitly recommends this.

### Use XML tags for structure

When a prompt mixes instructions, context, examples, and inputs, wrap each in its own tag: `<instructions>`, `<context>`, `<input>`, `<documents>`. Use consistent, descriptive names. Nest when there's natural hierarchy.

This also works as a format indicator: `<frontend_aesthetics>` content here `</frontend_aesthetics>` signals "this is a distinct block of guidance." Anthropic's own frontend-aesthetics snippet uses this pattern.

### Long-context structure

> "Put longform data at the top. Place your long documents and inputs near the top of your prompt, above your query, instructions, and examples. Queries at the end can improve response quality by up to 30% in tests."

Order: long data → instructions → examples → query.

### Ground responses in quotes (for long docs)

For long-document tasks, ask Claude to quote relevant passages first before answering. Reduces drift from source material.

## Thinking and effort (Opus 4.7 specific)

### Adaptive thinking is the only thinking mode

`thinking: {type: "enabled", budget_tokens: N}` returns a 400 error on Opus 4.7. Use `thinking: {type: "adaptive"}`. Also: sampling parameters (`temperature`, `top_p`, `top_k`) are removed on 4.7.

### Effort matters more on 4.7 than on any prior Opus

Five levels: `low`, `medium`, `high` (default), `xhigh` (new), `max`.

- `xhigh`: best for coding and agentic use cases (Anthropic's explicit recommendation for 4.7).
- `high`: minimum for intelligence-sensitive work.
- `low` / `medium`: latency-sensitive only. Shallow reasoning at these levels is a 4.7 behavior change — raise effort rather than prompting around it.

### Thinking is steerable

If the model thinks more than you'd like with large/complex system prompts:

```text
Thinking adds latency and should only be used when it will meaningfully improve answer quality — typically for problems that require multi-step reasoning. When in doubt, respond directly.
```

## Output formatting

### Control format positively

Three patterns (in order of preference):

1. **Tell it what to do** — "Your response should be composed of smoothly flowing prose paragraphs."
2. **Use XML format indicators** — "Write the prose sections of your response in `<smoothly_flowing_prose_paragraphs>` tags."
3. **Match prompt style to desired output** — removing markdown from the prompt reduces markdown in the output.

### Structured outputs replace prefill

Assistant-message prefills are deprecated on Claude 4.6+ (removed on Mythos Preview). Use the Structured Outputs feature (`output_config.format`) or tool calls with an enum field.

## Tool use

### Be explicit about action vs suggestion

> "If you say 'can you suggest some changes,' Claude will sometimes provide suggestions rather than implementing them."

For action, say "change this" or "make these edits," not "suggest changes."

### Parallel tool calling is on by default

The Anthropic parallel-tool-calls prompt snippet is proven to push parallel execution to ~100%:

```text
<use_parallel_tool_calls>
If you intend to call multiple tools and there are no dependencies between them, make all the independent tool calls in parallel.
</use_parallel_tool_calls>
```

## Agentic systems

### Long-horizon state tracking

Opus 4.7 excels at state tracking across long runs. Structured formats (JSON files like `tests.json`) work better than freeform text for structured data. Git is an effective state tracker.

### Safety / reversibility

Without guidance, the model may take destructive actions. Add explicit confirmation guidance for hard-to-reverse operations:

```text
Consider the reversibility and potential impact of your actions. For actions that are hard to reverse, affect shared systems, or could be destructive, ask the user before proceeding.
```

### Reduce file creation

If the model creates too many scratch files during agentic coding, add:

```text
If you create any temporary files, clean them up at the end of the task.
```

### Overeagerness / overengineering

4.5+ models tend to overengineer. Anthropic's recommended snippet is long but worth quoting verbatim when it applies (see `references/rewriting-patterns.md` for the full snippet).

## Model self-knowledge

If the product needs the model to identify itself correctly:

```text
The assistant is Claude, created by Anthropic. The current model is Claude Opus 4.7.
```

For apps that need the model string:

```text
When an LLM is needed, default to Claude Opus 4.7 unless the user requests otherwise. The exact model string for Claude Opus 4.7 is claude-opus-4-7.
```

## Anti-patterns with direct Anthropic quotes

Things the source doc explicitly warns against:

- **Anti-laziness prompts tuned for older models** — "If your prompts previously encouraged the model to be more thorough or use tools more aggressively, dial back that guidance."
- **Blanket defaults over targeted instructions** — "Instead of 'Default to using [tool],' add guidance like 'Use [tool] when it would enhance your understanding of the problem.'"
- **Over-prompting** — "Tools that undertriggered in previous models are likely to trigger appropriately now. Instructions like 'If in doubt, use [tool]' will cause overtriggering."
- **Qualitative severity language in code review** — "Report every issue you find, including ones you are uncertain about" outperforms "only report important bugs."
- **Prefill on the last assistant turn** — deprecated; migrate to structured outputs or direct instructions.

## Summary for auditing

When grading a prompt, the quickest signal checks are:

1. Does it state what to do, or what not to do? (positive framing)
2. Does it state scope explicitly? (4.7 literalism)
3. Does it use shouting / `CRITICAL` / `YOU MUST` throughout? (over-trigger risk)
4. Does it add motivation after non-obvious rules? (generalizability)
5. Does it use XML tags when mixing content types? (parseability)
6. Is it ordered stable-first for caching? (if applicable)
7. Does it reference deprecated parameters (`budget_tokens`, `temperature` on 4.7)? (stale guidance)
