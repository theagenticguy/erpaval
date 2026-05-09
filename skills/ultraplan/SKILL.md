---
name: ultraplan
description: >
  Generator-critic planning. Launches 3 parallel Opus 4.7 explorers with distinct
  divergence vectors (architectural, speed-first, simple-first), each producing an
  independent plan, then runs a critic synthesis that composes the best elements
  into a single plan with per-decision attribution. Defeats single-agent anchoring.
  Use when the user asks to plan a non-trivial task, design an approach, compare
  implementation strategies, or wants multiple angles on a problem before coding.
arguments:
  - name: problem
    description: The problem to plan. One or two sentences is enough.
    required: false
user_facing: true
---

## Contents

| Reference                          | When to load                                      |
| ---------------------------------- | ------------------------------------------------- |
| `references/orchestrator.md`       | Running `/ultraplan <problem>` — the 5-phase flow |
| `references/divergence-vectors.md` | The three explorer biases and their motivation    |
| `references/write-protocol.md`     | Copy verbatim into every explorer prompt          |
| `templates/explorer-skeleton.md`   | Per-explorer plan skeleton                        |
| `templates/plan-skeleton.md`       | Final composed plan skeleton                      |

# Ultraplan

Generator-critic planning, file-coordinated. Three Opus 4.7 explorers plan the same problem in parallel, each biased toward a different axis — architectural, speed-first, simple-first. A critic reads all three and composes a final plan that cherry-picks the best decision from each, with attribution. The user gets one clean `plan.md` to execute against.

Beats single-agent planning on two axes:

- **No anchoring.** A single agent commits to the first approach it reaches and defends it through the rest of the plan. Three independent explorers reach genuinely different conclusions, and the critic picks per-decision.
- **Calibrated confidence.** When all three converge, the approach is sound. When they diverge, the critic names the tradeoff explicitly.

## How it works

Read `references/orchestrator.md` and follow its phases. Short version:

1. **Intake** — parse the problem. One targeted `AskUserQuestion` only if scope is genuinely ambiguous; otherwise proceed.
2. **Skeletons** — create `planning/{slug}/` with three explorer files and a `plan.md` shell.
3. **Launch** — three `general-purpose` Opus 4.7 Agents in parallel, `run_in_background: true`, each with a distinct divergence vector from `references/divergence-vectors.md`. Orchestrator does not read the codebase; explorers do.
4. **Monitor** — escalating check-ins (30s → 2m → 5m). `wc -l` on explorer files; stuck detection via line-count delta; launch a fresh Agent with "resume from section N" context on stall.
5. **Critic synthesis** — one foreground `general-purpose` Opus 4.7 Agent reads all three explorer files and writes `plan.md` — chosen approach, per-decision attribution, explicit tradeoffs, step-by-step order, verification criteria.

## Write discipline

Every explorer prompt carries the write protocol verbatim from `references/write-protocol.md`: think → edit the file with the decision → next consideration. Partial plans written to disk survive timeouts; plans held in working memory do not.

## Cost note

Three parallel Opus 4.7 explorers plus one critic synthesis. Significant token spend per run — worth it for meaningful planning decisions, not for trivial refactors. The user invoked `/ultraplan` because they want the divergence; ship it.
