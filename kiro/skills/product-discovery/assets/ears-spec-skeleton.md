---
slug: <slug>
sequence: NNN
hmw_source: brainstorms/NNN-<slug>-requirements.md  # if HMW was run
---

**Status:** IN PROGRESS

<write_protocol>
{{ paste ${ERPAVAL_HOME}/skills/product-discovery/references/write-protocol.md verbatim }}
</write_protocol>

## User Story 1 — <title>

### Acceptance Criteria

AC-1-1 [P]
Ubiquitous: The <subject> shall <response>.

AC-1-2 [P]
Ubiquitous: The <subject> shall <response>.

AC-1-3
Dependencies: AC-1-1, AC-1-2
Event-driven: When <trigger>, the <subject> shall <response>.

AC-1-4
Dependencies: AC-1-3
Unwanted behavior: If <trigger>, then the <subject> shall <response>.

## User Story 2 — <title>

### Acceptance Criteria

AC-2-1 [P]
State-driven: While <precondition>, the <subject> shall <response>.

AC-2-2
Dependencies: AC-2-1
Event-driven: When <trigger>, the <subject> shall <response>.

---

## Instructions

Seed this file before launching the `ears-specifier` subagent. The agent fills it in place per the write protocol.

- Each AC ID is stable: `AC-<story>-<n>` where `<story>` is the 1-indexed user story and `<n>` is the AC number within that story.
- `[P]` means parallel-safe — AC can run in an isolated worktree with other `[P]` ACs; no file overlap expected.
- `Dependencies: AC-X-Y, AC-X-Z` lists ACs that must complete first.
- When uncertain about overlap, prefer `Dependencies:` over `[P]` — a missed dependency corrupts the task graph; a missed `[P]` only costs parallelism.

The five EARS templates (plus Complex) — see `${ERPAVAL_HOME}/skills/product-discovery/references/roles/ears-specifier.md`:

```text
Ubiquitous:        The <system> shall <response>.
Event-driven:      When <trigger>, the <system> shall <response>.
State-driven:      While <precondition>, the <system> shall <response>.
Optional feature:  Where <feature is included>, the <system> shall <response>.
Unwanted behavior: If <trigger>, then the <system> shall <response>.
Complex:           While <pre>, when <trigger>, the <system> shall <response>.
```

When every AC is written and every `[P]` / `Dependencies` annotation is set, flip `Status: IN PROGRESS` → `Status: COMPLETE`. The Plan phase derives `tasks.md` mechanically; hand-edits to `tasks.md` are destroyed on regeneration — edit `spec.md` instead.
