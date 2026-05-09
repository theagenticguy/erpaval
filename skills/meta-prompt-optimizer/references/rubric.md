# Prompt audit rubric

This is the scoring contract — both the `meta-prompt-optimizer` skill and the `prompt-critic` agent use this exact rubric so their outputs are comparable. Do not improvise new rubric items.

Each item scores **Pass**, **Needs work**, or **Rethink**. Cite evidence (line numbers, specific phrases) for anything less than Pass.

---

## Category 1: Directness and clarity

### 1.1 Specific and verifiable

The instruction describes an observable outcome. A third party reading the prompt could tell whether the model followed it.

- **Pass:** "Return a JSON object with fields `name`, `email`, `plan`."
- **Needs work:** "Format the output cleanly."
- **Rethink:** "Be helpful."

### 1.2 Imperative voice

Instructions use imperative verbs directed at the model. Declarative descriptions of desired behavior ("the response should be…") work too. Hedged, advisory language weakens the signal.

- **Pass:** "State conclusions directly."
- **Needs work:** "It would probably be good to state conclusions directly if possible."
- **Rethink:** "I'd like you to maybe try stating conclusions directly."

### 1.3 Passes the golden rule

Golden rule (Anthropic's phrasing): would a colleague with no context understand what's being asked?

Flag if the prompt assumes knowledge the model doesn't have (internal jargon, unstated conventions, implicit definitions).

### 1.4 Single-purpose sentences

One instruction per sentence. Run-on sentences that bundle multiple rules make it unclear which takes precedence.

---

## Category 2: Framing and tone

### 2.1 Positive framing

Anthropic's guidance: "Tell Claude what to do instead of what not to do."

Count the negative ("avoid X", "don't Y", "NEVER Z") constructions. If more than ~30% of rules are negative, flag the prompt for rewriting.

- **Pass:** "Write assertions as single positive statements."
- **Needs work:** "Avoid contrastive statements."
- **Rethink:** "NEVER use contrastive statements, don't hedge, avoid overclaiming, never shout, don't…" (all-negative ladder)

### 2.2 Motivation after non-obvious rules

Rules that explain *why* generalize better than rules without context.

- **Pass:** "Use structured formats for state data (JSON files like `tests.json`) — it helps the model track state across multi-session work."
- **Needs work:** "Use structured formats for state data."

Not every rule needs motivation — obvious ones don't. Flag when non-obvious rules lack any.

### 2.3 Emphasis used sparingly

Reserve `**IMPORTANT:**`, `**YOU MUST:**`, all-caps section headers, and "CRITICAL" for 1–2 high-cost rules. Blanket shouting over-triggers 4.x models.

- **Pass:** One or two emphasized rules in a long prompt.
- **Needs work:** Three or more.
- **Rethink:** Every section header is in all caps; every rule starts with "CRITICAL" or "YOU MUST."

### 2.4 No contrastive framing

Contrastive pairs ("not X — it's Y", "This isn't Z, it's W") add verbal noise. Flag them.

### 2.5 No hedging in the prompt itself

Prompts that use "likely / probably / maybe / might" teach the model to hedge. State conclusions directly.

### 2.6 Uncertainty handling follows ground → propose → confirm

When the prompt addresses what the model should do when it's unsure, the right shape is a three-step escalation: ground first (tools, search, code reading), then propose a specific call with the evidence, then ask the user to verify irreversible or thin-evidence calls. Flag prompts that either:

- License hallucination — "make your best guess," "just pick one."
- Block autonomy — "always ask the user before doing anything," "if unsure, stop and wait."

Both fail. The first teaches fabrication; the second blocks the model from resolving uncertainty it could have resolved itself.

- **Pass:** Prompt instructs the model to ground first, state its call, and ask only for irreversible or thin-evidence actions.
- **Needs work:** Prompt jumps straight to "ask the user" without encouraging grounding.
- **Rethink:** Prompt tells the model to guess, or to hide uncertainty.

See Pattern 14 in `rewriting-patterns.md` for the canonical shape.

---

## Category 3: Structure

### 3.1 Explicit scope

Opus 4.7 won't generalize from one item to others. Look for instructions that assume Claude will apply them broadly without being told.

- **Pass:** "Apply this formatting to every section, not just the first."
- **Needs work:** "Use this format." (ambiguous scope)

### 3.2 XML tags when mixing content types

When a prompt bundles instructions + context + examples + input, they should be delimited — ideally with XML tags. Pure markdown works for simple prompts but gets ambiguous as complexity grows.

Flag if a prompt has long interleaved sections without any structural markers.

### 3.3 Stable-first ordering (caching)

For prompts served via API with prompt caching enabled, stable content (system identity, role, fixed instructions) must precede volatile content (per-request context, user input, timestamps). If caching is in play and the prompt interpolates a timestamp or UUID early, that silently invalidates the cache.

Skip this check for CLAUDE.md, agent definitions, and skills (no caching concerns).

### 3.4 Deprecated parameter references

Flag mentions of:

- `budget_tokens` (deprecated on 4.6, removed on 4.7 — use adaptive thinking + effort)
- `temperature`, `top_p`, `top_k` on Opus 4.7 (removed)
- Assistant-message prefill on the last turn (deprecated on 4.6+)
- Manual thinking mode on 4.7 (only adaptive is supported)

These are factual errors in 4.7-targeted prompts.

### 3.5 Self-evident content

Rules that describe default model behavior add noise without adding signal. "Be helpful," "give accurate answers," "think before responding" — all filler. Flag them for removal.

### 3.6 Length appropriate to type

Each target type has length expectations:

- **CLAUDE.md**: under 200 lines (auto-load ceiling).
- **Agent description**: 2–4 sentences for triggering + 2–3 `<example>` blocks for the body.
- **Tool description (Pydantic/Zod)**: 1–3 sentences describing what, when, and what parameters mean.
- **System prompt**: as long as needed, but every line should earn its place.

---

## Category 4: Type-specific fitness

Load the section of `references/target-types.md` matching the prompt's type, then apply the checks there. Examples:

**CLAUDE.md checks:**

- Under 200 lines?
- Every rule earns its place ("would removing this cause Claude to make mistakes?")
- No contradictions between rules?
- Conditional or path-scoped content factored into `.claude/rules/` or imports?

**Agent definition checks:**

- Description is pushy enough to trigger but specific enough not to over-trigger?
- Has 2–3 `<example>` blocks showing when to invoke vs not?
- Tools list matches the agent's actual needs?

**Slash command checks:**

- Frontmatter complete (description, args if needed)?
- Clear separation between the command's instructions to Claude and any bash scaffolding?

**SKILL.md checks:**

- Description is pushy (combat under-triggering) and specific (what + when)?
- Body under ~500 lines with references for deep dives?
- References organized by when to load them?

**Jinja2 template checks:**

- Variables at stable positions (start of prompt) vs volatile positions (end)?
- No silent cache-invalidators (`{{ now() }}`, `{{ uuid4() }}` in cached region)?
- Rendered output reviewed, not just the template?

**Pydantic v2 / Zod tool description checks:**

- Answers what + when + when-not + what-it-returns?
- Names sibling tools for disambiguation ("use X for A, use Y for B")?
- Flags destructive or irreversible actions up front?
- Includes anti-misuse warnings when common mistakes exist?
- Parameter descriptions follow what/format/default/example/when-to-deviate?
- Enum values have semantic meaning (not opaque letters)?
- No filler ("A function that...", "This function is used to...")?
- Dense but concise — 2–5 sentences per tool, not 1.

---

## Scoring the whole prompt

After all individual rubric items, give the prompt an overall rating:

| Rating            | Criteria                             |
| ----------------- | ------------------------------------ |
| **Strong**        | All items Pass, at most 1 Needs work |
| **Needs polish**  | 2–4 items Needs work, 0 Rethink      |
| **Needs rewrite** | Any Rethink, or 5+ Needs work        |

## Producing the audit report

Use this structure verbatim:

```markdown
## Audit: [prompt identifier]

**Overall rating:** Strong / Needs polish / Needs rewrite

### Category 1: Directness and clarity

| Check                        | Score      | Evidence             |
| ---------------------------- | ---------- | -------------------- |
| 1.1 Specific and verifiable  | Pass/NW/RT | [finding + line ref] |
| 1.2 Imperative voice         | …          | …                    |
| 1.3 Golden rule              | …          | …                    |
| 1.4 Single-purpose sentences | …          | …                    |

### Category 2: Framing and tone

[same shape]

### Category 3: Structure

[same shape]

### Category 4: Type-specific fitness

[checks from target-types.md for the relevant type]

### Top priorities to fix

1. [Highest-leverage change]
2. [Next]
3. [Next]
```

The priorities list matters most — it's what the user acts on. Put it last so it reads as the takeaway.
