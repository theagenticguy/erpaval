# Product Discovery Orchestrator

The orchestrator runs inside a forked subagent so the main conversation stays clean of check-in noise and intermediate research. It routes the user's ask through one of five routes, spawns general-purpose `Agent`s with inline role prompts, watches output files with `wc -l`, and composes the final artifact.

Terms:

- `{{ slug }}` — kebab-case slug derived from the user's brief or a title hint, trimmed to ~40 chars.
- `product-discovery/{{ slug }}/` — the working directory; all files live here.
- All role prompts carry the write-protocol block verbatim from `${ERPAVAL_HOME}/skills/product-discovery/references/write-protocol.md`.

---

## Inputs

- The user's brief, parsed from `$ARGUMENTS`.
- `${ERPAVAL_HOME}/skills/product-discovery/references/write-protocol.md` — pasted into every role prompt.
- `${ERPAVAL_HOME}/skills/product-discovery/references/roles/` — nine role files (product-analyst, system-architect, research-scout, hmw-framer, ears-specifier, discovery-lead, jtbd-interviewer, prd-synthesizer, discovery-critic).
- `${ERPAVAL_HOME}/skills/product-discovery/assets/` — seven skeletons (prd-template, worklog-skeleton, discovery-memo, jtbd-skeleton, double-diamond-workbook, hmw-skeleton, ears-spec-skeleton).
- `${ERPAVAL_HOME}/skills/product-discovery/references/inference-heuristics.md` — for PRD-route signal parsing.
- `${ERPAVAL_HOME}/skills/product-discovery/references/quality/prd.md` — PRD-route quality bar.
- `${ERPAVAL_HOME}/skills/product-discovery/references/frameworks/INDEX.md` — routing guide covering BOTH discovery and spec frameworks (decision tables + discovery → spec composition). Per-framework files live in the same `frameworks/` directory — `double-diamond.md`, `how-might-we.md`, `jtbd-job-stories.md`, `user-stories-invest.md`, `ears.md`, `gherkin.md` — load only the file(s) a role needs.
- `${ERPAVAL_HOME}/skills/product-discovery/references/methodology/discovery-rounds.md` — six-phase methodology.

---

## Phase tracking

Before Phase 0, add 6 todo items via Kiro `/todo` — Route, Frame, Parallel execution, Synthesize, Critic review, Deliver. During Phase 2, additionally `/todo add` one item per role in the selected fan-out (e.g., product-analyst / system-architect / research-scout for the PRD route) and `/todo complete <n>` each when its work log shows `Status: COMPLETE`. The `/todo` mirror is advisory; the work-log files on disk are the source of truth.

---

## Phase 0 — Route

Before any subagent runs, identify which route this ask takes. The table routes on the user's utterance and whatever source material they provided.

| User signal                                                                 | Route           | Primary output                               |
| --------------------------------------------------------------------------- | --------------- | -------------------------------------------- |
| "write a PRD", "draft requirements", "spec out an app", one-sentence idea   | PRD             | `{product-slug}-prd.md` (15 sections)        |
| "brainstorm a product", "run discovery", "think through UX for…"            | Discovery round | `discovery-memo.md`                          |
| "turn these notes into HMW", "reframe this as HMW", emotional framing       | HMW-only        | `brainstorms/NNN-{{ slug }}-requirements.md` |
| "spec this for Kiro / Spec Kit", "write EARS ACs", contract-unclear feature | EARS-only       | `specs/NNN-{{ slug }}/spec.md`               |
| "write job stories for [segment] from these tickets"                        | JTBD-only       | `jtbd-job-stories.md`                        |

Default-in-doubt: PRD route. The PRD absorbs the most source-material shapes and the 3-role parallel research pattern is the skill's strongest lane.

Also gate: if the brief is genuinely ambiguous (audience unknown, source material unclear), ask the user up to 4 clarifying questions in a single message to resolve. Then proceed. Do not loop.

---

## Phase 1 — Frame

One foreground agent (the `discovery-lead` role) produces a `framing.md`. For the PRD route, this phase is abbreviated — the existing prd-drafter intake-capture heuristic runs and the framing.md collapses to a one-paragraph frame plus the Intent Profile.

### PRD route — abbreviated framing

Skip the discovery-lead agent. Instead, run the Intent Profile capture heuristic inline in the forked orchestrator:

1. Parse the user's idea using `${ERPAVAL_HOME}/skills/product-discovery/references/inference-heuristics.md`. Extract every signal (app type, core features, personas, scale, deployment, auth, data persistence, complexity).
2. Build the Intent Profile table. Present it inline with confidence levels.
3. Ask up to 3-4 genuine-ambiguity questions in a single message. Do not ask about tech choices (that's `/build-stack`) or obvious things the user already said.
4. Lock the Intent Profile after user confirmation. This is the frame input for Phase 2.

Write the frozen Intent Profile into `product-discovery/{{ slug }}/framing.md`. It becomes input to the three parallel research roles.

### Discovery-round / HMW-only / EARS-only / JTBD-only routes — full framing

Spawn the `discovery-lead` role with this prompt:

```text
You are the discovery lead framing a {{ route }} run. Read the user's brief in full and produce a short framing document that seeds Phase 2.

<scope>
Source: {{ user_brief_or_file_path }}
Route: {{ route }}
Slug: {{ slug }}

Your work log: product-discovery/{{ slug }}/framing.md
</scope>

<role_reference>
${ERPAVAL_HOME}/skills/product-discovery/references/roles/discovery-lead.md
</role_reference>

<responsibilities>
1. Pain-point excavation — observed friction, trigger situation, emotional texture, fixed-feels-like.
2. Routing call — which of HMW / JTBD / research-scout this run needs. Record rationale.
3. Vocabulary mapping preview — flag the likely framework for Phase 4.

Keep framing.md under ~80 lines. You are a seed, not the full round.
</responsibilities>

<write_protocol>
{{ paste ${ERPAVAL_HOME}/skills/product-discovery/references/write-protocol.md verbatim }}
</write_protocol>

<quality_bar>
- Problem section cites 3+ sources from the user's material.
- Routing call is explicit with one-sentence rationale.
- Flip Status: IN PROGRESS → COMPLETE when done. Final step: call the built-in `summary` tool with a 1-2 paragraph result; return nothing else.
</quality_bar>
```

Run foreground. Proceed to Phase 2 when the agent flips framing.md to COMPLETE.

---

## Phase 2 — Parallel execution

Fan-out depends on the route. In every case, launch parallel NL subagent dispatches (`> Use a general-purpose agent to ...`) in a **single turn** — one dispatch per role. All NL dispatches run in the background; Kiro caps active subagents at 4. The orchestrator agent's JSON sets `model` per agent (typically `claude-opus-4-7`); per-invocation model selection is not supported.

Seed each subagent's output file from the matching template before launching — no subagent faces a blank file. Each subagent also gets a work log seeded from `assets/worklog-skeleton.md` with role filled in.

### PRD route — three parallel roles

Launch three subagents in one turn. Each writes to its own work log; all three contribute sections to the PRD that the synthesizer assembles in Phase 3.

- Role 1: `product-analyst` → `work-log-product-analyst.md` → owns PRD sections 1, 2, 3, 4, 5, 6, 12.
- Role 2: `system-architect` → `work-log-system-architect.md` → owns PRD sections 7, 8, 9, 10.
- Role 3: `research-scout` → `work-log-research-scout.md` → owns PRD sections 11, 13.

Role prompt template (one per role — fill in role-specific fields):

```text
You are a product-discovery researcher in the {{ role }} role.

<role_reference>
${ERPAVAL_HOME}/skills/product-discovery/references/roles/{{ role }}.md
</role_reference>

<scope>
Frozen Intent Profile: product-discovery/{{ slug }}/framing.md
Working directory: product-discovery/{{ slug }}/
Your work log: product-discovery/{{ slug }}/work-log-{{ role }}.md
PRD template to fill: product-discovery/{{ slug }}/{{ product-slug }}-prd.md (seeded from prd-template.md)
</scope>

<reference_material>
${ERPAVAL_HOME}/skills/product-discovery/references/inference-heuristics.md
${ERPAVAL_HOME}/skills/product-discovery/references/quality/prd.md
${ERPAVAL_HOME}/skills/product-discovery/assets/prd-template.md
</reference_material>

<user_brief>
{{ the user's original idea, verbatim }}
</user_brief>

<write_protocol>
{{ paste ${ERPAVAL_HOME}/skills/product-discovery/references/write-protocol.md verbatim }}
</write_protocol>

{{ role-specific responsibilities block pulled from the role file }}

When every owned section has real content, flip Status: IN PROGRESS → COMPLETE on your work log.
```

### Discovery-round route — 2-3 parallel roles

The discovery-lead's routing call in Phase 1 decides the fan-out. Default: discovery-lead runs further in Phase 3; HMW and JTBD fire in Phase 2 only if framing.md flagged them.

- Always: none (discovery-lead is the synthesizer for this route; fan-out is framework-driven).
- Optional: `hmw-framer` → `brainstorms/NNN-{{ slug }}-requirements.md`.
- Optional: `jtbd-interviewer` → `jtbd-job-stories.md`.
- Optional: `research-scout` → `competitive-scan.md` if landscape depth is needed.

Launch whatever framing.md flagged in one turn. Write role prompts from the corresponding role files.

### HMW-only route — one agent

Dispatch `hmw-framer` via NL: `> Use a general-purpose agent to act as the hmw-framer role`. Single subagent (foreground, single subagent):

```text
You are the HMW framer. Read the user's brief and produce 3-5 outcome-level "How might we" questions that pass NN/g validation.

<role_reference>
${ERPAVAL_HOME}/skills/product-discovery/references/roles/hmw-framer.md
</role_reference>

<scope>
Source: {{ user_brief_or_file_path }}
Your output: brainstorms/NNN-{{ slug }}-requirements.md (seeded from hmw-skeleton.md)
</scope>

<reference_material>
${ERPAVAL_HOME}/skills/product-discovery/references/frameworks/how-might-we.md
</reference_material>

<write_protocol>
{{ paste write-protocol verbatim }}
</write_protocol>

Follow the 4-step process in the role reference. Flip Status: IN PROGRESS → COMPLETE when every HMW passes NN/g validation. Final step: call the built-in `summary` tool with a 1-2 paragraph result; return nothing else.
```

### EARS-only route — one agent

Dispatch `ears-specifier` via NL: `> Use a general-purpose agent to act as the ears-specifier role`. Single subagent:

```text
You are the EARS specifier. Read the user's feature brief and write dependency-aware acceptance criteria in the five EARS templates.

<role_reference>
${ERPAVAL_HOME}/skills/product-discovery/references/roles/ears-specifier.md
</role_reference>

<scope>
Source: {{ user_brief_or_file_path }}
Your output: specs/NNN-{{ slug }}/spec.md (seeded from ears-spec-skeleton.md)
Optional: brainstorms/NNN-{{ slug }}-requirements.md (if HMW was run first; cite in frontmatter)
</scope>

<reference_material>
${ERPAVAL_HOME}/skills/product-discovery/references/frameworks/ears.md
</reference_material>

<write_protocol>
{{ paste write-protocol verbatim }}
</write_protocol>

Follow the process in the role reference. Every AC uses one of the five templates literally. Every AC has [P] or Dependencies:. Flip Status: IN PROGRESS → COMPLETE when done. Final step: call the built-in `summary` tool with a 1-2 paragraph result; return nothing else.
```

### JTBD-only route — one agent

Dispatch `jtbd-interviewer` via NL: `> Use a general-purpose agent to act as the jtbd-interviewer role`. Single subagent:

```text
You are the JTBD interviewer. Read the PM-provided source material (interview notes, tickets, quotes) and produce Klement-style job stories.

<role_reference>
${ERPAVAL_HOME}/skills/product-discovery/references/roles/jtbd-interviewer.md
</role_reference>

<scope>
Source material: {{ paths to notes, tickets, quotes }}
Your output: jtbd-job-stories.md (seeded from jtbd-skeleton.md)
</scope>

<reference_material>
${ERPAVAL_HOME}/skills/product-discovery/references/frameworks/jtbd-job-stories.md
</reference_material>

<write_protocol>
{{ paste write-protocol verbatim }}
</write_protocol>

Every job story cites at least one source. No persona-simulator entries. Flip Status: IN PROGRESS → COMPLETE when done. Final step: call the built-in `summary` tool with a 1-2 paragraph result; return nothing else.
```

### Monitor (all routes with parallel agents)

Escalating check-ins: 30s → 2m → 5m → every 5m.

At each check-in, `wc -l` across all active work logs:

```bash
wc -l product-discovery/{{ slug }}/work-log-*.md product-discovery/{{ slug }}/*.md
```

Report compactly:

```text
Phase 2 check-in #2:
- product-analyst:   142 lines, personas done, user stories in progress
- system-architect:   98 lines, NFRs done, data models in progress
- research-scout:    156 lines, 5 competitors analyzed, matrix in progress
```

### Stuck detection

A work log with unchanged line count across two consecutive check-ins is stuck. Re-dispatch via NL with the existing file state and a "skip completed sections" prompt so the new subagent doesn't re-do work. Never wait for a stuck subagent to self-correct. (Kiro has no `kill --background` primitive — let the original drain.)

---

## Phase 3 — Synthesize

One foreground agent composes the final artifact.

### PRD route — `prd-synthesizer`

Dispatch `prd-synthesizer` via NL: `> Use a general-purpose agent to act as the prd-synthesizer role`. Single subagent:

```text
You are the PRD synthesizer. Read the three parallel work logs and compose the final PRD.

<role_reference>
${ERPAVAL_HOME}/skills/product-discovery/references/roles/prd-synthesizer.md
</role_reference>

<scope>
Input work logs:
- product-discovery/{{ slug }}/work-log-product-analyst.md
- product-discovery/{{ slug }}/work-log-system-architect.md
- product-discovery/{{ slug }}/work-log-research-scout.md

Frozen Intent Profile: product-discovery/{{ slug }}/framing.md

Your output: product-discovery/{{ slug }}/{{ product-slug }}-prd.md (template already seeded)
</scope>

<reference_material>
${ERPAVAL_HOME}/skills/product-discovery/references/quality/prd.md
</reference_material>

<write_protocol>
{{ paste write-protocol verbatim }}
</write_protocol>

Follow the 7-step process in the role reference. Resolve contradictions per the priority order. Build Sections 14 and 15. Run the cross-section consistency pass. Flip Status: IN PROGRESS → COMPLETE when the quality bar passes. Final step: call the built-in `summary` tool with a 1-2 paragraph result; return nothing else.
```

### Discovery-round route — `discovery-lead` (return)

The discovery-lead runs a second pass, this time composing `discovery-memo.md` from the Phase 2 outputs it orchestrated. Seed from `assets/discovery-memo.md`.

### HMW-only / EARS-only / JTBD-only — no synthesis

The single-agent output is the final artifact. Skip Phase 3; go straight to Phase 3.5.

---

## Phase 3.5 — Critic review

Dispatch `discovery-critic` via NL: `> Use a general-purpose agent to act as the discovery-critic role`. Single subagent:

```text
You are the discovery critic. Read the synthesized artifact and write a rubric-graded review.

<role_reference>
${ERPAVAL_HOME}/skills/product-discovery/references/roles/discovery-critic.md
</role_reference>

<scope>
Artifact under review: {{ path to final artifact }}
Synthesis log (if present): {{ path to synthesis log at bottom of artifact }}
Your output: product-discovery/{{ slug }}/review-critic.md
</scope>

<write_protocol>
{{ paste write-protocol verbatim }}
</write_protocol>

Score the rubric per dimension (Problem grounding, Coherence, Specificity, Scope integrity, Evidence hygiene, Structural compliance). Set overall score. Prioritize findings (critical / warning / suggestion). Flip Status: IN PROGRESS → COMPLETE when all dimensions are scored. Final step: call the built-in `summary` tool with a 1-2 paragraph result; return nothing else.
```

When the critic flips COMPLETE, read the review inline and present to the user:

```markdown
## Artifact drafted — critic review in

**Score**: {{ Strong / Needs polish / Needs rework }}

**Rubric highlights**:
{{ top 3 findings — critical first }}

Revision options:

1. Apply all recommendations automatically (1 revision pass — cap 2)
2. Select specific recommendations to apply
3. Skip revision, ship the current draft
```

For options 1 and 2, relaunch the synthesizer (PRD route) or discovery-lead (discovery-round route) in revision mode, passing the review file.

**Cap at 2 revise rounds.** After 2, surface remaining findings inline; let the user ship or decide whether further iteration is worth it.

---

## Phase 4 — Deliver

After revision (or the user skips revision), present inline:

```markdown
## {{ Route }} complete: {{ title }}

**Files**:

- product-discovery/{{ slug }}/{{ primary output }}
- product-discovery/{{ slug }}/work-log-*.md (role work logs)
- product-discovery/{{ slug }}/review-critic.md (critic review)

**Score**: {{ Strong / Needs polish / Needs rework }}

**Key numbers**:
{{ route-specific counts — PRD sections, HMW count, AC count, job story count }}

**Next steps**:
{{ routing suggestions — /build-stack for PRD route, another HMW round for discovery, etc. }}
```

---

## Ecosystem integration — erpaval hard-dep

**erpaval's CL-RIGOR classifier calls into `hmw-framer.md` and `ears-specifier.md` directly.** These two role files are a public API. Renames go through alias-then-delete. Changing the scope of either role (what it reads, what it writes, what format it produces) is a breaking change for erpaval's fuzzy and contract-unclear routes.

When editing either role file:

1. Keep the output file path convention stable — `brainstorms/NNN-<slug>-requirements.md` for HMW, `specs/NNN-<slug>/spec.md` for EARS.
2. Keep the AC numbering (`AC-X-Y`) and annotation (`[P]`, `Dependencies:`) conventions stable in ears-specifier.
3. Keep the NN/g validation table shape stable in hmw-framer.
4. If a change is unavoidable, open an issue in the plugin repo and coordinate erpaval's update in the same commit.

---

## Inline mode (no subagents)

For single-section polish or quick edits to an existing artifact, the orchestrator edits inline without spawning subagents. The write-protocol rhythm still applies: edit → read → edit.

Use inline mode when:

- The user asks "tighten the MVP section of the PRD I already have."
- The user wants one more HMW added to an existing set.
- The user wants to retag `[P]` vs. `Dependencies:` on a handful of ACs.

Use the full pipeline when:

- The user hands over raw material.
- The user asks for a whole new PRD / discovery memo / HMW set / EARS spec.
- The user wants a critic review of an existing artifact.
