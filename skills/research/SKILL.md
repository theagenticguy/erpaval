---
name: research
description: >
  Multi-agent research skill. Decomposes a question into 2–4 parallel Opus 4.7
  research agents that write findings to per-agent Markdown files in real time,
  then runs a synthesis agent to merge by theme. Use when the user wants to
  research a topic, investigate something, find comparisons, compare options,
  learn about a technology, do a literature review, or understand a domain.
arguments:
  - name: topic
    description: The research topic or question.
    required: false
user_facing: true
---

## Contents

| Reference                         | When to load                                        |
| --------------------------------- | --------------------------------------------------- |
| `references/orchestrator.md`      | Running `/research <topic>` — the full 5-phase flow |
| `references/write-protocol.md`    | Copy verbatim into every agent prompt               |
| `references/search-strategies.md` | Tool inventory, priority order, query patterns      |
| `templates/agent-skeleton.md`     | Per-agent Markdown file skeleton                    |
| `templates/synthesis-skeleton.md` | Synthesis output skeleton                           |

# Research

A single-mode research orchestrator. Runs inside a forked subagent so the main conversation stays clean. Decomposes the question, launches 2–4 Opus 4.7 agents in parallel with a file-first write protocol, monitors progress by reading their files, recovers stuck agents, and then runs one synthesis pass to produce the final brief.

## How it works

Read `references/orchestrator.md` and follow its phases. The short version:

1. **Plan** — decompose into 2–4 workstreams with non-overlapping scopes and 3–6 sections each. Present plan. Wait for approval.
2. **Skeletons** — create `research/{slug}/` and write a file per agent plus a synthesis file, each starting with `Status: IN PROGRESS`.
3. **Launch** — fire all research agents in one message as parallel `Agent` calls with `model: "opus"` and `run_in_background: true`.
4. **Monitor** — escalating check-ins (30s → 2m → 5m). `wc -l` per file to track progress. If an agent's line count stalls across two checks, launch a fresh `Agent` with the existing file state and a "skip these sections" prompt.
5. **Synthesize** — one foreground `Agent` reads every agent file and writes `synthesis.md` with themed findings, contradictions, confidence, gaps, next steps, and deduplicated sources.

## Write discipline

Every agent prompt carries the write protocol verbatim from `references/write-protocol.md`: one search or fetch → edit the file with findings → next search. This keeps partial progress on disk where it survives timeouts and 403 errors.

## Citation conventions

- Inline Markdown links with publication date when available: `[Source Name, 2026-04-15](https://url.com)`.
- Citations for the same point are ordered newest-first.
- Primary focus on the last 6 months. Reach further back only for canonical sources or when recent literature is thin.
- Synthesis builds a deduplicated `Sources` section at the end, newest-first.

## Cost note

All research and synthesis agents run as Opus 4.7 in parallel. Expect significant token usage on a full run — 2–4 parallel Opus agents plus one synthesis pass. Worth it for the quality, but know what you're ordering.
