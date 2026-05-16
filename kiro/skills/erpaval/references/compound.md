# Compound + Recall — persist and surface lessons

The tail of the loop. After merge, extract lessons from the session and persist them in a grep-retrievable layout under `.erpaval/solutions/`. At session start and again pre-Act, retrieve relevant lessons and inject them into context packets. Compound writes; Recall reads — one skill, two operations, tied together by the `erpaval-recall.py` tool.

The pattern is borrowed from EveryInc, Lavra, dspy-compounding, iliaal, and tajmahal226 compound-engineering plugins — all converge on dual-track markdown + YAML frontmatter + grep retrieval.

---

## Dual-track schema

Two tracks — `bug` for encountered-and-resolved failures, `knowledge` for non-obvious patterns worth preserving. The full category list with descriptions lives in `references/solution-categories.yaml` — single source of truth, read by `erpaval-new.py` at scaffold time.

| Track         | Body content                                                                   |
| ------------- | ------------------------------------------------------------------------------ |
| **bug**       | A failure was encountered and resolved. Record symptoms + root cause + fix.    |
| **knowledge** | A non-obvious pattern was discovered. Record applies_when + pattern + example. |

## Canonical file layout

Directory structure matches `solution-categories.yaml` — `erpaval-new.py` scaffolds exactly these at session-zero:

```text
.erpaval/
  solutions/
    <one folder per entry in solution-categories.yaml>
  brainstorms/
  specs/
  INDEX.md
```

### Slug rules

- Kebab-case, no dates in any filename.
- `brainstorms/` and `specs/` prefix with `NNN-` (sequence) because multiple drafts of the same feature can coexist.
- `solutions/` filenames have no sequence prefix — each slug is globally unique.

### Why no dates

Filenames use sequence numbers or bare slugs. Dates create false precision — lessons age by relevance, not calendar time. Sequence numbers stay stable when files are renamed. `git log` already provides timestamps when needed.

---

## Bug-track frontmatter

```yaml
---
title: <short descriptive title>
track: bug
category: build-errors | test-failures | deploy-errors
module: <path or package>
component: <library or subsystem>
severity: low | medium | high | critical
tags: [list, of, searchable, tags]
symptoms:
  - <observable symptom 1>
root_cause: |
  <multi-line explanation>
resolution_type: config-change | code-fix | dependency-upgrade | workaround
applies_when:
  - <condition>
---
```

Body sections: `# Fix` (resolution steps) and optional `# Why this matters`.

## Knowledge-track frontmatter

```yaml
---
title: <short descriptive title>
track: knowledge
category: architecture-patterns | best-practices | conventions | api-patterns
module: <path or package>
component: <library or subsystem>
severity: info
tags: [list, of, searchable, tags]
applies_when:
  - <condition>
pattern: |
  <multi-line description of the pattern>
example_files:
  - <path>
---
```

Body sections: `# Why this matters` and optional `# Example`.

---

## CL-LESSONS — novelty + reusability filter

Not every session produces a lesson. `CL-LESSONS` judges each candidate:

1. **Novel** — grep `.erpaval/solutions/` for overlapping tags + title. If a match exists, merge (update existing) or skip.
2. **Reusable** — likely to apply to a future session? One-off hacks with no transfer value are not lessons.

Write only when both are true. See `classifiers.md` for the full prompt.

---

## Compound — operating sequence

Runs post-merge as the final ERPAVal phase. Can also run ad-hoc when the user wants to force-extract lessons mid-session or when a session ended without formal Compound (e.g., Ctrl+C'd a long-running flow).

```text
1. Verify session state:
   - .erpaval/sessions/<id>/ exists
   - CP-VALIDATION.yaml shows resolution

2. Read the full session trace (all packets + cycle counts from packet `status:` history).

3. Run CL-LESSONS (model: opus) — returns candidate lessons.

4. For each candidate:
   a. Grep solutions/ for conflicts (title, tag overlap)
   b. If novel + reusable: write solutions/<category>/<slug>.md
   c. If mergeable into existing: edit the existing lesson instead

5. Update .erpaval/INDEX.md with category counts + recent additions.

6. Ensure root AGENTS.md has a pointer to .erpaval/INDEX.md (add if missing).

7. Write sessions/<id>/lessons.yaml summarizing what was extracted.
```

### Scope boundaries

- **Only from merged work** — Gate-2-rejected sessions haven't proven the lesson yet.
- **Add signal beyond the project's wiki** — duplicating docs erodes trust in `solutions/`.
- **Redact paths, env hints, stderr tails** — the schema validator rejects these on write; summaries can leak context that raw dumps don't.

### Stop-hook nudge — advisory under Kiro

Unlike Claude Code (where the `Stop` hook can re-prompt the model with `decision: "block"` plus a reason), Kiro `stop` hooks **cannot block-and-re-prompt the model**. Exit code 2 is not honored on `stop`; STDERR is shown as a warning, STDOUT is folded into context. This means the Compound nudge that fires when the six gates hold is **advisory only**:

- The user (or the orchestrator agent on the next conversational turn) reads the warning and explicitly drives Compound — for example by typing `/erpaval` (the skill auto-exposes a slash command), invoking the skill via NL ("run Compound now"), or calling the Compound-track procedure inline.
- The `.erpaval/sessions/.nudged` ledger and the `HookState.compound_nudged` flag both remain — they ensure the warning fires exactly once per session.
- If the warning is missed, Compound can still be triggered ad-hoc later via `/erpaval` or by re-opening the session.

Treat the nudge as a reminder, not a forced re-prompt. The methodology gate (six conditions) still defines when Compound *should* run; only the enforcement channel changes.

---

## Discoverability — INDEX.md + AGENTS.md pointer

Example `INDEX.md` (counts and filenames illustrative):

```markdown
# ERPAVal lessons index

Lessons from prior ERPAVal sessions. The orchestrator agent reads this at
session start and greps `.erpaval/solutions/**` for relevant lessons before
starting work.

## By category

- **build-errors/** — N lessons
- **test-failures/** — N lessons
- **architecture-patterns/** — N lessons
- **best-practices/** — N lessons
- **conventions/** — N lessons
- **api-patterns/** — N lessons

## Recent additions

- [<slug-1>](solutions/<category>/<slug-1>.md) — bug-track, <severity>
- [<slug-2>](solutions/<category>/<slug-2>.md) — knowledge-track
```

Root `AGENTS.md` (Kiro project memory) gets a one-block pointer (add if missing, leave alone if present):

```markdown
## Prior lessons

Before making non-trivial changes, grep `.erpaval/solutions/**.md` for
lessons matching your task's module, tags, or problem_type. See
`.erpaval/INDEX.md` for the category summary.
```

---

## Recall — how lessons feed the next session

Recall is the retrieval half. Invoked in three cases:

1. **Session start** — the `agentSpawn` hook on the `erpaval-orchestrator` agent (`kiro/hooks/kiro_session_start_bootstrap.py`) emits category counts to STDOUT, which Kiro folds into the conversation context. No-ops outside projects with `.erpaval/solutions/`. Guarded by `HookState` so it fires once per session.
2. **Pre-Act** — the orchestrator runs `erpaval-recall.py search` per task during Plan → Act, populating each packet's Prior Lessons section.
3. **Mid-session** — when the orchestrator agent encounters a new sub-problem and wants to check whether prior sessions hit it.

Skip when `.erpaval/solutions/` is absent. The tool returns empty with `exit 0` and a single-line note: `no prior lessons — this is a new .erpaval project or solutions/ is empty`. Treat as normal, not an error.

### Retrieval scoring

```text
score = 3 × (module match) + 1 × (tag overlap count) + 0.5 × (recency rank)
```

- **Module match** — path-boundary match between query and lesson `module` field: equal, query is a parent of lesson (e.g. `src` matches `src/auth`), or lesson is a parent of query (e.g. `src/auth/oauth_service.py` matches `src/auth`). Prevents `src/a` from matching `src/auth`.
- **Tag overlap** — count of intersection between query tags and lesson tags.
- **Recency rank** — among matched lessons only, rank by `mtime` descending and normalize to `[0, 1]` (newest = 1.0, oldest = 0.0). Tiebreaker multiplied by 0.5 so module + tag signals dominate.

Return top N (default 5). The formula lives in `scripts/erpaval-recall.py` — update the Python when the formula changes.

### Invocation

From the orchestrator:

```bash
uv run ${ERPAVAL_HOME}/skills/erpaval/scripts/erpaval-recall.py \
  --module src/auth \
  --tags oauth,pkce,pytest \
  --limit 5
```

Output: JSON array of `{path, title, track, score, matched_on}`.

From inside an Act context packet — the orchestrator lists matched lesson paths under the packet's Prior lessons section:

```markdown
## 8. Prior lessons

- .erpaval/solutions/api-patterns/oauth-state-param-validation.md
- .erpaval/solutions/test-failures/pytest-asyncio-scope-mismatch.md
```

The subagent reads each lesson's frontmatter and body as part of the task's guidance.

### Scope

- **Ranking**: grep + YAML frontmatter. At personal / small-team scale this beats embedding similarity on latency and simplicity; revisit past ~500 lessons.
- **Injection**: per Act task, using task-specific tags. Global injection floods unrelated contexts and dilutes signal.
- **Index**: grep `.erpaval/solutions/` fresh each call. Corpus is small enough that a maintained index would add cost without measurable win.

---

## Citations

- EveryInc/compound-engineering-plugin — 15.4k stars, dual-track schema canonical
- roberto-mello/lavra — `.lavra/memory/knowledge.jsonl` with 6 typed records
- Strategic-Automation/dspy-compounding-engineering — `.knowledge/*.json` + Qdrant
- iliaal/compound-engineering-plugin — docs/brainstorms, docs/solutions, docs/audit
- tajmahal226/compound-engineering-plugin — similar directory conventions
