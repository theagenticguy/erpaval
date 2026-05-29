# Fan-out — how many subagents per phase, and how to launch them

ERPAVal is subagent-driven by design. The orchestrator (main Claude Code
session) holds gate state and composes context; **the actual work happens in
parallel subagents**, not inline in the orchestrator thread. This file is the
single source of truth for how wide each phase fans out. Every other reference
links here instead of restating counts.

Terms like `CP-*`, Gate 0/1/2, Wave are defined in `glossary.md`.

## The rule, stated once and applied everywhere

Launch all subagents for a phase in **one message** with multiple `Agent` calls
and `run_in_background: true`. Current Claude models under-delegate by default
and will tend to do the phase sequentially in the main thread — the fan-out must
be explicit. Do not work a fan-out phase inline in the orchestrator thread.

This is the most common ERPAVal under-performance: running Explore as one agent,
Research as one agent, Validate as one agent, and the Act wave one task at a
time. Each of those is a fan-out point. Treat single-agent execution of a
fan-out phase as a bug.

## Per-phase fan-out targets

| Phase        | Subagents to launch                                                          | Agent type        | Launch                |
| ------------ | ---------------------------------------------------------------------------- | ----------------- | --------------------- |
| **Explore**  | **4–7 perspective agents** (brownfield)                                      | `Explore`         | one message, parallel |
| **Research** | **one agent per library/domain**, floor of 2 when any new dep/API is in play | `researcher`      | one message, parallel |
| **Act**      | **every task in the wave** + eager-unblock as blockers clear                 | `general-purpose` | one message per wave  |
| **Validate** | **4–8 dimension agents** (quality + security split into sub-dimensions)      | `opus`            | one message, parallel |

### Explore — fan out by perspective

One agent per lens, each owning a slice of the mental model:

- architecture and module boundaries
- data model, schemas, and the contracts between modules
- test infrastructure and fixture style
- conventions, naming, error-handling, async discipline
- integration points and touch-points for the change
- build and toolchain (`mise.toml`, `pyproject.toml`, `package.json`)

Pick 4–7 of these per the codebase size. Each writes its own `explore-<n>.yaml`,
so parallel agents never collide. **Rip-and-replace** runs this set twice — once
over the system being replaced, once over the reference/target architecture.

### Research — fan out by domain, ground every claim

Split the research surface into domains — one researcher per library, framework,
or subsystem — and launch them together. Floor of 2 whenever the task pulls in a
new dependency or API. The grounding mandate (every version pin and API surface
cited to a current source, Context7-first) is non-negotiable and lives in
`orchestrator.md` § Research; the tool inventory and priority order live in
`${CLAUDE_PLUGIN_ROOT}/skills/research/references/search-strategies.md`.

### Act — fan out by task within the wave

Wave 1 scaffold is orchestrator-run (see `orchestrator.md` § Act). Every other
wave: launch all of the wave's tasks in one message, each as its own
backgrounded `Agent` editing its own packet file. Eager unblocking (cycle C6)
launches later-wave tasks the moment their individual blockers clear — don't
wait for sibling tasks to finish.

### Validate — fan out by dimension

Replace the monolithic "one quality agent + one security agent" with a set of
read-only Opus reviewers, each owning one axis, all launched together:

- **Quality**: tech-debt / coupling · DRY violations · dead code · convention
  drift · API surface
- **Security**: injection · auth/authz · crypto · data exposure · dangerous-API
  / deserialization

Group the axes into 4–8 agents based on changeset size. Per-finding adversarial
verification runs after — see `validation-playbook.md`.

## Concurrency hygiene

Sub-batch into messages of **≤ 10 concurrent spawns** each so the harness
doesn't choke. A 14-agent Explore+Validate burst is two back-to-back messages,
not one. Within a batch, every agent is `run_in_background: true` so results come
back as ~100–300-token summaries rather than full transcripts dumped into the
orchestrator's context.

## Stuck detection applies to every fan-out

The `wc -l` monitor and fresh-relaunch recovery in `orchestrator.md` § Monitor
apply to all parallel agents, not just Act. A perspective or dimension agent
whose output file is unchanged across two check-ins is stuck — relaunch it with a
prompt that lists the sections already complete. The filesystem is the source of
truth; agent notifications arrive out of order.

## Cost framing — know what you're ordering

A full ERPAVal run on a real feature spends significant tokens: 4–7 Explore
agents, N researchers, parallel Act waves, and 4–8 Validate reviewers, several of
them Opus. That is the intended trade — correctness and wall-clock speed over API
cost. The user invoked an autonomous-development flow because they want the
fan-out; ship it. Scale the counts down only for genuinely small changes (and
`CL-COMPLEXITY` already routes 1-file fixes out of the flow entirely).
