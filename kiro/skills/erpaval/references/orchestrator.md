# Orchestrator — phase-by-phase runbook

How the orchestrator (a Kiro CLI session running the `erpaval-orchestrator` agent) runs an ERPAVal session using Kiro's two execution primitives: **filesystem-driven task packets** (Markdown files at `.erpaval/sessions/<id>/tasks/T-AC-X-Y.md` carrying `status:` frontmatter) for gate state, with Kiro's `/todo` slash command mirroring progress for the user, and the **`subagent` built-in tool** (driven via `/spawn` or in-chat NL) for subagent execution. Adapts the research/ultraplan file-first pattern to a stateful, multi-phase development loop: every subagent edits a per-task Markdown packet section-by-section, and the orchestrator monitors progress by reading those files (`wc -l` for stuck detection), not by polling the subagent's output stream.

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

| Gate       | Condition                                                                                          | Enforcement                  |
| ---------- | -------------------------------------------------------------------------------------------------- | ---------------------------- |
| **Gate 0** | Both Explore and Research packets show `status: COMPLETE`                                          | Plan blocks until satisfied  |
| **Gate 1** | Plan reviewed and approved by the user                                                             | Act blocks until satisfied   |
| **Gate 2** | All three validation layers green or findings dispositioned                                        | Merge blocks until satisfied |

Before advancing, always `grep -l "^status: COMPLETE" .erpaval/sessions/<id>/tasks/*.md` and verify every task in the current phase is `COMPLETE`. If any task is `IN_PROGRESS` or `BLOCKED`, wait. The orchestrator gates each wave by reading every blocker packet's `status:` frontmatter — a task in wave N+1 will not be `/spawn`-ed until every wave-N blocker is `COMPLETE`.

> **Kiro gap shim — task dependencies.** Kiro's `/todo` does not implement `addBlockedBy`. Dependency wiring is encoded in the per-task packet's frontmatter (`blocked_by: [T-AC-1-1, T-AC-1-2]`) and enforced by the orchestrator before each `/spawn` call. The `/todo` mirror lets the user see progress; it does not enforce ordering.

---

## Subagent lifecycle per phase

### Explore / Research (Gate 0)

**Always launch Explore and Research in parallel from a single message.** They have no data dependency on each other — Explore reads the codebase, Research reads the world. Sequencing them doubles wall-clock for zero correctness benefit. Multiple `/spawn` invocations in a single Kiro turn dispatch concurrently, capped at 4 active subagents.

For non-trivial work, decompose further: 2-3 explorer subagents split by module, 2-4 researcher subagents split by domain. The rip-and-replace section below confirms the pattern; the standard flow follows it too.

```text
# Seed packet files (filesystem state)
.erpaval/sessions/<id>/tasks/explore.md          status: IN_PROGRESS
.erpaval/sessions/<id>/tasks/research.md         status: IN_PROGRESS

# Mirror to /todo for user UI
/todo add "Explore codebase"
/todo add "Research dependencies"

# Launch both in a single message — Kiro dispatches in parallel (max 4)
/spawn --name explore   "Use the erpaval-explorer agent. Read .erpaval/sessions/<id>/tasks/explore.md and follow the write protocol …"
/spawn --name research  "Use the erpaval-researcher agent. Read .erpaval/sessions/<id>/tasks/research.md …"

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
- **Missing citation = blocker** — if a planned task touches a library and Research has no covering entry, do NOT seed the task packet. Route back to Research via cycle C1b with a scoped `/spawn` naming the missing library/service. Plan re-runs after Research returns.

This makes "the dep was upgraded last month and broke" detectable at Gate 1 instead of Wave 3.

```text
/todo add "Validate all"          # blocked_by: every T-AC-*

# When the plan is approved by the user, flip the plan packet:
sed -i '' 's/^status: IN_PROGRESS/status: COMPLETE/' .erpaval/sessions/<id>/tasks/plan.md
/todo complete <plan-index>
```

Present the plan to the user. Expect 2-4 revision rounds (cycle C1) — Gate 1 is the design-review checkpoint, not a rubber stamp.

### Act

**Within a wave, every parallel-safe task must launch in a single message** (subject to Kiro's 4-parallel cap; see batching note below). A wave is *defined* as "tasks with no inter-wave dependency", so the only correct way to dispatch them is concurrent `/spawn` calls in one turn. Two turns = two waves = wall-clock drag. The dependency graph is what gates work, not the turn boundary.

On a 26-task session this single discipline drops total wall-clock by ~40%. If you find yourself `/spawn`-ing one and waiting before `/spawn`-ing the next, stop — you've collapsed the wave back into a sequence. Re-read the wave's `[P]` AC flags and the dependency graph, then re-launch in a single turn.

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

# Launch all tasks in the wave in a SINGLE turn (parallel, cap-of-4):
/spawn --name T-AC-1-1 "You are an Act-phase subagent. Your context packet is at .erpaval/sessions/<id>/tasks/T-AC-1-1.md — read it first, then work through its sections per the write protocol …"
/spawn --name T-AC-1-2 "You are an Act-phase subagent. Your context packet is at .erpaval/sessions/<id>/tasks/T-AC-1-2.md — read it first, then work through its sections per the write protocol …"
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
2. Relaunch with a fresh `/spawn` call:
   - Prompt lists the sections already complete and tells the new subagent to skip them.
   - Same agent (`erpaval-explorer` / `erpaval-researcher` / general-purpose), same `--name` suffix + `-retry`.
3. The original backgrounded subagent will finish or timeout on its own; its writes stopped updating the packet so its continued existence is harmless. (Kiro has no `kill --background` primitive — let it drain.)
4. Resume normal check-ins.

Do not tally completion from subagent `summary` returns alone — they may arrive out of order, and the orchestrator may receive them as terse hints. The filesystem is the source of truth. Completion gate:

```bash
total=$(ls .erpaval/sessions/<id>/tasks/*.md | wc -l)
done=$(grep -l '^status: COMPLETE' .erpaval/sessions/<id>/tasks/*.md | wc -l)
echo "complete: $done / $total"
```

### Eager unblocking (cycle C6)

After each packet flips to `status: COMPLETE`, scan the dependency graph (`blocked_by:` frontmatter on remaining `BLOCKED` packets) for tasks whose blockers are now clear. `/spawn` them immediately — don't wait for sibling tasks in the current wave. On a 26-task session this saves ~30-40% wall-clock time. Subject to Kiro's 4-parallel cap; let one slot free, fill the next.

### Validate

```text
# Verify all Act packets are COMPLETE
grep -L "^status: COMPLETE" .erpaval/sessions/<id>/tasks/T-AC-*.md  # must be empty

# Seed validate packet
.erpaval/sessions/<id>/tasks/validate.md         status: IN_PROGRESS

# Layer 1: bash, not subagent (orchestrator-direct)
ruff check . && pyright && pytest -q

# Layer 2: code-quality review via /spawn
/spawn --name validate-quality "Code quality review per validation-playbook.md. Read-only. Use the opus model."
# Layer 3: security review via /spawn
/spawn --name validate-security "Security review per validation-playbook.md. Read-only. Use the opus model."

# If both layers pass → flip validate.md to status: COMPLETE
# If fail → identify failing tasks, flip their packets back to IN_PROGRESS, fix the body, relaunch (C4)
```

See `validation-playbook.md` for layer-by-layer prompts and severity rubrics.

---

## Kiro `/spawn` — invocation mapping

This table maps the Claude Code `Agent` tool parameters to Kiro `/spawn` semantics, for porting prompts and runbooks.

| Claude Code `Agent` param | Kiro equivalent                                                                                          |
| ------------------------- | -------------------------------------------------------------------------------------------------------- |
| `description`             | The `--name` flag of `/spawn` (3-5 word label, kebab-case, e.g. `T-AC-1-1`)                              |
| `prompt`                  | The free-text body that follows `--name <id>`; the per-task prompt template above                       |
| `subagent_type`           | The custom-agent name in the prompt: `"Use the erpaval-explorer agent to …"` / `"… erpaval-researcher …"` / general-purpose (default) for Act |
| `model`                   | Set in the agent JSON's `model` field, **not** at invocation time. To vary per task, define multiple agents (e.g. `erpaval-act-haiku`, `erpaval-act-sonnet`) and route via the prompt phrasing |
| `run_in_background`       | All `/spawn` calls run in the background by default; the orchestrator monitors via Ctrl+G (crew monitor) and packet `wc -l` |
| `isolation`               | **Not supported.** Kiro has no worktree primitive. Subagents share the working tree — rely on `Scope` discipline in packets instead |
| `name`                    | Same as `description` — the `--name` flag                                                                |

Concrete examples:

```text
# Explore (single)
/spawn --name explore "Use the erpaval-explorer agent to scan src/ and produce CP-EXPLORE per .erpaval/sessions/<id>/tasks/explore.md."

# Research (single)
/spawn --name research-pydantic "Use the erpaval-researcher agent. Topic: pydantic v2 migration. Output to .erpaval/sessions/<id>/research-pydantic.yaml."

# Act wave (multiple, single turn — Kiro caps at 4)
/spawn --name T-AC-1-1 "{{ packet path + write protocol + success criteria }}"
/spawn --name T-AC-1-2 "{{ packet path + write protocol + success criteria }}"
/spawn --name T-AC-1-3 "{{ packet path + write protocol + success criteria }}"
/spawn --name T-AC-2-1 "{{ packet path + write protocol + success criteria }}"
```

In-chat NL invocation also works: `> Use the erpaval-explorer agent to scan src/auth and produce …`. Use NL when the orchestrator agent is in tangent-style chat; use `/spawn` when running a structured wave dispatch.

Subagents cannot spawn sub-subagents (Kiro requires the `subagent` built-in tool to be in the agent's `tools` array; only the orchestrator has it). If a task needs nested delegation, break it into separate tasks.

Tool access for Act subagents: `read` (`fs_read`), `write` (`fs_write`), `shell` (`execute_bash`), `glob`, `grep`. They do not need `web_fetch`, `web_search`, MCP tools, or `subagent` — if a subagent needs to research, the Research phase was incomplete. Go back and fill the gap.

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

1. **Structural**: encode `blocked_by:` in every implementation packet's frontmatter — the orchestrator gates each `/spawn` call on the blocker packets being `status: COMPLETE`.
2. **Prompt-level**: the anti-goals section of every packet includes "Do not start work on tasks assigned to other subagents; if a prerequisite is missing, report back via `summary` instead of improvising."
3. **Orchestrator discipline**: never `/spawn` an Act subagent before the plan packet is `status: COMPLETE`; never start Phase N+1 before all Phase N packets are `COMPLETE`; always `grep -L "^status: COMPLETE"` between phases; if a subagent reports a missing prereq via `summary`, go back to Plan (C3) rather than improvising.
