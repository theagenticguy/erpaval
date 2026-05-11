# Orchestrator — phase-by-phase runbook

How the orchestrator (the main Claude Code session) runs an ERPAVal session using Claude's two execution primitives: **Task tools** (`TaskCreate` / `TaskUpdate` / `TaskList` / `TaskGet`) for gate state, and the **Agent tool** for subagent execution. Adapts the research/ultraplan file-first pattern to a stateful, multi-phase development loop: every subagent edits a per-task Markdown packet section-by-section, and the orchestrator monitors progress by reading those files (`wc -l` for stuck detection), not by polling the agent's output stream.

Terms like `CP-*`, `CL-*`, `T-AC-X-Y`, Wave are defined in `glossary.md`. The graph is in `flow.md`.

---

## Division of labor

- **Task tools hold authoritative state.** "What's next, what's blocked, what's stuck" — answer from `TaskList`, not from packet YAML.
- **YAML packets under `.erpaval/sessions/<id>/`** are read-only hints that inform which tasks to create and what goes in their `prompt`.
- **Markdown per-task packets (`CP-TASK-N`)** double as subagent work logs edited in place per `write-protocol.md`.
- **The filesystem is the shared memory.** Subagents never message each other — they write to their own packet file, and the orchestrator reads all files during check-ins.

---

## Session 0 — mandatory intake

Run before any classifier except CL-SCOPE / CL-COMPLEXITY. Without these two tool calls, the six-gate `Stop` hook in `compound_nudge.py` never fires and the Compound phase silently no-ops at session end — the #1 reason lessons don't get written.

1. **Recall bootstrap** — always, regardless of project state:

   ```bash
   uv run ${CLAUDE_PLUGIN_ROOT}/skills/erpaval/tools/erpaval-recall.py bootstrap
   ```

   Emits `no prior lessons` on cold repos; otherwise prints category counts + `INDEX.md` path. The output goes into `CP-RECALL`.

2. **Session scaffolding** — after `CL-COMPLEXITY` returns `multi-module` or `rebuild`, run `CL-RESUME`:
   - **new** → required tool call:

     ```bash
     uv run ${CLAUDE_PLUGIN_ROOT}/skills/erpaval/tools/erpaval-new.py --request "<raw_request>"
     ```

     Creates `.erpaval/sessions/session-<hex>/intake.yaml`, ensures `.gitignore` entry and `INDEX.md`. The session id is how the `Stop` hook recognizes an ERPAVal session worth nudging.
   - **resume** → read `.erpaval/sessions/<session_id>/session.yaml` and the latest `tasks/T-AC-*.md` packets. Append the new ask to `intake.yaml.raw_request`. Do not scaffold a new `session-<hex>/` — the existing one is the continuity.

On 1-file fixes, `CL-COMPLEXITY` exits before this step — recall-only is correct, and no session dir is needed.

## Phase gates

| Gate       | Condition                                                    | Enforcement                  |
| ---------- | ------------------------------------------------------------ | ---------------------------- |
| **Gate 0** | Both Explore and Research tasks show `completed` in TaskList | Plan blocks until satisfied  |
| **Gate 1** | Plan reviewed and approved by the user                       | Act blocks until satisfied   |
| **Gate 2** | All three validation layers green or findings dispositioned  | Merge blocks until satisfied |

Before advancing, always `TaskList` and verify every task in the current phase is `completed`. If any task is `in_progress` or `pending`, wait. `addBlockedBy` wires the gate mechanically — a blocked task cannot start until every blocker is `completed`.

---

## Task-tool lifecycle per phase

### Explore / Research (Gate 0)

**Always launch Explore and Research in parallel from a single message.** They have no data dependency on each other — Explore reads the codebase, Research reads the world. Sequencing them doubles wall-clock for zero correctness benefit. The single-message rule is enforced by the Claude Code Agent tool's "tool calls in one message run concurrently" semantics; two separate messages run sequentially.

For non-trivial work, decompose further: 2-3 Explore subagents split by module, 2-4 researcher subagents split by domain. The rip-and-replace section below confirms the pattern; the standard flow follows it too.

```text
TaskCreate(subject="Explore codebase",   description="...")  # → id "1"
TaskCreate(subject="Research dependencies", description="...")  # → id "2"
TaskUpdate(taskId="1", status="in_progress")
TaskUpdate(taskId="2", status="in_progress")

# Launch both in a single message, run_in_background=true
Agent(subagent_type="Explore",    prompt="...", run_in_background=true)
Agent(subagent_type="researcher", prompt="...", run_in_background=true)

# When each returns
TaskUpdate(taskId="1", status="completed")
TaskUpdate(taskId="2", status="completed")
```

### Plan

```text
TaskList  # verify "1"=completed, "2"=completed
TaskCreate(subject="Create implementation plan", description="...")  # → id "3"
TaskUpdate(taskId="3", addBlockedBy=["1", "2"], status="in_progress")

# Orchestrator walks spec.md and emits one TaskCreate per AC (EARS methodology: ${CLAUDE_PLUGIN_ROOT}/skills/product-discovery/references/frameworks/ears.md)
TaskCreate(subject="T-AC-1-1: ...", description="...")  # → id "4"
TaskCreate(subject="T-AC-1-2: ...", description="...")  # → id "5"
TaskCreate(subject="T-AC-1-3: ...", description="...")  # → id "6"
TaskCreate(subject="T-AC-2-1: ...", description="...")  # → id "7"
TaskCreate(subject="Validate all", description="...")   # → id "8"

# Wire dependencies
TaskUpdate(taskId="4", addBlockedBy=["3"])
TaskUpdate(taskId="5", addBlockedBy=["3"])
TaskUpdate(taskId="6", addBlockedBy=["4", "5"])
TaskUpdate(taskId="7", addBlockedBy=["3"])
TaskUpdate(taskId="8", addBlockedBy=["4", "5", "6", "7"])

TaskUpdate(taskId="3", status="completed")
```

Present the plan to the user. Expect 2-4 revision rounds (cycle C1) — Gate 1 is the design-review checkpoint, not a rubber stamp.

### Act

**Within a wave, every parallel-safe task must launch in a single message.** A wave is *defined* as "tasks with no inter-wave dependency", so the only correct way to dispatch them is concurrent `Agent` calls in one message with `run_in_background=true`. Two messages = two waves = wall-clock drag. The dependency graph is what gates work, not the message boundary.

On a 26-task session this single discipline drops total wall-clock by ~40%. If you find yourself launching one Agent and waiting before launching the next, stop — you've collapsed the wave back into a sequence. Re-read the wave's `[P]` AC flags and the dependency graph, then re-launch in a single message.

Wave 1 (scaffold) is better done by the orchestrator directly: project structure, `pyproject.toml`, `mise.toml`, directory creation. Fast, benefits from interactive `uv sync` verification, every subsequent agent depends on the file structure it creates.

For every other wave:

```text
TaskList  # verify plan = completed
TaskUpdate(taskId=N, status="in_progress")  # for each task in the current wave

# Seed each task's packet file from templates/session/task-skeleton.md
# filename: .erpaval/sessions/<id>/tasks/T-AC-X-Y.md
# Fill the 10 sections from CP-EXPLORE, CP-RESEARCH, CP-RECALL, CP-EARS

# Launch all tasks in the wave in a SINGLE message (parallel)
Agent(description="T-AC-1-1: ...", prompt="{see template below}", model="sonnet", run_in_background=true, name="T-AC-1-1")
Agent(description="T-AC-1-2: ...", prompt="{see template below}", model="haiku",  run_in_background=true, name="T-AC-1-2")
```

#### Per-task Agent prompt template

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
- The Status line at the top is flipped from IN PROGRESS to COMPLETE.
- Every code change is cited with file:line in the Summary.
</success_criteria>

<anti_goals>
- Do not modify files outside Scope.
- Do not add new dependencies.
- Do not refactor existing code.
- If a prerequisite is missing, write the gap to the Work log and report
  back instead of improvising — this triggers cycle C3.
</anti_goals>
```

### Monitor — `wc -l` stuck detection

Escalating check-ins: 30s → 2m → 5m → every 5m after.

```bash
wc -l .erpaval/sessions/<id>/tasks/*.md
```

A task is **stuck** when its packet's line count is identical across two consecutive check-ins. Recovery:

1. `Read` the packet to see which sections have real content.
2. Relaunch with a fresh `Agent` call:
   - Prompt lists the sections already complete and tells the new agent to skip them.
   - Same `model`, same `isolation`, same `name` suffix + `-retry`.
3. The original backgrounded agent will finish or timeout on its own; its writes stopped updating the packet so its continued existence is harmless.
4. Resume normal check-ins.

Do not tally completion from agent notifications in the main conversation — they arrive out of order. The filesystem is the source of truth. Completion gate:

```bash
total=$(ls .erpaval/sessions/<id>/tasks/*.md | wc -l)
done=$(grep -l '^\*\*Status:\*\* COMPLETE' .erpaval/sessions/<id>/tasks/*.md | wc -l)
echo "complete: $done / $total"
```

### Eager unblocking (cycle C6)

After each `TaskUpdate(..., status="completed")`, scan the dependency graph for tasks whose blockers are now clear. Launch them immediately — don't wait for sibling tasks in the current wave. On a 26-task session this saves ~30-40% wall-clock time.

### Validate

```text
TaskList  # verify all Act tasks = completed
TaskUpdate(taskId=validate, status="in_progress")

# Layer 1: Bash, not subagent
# Layer 2: Opus agent, read-only
Agent(description="Code quality review", prompt="{see validation-playbook.md}", model="opus")
# Layer 3: SAST + Opus security review
Agent(description="Security review",     prompt="{see validation-playbook.md}", model="opus")

# If pass → TaskUpdate status=completed
# If fail → identify failing tasks, TaskUpdate them back to in_progress, fix packet, relaunch (C4)
```

See `validation-playbook.md` for layer-by-layer prompts and severity rubrics.

---

## Agent tool — parameter mapping

| Parameter           | Usage                                                                                                   |
| ------------------- | ------------------------------------------------------------------------------------------------------- |
| `description`       | 3-5 word label ("Implement user service")                                                               |
| `prompt`            | The per-task prompt template above; packet path + write_protocol + success criteria                     |
| `subagent_type`     | `"Explore"` for E, `"researcher"` for R, `"general-purpose"` (default) for Act                          |
| `model`             | `"sonnet"` for clear specs, `"opus"` for complex logic, `"haiku"` for boilerplate                       |
| `run_in_background` | **Always `true` when launching ≥2 sibling tasks in one message.** `false` only for solo blocking calls. |
| `isolation`         | `"worktree"` when AC is marked `[P]` or files overlap; omit otherwise                                   |
| `name`              | `"T-AC-X-Y"` — enables `SendMessage` continuation for C2 in-task fixes                                  |

Subagents cannot spawn sub-subagents. If a task needs nested delegation, break it into separate tasks.

Tool access for Act subagents: `Read`, `Write`, `Edit`, `Bash`, `Glob`, `Grep`. They do not need `WebFetch`, `WebSearch`, MCP tools, or `Agent` — if a subagent needs to research, the Research phase was incomplete. Go back and fill the gap.

---

## Context packet composition — Zero-Context Principle

Assume the subagent has never seen this codebase, doesn't know project structure, conventions, or what other agents are building in parallel. Every Act packet must include all 10 sections from `templates/session/task-skeleton.md`. Omitting any section is the most common cause of subagent failure.

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

1. **Explore**: both the system being replaced AND the reference architecture. Multiple Explore agents in parallel.
2. **Research**: the NEW stack — replacement libraries, frameworks, patterns. Split by domain (3-5 parallel).
3. **Plan**: more architecture document than task list. Include package structure, data models, module layout, migration strategy, explicit "what's dropped" section. Expect 2-4 Gate 1 revision rounds.
4. **Wave 1 (scaffold)**: destructive — `rm -rf packages/*` then create the new structure. Orchestrator-executed. Verify with `uv sync` before proceeding.
5. **Remaining waves**: standard Act flow, but no "existing code" to break — skip worktree isolation and the "do not modify files outside scope" anti-goal. The whole codebase is new.
6. **DB migration**: if rebuilding targets an existing database, include a migration task early (Wave 3-4) that creates transformation SQL. Separate concern from code rebuild.

---

## Context-budget discipline at scale

With 20-30+ background agents, be aware of orchestrator context pressure:

- **Agent results are summaries** (~100-300 tokens), not full transcripts. `run_in_background: true` is critical — foreground agents dump their full output into your context.
- **Task notifications** include only `summary` and `result` fields. Full transcripts live on disk — don't read them unless debugging.
- **Per-task packets are the big artifact**. Each is ~200-400 lines by the end. The orchestrator reads them during gate checks and Compound, not during Act.
- **Prune completed-phase context**: after Wave N is done and Wave N+1 is running, you don't need Wave N's agent results in active reasoning. The code is on disk; the packets are on disk.

---

## Preventing premature implementation

The most common ERPAVal failure mode: agents starting to implement before the plan is complete or before phase dependencies are met.

1. **Structural**: wire `addBlockedBy` on every implementation task — the task system itself prevents early starts.
2. **Prompt-level**: the anti-goals section of every packet includes "Do not start work on tasks assigned to other agents; if a prerequisite is missing, report back instead of improvising."
3. **Orchestrator discipline**: never launch an Act agent before the plan task is `completed`; never launch Phase N+1 before all Phase N tasks return; always `TaskList` between phases; if an agent reports a missing prereq, go back to Plan (C3) rather than improvising.
