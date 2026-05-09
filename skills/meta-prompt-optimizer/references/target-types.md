# Type-specific guidance

Different prompt types have different constraints. Load the section matching the target before auditing or rewriting.

Jump to:

- [CLAUDE.md files](#claudemd-files)
- [Claude Code agent definitions](#claude-code-agent-definitions)
- [Slash commands](#slash-commands)
- [SKILL.md bodies](#skillmd-bodies)
- [System prompts in production code](#system-prompts-in-production-code)
- [Jinja2 templates](#jinja2-templates)
- [Pydantic v2 / Zod tool descriptions](#pydantic-v2--zod-tool-descriptions)

---

## CLAUDE.md files

### Constraints

- **200-line auto-load ceiling.** Only the first 200 lines are automatically included in context. Everything below is ignored unless loaded via `@import`.
- **Every line costs context.** Longer CLAUDE.md files reduce adherence to everything in them — the model tunes out.
- **Applies globally** (or per-project if scoped). Anything in here fires on every single request; weigh carefully.

### Include in CLAUDE.md

- Commands Claude can't guess from context (test runners, lint, deploy).
- Code style that differs from defaults (custom indentation, naming).
- Repo etiquette (commit message format, PR conventions).
- Architecture decisions with non-obvious motivation.
- Environment quirks (auth flow, local vs CI).
- Tool choices (`uv`, `mise`, specific libraries).
- Persistent voice/style preferences.

### Exclude from CLAUDE.md

- Standard language conventions Claude already knows.
- API documentation (link instead — or use a skill).
- Self-evident practices ("write clean code").
- File-by-file codebase descriptions (model can grep).
- Per-feature todos or in-progress state (use the project memory system).

### Type-specific rubric additions

1. **Under 200 lines?** Hard ceiling.
2. **Every rule earns its place?** Apply "would removing this cause Claude to make mistakes?" — if no, cut.
3. **Uses `@path` imports for conditional or voluminous content?**
4. **No contradictions between rules?** Two rules saying different things in different sections leads to arbitrary choice.
5. **Organized by frequency of use?** Most-hit rules near the top.

### Common issues in CLAUDE.md audits

- Over 200 lines.
- Copy-pasted rules from older model eras ("ALWAYS use CoT", "CRITICAL: YOU MUST...").
- Contradicting the auto-memory system or global Claude Code conventions.
- Mixing voice rules, coding rules, and environment rules without separation.

---

## Claude Code agent definitions

Agents live in `agents/` as `.md` files with YAML frontmatter.

### Constraints

- **The `description` field is the triggering mechanism.** It's what determines whether Claude delegates to this agent. Too vague → under-triggers (user manually invokes). Too broad → over-triggers (fires on unrelated requests).
- The `whenToUse` field typically contains 2–3 `<example>` blocks showing matching user requests.
- The `tools` list must match the agent's actual needs — extra tools waste context, missing tools block the agent.
- The body is the agent's system prompt. Every word ships on every invocation.

### Type-specific rubric additions

1. **Description starts with a verb or "Use when"?** Action-oriented descriptions trigger better than passive descriptions.
2. **Description is specific enough not to over-trigger?** Describe when to invoke and when not to.
3. **2–3 `<example>` blocks in `whenToUse`?** Each with user request + expected assistant response + commentary.
4. **Tools list is minimal but complete?** Grep through the body for tool references — any mentioned but not listed, or listed but not used?
5. **Body under ~200 lines?** Longer agents rarely out-perform tighter ones.
6. **Uses `${CLAUDE_PLUGIN_ROOT}` for plugin-relative paths?** Hardcoded paths break when the plugin moves.

### Common issues in agent audits

- Description reads like a marketing blurb ("Powerful assistant for...") instead of a trigger-phrase list.
- Missing `<example>` blocks — the single most effective triggering mechanism.
- Tools list bloat (asking for `Edit` and `Write` on a read-only analysis agent).
- Instructions that duplicate Claude's default behavior.

---

## Slash commands

Slash commands live in `commands/` as `.md` files with YAML frontmatter.

### Constraints

- User invokes explicitly via `/command-name`. No triggering concern.
- Frontmatter describes arguments and permissions.
- Body can mix prose instructions with bash blocks and file references.
- Executes once per invocation — there's no "run repeatedly" context.

### Type-specific rubric additions

1. **Frontmatter complete?** `description`, `argument-hint` (if args), `allowed-tools` if the command calls tools.
2. **Clear separation between instructions to Claude vs. bash scaffolding?** Mixing them confuses the model.
3. **`$ARGUMENTS` or named args documented?** The model needs to know what the user passed in.
4. **References other skills/agents cleanly via `${CLAUDE_PLUGIN_ROOT}`?**
5. **Idempotent?** Running it twice should produce a sensible result or refuse.

### Common issues in slash command audits

- Ambiguous argument handling.
- Inline bash that should be in a script.
- Assumes the user is in a specific directory without checking.
- Leaves working files in the project root with no cleanup.

---

## SKILL.md bodies

Skills live in `skills/{skill-name}/SKILL.md`.

### Constraints

- **Description is the triggering mechanism** (same as agents). Must be pushy enough to combat under-triggering but specific enough to avoid over-triggering.
- **Three-level progressive disclosure:** metadata always loaded → SKILL.md body loaded on trigger → references loaded on demand.
- **Body target under ~500 lines.** If bigger, split into references.
- Bundled scripts in `scripts/` can run without being loaded into context.

### Type-specific rubric additions

1. **Description lists trigger phrases explicitly?** Include verb phrases the user would actually say.
2. **Description is pushy without being generic?** "Use whenever the user mentions X, Y, or Z, even if they don't say 'skill'."
3. **Body has a "Contents" table pointing to references?**
4. **References organized by when to load them?** Not just alphabetically.
5. **Scripts in `scripts/` for deterministic/repetitive work?** If the skill describes a multi-step process that's the same every time, it's a script candidate.

### Common issues in SKILL.md audits

- Description under-triggers because it's too narrow.
- Description over-triggers because it's too broad ("data science skill").
- Body is 1000 lines with no references (everything loads every time).
- References loaded unconditionally in the body ("Always read X before proceeding") — defeats progressive disclosure.

---

## System prompts in production code

System prompts passed via the `system` parameter in API calls. Usually multi-line strings, f-strings, or imported from separate files.

### Constraints

- **Caching matters.** System prompts are typically the stable prefix of cached requests. Silent invalidators here break caching for everything downstream.
- **Runs on every request.** Every token costs on every call.
- **Versioned with the code.** Changes ship via deploy, not via conversation.

### Type-specific rubric additions

1. **No silent cache invalidators?** No `datetime.now()`, `uuid4()`, or unordered dict serialization in the prompt.
2. **Stable content first, volatile content last?**
3. **Role / identity stated up front?** "You are a helpful coding assistant specializing in Python" — even one sentence shifts behavior.
4. **Task structure matches long-context guidance?** Long docs at top, query at bottom.
5. **Deprecated parameter references?** Mentions of `budget_tokens`, `temperature` on 4.7 are flagged.
6. **Model identity declared?** For apps where the model needs to identify itself correctly: `"The current model is Claude Opus 4.7."`

### Common issues in production system prompt audits

- Time-based filler (`"Today is {date}"`) breaks caching unnecessarily.
- Unsorted `json.dumps()` for tool lists invalidates cache non-deterministically.
- System prompt tries to do work the system prompt can't do (per-request variables in the cached region).
- Reference to `budget_tokens` in comments or in the string.

---

## Jinja2 templates

Templates are the pre-render form of a prompt. Audit both the template and a rendered example.

### Constraints

- Variables in `{{ }}` are substituted at render time.
- `{% for %}` / `{% if %}` blocks produce different prompts on different invocations.
- A template can render differently per user / per request — the rubric applies to each variant, not just the template.

### Type-specific rubric additions

1. **Variable positions** — stable vars (role, system identity) appear before volatile vars (user query, session ID)?
2. **No silent invalidators in the cached region** — check for `{{ now() }}`, `{{ uuid4() }}`, `{{ request_id }}` early in the template.
3. **Conditional sections don't accidentally re-order** — a `{% if admin %}` block that moves content around between requests fragments the cache.
4. **Iteration output is deterministic** — `{% for item in items %}` where `items` is an unordered set will render differently across calls.
5. **Rendered prompt passes the normal rubric** — render it once with real vars and audit the result.

### Common issues in Jinja2 template audits

- Timestamp interpolation in the header.
- User ID / session ID in the first 100 tokens.
- Ordered list where the ordering is non-deterministic.
- Huge conditional blocks that generate wildly different prompts per code path.

### Worked example

**Before (template):**

```jinja
You are helping {{ user.name }} on {{ now() }}.
User ID: {{ user.id }}

<instructions>
{% for rule in rules %}
- {{ rule }}
{% endfor %}
</instructions>

{{ user_query }}
```

Issues:

- `{{ now() }}` and `{{ user.id }}` at the top invalidate the cache per-request and per-user.
- `rules` iteration order may be non-deterministic.
- Long-context best practice violated (query at bottom is good, but `instructions` should follow the long data).

**After:**

```jinja
You are a helpful assistant.

<instructions>
{% for rule in rules|sort %}
- {{ rule }}
{% endfor %}
</instructions>

{# ---- cache boundary ---- #}

Personalization:
- User: {{ user.name }}
- Current date: {{ now() }}

{{ user_query }}
```

The `|sort` filter ensures deterministic ordering. Volatile content moves below a logical cache boundary. The user query stays at the end per long-context guidance.

---

## Pydantic v2 / Zod tool descriptions

Tool descriptions are short natural-language strings the model reads to decide whether and how to call a tool. They live in:

- Pydantic v2: `Field(description="...")` on model fields, docstrings on model classes, `description` kwarg on tool decorators.
- Zod: `.describe("...")` on schema fields, tool description strings passed to `betaZodTool()` or similar.

### Constraints

- **Short.** 1–3 sentences each. Long descriptions bloat every tool-selection prompt.
- **High signal.** The model uses these to pick the right tool — imprecise descriptions cause wrong-tool selection.
- **Parameter descriptions matter more than people think.** The model uses them to know what values to fill in.

### Type-specific rubric additions

A good tool description is terse but *dense*. Short descriptions that answer only "what does this do" fail — the model needs enough information to pick this tool over its siblings, know when *not* to call it, and fill parameters correctly. Aim for 2–5 sentences per tool description, not 1.

1. **Answers what + when + when-not + what-it-returns?** The full picture. Missing any of the four is a common failure.
2. **Names sibling tools for disambiguation?** "Use `search_docs` for internal wiki pages; use `web_search` for public web content." Sibling redirects are the single highest-leverage addition for tool-selection accuracy.
3. **Flags destructive or irreversible actions up front?** A `delete_item` description should open with the destructive flag: "Permanently deletes an item. Not reversible. Prefer `archive_item` if the caller wants soft-delete."
4. **Includes anti-misuse warnings when common mistakes exist?** "Do NOT call this repeatedly in a loop — use `batch_create` instead." "Check with `search` first to avoid duplicates."
5. **Parameter descriptions follow what/format/default/example/when-to-deviate?** `Field(description="User's email. Format: RFC 5322. Example: foo@example.com. Case-insensitive match.")` beats `Field(description="The email")`.
6. **Enum values have semantic meaning in the description?** If `type: Literal["a", "b", "c"]`, each letter must have a meaning the model can map an intent to. Lists of opaque enum values produce random tool calls.
7. **JSDoc/docstring mirrors the runtime description?** Human reviewers and runtime LLM selection read different sources — keep both in sync.
8. **No filler?** Cut "A function that...", "This function is used to...", "Utility for...", and every variant. Start with the verb: "Returns X." "Creates Y." "Searches Z."

### Common issues in tool description audits

- One-word parameter descriptions that repeat the parameter name.
- Tool descriptions that start with "A function that..." — filler.
- Missing when-to-use guidance (model can't decide when to fire the tool).
- Enum values without semantic meaning in the description.

### Worked example (Pydantic v2)

**Before:**

```python
class SearchInput(BaseModel):
    query: str = Field(description="The query")
    limit: int = Field(description="Limit")

def search(input: SearchInput) -> list[dict]:
    """Search function."""
    ...
```

Issues:

- `description="The query"` says nothing.
- No docstring on `search` describing when to call it.
- `limit` description is meaningless.

**After:**

```python
class SearchInput(BaseModel):
    query: str = Field(
        description="Natural-language search query. Supports phrase matching with quotes and exclusions with minus sign."
    )
    limit: int = Field(
        default=10,
        description="Max number of results to return. Use 3-5 for quick answers, 10+ for research tasks."
    )

def search(input: SearchInput) -> list[dict]:
    """Search the internal knowledge base for documents matching the query.

    Use this for questions about company docs, policies, and internal wiki pages.
    For general web knowledge, use web_search instead.
    """
    ...
```

### Worked example (Zod)

**Before:**

```typescript
const searchTool = {
  description: "Search tool.",
  schema: z.object({
    query: z.string().describe("Query"),
    limit: z.number().describe("Limit"),
  }),
};
```

**After:**

```typescript
const searchTool = {
  description:
    "Search the internal knowledge base for documents matching the query. Use for company docs, policies, and wiki pages. Use web_search instead for general web knowledge.",
  schema: z.object({
    query: z
      .string()
      .describe(
        "Natural-language search query. Supports phrase matching with quotes and exclusions with minus sign."
      ),
    limit: z
      .number()
      .default(10)
      .describe("Max results. Use 3-5 for quick answers, 10+ for research tasks."),
  }),
};
```
