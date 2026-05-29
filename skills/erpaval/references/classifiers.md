# Classifiers — decision prompts

Each classifier is a runtime prompt the orchestrator runs against the current context-packet stack. They replace human "pick a path" decisions with logged, auditable LLM judgments. Every verdict appends to `session.yaml.classifier_trace`.

Terms like `CP-INTAKE`, `CL-DIR`, `Gate 0/1/2` are defined in `glossary.md`.

## Contents

- Prompt conventions
- CL-SCOPE — is this a coding task?
- CL-REFINE — did the user return with a build ask?
- CL-COMPLEXITY — is ERPAVal warranted?
- CL-RESUME — new session or resume a prior one?
- CL-DIR — directory probe
- CL-RIGOR — does the problem need HMW or EARS?
- CL-SPEC — are prerequisites ready?
- CL-VALIDATE — validation verdict
- CL-C2 — attempt-4 escalation disposition
- CL-DISP — human disposition of Gate 2 findings
- CL-LESSONS — did the session produce novel learnings?
- Classifier trace

## Prompt conventions

Every classifier below uses the same shape so Opus parses consistently:

- `<role>` states the classifier ID and the strict-JSON output rule.
- `<input>` names the packet fields the classifier reads, bound with `{{ templating }}`. The orchestrator substitutes real values before invocation.
- `<criteria>` enumerates the decision rules.
- `<output_format>` shows the exact JSON shape.

Interpolation syntax: `{{ path.to.field }}` reads from a named packet. The orchestrator replaces these at call time.

## CL-SCOPE — is this a coding task?

```text
<role>
You are the CL-SCOPE classifier for the ERPAVal orchestrator.
Return one JSON object matching the schema. Emit no prose, no code
fences, no preamble.
</role>

<input>
raw_request: {{ CP-INTAKE.raw_request }}
</input>

<criteria>
Classify the input:

- "coding" — the primary deliverable is source code, tests, config,
  or infrastructure that runs in a codebase.
- "non-coding" — the primary deliverable is research, writing, a
  PRD, analysis, or strategy.

Signals that favor "coding": file paths, code identifiers, error
messages, test-framework names.
Signals that favor "non-coding": opens with "explore", "write",
"summarize", "design", "present".

Set confidence by evidence count:
- "high" — two or more signals from the same side.
- "medium" — one clear signal.
- "low" — no clear signal; apply the default rule (prefer "coding"
  when mixed).
</criteria>

<output_format>
{"scope": "coding" | "non-coding",
 "confidence": "high" | "medium" | "low",
 "reason": "<one sentence citing the evidence>"}
</output_format>
```

Branches:

- `coding` → CL-COMPLEXITY
- `non-coding` → route to upstream skill (`/research`, `/product-discovery`, `/product-strategy`, `/working-backwards`, `/customer-research`, `/meta-prompt-optimizer`) → CL-REFINE

## CL-REFINE — did the user return with a build ask?

```text
<role>
You are the CL-REFINE classifier. Return one JSON object matching
the schema. Emit no prose.
</role>

<input>
prior_route: non-coding
follow_up_message: {{ latest_user_turn }}
</input>

<criteria>
Decide whether the user has pivoted into a build request:

- "yes" — the follow-up names files to create, asks to implement
  or build, or references the prior deliverable as context for new
  coding work.
- "no" — the deliverable stands on its own; the conversation is
  shifting to an unrelated topic or closing.
</criteria>

<output_format>
{"refined": "yes" | "no",
 "reason": "<one sentence>"}
</output_format>
```

Branches:

- `yes` → re-enter CL-SCOPE (the non-coding artifact enters `CP-INTAKE.upstream_artifacts`)
- `no` → exit

## CL-COMPLEXITY — is ERPAVal warranted?

```text
<role>
You are the CL-COMPLEXITY classifier. Return one JSON object.
Emit no prose.
</role>

<input>
raw_request: {{ CP-INTAKE.raw_request }}
working_tree_hint: {{ git_ls_files_sample }}  # optional
</input>

<criteria>
Classify the scope of the coding task:

- "1-file-fix" — bug fix, typo, single-function tweak, or config
  change touching 1-2 files. No architecture decisions needed.
- "multi-module" — feature or refactor spanning 3+ files or
  multiple modules. Needs Explore + Research + Plan + Act +
  Validate.
- "rebuild" — rip-and-replace of an existing subsystem. Needs
  Explore of both existing AND target patterns, destructive
  scaffold in Wave 1.

Default when mixed: "multi-module". Running ERPAVal on a smaller
change costs tokens; skipping it on a real change costs correctness.
</criteria>

<output_format>
{"complexity": "1-file-fix" | "multi-module" | "rebuild",
 "reason": "<one sentence>"}
</output_format>
```

Branches:

- `1-file-fix` → skip ERPAVal, fix directly, run Compound-lite if non-obvious
- `multi-module` | `rebuild` → CL-RESUME

## CL-RESUME — new session or resume a prior one?

```text
<role>
You are the CL-RESUME classifier. Decide whether this ask continues
prior ERPAVal work or starts fresh. Return one JSON object. Emit
no prose.
</role>

<input>
raw_request: {{ CP-INTAKE.raw_request }}
prior_sessions: {{ ls_sessions_sorted_by_mtime_desc }}  # up to 10
recent_session_yamls: {{ top_5_session_yaml_contents }}
</input>

<criteria>
Classify the intent:

- "resume" — the ask continues work from a recent session. Signals:
  - references a prior session id, branch, or artifact
  - "continue", "follow-on", "session 2", "finish", "pick up"
  - fixes a gap surfaced in the prior session's validation or lessons
  - working directory and scope overlap a session whose last mtime
    is within ~72h and whose status is not `merged`

- "new" — the ask is a fresh problem. Signals:
  - no prior session references, or prior sessions are stale (>72h
    and `merged` / `abandoned`), or on a different subsystem
  - greenfield request, different module, or explicit "new work"
  - prior_sessions is empty

Default when mixed: "new". A fresh session dir is cheap; resuming
the wrong session corrupts `intake.yaml` and derails Compound.
</criteria>

<output_format>
{"decision": "new" | "resume",
 "session_id": "<session-<hex> when resume, null when new>",
 "reason": "<one sentence citing the signal>"}
</output_format>
```

Branches:

- `new` → run `uv run ${CLAUDE_PLUGIN_ROOT}/skills/erpaval/tools/erpaval-new.py --request "<raw_request>"`, then CL-DIR
- `resume` → read `.erpaval/sessions/<session_id>/session.yaml` + latest `tasks/*.md`, append new ask to `intake.yaml.raw_request`, skip CL-DIR if the prior session already recorded it, continue from the last completed gate

The tool call is mandatory on `new` — without `session-<hex>/` on disk, the `Stop` hook's six-gate check never clears and Compound silently no-ops at session end.

## CL-DIR — directory probe

```text
<role>
You are the CL-DIR classifier. Return one JSON object.
Emit no prose.
</role>

<input>
Run these commands and use the output as evidence:
- `ls -A` in the working directory
- `git status --porcelain` and `git rev-parse --is-inside-work-tree`
</input>

<criteria>
Classify the working directory:

- "empty" — no source files. Only config files (mise.toml,
  pyproject.toml, .gitignore) may be present. Greenfield — skip
  Explore.
- "existing" — populated codebase with source files. Brownfield —
  full Explore needed.
- "rebuild-in-place" — existing code, but the task explicitly asks
  to replace it wholesale. Rip-and-replace mode — Explore both
  existing AND target patterns.
</criteria>

<output_format>
{"dir_state": "empty" | "existing" | "rebuild-in-place",
 "reason": "<one sentence citing observed files>"}
</output_format>
```

Branches:

- `empty` → Greenfield mode, skip Explore, proceed to CL-RIGOR
- `existing` → Brownfield mode, full Explore, proceed to CL-RIGOR
- `rebuild-in-place` → Rip-and-replace mode, Explore both, proceed to CL-RIGOR

## CL-RIGOR — does the problem need HMW or EARS?

```text
<role>
You are the CL-RIGOR classifier. Return one JSON object.
Emit no prose.
</role>

<input>
raw_request: {{ CP-INTAKE.raw_request }}
prior_lessons: {{ CP-RECALL.applicable_lessons | titles_only }}
</input>

<criteria>
Judge two dimensions:

(a) Is the problem statement crisp?
  - "crisp" — names a specific user segment, an observable
    outcome, and a measurable success criterion.
  - "fuzzy" — vague motivation, emotional framing ("users hate
    X"), or solution-oriented phrasing ("build a dashboard").

(b) Is the contract obvious?
  - "obvious" — API surface and behavior boundaries are already
    documented or trivially inferable from existing code.
  - "unclear" — multiple interpretations of "done", behavior is
    critical, or regressions would be hard to detect.

Build rigor_needed as the set of applicable substeps:
  - fuzzy → add "hmw"
  - unclear → add "ears"
  - crisp + obvious → empty list (skip both substeps)
</criteria>

<output_format>
{"rigor_needed": ["hmw" and/or "ears", possibly empty],
 "reason": "<one sentence>"}
</output_format>
```

Branches:

- `["hmw"]` → run HMW substep (`framing-hmw.md`), then re-check if EARS needed
- `["ears"]` → run EARS substep (`framing-ears.md`)
- `["hmw", "ears"]` → run HMW first (HMW informs EARS), then EARS
- `[]` → skip both, proceed to CL-SPEC

## CL-SPEC — are prerequisites ready?

```text
<role>
You are the CL-SPEC classifier. Decide whether ERPAVal has the
prerequisites it needs. Return one JSON object. Emit no prose.

This classifier loops: after each upstream skill returns an
artifact, re-run with the updated input.
</role>

<input>
raw_request: {{ CP-INTAKE.raw_request }}
upstream_artifacts_present: {{ CP-INTAKE.upstream_artifacts | keys }}
dir_state: {{ CL-DIR.dir_state }}
</input>

<criteria>
Check each prerequisite. Mark missing only when evidence is absent:

- "prd" — missing when the task is user-facing AND no PRD appears
  in upstream_artifacts. Skip this check for internal tooling
  and refactors.
- "stack" — missing when dir_state is "empty" AND no stack
  decision appears in upstream_artifacts. Skip for "existing"
  and "rebuild-in-place".
- "concept" — missing when raw_request is fuzzy at the product
  level (unclear user or unclear problem), not at the
  implementation level.

ready is true only when missing is empty.
</criteria>

<output_format>
{"ready": true | false,
 "missing": [may include "prd", "stack", "concept"],
 "reason": "<one sentence>"}
</output_format>
```

Branches:

- `ready: true` → preparation complete, begin Explore + Research
- `ready: false` → route to each upstream skill in `missing`, loop back when each completes

## CL-VALIDATE — validation verdict

```text
<role>
You are the CL-VALIDATE classifier. Return one JSON object.
Emit no prose.
</role>

<input>
validation: {{ CP-VALIDATION }}
</input>

<criteria>
All three validation layers completed. Decide:

- "pass" — all layers green, no CRITICAL or HIGH findings.
- "fail" — any layer failed, or findings contain CRITICAL or
  HIGH severity.

Severity bar:
  - L1 (static): any non-zero exit = fail.
  - L2 (quality): findings with severity ≥ HIGH = fail.
  - L3 (security): CRITICAL or HIGH = fail. MEDIUM surfaces in
    findings but does not block pass.
</criteria>

<output_format>
{"verdict": "pass" | "fail",
 "failing_layers": [may include "l1_static", "l2_quality", "l3_security"],
 "reason": "<one sentence>"}
</output_format>
```

Branches:

- `pass` → Gate 2
- `fail` → C4 cycle: identify failing tasks, re-open with scoped fix packets, re-run Act

## CL-C2 — attempt-4 escalation disposition

```text
<role>
You are the CL-C2 classifier. A subagent has burned 3 in-task fix
attempts (C2 cycle) and is stuck. Decide how the orchestrator should
recover. Return one JSON object. Emit no prose.
</role>

<input>
task_packet: {{ CP-TASK-N contents }}
last_agent_output: {{ agent's final message before attempt 4 }}
error: {{ last validator or tool error }}
attempts_so_far: 3
</input>

<criteria>
Review the packet, the agent's last state, and the error. Pick one:

- "fix-directly" — a 1-2 line typo, off-by-one, or trivial mechanical
  fix the orchestrator can apply without respawning. Examples: a
  missing import, a wrong literal, a single stale type annotation.
  The agent already identified the fix but couldn't apply it cleanly.

- "respawn" — the packet is sound but the agent got tangled. Kill
  the agent, clear its state, re-run with the same packet and same
  model. Typical when the agent made partial progress then drifted.

- "missing-prereq" — the agent hit a gap the packet didn't cover
  (a missing file, a dependency not scaffolded, an interface not
  yet defined). Route to C3: insert a prereq task, re-wire
  addBlockedBy, resume original task when prereq lands.
</criteria>

<output_format>
{"disposition": "fix-directly" | "respawn" | "missing-prereq",
 "reason": "<one sentence>",
 "fix_instructions": "<only when disposition is fix-directly>",
 "missing_prereq": "<only when disposition is missing-prereq>"}
</output_format>
```

Branches:

- `fix-directly` → orchestrator applies the fix inline, validates, task marked complete
- `respawn` → fresh `Agent` call with the same packet and `-retry` name suffix; the original backgrounded agent can finish or timeout on its own
- `missing-prereq` → route to C3 protocol (`flow.md`)

## CL-DISP — human disposition of Gate 2 findings

```text
<role>
You are the CL-DISP classifier. Parse the human's disposition
of Gate 2 findings. Return one JSON object. Emit no prose.
</role>

<input>
findings: {{ CP-VALIDATION.findings }}
human_response: {{ latest_human_turn }}
</input>

<criteria>
Parse the human's intent:

- "accept" — findings acknowledged, not blocking merge.
- "fix" — findings must be fixed before merge. Extract the fix
  instructions verbatim from the human's message.

Include fix_instructions only when disposition is "fix".
</criteria>

<output_format>
{"disposition": "accept" | "fix",
 "fix_instructions": "<verbatim from human, only when disposition is fix>",
 "reason": "<one sentence>"}
</output_format>
```

Branches:

- `accept` → merge → Compound
- `fix` → C5 cycle back to Act with the human's fix instructions

## CL-LESSONS — did the session produce novel learnings?

```text
<role>
You are the CL-LESSONS classifier. Identify lessons worth
persisting to `.erpaval/solutions/`. Return one JSON object.
Emit no prose.
</role>

<input>
session_trace: {{ CP-SESSION + all referenced packets }}
existing_solutions: {{ ls_of_solutions_dir }}
</input>

<criteria>
Review the session end-to-end. Identify candidate lessons:

bug-track candidates:
- C2 fix cycles that revealed a non-obvious root cause.
- C4 validation failures that exposed a repeatable gotcha.
- Research dead-ends that future sessions should avoid.

knowledge-track candidates:
- Architectural patterns surfaced in Explore that newcomers
  wouldn't infer.
- New API or library usage patterns worth capturing.
- Conventions the codebase follows that weren't documented.

For each candidate, judge two filters:

- novel — no existing lesson in `.erpaval/solutions/` already
  covers it. Grep for overlapping tags and title before claiming
  novel.
- reusable — likely to apply to a future session, not a one-off
  hack.

Include a lesson only when both filters pass.
</criteria>

<output_format>
{"lessons": [
   {"track": "bug" | "knowledge",
    "category": "<one of the canonical category folders>",
    "slug": "<kebab-case, no dates>",
    "novel": true,
    "reusable": true}
 ]}
</output_format>
```

Branches:

- `lessons: [...]` → write each to `.erpaval/solutions/<category>/<slug>.md`, update `INDEX.md`
- `lessons: []` → skip write, session-only

## Classifier trace

Every verdict is appended to `session.yaml.classifier_trace` so auditors can reconstruct the routing decisions. Example trace (illustrative — the actual entries come from real classifier runs):

```yaml
classifier_trace:
  - CL-SCOPE: coding (high confidence)
  - CL-COMPLEXITY: multi-module
  - CL-RESUME: new (no prior sessions within 72h)
  - CL-DIR: existing
  - CL-RIGOR: [hmw, ears]
  - CL-SPEC: ready
  - CL-VALIDATE: findings
  - CL-DISP: accepted_with_followup
  - CL-LESSONS: wrote_2
```
