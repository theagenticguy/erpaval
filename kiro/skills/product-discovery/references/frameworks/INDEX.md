# Product-Discovery Frameworks — Routing Guide

First thing a product-discovery orchestrator or role reads when deciding which framework(s) to run. This file covers BOTH discovery frameworks (upstream, problem-space) and spec frameworks (downstream, contract-shaped) because they compose as a single pipeline: discovery → HMW / JTBD → candidate directions → user stories / EARS / Gherkin. It routes to per-framework files in the same directory; it does not restate their canonical structures. When a role already knows it needs one specific framework, read that file directly and skip this index.

## Discovery frameworks — when to use

Reach for a discovery framework when the user has a situation but not a solution, when insights are mounting but the problem statement has not been sharpened, when stakeholders disagree on what to build because they disagree on what the real problem is. Discovery frameworks convert "we should look at X" into a bounded, framed, research-grounded question set that a downstream PRD or spec can execute against.

| User signal / ask                                        | Framework file                                                                    | One-line why                                                                          |
| -------------------------------------------------------- | --------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| "We need to run a discovery round"                       | `${ERPAVAL_HOME}/skills/product-design-shared/references/double-diamond.md` | Gives the team a shared cadence — diverge, converge, diverge, converge.               |
| "We have a fuzzy problem and no obvious owner framework" | `${ERPAVAL_HOME}/skills/product-design-shared/references/double-diamond.md` | The diamond structure surfaces the ownership question naturally.                      |
| "The team keeps converging too early"                    | `${ERPAVAL_HOME}/skills/product-design-shared/references/double-diamond.md` | The divergent-then-convergent rhythm is literally why this framework exists.          |
| "Turn these interview notes into opportunity questions"  | `how-might-we.md`                                                                 | Converts research-backed observations into 3-5 outcome-level frames.                  |
| "Reframe this — it feels solution-shaped"                | `how-might-we.md`                                                                 | The 9-strategy move set is built for solution-hidden problems.                        |
| "We're at the 'we have insights' phase"                  | `how-might-we.md`                                                                 | HMW converges insights into outcome-level questions without committing to a solution. |
| "Who is hiring this product and for what job?"           | `jtbd-job-stories.md`                                                             | Centers situations and motivation; strips out persona noise.                          |
| "Write job stories from these customer interviews"       | `jtbd-job-stories.md`                                                             | Klement's "When/I want/So I can" shape is the canonical JTBD output.                  |

## Spec frameworks — when to use

Reach for a spec framework when the PRD is written or the problem is otherwise framed and you need to cut the work into units that an engineer, an AI coding agent, or a test runner can execute against. These frameworks are contract-shaped: they name what "done" looks like in a way that can be verified mechanically or reviewed point-by-point.

| User signal / ask                                        | Framework file           | One-line why                                                       |
| -------------------------------------------------------- | ------------------------ | ------------------------------------------------------------------ |
| "Write acceptance criteria for this user-facing feature" | `user-stories-invest.md` | Agile baseline; backlog-ready; pairs with Gherkin scenarios.       |
| "Define backlog items for the next sprint"               | `user-stories-invest.md` | INVEST keeps stories independent, small, testable.                 |
| "Spec this feature for Kiro / Spec Kit / AI coder"       | `ears.md`                | Structured syntax is machine-parseable; Kiro makes EARS canonical. |
| "The contract has multiple valid 'done' interpretations" | `ears.md`                | Invariants + unwanted-behavior templates eliminate ambiguity.      |
| "High-regression-risk path — auth, billing, data"        | `ears.md`                | Unwanted-behavior template forces explicit failure-mode specs.     |
| "Write BDD scenarios we can automate"                    | `gherkin.md`             | Cucumber-runnable; happy path + named edge cases.                  |
| "Turn this user story into executable tests"             | `gherkin.md`             | Given/When/Then maps 1:1 to Cucumber step definitions.             |

Common heuristic: **user stories for feature framing → EARS for contract-unclear paths (AI coder specs, regulatory, high-regression-risk) → Gherkin for test-driven acceptance.** Modern Kiro and Spec Kit teams use all three — EARS for invariants, Gherkin for scenarios, user stories for backlog items.

## Composing discovery → spec

The natural pipeline runs top-down through this index:

- **Double Diamond structures the whole round.** HMW sits at the Define → Develop transition; JTBD interviews live in Discover.
- **HMW feeds JTBD framing.** Once you have 3-5 HMW candidates, write a job story for the top one to sharpen the "who, when, why" before handing to a PRD.
- **JTBD job stories feed user stories.** Job stories are upstream (reframing around progress); user stories are downstream (backlog-ready). The job story's situation becomes the user story's role-and-context; the job story's outcome becomes the acceptance criterion.
- **User stories carry acceptance criteria in EARS and/or Gherkin.** One story, multiple ACs — the formats don't conflict. Use EARS for invariants and unwanted behavior; use Gherkin for concrete scenarios.
- **EARS is the contract-unclear path instead of user stories.** For AI-coder specs, safety-critical paths, or high-regression-risk work, EARS is the primary artifact; the user-story wrapper is optional.
- **The PRD consumes user stories.** See `assets/prd-template.md` section 5.1 (user-story table) and sections 9-10 (EARS-style NFRs and edge cases).

## When to skip

- **The ask is business-strategy work** (Rumelt kernel, Wardley map, PR-FAQ-as-discovery). Route to `product-strategy`.
- **The ask is a long-form narrative.** Strategy and discovery produce the thinking; hand the artifacts to whatever narrative-writing workflow your team uses.
- **The problem is already well-framed with a metric** ("reduce p95 latency below 800ms"). Skip HMW, go straight to spec.

## Framework file index

Discovery (upstream, problem-space):

- `${ERPAVAL_HOME}/skills/product-design-shared/references/double-diamond.md` — Design Council's four-stage divergent/convergent rhythm (Discover / Define / Develop / Deliver). Use as the round-level cadence.
- `how-might-we.md` — NN/g template + d.school nine reframing strategies. Use to convert insights into outcome-level questions.
- `jtbd-job-stories.md` — Klement's "When X, I want Y, so I can Z" format. Use to re-frame around customer progress and skip persona noise.

Spec (downstream, contract-shaped):

- `user-stories-invest.md` — "As a / I want / so that" with Wake's INVEST rubric. Use for backlog-ready items.
- `ears.md` — Five templates + Complex composite (Ubiquitous, Event-driven, State-driven, Optional, Unwanted). Use for AI-coder specs, invariants, and high-regression-risk paths.
- `gherkin.md` — Given/When/Then scenarios for BDD tooling (Cucumber, SpecFlow, Behave). Use for executable acceptance tests.
