# Research Orchestrator

The orchestrator runs inside a forked subagent so the main conversation stays clean. It decomposes the user's question into 2–4 parallel Opus 4.7 research agents, monitors them by reading their output files, recovers any that stall, and then runs a single synthesis agent to produce the final brief.

---

## Inputs

- `{{ topic }}` — the research question, parsed from `$ARGUMENTS`.
- `${CLAUDE_PLUGIN_ROOT}/skills/research/references/write-protocol.md` — the write-protocol block that gets copied into every agent prompt.
- `${CLAUDE_PLUGIN_ROOT}/skills/research/references/search-strategies.md` — the 8-tool inventory and priority table.
- `${CLAUDE_PLUGIN_ROOT}/skills/research/templates/agent-skeleton.md` — the per-agent file skeleton.
- `${CLAUDE_PLUGIN_ROOT}/skills/research/templates/synthesis-skeleton.md` — the synthesis file skeleton.

---

## Phase tracking

Before Phase 1, create 5 todo items — one per phase (Plan, Skeletons, Launch, Monitor, Synthesize). During Launch, additionally `TaskCreate` one item per research agent and flip each to `completed` when its output file shows `Status: COMPLETE`. Flip the phase item to `in_progress` on entry, `completed` on exit. Progress stays visible mid-run without polling agent output streams.

---

## Phase 1 — Plan

Read the research question. If `$ARGUMENTS` is empty, ask the user: "What would you like us to research? One sentence is enough to start."

Decompose the question into **2–4 non-overlapping workstreams**. Each workstream gets:

- A clear, one- or two-sentence scope.
- 3–6 specific sections the agent must fill.
- An output file path: `research/{{ slug }}/{{ agent-name }}.md`.

`{{ slug }}` is a kebab-case slug derived from the topic. Trim to ~40 characters.

Also plan the synthesis agent. It runs after every research agent completes and writes `research/{{ slug }}/synthesis.md`.

Summarize the plan inline before launching — one short block so the user can see what's about to run, then continue immediately to Phase 2. No approval gate; research is reversible and the user already committed by invoking `/research`.

```markdown
## Research Plan: {{ topic }}

### Agent 1: {{ name }}

**Scope:** {{ 1–2 sentences }}
**Sections:**

1. {{ section }}
2. {{ section }}
3. {{ section }}

**Output:** `research/{{ slug }}/{{ agent-name }}.md`

### Agent 2: {{ name }}

…

### Synthesis Agent

**Runs after:** All research agents complete.
**Output:** `research/{{ slug }}/synthesis.md`
```

Use `AskUserQuestion` only when scope ambiguity would send the research in the wrong direction entirely (e.g., "evaluate vector databases" — for what workload, scale, latency budget?). One targeted question, then proceed with the answer.

---

## Phase 2 — Skeleton files

Once the user approves:

1. Create the output directory: `mkdir -p research/{{ slug }}/`.
2. For each research agent, write its skeleton file from `templates/agent-skeleton.md` with the agent's scope title and numbered section names filled in. The skeleton already contains the write protocol verbatim.
3. Write the synthesis skeleton from `templates/synthesis-skeleton.md` in the same directory.

All skeleton files start with `Status: IN PROGRESS` — agents flip their own file to `COMPLETE` when done.

---

## Phase 3 — Launch research agents

Launch every research agent in a **single message** using multiple `Agent` tool calls. All launches are parallel.

Each `Agent` call uses:

- `subagent_type: "general-purpose"`
- `model: "opus"`
- `run_in_background: true`
- `description`: 3–5 word summary, e.g. "Market sizing research"
- `prompt`: built from the template below

### Agent prompt template

```text
You are a research agent. Work the scope below and write findings to the output file as you go.

<scope>
Research question: {{ topic }}

Your workstream: {{ agent_name }}
Your scope: {{ one_or_two_sentence_scope }}

Sections to complete, in order:
1. {{ section_1 }}
2. {{ section_2 }}
3. {{ section_3 }}
...
</scope>

<output>
Output file: {{ absolute_path_to_agent_markdown }}

The file already exists with a skeleton and the write protocol embedded at the top. Edit it in place — don't overwrite.
</output>

<preamble>
Before your first search, run `date +"%Y-%m-%d"` to get today's date. Include the current year in your search queries — e.g., `best python ORM 2026`, not `best python ORM`.
</preamble>

<write_protocol>
{{ paste write-protocol.md verbatim — the block inside its <write_protocol> tags }}
</write_protocol>

<search_strategy>
Load MCP search tools with ToolSearch before using them. The full tool inventory and priority-by-research-type table lives at:
${CLAUDE_PLUGIN_ROOT}/skills/research/references/search-strategies.md

Read that file before your first search. Match the tool to the section you're working on.
</search_strategy>

<quality_bar>
- Every quantitative claim carries an inline URL with the source's publication date when available.
- Citations for the same point are ordered newest-first.
- Primary focus: sources from the last 6 months. Older sources are fine when canonical or when recent coverage is thin — flag the date either way.
- Findings are specific (numbers, quotes, named sources), not generic paraphrase.
</quality_bar>
```

After launching, tell the user how many agents are running and list their output file paths.

---

## Phase 4 — Monitor

Use escalating check-in intervals: ~30s → 2m → 5m → every 5m afterward.

At each check-in:

1. Run `wc -l` across every agent file in one Bash call.
2. Read specific files only when you need to see which sections are populated.
3. Report compactly. Example:

```text
Check-in #2:
- Agent 1 (Market sizing): 118 lines, sections 1–3 populated, section 4 in progress
- Agent 2 (Technical):      82 lines, sections 1–2 populated, section 3 in progress
- Agent 3 (Regulatory):    COMPLETE (184 lines)
```

Continue until every agent shows `Status: COMPLETE` at the top of its file.

### Stuck-agent recovery

<stuck_agent_recovery>
An agent is stuck when its file's line count is identical across two consecutive check-ins. Don't wait for it to self-correct — at that point it's usually in a fetch loop against a blocked URL and won't escape on its own.

Recovery steps:

1. Read the stuck agent's file to see which sections already have real content.
2. Launch a fresh `Agent` with:
   - A prompt that lists the sections already complete and instructs the new agent to skip them.
   - An instruction to resume from the first incomplete section and append to the existing file.
   - A slightly tightened write-protocol reminder: "If a URL returns an error, write what you have before trying the next one — don't chain alternative URLs without an edit between them."
3. The original backgrounded agent will finish or timeout on its own; its writes stopped updating the file so its continued existence is harmless.
4. Resume normal check-ins on the new agent.
   </stuck_agent_recovery>

---

## Phase 5 — Synthesize

Once every research agent shows `Status: COMPLETE` (or the user decides to proceed with what's available), launch one synthesis `Agent`.

Synthesis runs **foreground** — the user waits for this one. Use:

- `subagent_type: "general-purpose"`
- `model: "opus"`
- `run_in_background: false`

### Synthesis agent prompt template

```text
You are a synthesis agent. Read every research agent file and write a single coherent synthesis document.

<inputs>
Research question: {{ topic }}

Agent files to read:
- {{ absolute_path_1 }}
- {{ absolute_path_2 }}
- {{ absolute_path_3 }}
</inputs>

<output>
Output file: research/{{ slug }}/synthesis.md

The file already exists with a skeleton and a synthesis protocol block at the top. Edit it in place — don't overwrite.
</output>

<synthesis_discipline>
Read every input file in full before drafting. Merge findings by theme, not by agent. Surface contradictions where researchers disagreed. Label confidence honestly.

Write section by section, editing the synthesis file after each input file you process. Partial progress written to disk survives termination; plans held in working memory do not.

Quote or paraphrase findings with the inline URL carried over from the agent file. Deduplicate sources in the final Sources section. Order citations newest-first within each point.

When every section has real content, change the file's Status line from IN PROGRESS to COMPLETE.
</synthesis_discipline>

<required_sections>
- Executive Summary (3–5 bullets answering the question directly)
- Key Findings by Theme (grouped by theme, not by agent)
- Contradictions and Tensions
- Confidence Assessment (per-claim High/Medium/Low with reasoning)
- Gaps and Limitations
- Recommended Next Steps
- Sources (deduplicated, newest-first)
</required_sections>
```

When synthesis completes, read `research/{{ slug }}/synthesis.md` and present inline:

```markdown
## Research Complete: {{ topic }}

{{ 1–2 sentence central finding }}

### Output

- `research/{{ slug }}/synthesis.md` — full synthesis
- `research/{{ slug }}/*.md` — per-agent research files

### Key Findings

{{ paste the Executive Summary bullets }}

### Confidence

{{ 1 sentence overall confidence }}

### Gaps

{{ top 2–3 gaps from the Gaps section }}
```

Offer the user: follow-up questions on any finding, a narrower re-run, or handoff to `/draft-prd` or another skill that consumes research.
