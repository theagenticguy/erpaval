# Orchestrator — phase-by-phase runbook

How the orchestrator (a Kiro CLI session running the `erpaval-orchestrator` agent) runs an ERPAVal session using Kiro's two execution primitives: **filesystem-driven task packets** (Markdown files at `.erpaval/sessions/<id>/tasks/T-AC-X-Y.md` carrying `status:` frontmatter) for gate state, with Kiro's `/todo` slash command mirroring progress for the user, and the **`subagent` built-in tool** for subagent execution. Adapts the research/ultraplan file-first pattern to a stateful, multi-phase development loop: every subagent edits a per-task Markdown packet section-by-section, and the orchestrator monitors progress by reading those files (`wc -l` for stuck detection plus the Ctrl+G crew monitor for live state), not by polling the subagent's output stream.

> **Dispatch contract — NL is the orchestrator's primitive, `/spawn` is the user's.** The canonical way the orchestrator delegates is in-chat natural language: `> Use the erpaval-explorer agent to <task>`. That fires the `subagent` built-in tool, which is bounded to the parent's task graph, capped at 4 concurrent, and returns via the **built-in `summary` tool**. `/spawn` is a *user-driven* command that starts a fresh long-running session for the human to revisit via `/chat resume` or Ctrl+G — it is **not** the orchestrator's delegation channel. Don't confuse them. Per `kiro.dev/docs/cli/chat/subagents/`: *"`/spawn` is a user-driven command that starts a fresh long-running session you can return to later."*

> **Return contract — every subagent must call `summary` as its final act.** Kiro subagents have exactly one return path: the auto-attached built-in `summary` tool. Writing output to a packet on disk is necessary but **not sufficient** — without a `summary` call the parent receives nothing and the dispatch reads as "No result". Every spawn prompt must end with: `Final step: call the built-in`summary`tool with a 1-2 paragraph result; return nothing else.`

Terms like `CP-*`, `CL-*`, `T-AC-X-Y`, Wave are defined in `glossary.md`. The graph is in `flow.md`.

---

## Division of labor

- **Per-task Markdown packets hold authoritative state.** "What's next, what's blocked, what's stuck" — answer by reading the `status:` frontmatter of every `tasks/T-AC-*.md` packet, not from working memory or a YAML cache.
- **Kiro `/todo` mirrors user-visible progress.** Add one `/todo` entry per task at Plan time; `/todo complete <n>` when the packet flips to `status: COMPLETE`. `/todo` cannot encode dependencies, so it is purely UI; the packet `status:` is the source of truth.
- **YAML packets under `.erpaval/sessions/<id>/`** are read-only hints that inform which packets to seed and what goes in each subagent's prompt.
- **Markdown per-task packets (`CP-TASK-N`)** double as subagent work logs edited in place per `write-protocol.md`.
- **The filesystem is the shared memory.** Subagents never message each other — they write to their own packet file, and the orchestrator reads all files during check-ins. Kiro subagents return to the orchestrator via the built-in `summary` tool; that summary is a hint, the packet is the truth.

---

## Session 0 — mandatory intake

Run before any classifier except CL-SCOPE / CL-COMPLEXITY. Without these two tool calls, the six-gate `stop` hook in `kiro_compound_nudge.py` never fires and the Compound phase silently no-ops at session end — the #1 reason lessons don't get written.

1. **Recall bootstrap** — always, regardless of project state:

   ```bash
   uv run ${ERPAVAL_HOME}/skills/erpaval/scripts/erpaval-recall.py bootstrap
   ```

   Emits `no prior lessons` on cold repos; otherwise prints category counts + `INDEX.md` path. The output goes into `CP-RECALL`.

2. **Session scaffolding** — after `CL-COMPLEXITY` returns `multi-module` or `rebuild`, run `CL-RESUME`:
   - **new** → required tool call:

     ```bash
     uv run ${ERPAVAL_HOME}/skills/erpaval/scripts/erpaval-new.py --request "<raw_request>"
     ```

     Creates `.erpaval/sessions/session-<hex>/intake.yaml`, ensures `.gitignore` entry and `INDEX.md`. The session id is how the `stop` hook recognizes an ERPAVal session worth nudging.
   - **resume** → read `.erpaval/sessions/<session_id>/session.yaml` and the latest `tasks/T-AC-*.md` packets. Append the new ask to `intake.yaml.raw_request`. Do not scaffold a new `session-<hex>/` — the existing one is the continuity.

On 1-file fixes, `CL-COMPLEXITY` exits before this step — recall-only is correct, and no session dir is needed.

## Phase gates

| Gate       | Condition                                                   | Enforcement                  |
| ---------- | ----------------------------------------------------------- | ---------------------------- |
| **Gate 0** | Both Explore and Research packets show `status: COMPLETE`   | Plan blocks until satisfied  |
| **Gate 1** | Plan reviewed and approved by the user                      | Act blocks until satisfied   |
| **Gate 2** | All three validation layers green or findings dispositioned | Merge blocks until satisfied |

Before advancing, always `grep -l "^status: COMPLETE" .erpaval/sessions/<id>/tasks/*.md` and verify every task in the current phase is `COMPLETE`. If any task is `IN_PROGRESS` or `BLOCKED`, wait. The orchestrator gates each wave by reading every blocker packet's `status:` frontmatter — a task in wave N+1 will not be `/spawn`-ed until every wave-N blocker is `COMPLETE`.

> **Kiro gap shim — task dependencies.** Kiro's `/todo` does not implement `addBlockedBy`. Dependency wiring is encoded in the per-task packet's frontmatter (`blocked_by: [T-AC-1-1, T-AC-1-2]`) and enforced by the orchestrator before each NL subagent dispatch. The `/todo` mirror lets the user see progress; it does not enforce ordering.

---

## Subagent lifecycle per phase

### Explore / Research (Gate 0)

**Always launch Explore and Research in parallel from a single turn.** They have no data dependency on each other — Explore reads the codebase, Research reads the world. Sequencing them doubles wall-clock for zero correctness benefit. Multiple NL subagent dispatches in a single Kiro turn run concurrently, capped at 4 active subagents.

For non-trivial work, decompose further: 2-3 explorer subagents split by module, 2-4 researcher subagents split by domain. The rip-and-replace section below confirms the pattern; the standard flow follows it too.

```text
# Seed packet files (filesystem state)
.erpaval/sessions/<id>/tasks/explore.md          status: IN_PROGRESS
.erpaval/sessions/<id>/tasks/research.md         status: IN_PROGRESS

# Mirror to /todo for user UI
/todo add "Explore codebase"
/todo add "Research dependencies"

# Dispatch via NL in a single turn — Kiro's `subagent` built-in dispatches in parallel (max 4)
> Use the erpaval-explorer agent to read .erpaval/sessions/<id>/tasks/explore.md, follow the write protocol, flip the packet to status: COMPLETE, and call the built-in `summary` tool with a 1-2 paragraph result as your final step.
> Use the erpaval-researcher agent to read .erpaval/sessions/<id>/tasks/research.md, follow the write protocol, flip the packet to status: COMPLETE, and call the built-in `summary` tool with a 1-2 paragraph result as your final step.

# Subagents flip their packet to `status: COMPLETE` and return via the built-in `summary` tool.
# When the orchestrator confirms `status: COMPLETE` in both packets:
/todo complete 1
/todo complete 2
```

### Plan

```text
# Verify Gate 0
grep -l "^status: COMPLETE" .erpaval/sessions/<id>/tasks/{explore,research}.md  # both must match

# Seed plan packet
.erpaval/sessions/<id>/tasks/plan.md             status: IN_PROGRESS
                                                 blocked_by: [explore, research]

/todo add "Create implementation plan"

# Orchestrator walks spec.md and seeds one task packet per AC (EARS methodology: ${ERPAVAL_HOME}/skills/product-discovery/references/frameworks/ears.md)
# Each packet carries frontmatter encoding dependencies:

cat > .erpaval/sessions/<id>/tasks/T-AC-1-1.md <<'EOF'
---
task_id: T-AC-1-1
status: BLOCKED
blocked_by: [plan]
EOF
# … one such packet per AC: T-AC-1-2, T-AC-1-3, T-AC-2-1, validate-all

# Mirror to /todo
/todo add "T-AC-1-1: <subject>"
/todo add "T-AC-1-2: <subject>"
/todo add "T-AC-1-3: <subject>"  # blocked_by: [T-AC-1-1, T-AC-1-2]
/todo add "T-AC-2-1: <subject>"
```

#### Library binding — every dependency cites Research

Every plan task that touches a third-party library, SDK, API, or AWS service must cite a `CP-RESEARCH` entry by file:line in its `Dependencies` packet section. The cited entry must include a pinned version, an authoritative source URL, and an `as_of:` date within the last 6 months. Three concrete rules:

- **Code / library tasks** — cite a `@context7` lookup (`@context7/query-docs`) for the library's current API. If `@context7` returns nothing, `@deepwiki` / `@exa` / `web_fetch` are acceptable, but the packet must say so.
- **AWS-specific tasks** — cite an `@awsknowledge` lookup (`@awsknowledge/aws___search_documentation` or `aws___read_documentation`) for first-party AWS services (Bedrock, CDK, Aurora, Strands, Q Developer, IAM, any `aws-*` SDK). Training-data recall on AWS APIs is the #1 cause of plausibly-wrong CDK constructs and Bedrock invocation shapes.
- **Missing citation = blocker** — if a planned task touches a library and Research has no covering entry, do NOT seed the task packet. Route back to Research via cycle C1b with a scoped NL dispatch naming the missing library/service (`> Use the erpaval-researcher agent to look up <library> v<version>...`). Plan re-runs after Research returns.

This makes "the dep was upgraded last month and broke" detectable at Gate 1 instead of Wave 3.

```text
/todo add "Validate all"          # blocked_by: every T-AC-*

# When the plan is approved by the user, flip the plan packet:
sed -i '' 's/^status: IN_PROGRESS/status: COMPLETE/' .erpaval/sessions/<id>/tasks/plan.md
/todo complete <plan-index>
```

Present the plan to the user. Expect 2-4 revision rounds (cycle C1) — Gate 1 is the design-review checkpoint, not a rubber stamp.

### Act

**Within a wave, every parallel-safe task must launch in a single turn** (subject to Kiro's 4-parallel cap; see batching note below). A wave is *defined* as "tasks with no inter-wave dependency", so the only correct way to dispatch them is concurrent NL subagent calls in one turn. Two turns = two waves = wall-clock drag. The dependency graph is what gates work, not the turn boundary.

On a 26-task session this single discipline drops total wall-clock by ~40%. If you find yourself dispatching one subagent and waiting before dispatching the next, stop — you've collapsed the wave back into a sequence. Re-read the wave's `[P]` AC flags and the dependency graph, then re-launch in a single turn.

> **Kiro gap shim — concurrency cap.** Kiro hard-caps parallel subagents at **4**. If a wave has more than 4 parallel-safe tasks, dispatch in batches of 4 and re-issue when slots free up (Ctrl+G crew monitor shows live status). The dependency graph still permits the next batch — the cap is purely a runtime throttle.

Wave 1 (scaffold) is better done by the orchestrator directly: project structure, `pyproject.toml`, `mise.toml`, directory creation. Fast, benefits from interactive `uv sync` verification, every subsequent subagent depends on the file structure it creates.

For every other wave:

```text
# Verify the plan packet is COMPLETE
grep "^status: COMPLETE" .erpaval/sessions/<id>/tasks/plan.md

# For each task in the current wave: flip BLOCKED → IN_PROGRESS in the packet
sed -i '' 's/^status: BLOCKED/status: IN_PROGRESS/' .erpaval/sessions/<id>/tasks/T-AC-1-1.md
sed -i '' 's/^status: BLOCKED/status: IN_PROGRESS/' .erpaval/sessions/<id>/tasks/T-AC-1-2.md

# Seed each packet's body from assets/session/task-skeleton.md
# Fill the 10 sections from CP-EXPLORE, CP-RESEARCH, CP-RECALL, CP-EARS

# Dispatch all tasks in the wave in a SINGLE turn (parallel, cap-of-4):
> Use a general-purpose agent to act as the T-AC-1-1 Act subagent. Your context packet is at .erpaval/sessions/<id>/tasks/T-AC-1-1.md — read it first, follow the write protocol, flip status: IN_PROGRESS → COMPLETE when done, and call the built-in `summary` tool with a 1-2 paragraph result as your final step.
> Use a general-purpose agent to act as the T-AC-1-2 Act subagent. Your context packet is at .erpaval/sessions/<id>/tasks/T-AC-1-2.md — same contract.
```

#### Per-task subagent prompt template

```text
You are an Act-phase subagent. Your context packet is at the path below —
read it first, then work through its sections in order, editing the packet
in place as you go.

<packet>
{{ absolute_path_to_CP-TASK-N.md }}
</packet>

<preamble>
Before starting section 1, read the packet in full, then read every file
listed under Scope. Subagents have zero context about the codebase —
everything you need is in the packet or in the files it cites.
</preamble>

<write_protocol>
{{ paste references/write-protocol.md verbatim }}
</write_protocol>

<success_criteria>
- Every section of the packet has real content by the end.
- Every check under Success criteria exits 0.
- The `status:` frontmatter line at the top of the packet is flipped from IN_PROGRESS to COMPLETE.
- Every code change is cited with file:line in the Summary.
- Final return: call the built-in `summary` tool with a 1-2 paragraph result.
</success_criteria>

<anti_goals>
- Do not modify files outside Scope.
- Do not add new dependencies.
- Do not refactor existing code.
- If a prerequisite is missing, write the gap to the Work log, leave the
  packet at status: BLOCKED, and report back via `summary` instead of
  improvising — this triggers cycle C3.
</anti_goals>
```

### Monitor — `wc -l` stuck detection

Escalating check-ins: 30s → 2m → 5m → every 5m after. Use Kiro's Ctrl+G crew monitor to see live subagent state alongside the filesystem snapshot.

```bash
wc -l .erpaval/sessions/<id>/tasks/*.md
```

A task is **stuck** when its packet's line count is identical across two consecutive check-ins. Recovery:

1. Read the packet to see which sections have real content.
2. Re-dispatch with a fresh NL subagent call:
   - Prompt lists the sections already complete and tells the new subagent to skip them.
   - Same agent (`erpaval-explorer` / `erpaval-researcher` / general-purpose); name the retry in the prompt (e.g. `T-AC-1-1-retry`) for traceability via `kiro-cli chat --resume-id`.
   - Same `summary`-as-final-step contract.
3. The original backgrounded subagent will finish or timeout on its own; its writes stopped updating the packet so its continued existence is harmless. (Kiro has no `kill --background` primitive — let it drain.)
4. Resume normal check-ins.

Do not tally completion from subagent `summary` returns alone — they may arrive out of order, and the orchestrator may receive them as terse hints. The filesystem is the source of truth. Completion gate:

```bash
total=$(ls .erpaval/sessions/<id>/tasks/*.md | wc -l)
done=$(grep -l '^status: COMPLETE' .erpaval/sessions/<id>/tasks/*.md | wc -l)
echo "complete: $done / $total"
```

### Eager unblocking (cycle C6)

After each packet flips to `status: COMPLETE`, scan the dependency graph (`blocked_by:` frontmatter on remaining `BLOCKED` packets) for tasks whose blockers are now clear. Dispatch them immediately via NL — don't wait for sibling tasks in the current wave. On a 26-task session this saves ~30-40% wall-clock time. Subject to Kiro's 4-parallel cap; let one slot free, fill the next.

### Validate

```text
# Verify all Act packets are COMPLETE
grep -L "^status: COMPLETE" .erpaval/sessions/<id>/tasks/T-AC-*.md  # must be empty

# Seed validate packet
.erpaval/sessions/<id>/tasks/validate.md         status: IN_PROGRESS

# Layer 1: bash, not subagent (orchestrator-direct)
ruff check . && pyright && pytest -q

# Layer 2: code-quality review via NL subagent dispatch
> Use the erpaval-explorer agent to do a code-quality review per validation-playbook.md. Read-only. Final step: call the built-in `summary` tool with the L2 report.
# Layer 3: security review via NL subagent dispatch
> Use the erpaval-explorer agent to do a security review per validation-playbook.md. Read-only. Final step: call the built-in `summary` tool with the L3 report.

# If both layers pass → flip validate.md to status: COMPLETE
# If fail → identify failing tasks, flip their packets back to IN_PROGRESS, fix the body, relaunch (C4)
```

See `validation-playbook.md` for layer-by-layer prompts and severity rubrics.

---

## Subagent dispatch — invocation mapping

This table maps the Claude Code `Agent` tool parameters to Kiro's NL subagent-dispatch semantics, for porting prompts and runbooks.

| Claude Code `Agent` param | Kiro equivalent                                                                                                                                                                                     |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `description`             | A short, kebab-case task label embedded in the NL prompt (e.g. `the T-AC-1-1 Act subagent`). Use it consistently across the prompt and packet so `kiro-cli chat --list-sessions` is searchable.     |
| `prompt`                  | The free-text NL dispatch: `> Use the <agent-name> agent to <task>...`. Always end with the `summary`-as-final-step instruction.                                                                    |
| `subagent_type`           | The custom-agent name in the NL phrasing: `Use the erpaval-explorer agent to …` / `Use the erpaval-researcher agent to …` / `Use a general-purpose agent to …` (default for Act)                    |
| `model`                   | Set in the subagent's agent JSON `model` field, **not** at invocation time. To vary per task, define multiple agents (e.g. `erpaval-act-haiku`, `erpaval-act-sonnet`) and route via the NL phrasing |
| `run_in_background`       | All NL subagent dispatches are async by default; the orchestrator monitors via Ctrl+G crew monitor (live state) and packet `wc -l` (filesystem snapshot)                                            |
| `isolation`               | **Not supported.** Kiro has no worktree primitive. Subagents share the working tree — rely on `Scope` discipline in packets instead                                                                 |
| `name`                    | Set via the in-prompt task label (above). Subagent sessions persist with the parent session ID; recover any one with `kiro-cli chat --resume-id <subagent-session-id>`                              |

> **`/spawn` is for users, not the orchestrator.** `/spawn --name X "..."` starts a fresh long-running session for the *human* to switch into via `/chat resume` or Ctrl+G. It is not the agent's delegation primitive. Do not put `/spawn` lines in orchestrator prompts. If you see them in older runbooks, treat them as bugs to translate into NL dispatch.

Concrete examples:

```text
# Explore (single)
> Use the erpaval-explorer agent to scan src/ and produce CP-EXPLORE per .erpaval/sessions/<id>/tasks/explore.md. Final step: call the built-in `summary` tool with a 1-2 paragraph result.

# Research (single)
> Use the erpaval-researcher agent. Topic: pydantic v2 migration. Output to .erpaval/sessions/<id>/research-pydantic.yaml. Final step: call the built-in `summary` tool with the findings.

# Act wave (multiple subagents, single orchestrator turn — Kiro caps at 4 concurrent)
> Use a general-purpose agent to act as the T-AC-1-1 Act subagent (packet at .erpaval/sessions/<id>/tasks/T-AC-1-1.md). Final step: call the built-in `summary` tool.
> Use a general-purpose agent to act as the T-AC-1-2 Act subagent (packet at .erpaval/sessions/<id>/tasks/T-AC-1-2.md). Final step: call the built-in `summary` tool.
> Use a general-purpose agent to act as the T-AC-1-3 Act subagent (packet at .erpaval/sessions/<id>/tasks/T-AC-1-3.md). Final step: call the built-in `summary` tool.
> Use a general-purpose agent to act as the T-AC-2-1 Act subagent (packet at .erpaval/sessions/<id>/tasks/T-AC-2-1.md). Final step: call the built-in `summary` tool.
```

### Permission contract for reliable dispatch

The orchestrator's agent JSON must declare:

```json
{
  "tools": ["...", "subagent"],
  "allowedTools": ["*"],
  "toolsSettings": {
    "subagent": {
      "availableAgents": ["erpaval-explorer", "erpaval-researcher", "erpaval-act-*"],
      "trustedAgents": ["erpaval-explorer", "erpaval-researcher", "erpaval-act-*"]
    }
  }
}
```

Each subagent JSON must declare:

```json
{
  "tools": ["read", "grep", "glob", "shell", "..."],
  "allowedTools": ["*"]
}
```

If the parent omits the subagent from `availableAgents`, the dispatch is rejected. If it omits `trustedAgents` (or lists it under `availableAgents` but not `trustedAgents`), the user is prompted to approve every spawn — and in headless / autonomous-overnight contexts that surfaces as an empty result. Subagents are `is_interactive: false`, so a missing entry in their own `allowedTools` causes them to **fail fast** (no hang) and return without calling `summary` — the same "No result" failure mode.

### Diagnosing "No result"

If a subagent dispatch returns empty or the orchestrator sees no summary:

1. Confirm the dispatch prompt explicitly demanded a `summary` call as the final step.
2. Check the parent's `trustedAgents` includes the subagent name.
3. Check the subagent's `allowedTools` covers everything the task needs.
4. Open the Ctrl+G crew monitor mid-run to see if the subagent is actually doing work or fail-fasting on a missing tool.
5. List recent subagent sessions (`kiro-cli chat --list-sessions`) and inspect the failed one with `--resume-id <id>` to see what the subagent actually did.

In-chat NL is the *only* dispatch primitive for the orchestrator: `> Use the erpaval-explorer agent to scan src/auth and produce …`. Multiple NL dispatches in a single turn run concurrently (capped at 4). `/spawn` remains a user command for fresh long-running sessions and is irrelevant inside the orchestrator's runbook.

Subagents cannot dispatch sub-subagents (Kiro requires the `subagent` built-in tool to be in the agent's `tools` array; only the orchestrator has it). If a task needs nested delegation, break it into separate tasks.

Tool access for Act subagents: `read`, `write`, `shell`, `glob`, `grep` (the canonical built-in names; `fs_read`/`fs_write`/`execute_bash` are deprecated Q-era aliases that still resolve). They do not need `web_fetch`, `web_search`, MCP tools, or `subagent` — if a subagent needs to research, the Research phase was incomplete. Go back and fill the gap.

---

## Context packet composition — Zero-Context Principle

Assume the subagent has never seen this codebase, doesn't know project structure, conventions, or what other agents are building in parallel. Every Act packet must include all 10 sections from `assets/session/task-skeleton.md`. Omitting any section is the most common cause of subagent failure.

| Section              | Source                                                                                          |
| -------------------- | ----------------------------------------------------------------------------------------------- |
| Objective            | One sentence — what to build, restated from the AC                                              |
| Scope                | Files to create/modify; files to NOT touch                                                      |
| EARS requirement     | Paste AC text verbatim from `spec.md`                                                           |
| Architecture context | Excerpt from `CP-EXPLORE` — patterns, DI, error handling, test style                            |
| API contracts        | Exact signatures, types, interfaces the work must match (critical for parallel agents)          |
| Conventions          | From `CP-EXPLORE` — naming, imports, async discipline                                           |
| Dependencies         | From `CP-RESEARCH` — pinned versions, breaking changes, known pitfalls                          |
| Prior lessons        | Paths from `CP-RECALL` — `.erpaval/solutions/<category>/<slug>.md`                              |
| Success criteria     | Baseline (ruff/pyright/pytest all exit 0) + task-specific verifiable checks                     |
| Anti-goals           | No refactoring, no new deps, no new abstractions, report missing prereqs instead of improvising |

### Common anti-patterns

| Anti-pattern                 | Fix                                                                                      |
| ---------------------------- | ---------------------------------------------------------------------------------------- |
| "Follow existing patterns"   | List specific patterns with file references                                              |
| Omitting types/signatures    | Specify exact signatures — parallel agents will invent incompatible interfaces otherwise |
| "Use best practices"         | State the specific practices to follow                                                   |
| Including the whole codebase | Curate only relevant files and snippets                                                  |
| No anti-goals                | Explicitly state what not to do                                                          |
| Vague success criteria       | Make every check mechanically verifiable                                                 |

---

## Rip-and-replace variant

When the task is rebuilding a subsystem from scratch (not incremental feature work):

1. **Explore**: both the system being replaced AND the reference architecture. Multiple `erpaval-explorer` subagents in parallel (cap-of-4).
2. **Research**: the NEW stack — replacement libraries, frameworks, patterns. Split by domain (3-5 parallel, batch as needed).
3. **Plan**: more architecture document than task list. Include package structure, data models, module layout, migration strategy, explicit "what's dropped" section. Expect 2-4 Gate 1 revision rounds.
4. **Wave 1 (scaffold)**: destructive — `rm -rf packages/*` then create the new structure. Orchestrator-executed. Verify with `uv sync` before proceeding.
5. **Remaining waves**: standard Act flow. Since Kiro has no worktree isolation, scope discipline in each packet's `Scope` section is the only safeguard against parallel subagents stepping on each other; in rip-and-replace mode the whole codebase is new, so collisions are mostly impossible by construction.
6. **DB migration**: if rebuilding targets an existing database, include a migration task early (Wave 3-4) that creates transformation SQL. Separate concern from code rebuild.

---

## Context-budget discipline at scale

With 20-30+ background subagents, be aware of orchestrator context pressure:

- **Subagent results are short summaries** returned via Kiro's built-in `summary` tool (~100-300 tokens), not full transcripts. The packet on disk is the artifact.
- **Crew-monitor notifications** (Ctrl+G) show live state without dumping into context.
- **Per-task packets are the big artifact**. Each is ~200-400 lines by the end. The orchestrator reads them during gate checks and Compound, not during Act.
- **Prune completed-phase context**: after Wave N is done and Wave N+1 is running, you don't need Wave N's `summary` returns in active reasoning. The code is on disk; the packets are on disk.

---

## Preventing premature implementation

The most common ERPAVal failure mode: subagents starting to implement before the plan is complete or before phase dependencies are met.

1. **Structural**: encode `blocked_by:` in every implementation packet's frontmatter — the orchestrator gates each NL subagent dispatch on the blocker packets being `status: COMPLETE`.
2. **Prompt-level**: the anti-goals section of every packet includes "Do not start work on tasks assigned to other subagents; if a prerequisite is missing, report back via `summary` instead of improvising."
3. **Orchestrator discipline**: never dispatch an Act subagent before the plan packet is `status: COMPLETE`; never start Phase N+1 before all Phase N packets are `COMPLETE`; always `grep -L "^status: COMPLETE"` between phases; if a subagent reports a missing prereq via `summary`, go back to Plan (C3) rather than improvising.
