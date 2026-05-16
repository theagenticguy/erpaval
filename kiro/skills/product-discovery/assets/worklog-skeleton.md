# Product-discovery task — {{ role }}

**Status:** IN PROGRESS
**Role:** {{ discovery-lead | product-analyst | system-architect | research-scout | hmw-framer | jtbd-interviewer | ears-specifier | prd-synthesizer | discovery-critic }}
**Run slug:** {{ slug }}
**Working directory:** `product-discovery/{{ slug }}/`
**Your output file:** `product-discovery/{{ slug }}/{{ output_filename }}`

<write_protocol>
Your output file is the single source of truth for your work. Edit it after every meaningful step, before starting the next one. Partial progress written to disk survives timeouts, SendMessage interrupts, and orchestrator context pressure; state held in working memory does not.

The rhythm is: one unit of thought → edit the file with the outcome → next unit. One decision at a time.

Work through your sections in numbered order. For each section:

1. Think through the decision, research finding, or draft. Read adjacent files, run a web search, or consult the framework reference when the answer is not in your head.
2. Edit the file under that section — the claim, the evidence, the user story or HMW or spec statement. Cite sources inline.
3. If the section needs more depth, do another unit of thought and edit again.
4. Move to the next section only after the current one has real content.

Name the tradeoff on every non-obvious call. "Chose JTBD job story over user story for the top-level framing because the goal is reframing around progress, not stakeholder persona" beats "used job story." The synthesizer reads these attributions when composing the final artifact.

Cite adjacent material inline when a decision depends on source evidence — framework file + heading, research synthesis line number, interview quote, or external URL. Reviewers read the citations to verify your reasoning.

When every section has real content, change the `Status:` line at the top of the file from `IN PROGRESS` to `COMPLETE`.
</write_protocol>

## 1. Objective

{{ one-sentence objective — what this role is producing for this run }}

## 2. Scope

- **Input**: {{ source files, prior-phase outputs — whatever this role reads }}
- **Output**: {{ exact file path this role writes to }}
- **Role reference**: the matching file in `${ERPAVAL_HOME}/skills/product-discovery/references/roles/`

Sections to complete in the output file (varies by role):

- {{ section 1 }}
- {{ section 2 }}

Out of scope:

- {{ anything this role should NOT touch — e.g., discovery-critic never rewrites the artifact, only reviews }}

## 3. Inputs

Files to read in full before writing:

- {{ the user's brief or frozen Intent Profile }}
- {{ prior-phase work logs, if any }}

Reference material:

- `${ERPAVAL_HOME}/skills/product-discovery/references/frameworks/INDEX.md` (routing guide — discovery + spec decision tables, composition)
- Per-framework files in `${ERPAVAL_HOME}/skills/product-discovery/references/frameworks/` — `double-diamond.md`, `how-might-we.md`, `jtbd-job-stories.md`, `user-stories-invest.md`, `ears.md`, `gherkin.md`
- `${ERPAVAL_HOME}/skills/product-discovery/references/methodology/discovery-rounds.md` (six-phase methodology)
- `${ERPAVAL_HOME}/skills/product-discovery/references/inference-heuristics.md` (PRD-route runs)
- `${ERPAVAL_HOME}/skills/product-discovery/references/quality/prd.md` (PRD quality bar)

Load only what this role needs (progressive disclosure).

## 4. Success criteria

Baseline:

- Output file populated with real content in every required section.
- `Status:` flipped from `IN PROGRESS` to `COMPLETE` when done.
- Write protocol followed — no batched-writes-at-the-end.
- Every non-obvious decision has a rationale clause and a source citation.

Role-specific:

- **discovery-lead**: problem grounded in 3+ sources; routing calls (landscape research + frameworks) explicit.
- **product-analyst**: 2+ personas, 10+ P0 stories with testable ACs, IA covers all features.
- **system-architect**: all 6 NFR categories covered, core entities + relationships + indexes, 5+ edge cases.
- **research-scout**: 5-7 competitors analyzed, feature benchmark matrix, open questions with resolution paths.
- **hmw-framer**: 3-5 HMWs, all pass NN/g validation, `strategies_used:` populated.
- **jtbd-interviewer**: 3+ job stories, each cited, no persona-simulator entries.
- **ears-specifier**: every AC uses one of the 5 templates literally, every AC has `[P]` or `Dependencies:`.
- **prd-synthesizer**: no `[FILL]` remains, cross-section consistency checks pass, synthesis log complete.
- **discovery-critic**: rubric scored per dimension, overall score set, recommendations prioritized (critical / warning / suggestion).

## 5. Anti-goals

- Do not silently reshape the scope. If you disagree with the framing, note it in the work log and continue with what was asked.
- Do not invent content to fill gaps. Flag the gap and surface it to the synthesizer or the critic.
- Do not rewrite work from other roles. Each role has a single ownership slice.
- Do not leave empty sections — write the finding, or note that it doesn't apply with a one-line rationale.

---

## Work log

{{ the agent fills this section per the write protocol — one entry per action }}

### {{ timestamp-or-step }}: {{ what was done }}

{{ what changed, what file or line, what source was cited, any issues surfaced }}

---

## Validation

{{ self-check output: section completeness, citation count, any flagged contradictions }}

### Manual check

- [ ] Output file has real content in every required section
- [ ] Role-specific quality bar met
- [ ] `Status:` flipped to `COMPLETE`

---

## Summary

{{ one paragraph — what this run produced, where it lives, and any decisions worth calling out for the next role to see (e.g., "chose HMW reframe because the brief was emotionally loaded — three strategies: Remove the bad, Question assumption, Explore opposite"). }}
