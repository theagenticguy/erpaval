---
task_id: "{{ task_id }}"
ac_source: {{ ac_id }}
agent_name: {{ agent_name }}
parallel_safe: {{ true | false }}
blocked_by: [{{ T-AC-X-Y, ... }}]
status: IN_PROGRESS
---

# Task {{ task_id }} — {{ title }}

<write_protocol>
Your task packet file is the single source of truth for what you've done, decided, and verified. Edit it after every meaningful step, before starting the next one. Partial progress written to disk survives subagent timeouts, mid-turn interrupts, and orchestrator context pressure; state held in working memory does not.

The rhythm is: one action → edit the packet with the outcome → next action. One exchange at a time.

Work through your sections in numbered order. For each section:

1. Do one unit of work — read a file, write a code change, run a check, capture a finding.
2. Edit this file under that section with what happened — the exact files touched, the check output, the decision made, any surprises.
3. If the section needs more depth, do another unit and edit again.
4. Move to the next section only after the current one has real content.

If a check fails (lint, type, test, semgrep): write the failure here, then fix, then edit again with the fix. Keep the file ahead of your working memory at all times.

**Cite every code change with file:line.** "Added `verify_pkce` at `src/auth/oauth_service.py:142-168`" beats "Added the PKCE helper."

When every section has real content and every success criterion is checked off, change `status: IN_PROGRESS` in the frontmatter to `status: COMPLETE`.
</write_protocol>

## 1. Objective

{{ one-sentence objective }}

## 2. Scope

Files to create:

- {{ path }}

Files to modify:

- {{ path }}

Do not touch: {{ everything else }}

## 3. EARS requirement

{{ paste AC text verbatim — Ubiquitous / Event-driven / State-driven / Optional / Unwanted behavior }}

## 4. Architecture context

{{ excerpted from CP-EXPLORE — patterns, conventions, error handling, DI, test style }}

## 5. API contracts

{{ signatures, types, interfaces the work must match }}

## 6. Conventions

{{ from CP-EXPLORE — naming, imports, async discipline, error types }}

## 7. Dependencies

{{ from CP-RESEARCH — library names, pinned versions, known pitfalls }}

## 8. Prior lessons

{{ paths from CP-RECALL — `.erpaval/solutions/<category>/<slug>.md` }}

## 9. Success criteria

Baseline (non-negotiable):

- `uvx ruff check <files>` exits 0
- `uvx ruff format --check <files>` exits 0
- `uv run pyright <files>` exits 0
- `uv run pytest <test-path>` exits 0

Task-specific:

- {{ verifiable check 1 }}
- {{ verifiable check 2 }}

## 10. Anti-goals

- No refactoring outside scope
- No new dependencies
- No new abstractions "for future use"
- If a prerequisite is missing, report back instead of improvising

---

## Work log

{{ the agent fills this section section-by-section per the write protocol }}

## Validation

{{ checks run, outputs pasted, any fixes applied }}

## Summary

{{ one paragraph — what changed, where, why the approach was chosen }}
