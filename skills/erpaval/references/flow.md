# The adaptive flow

Canonical graph for ERPAVal. Where this file disagrees with the glance-graph in `SKILL.md`, this file wins. Terms like `CP-*`, `CL-*`, Gates 0/1/2, Wave are defined in `glossary.md`.

Conventions:

- Solid edges are forward flow; dashed edges are named cycles.
- Diamond nodes are classifiers or gates.
- Cylinder nodes are persisted context packets (`CP-*`).
- Optional steps carry the edge label `fuzzy` or `contract unclear` — Claude runs them only when `CL-RIGOR` returns the matching signal (see `classifiers.md`).

---

## Contents

- §A — Intake & triage
- §B — Build loop
- §C — Validate · merge · compound
- Named cycles
  - Disambiguating C1 / C1b / C1c
  - C2 protocol
  - C3 protocol
  - C4 / C5 protocol
  - C6 — eager unblocking

## §A — Intake & triage

Session start through "ready to build". Every branch either routes to another skill, exits, or hands off to §B.

```mermaid
flowchart LR
  START([User request]) --> INTAKE[Intake]
  INTAKE --> CP_INTAKE[(CP-INTAKE)]
  CP_INTAKE --> RECALL[Recall prior lessons]
  RECALL --> CP_RECALL[(CP-RECALL)]
  CP_RECALL --> CL_SCOPE{CL-SCOPE coding?}

  CL_SCOPE -->|non-coding| ROUTE_OTHER[Upstream skill]
  ROUTE_OTHER --> CL_REFINE{CL-REFINE build ask?}
  CL_REFINE -->|yes| CL_SCOPE
  CL_REFINE -->|no| EXIT_NONCODE([Exit · non-coding])

  CL_SCOPE -->|coding| CL_COMPLEXITY{CL-COMPLEXITY}
  CL_COMPLEXITY -->|1-file| DIRECT[Direct fix]
  DIRECT --> COMPOUND_LITE[Compound-lite]
  COMPOUND_LITE --> EXIT_DIRECT([Exit · patched])

  CL_COMPLEXITY -->|multi-module or rebuild| CL_RESUME{CL-RESUME}
  CL_RESUME -->|new| NEW_SESSION[erpaval-new.py · scaffold session-hex]
  CL_RESUME -->|resume| LOAD_PRIOR[Read prior session-hex · append to raw_request]
  NEW_SESSION --> CL_DIR{CL-DIR}
  LOAD_PRIOR --> CL_DIR
  CL_DIR -->|empty| GREENFIELD[Greenfield]
  CL_DIR -->|existing| BROWNFIELD[Brownfield]
  CL_DIR -->|rebuild-in-place| RIPREPLACE[Rip-and-replace]

  GREENFIELD --> CL_RIGOR{CL-RIGOR}
  BROWNFIELD --> CL_RIGOR
  RIPREPLACE --> CL_RIGOR

  CL_RIGOR -.->|fuzzy| FRAME_HMW[Frame HMW]
  FRAME_HMW --> CP_HMW[(CP-HMW)]
  CP_HMW --> FRAME_EARS
  CL_RIGOR -.->|contract unclear| FRAME_EARS[Frame EARS]
  FRAME_EARS --> CP_EARS[(CP-EARS)]
  CL_RIGOR -->|crisp| CL_SPEC{CL-SPEC ready?}
  CP_EARS --> CL_SPEC

  CL_SPEC -->|no PRD| UP_PRD[/product-discovery]
  UP_PRD --> CL_SPEC
  CL_SPEC -->|no stack| UP_STACK[/build-stack]
  UP_STACK --> CL_SPEC
  CL_SPEC -->|fuzzy| UP_DESIGN[/product-discovery]
  UP_DESIGN --> CL_SPEC
  CL_SPEC -->|ready| HANDOFF_B([to §B])
```

## §B — Build loop

Explore through Act, with four cycles: C1 / C1b / C1c (plan, re-explore, reframe), C2 (in-task fix), C3 (missing-prereq replan), C6 (wave progression).

```mermaid
flowchart LR
  FROM_A([from §A]) --> PREP[Preparation complete]
  PREP --> PH_EXPLORE[Phase Explore]
  PREP --> PH_RESEARCH[Phase Research]

  PH_EXPLORE --> CP_EXPLORE[(CP-EXPLORE)]
  PH_RESEARCH --> CP_RESEARCH[(CP-RESEARCH)]

  CP_EXPLORE --> GATE_ER{Gate 0 E+R done?}
  CP_RESEARCH --> GATE_ER
  GATE_ER -->|no| WAIT_ER[Wait · wc -l poll]
  WAIT_ER --> GATE_ER
  GATE_ER -->|yes| PH_PLAN[Phase Plan · derive tasks from EARS]

  PH_PLAN --> CP_PLAN[(CP-PLAN)]
  CP_PLAN --> GATE_1{Gate 1 user approves?}
  GATE_1 -.->|C1 revise| PH_PLAN
  GATE_1 -.->|C1b deeper| PH_EXPLORE
  GATE_1 -.->|C1c reframe| FROM_A
  GATE_1 -->|approved| PH_ACT[Phase Act · waves]

  PH_ACT --> CP_TASK[(CP-TASK-N)]
  CP_TASK --> MONITOR[Monitor · wc -l + eager unblock]
  MONITOR --> TASK_RESULT{Task result?}
  TASK_RESULT -.->|C2 lint/type fail| FIX_SEND[SendMessage]
  FIX_SEND --> MONITOR
  TASK_RESULT -.->|C3 missing prereq| REPLAN[Insert task · replan]
  REPLAN --> PH_PLAN
  TASK_RESULT -->|success| WAVE_CHECK{Wave done?}
  WAVE_CHECK -.->|C6 next wave| PH_ACT
  WAVE_CHECK -->|all done| HANDOFF_C([to §C])
```

`PH_EXPLORE`, `PH_RESEARCH`, and `PH_ACT` are **fan-out phases**. Each launches
many parallel subagents in one message, not one agent. Explore fans out by
perspective, Research by library or domain, Act by wave task. Research also
carries the grounding mandate: no library or version claim leaves Research
un-grounded. See `fan-out.md` for counts and `orchestrator.md` § Research for the
grounding rule.

## §C — Validate · merge · compound

Three validation layers run in sequence. Gate 2 auto-merges if clean; otherwise human dispositions findings. After merge, Compound extracts lessons from the session trace — this is what makes N+1 smarter than N.

```mermaid
flowchart LR
  FROM_B([from §B]) --> PH_VALIDATE[Phase Validate]
  PH_VALIDATE --> V1[L1 static]
  V1 --> V2[L2 quality]
  V2 --> V3[L3 security]
  V3 --> CP_VALIDATION[(CP-VALIDATION)]

  CP_VALIDATION --> CL_VALIDATE{All green?}
  CL_VALIDATE -.->|C4 fail| FIX_CYCLE[Re-open failing tasks]
  FIX_CYCLE --> BACK_B([back to §B])
  CL_VALIDATE -->|pass| GATE_2{Gate 2 auto-merge?}

  GATE_2 -->|clean| MERGE[Auto-merge]
  GATE_2 -->|findings| HUMAN[Human review]
  HUMAN --> CL_DISP{Disposition?}
  CL_DISP -.->|C5 fix| FIX_CYCLE
  CL_DISP -->|accept| MERGE

  MERGE --> PH_COMPOUND[Phase Compound]
  PH_COMPOUND --> CL_LESSONS{CL-LESSONS novel?}
  CL_LESSONS -->|yes| WRITE_LESSONS[Write .erpaval/solutions/]
  CL_LESSONS -->|no| SKIP_LESSONS[Session-only]
  WRITE_LESSONS --> CP_LESSONS[(CP-LESSONS)]
  SKIP_LESSONS --> CP_SESSION
  CP_LESSONS --> CP_SESSION[(CP-SESSION)]
  CP_SESSION --> DONE([Done])
```

`PH_VALIDATE` fans out too. The quality and security layers each split into
parallel dimension reviewers, launched in one message. Per-finding adversarial
verification then runs before Gate 2. See `fan-out.md` and
`validation-playbook.md`.

---

## Named cycles

Cycles are the adaptive core — they let the flow recover from premature planning, missing context, or bad implementations without restarting. Each has a bounded re-entry point and a persistence contract.

| ID    | Name                  | Trigger                                              | Re-entry point                                                                         |
| ----- | --------------------- | ---------------------------------------------------- | -------------------------------------------------------------------------------------- |
| `C1`  | Plan revision         | Gate 1 rejection — user amends scope or architecture | Plan. Each revision diffs `CP-PLAN`; history kept. Expect 2-4 iterations.              |
| `C1b` | Deeper context        | Gate 1 reveals Explore missed a critical area        | Explore with a scoped prompt. Only the gap is re-explored.                             |
| `C1c` | Reframe problem       | Gate 1 reveals the problem itself was wrong          | HMW framing. Rare but valuable — EARS spec gets regenerated.                           |
| `C2`  | In-task fix           | Lint / type / unit-test fail inside a subagent       | Same subagent via `SendMessage`. Cap 3 attempts; orchestrator escalates on attempt 4.  |
| `C3`  | Missing prereq replan | Subagent reports "I need X that doesn't exist yet"   | Plan. Insert missing task, re-wire `addBlockedBy`, resume Act where safe.              |
| `C4`  | Validation fail       | Any of 3 validation layers returns red               | Act. Re-open failing tasks with scoped fix packets. Validate re-runs.                  |
| `C5`  | Human fix disposition | Gate 2 finding accepted by reviewer as "must fix"    | Act. Same as C4 with human-authored fix instructions.                                  |
| `C6`  | Wave progression      | Current Act wave complete, more waves in plan        | Act. Self-loop with eager unblocking — launch next-wave tasks as their blockers clear. |

### Disambiguating C1 / C1b / C1c

All three fire on Gate 1 rejection. Pick by the shape of the user's feedback:

- Scope or architecture is wrong → **C1** (plan revision).
- A specific part of the codebase wasn't explored → **C1b** (deeper context).
- The problem statement itself was off → **C1c** (reframe HMW).

### C2 protocol

Resume the same subagent with a scoped fix message. Cap at 3 attempts; on attempt 4 the orchestrator runs `CL-C2` (see `classifiers.md`) against the packet, the agent's last output, and the error. CL-C2 returns one of `fix-directly` (orchestrator applies 1-2 line fix inline), `respawn` (fresh agent, same packet), or `missing-prereq` (route to C3).

### C3 protocol

1. Read the agent's report.
2. `TaskCreate(subject="Add X prereq", ...)`.
3. `TaskUpdate(taskId=new, addBlockedBy=[...])` and `TaskUpdate(taskId=original, addBlockedBy=[new])`.
4. Launch the prereq task.
5. When prereq completes, resume the original task with updated context.

Missing prereqs often indicate the EARS spec was incomplete — consider revising `spec.md` so future sessions don't repeat the gap.

### C4 / C5 protocol

Re-open only the failing tasks. Layer 1 re-runs on touched files only (fast); Layers 2-3 re-run on the full diff.

### C6 — eager unblocking

After every task completion, scan the dependency graph for tasks whose blockers are now clear. Launch them immediately, even if originally scheduled for a later wave. On a 26-task session this saves ~30-40% wall-clock time versus strict wave-by-wave execution.

Example: Wave 2 = [A, B, C]; Wave 3 = [D, E] where D depends only on A. When A completes, launch D — don't wait for B and C.
