# Ultraplan Orchestrator

The orchestrator runs inside a forked subagent so the main conversation stays clean. It intakes the problem, launches three Opus 4.7 explorers in parallel (each with a distinct divergence vector), monitors them by reading their output files, recovers any that stall, and then runs a critic synthesis that composes a final plan with per-decision attribution.

---

## Inputs

- `{{ problem }}` — parsed from `$ARGUMENTS`.
- `${CLAUDE_PLUGIN_ROOT}/skills/ultraplan/references/divergence-vectors.md` — the three vector blocks to paste into explorer prompts.
- `${CLAUDE_PLUGIN_ROOT}/skills/ultraplan/references/write-protocol.md` — the write-protocol block copied into every explorer prompt.
- `${CLAUDE_PLUGIN_ROOT}/skills/ultraplan/templates/explorer-skeleton.md` — per-explorer skeleton.
- `${CLAUDE_PLUGIN_ROOT}/skills/ultraplan/templates/plan-skeleton.md` — final plan skeleton.

---

## Phase tracking

Before Phase 1, create 5 todo items — one per phase (Intake, Skeletons, Launch, Monitor, Critic). During Launch, additionally `TaskCreate` one item per explorer (Architectural / Speed-first / Simple-first) and flip each to `completed` when its explorer file shows `Status: COMPLETE`. Flip the phase item to `in_progress` on entry, `completed` on exit. This keeps the user oriented mid-run and makes stuck explorers visible without reading files.

---

## Phase 1 — Intake

Read the problem from `$ARGUMENTS`. If it's empty and no problem can be derived from prior conversation context, ask: "What would you like us to plan? One or two sentences is enough." Then proceed. Do **not** invoke the `ultraplan` Skill again — you are already inside it.

If the problem is non-trivially ambiguous — the kind of ambiguity that would send all three explorers in the wrong direction — ask **one** targeted `AskUserQuestion` to pin down scope. Then proceed. Do not stop to confirm the plan itself; the user invoked `/ultraplan` because they want the divergence run.

> **Orchestrator scope constraint:** Do not read the target codebase in Phases 1–3. Your job is to frame the problem, write skeleton files, and launch explorers. Codebase reading belongs inside each explorer's run — they have the vector to interpret what they find. Pre-reading here inflates your context, delays the launch, and risks a context-overflow hang before the explorers even start.

Derive a kebab-case slug from the problem (trim to ~40 chars). Derive a human-readable `problem_title` for file headers.

Summarize the run in one short block before launching:

```markdown
## Ultraplan: {{ problem_title }}

Launching 3 Opus 4.7 explorers in parallel:

- **Architectural** — optimizes for clean boundaries and future-change cost
- **Speed-first** — optimizes for shortest path to working code
- **Simple-first** — optimizes for fewest moving parts and deletion odds

Critic synthesis will compose the final plan at `planning/{{ slug }}/plan.md`.
```

Move to Phase 2.

---

## Phase 2 — Skeleton files

1. Create the output directory: `mkdir -p planning/{{ slug }}/`.
2. Write three explorer files from `templates/explorer-skeleton.md`:
   - `planning/{{ slug }}/explorer-architectural.md`
   - `planning/{{ slug }}/explorer-speed.md`
   - `planning/{{ slug }}/explorer-simple.md`
3. Write `planning/{{ slug }}/plan.md` from `templates/plan-skeleton.md`.

All four files start with `Status: IN PROGRESS`. Explorers flip their own file to `COMPLETE` when done; the critic flips `plan.md`.

---

## Phase 3 — Launch explorers

Launch all three explorers in a **single message** using parallel `Agent` calls.

Each `Agent` call uses:

- `subagent_type: "general-purpose"`
- `model: "opus"`
- `run_in_background: true`
- `description`: 3–5 words, e.g. "Architectural ultraplan explorer"
- `prompt`: built from the template below

### Explorer prompt template

```text
You are a planning explorer. Plan the problem below under the divergence vector assigned to you, and write your plan to the output file as decisions crystallize.

<problem>
{{ problem }}
</problem>

<divergence_vector>
{{ paste the full vector block for this explorer — one of Architectural, Speed-first, or Simple-first from divergence-vectors.md }}
</divergence_vector>

<output>
Output file: {{ absolute_path_to_explorer_markdown }}

The file already exists with a skeleton and the write protocol embedded at the top. Edit it in place — don't overwrite.
</output>

<preamble>
If the problem references a codebase, read the relevant files before drafting decisions. Your plan should cite specific file paths and line numbers where decisions depend on existing structure.
</preamble>

<write_protocol>
{{ paste write-protocol.md verbatim — the block inside its <write_protocol> tags }}
</write_protocol>

<quality_bar>
- Every non-obvious decision names the tradeoff accepted.
- Your vector shapes the decisions; a plan that reads like the default "balanced" plan is a failed run.
- Cite adjacent code with `path/to/file.py:42` style when decisions depend on existing structure.
- Sections are specific (files, modules, exact changes), not generic paraphrase.
</quality_bar>
```

After launching, tell the user how many explorers are running and list their file paths.

**Launch verification:** ~15 seconds after the three Agent calls, run `wc -l` on all three explorer files and record their baseline line counts. If any file is still at its skeleton line count (the explorer wrote nothing yet), re-launch it immediately as a fresh Agent with the same prompt before entering the Phase 4 monitor loop. Do not proceed to Phase 4 until at least one explorer shows new lines above the skeleton baseline.

---

## Phase 4 — Monitor

Use escalating check-in intervals: ~30s → 2m → 5m → every 5m afterward.

At each check-in:

1. Run `wc -l` across every explorer file in one Bash call.
2. Read a specific file only when you need to see which sections have content.
3. Report compactly:

```text
Check-in #2:
- Architectural: 84 lines, sections 1–3 populated, working on 4
- Speed-first:   62 lines, sections 1–2 populated, working on 3
- Simple-first:  COMPLETE (108 lines)
```

Continue until every explorer shows `Status: COMPLETE` at the top of its file.

### Stuck-explorer recovery

<stuck_agent_recovery>
An explorer is stuck when either:

- Its file's line count is identical across two consecutive check-ins (stalled mid-run), **or**
- Its file's line count equals the skeleton baseline at the first check-in (~30s after launch), meaning it never started writing.

Don't wait for self-correction — in both cases it's time to recover.

Recovery steps:

1. Read the stuck explorer's file to see which sections already have real content.
2. Launch a fresh `Agent` with:
   - A prompt that lists the sections already complete and tells the new explorer to skip them.
   - The same divergence vector as the original — don't switch vectors mid-run.
   - An instruction to resume from the first incomplete section and append to the existing file.
3. The original backgrounded explorer will finish or timeout on its own; its writes stopped updating the file so its continued existence is harmless.
4. Resume normal check-ins on the new explorer.

</stuck_agent_recovery>

**Hard timeout:** If any explorer has not reached `Status: COMPLETE` within 90 minutes of Phase 3 launch, proceed to Phase 5 with whatever content is available. Tell the user which explorer(s) did not complete and that the critic will synthesize from partial plans. Do not wait indefinitely — a partial synthesis is always better than no output.

---

## Phase 5 — Critic synthesis

Once every explorer shows `Status: COMPLETE` (or the user explicitly decides to proceed with what's available), launch one critic `Agent`.

The critic runs **foreground** — the user waits for this one. Use:

- `subagent_type: "general-purpose"`
- `model: "opus"`
- `run_in_background: false`

### Critic prompt template

```text
You are a planning critic. Read three independent explorer plans and compose a single final plan that cherry-picks the best decision from each. Do not average — pick per-decision.

<inputs>
Problem: {{ problem }}

Explorer files to read:
- {{ absolute_path_to_explorer_architectural }}
- {{ absolute_path_to_explorer_speed }}
- {{ absolute_path_to_explorer_simple }}
</inputs>

<output>
Output file: planning/{{ slug }}/plan.md

The file already exists with a skeleton and a critic protocol block at the top. Edit it in place — don't overwrite.
</output>

<critic_discipline>
Read every explorer file in full before drafting. Note where explorers converged (high-confidence signal) and where they diverged (explicit tradeoff to resolve).

Write section by section, editing the plan file as you process each explorer. Partial progress written to disk survives termination.

Pick decisions per-axis, not per-explorer. The final plan may take its architecture from Architectural, its error handling from Speed-first, and its data model from Simple-first. Attribute each decision with `(Source: Architectural)` style parentheticals.

Write prescriptively. The user is reading this to execute; they are not reading a comparison of the three explorers. Convergence and divergence get one short note at the end, not a whole section.

When every section has real content, change the Status line from IN PROGRESS to COMPLETE.
</critic_discipline>

<required_sections>
- Problem (one paragraph)
- Chosen Approach (composed, with convergence/divergence noted)
- Decisions (per-decision blocks with Call / Source / Reason / Tradeoff)
- Implementation Order (numbered, file-specific, verifiable)
- Risks (especially around load-bearing tradeoffs where explorers diverged)
- Verification Criteria (tests, observable outputs)
- Convergence Notes (one short paragraph)
</required_sections>
```

When the critic completes, read `planning/{{ slug }}/plan.md` and present inline:

```markdown
## Ultraplan Complete: {{ problem_title }}

{{ 1–2 sentence summary of the chosen approach }}

### Output

- `planning/{{ slug }}/plan.md` — the final plan
- `planning/{{ slug }}/explorer-*.md` — the three independent plans

### Chosen Approach

{{ paste the Chosen Approach section's first paragraph }}

### Convergence

{{ paste the Convergence Notes }}
```

Offer the user: follow-up questions on any decision, a re-run with different vectors, or handoff to an implementation skill.
