# Product Strategy Orchestrator

The orchestrator runs inside a forked subagent so the main conversation stays clean of check-in noise, tool chatter, and packet scaffolding. It routes the user's ask through five phases (plus a critic pass between synthesize and deliver) — framing, parallel framework execution, synthesis, critic review, delivery — each one a general-purpose `Agent` with its role prompt copied from `references/roles/`. Outputs are files on disk. Progress is `wc -l` on those files.

Terms: `{{ slug }}` is a kebab-case slug derived from the challenge statement, trimmed to ~40 chars. `product-strategy/{{ slug }}/` is the working directory. All role prompts carry the write-protocol block verbatim from `references/write-protocol.md`.

---

## Inputs

- `{{ source }}` — the user's ask (question, topic, prior memo path) parsed from `$ARGUMENTS`.
- `${CLAUDE_PLUGIN_ROOT}/skills/product-strategy/references/write-protocol.md` — verbatim block pasted into every role prompt.
- `${CLAUDE_PLUGIN_ROOT}/skills/product-strategy/references/frameworks/INDEX.md` — routing guide. Decision table + cross-framework composition. Read this first to pick fan-out. Per-framework canonical structures live in the same `frameworks/` directory as `rumelt-kernel.md`, `wardley-maps.md`, `minto-pyramid.md`, `working-backwards.md` — load only the file(s) a role needs.
- `${CLAUDE_PLUGIN_ROOT}/skills/product-strategy/references/roles/` — per-role prompt bodies.
- `${CLAUDE_PLUGIN_ROOT}/skills/product-strategy/templates/worklog-skeleton.md` — per-role work-log skeleton.
- `${CLAUDE_PLUGIN_ROOT}/skills/product-strategy/templates/{strategy-memo,rumelt-packet,wardley-packet,pr-faq-discovery,minto-outline}.md` — per-role output skeletons.

---

## Phase tracking

Before Phase 0, create 6 todo items — Route, Frame, Parallel frameworks, Synthesize, Critic review, Deliver. During Phase 2, additionally `TaskCreate` one item per framework role (rumelt / wardley / pr-faq / minto) and flip each to `completed` when its packet shows `Status: COMPLETE`. During Phase 3.5 revision cycles, create a new todo per revision round. Flip phase items to `in_progress` on entry, `completed` on exit.

---

## Phase 0 — Route

Before any subagent runs, route by intent. Each intent fans out to a different Phase 2 set.

| User signal                                                               | Fan-out                                      | Notes                                                                            |
| ------------------------------------------------------------------------- | -------------------------------------------- | -------------------------------------------------------------------------------- |
| "Run a Rumelt kernel on X" / "what's the crux" / "our strategy is fluffy" | rumelt-architect only                        | Single-packet run; synthesizer still composes a short memo around the packet.    |
| "Build a Wardley map for X" / "should we build or buy X"                  | wardley-cartographer only                    | Single-packet run; synthesizer composes a build/buy-focused memo.                |
| "Draft a PR-FAQ for X"                                                    | pr-faq-discovery only                        | Single-packet run; memo is optional — sometimes the PR-FAQ *is* the deliverable. |
| "Structure this argument for leadership" / "build a Minto pyramid"        | minto-pyramid-builder only                   | Single-packet run; memo wraps the outline.                                       |
| "Write an executive strategy memo on X" / "we need a full strategy read"  | rumelt + wardley + minto + pr-faq (all four) | Full strategy memo with all four packets composed.                               |
| "Portfolio question / build-vs-buy for a bet"                             | CSO framing + wardley + rumelt               | CSO takes Phase 1; fan-out skips PR-FAQ if the decision is internal.             |
| "Customer-centric strategy / new product bet"                             | CPO + VP Design framing + pr-faq + rumelt    | VP Design adds a customer framing file; PR-FAQ is load-bearing.                  |
| "Review my existing strategy memo"                                        | Skip to Phase 3.5 — critic only              | No Phase 2 re-run; the critic evaluates the existing memo.                       |

Parse the user's ask in one pass, pick the fan-out, then announce the plan inline (one short paragraph) before moving to Phase 1. Don't wait for approval — the pipeline is fully reversible (files on disk; nothing published).

Use `AskUserQuestion` only when the ask is genuinely ambiguous on audience (internal vs external), horizon (this quarter vs 3-year), or deliverable shape (memo vs PR-FAQ vs kernel-only). Batch up to 3 questions; proceed with the answers.

---

## Phase 1 — Frame

Runs **foreground** (one agent, user waits — the framing drives all Phase 2 work).

### Setup

Derive the slug from the challenge statement. Create the working directory.

```bash
mkdir -p product-strategy/{{ slug }}/
```

Instantiate skeletons:

- `product-strategy/{{ slug }}/framing.md` — (CPO writes this).
- `product-strategy/{{ slug }}/framing-cso.md` — if CSO role is summoned (portfolio ask).
- `product-strategy/{{ slug }}/framing-design.md` — if VP Design role is summoned (customer-centric ask).
- `product-strategy/{{ slug }}/work-log-cpo.md` (and work-log-cso, work-log-vp-design as applicable) from `templates/worklog-skeleton.md` with role slot filled.

All start `Status: IN PROGRESS`.

### Launch

Default: one foreground `Agent` with the CPO role prompt. Launch the CSO and/or VP Design tasks in the same Phase 1 only when the Phase 0 routing specifies it — they run in parallel with each other but foreground to the user.

- `subagent_type: "general-purpose"`
- `model: "opus"`
- `run_in_background: false`

### Role prompt template

```text
You are the Chief Product Officer framing a strategic question for a pipeline of framework agents.

<scope>
Ask: {{ user_source }}
Slug: {{ slug }}
Working directory: {{ absolute_path }}/
Your work log: {{ absolute_path }}/work-log-cpo.md
Your deliverable: {{ absolute_path }}/framing.md (skeleton already seeded)
</scope>

<responsibilities>
Read any supporting files or prior memos in the working directory. Frame the challenge for the Phase 2 framework roles — name the audience, state a candidate crux, commit to a framework fan-out plan.

Fill the sections in {{ absolute_path }}/framing.md (see the role reference for the exact section list):
1. Challenge
2. Audience
3. Crux read (candidate — the rumelt architect sharpens this)
4. Stakes
5. Framework fan-out plan
6. Known facts (cited inline)
7. Open questions
8. Voice and audience guidelines

Fill in place — don't overwrite the template.
</responsibilities>

<reference_material>
${CLAUDE_PLUGIN_ROOT}/skills/product-strategy/references/frameworks/INDEX.md — decision table to pick the fan-out. Don't load per-framework files yet — that's Phase 2.
${CLAUDE_PLUGIN_ROOT}/skills/product-strategy/references/roles/cpo.md — full role reference.
</reference_material>

<write_protocol>
{{ paste ${CLAUDE_PLUGIN_ROOT}/skills/product-strategy/references/write-protocol.md verbatim }}
</write_protocol>

<quality_bar>
- The challenge is a specific question, not a topic.
- The crux is named as a candidate, not hedged.
- The framework fan-out plan is committed (run or skip per framework, with reason).
- Audience is specific enough that a reader can say "this would land with that reader."
- Citations inline for factual claims.
- When every section has real content, flip Status to COMPLETE.
</quality_bar>
```

Swap `cpo.md` for `cso.md` or `vp-design.md` when Phase 0 selected those variants; the skeleton paths change correspondingly.

Present the framing inline when the CPO flips to `COMPLETE`. Move to Phase 2 without gating — the user can redirect if the framing is off, but the pipeline keeps moving by default.

---

## Phase 2 — Parallel framework execution

This is where the filesystem-as-memory pattern earns its keep. Each framework role reads `framing.md` (plus siblings if present), reads its framework reference section, and writes to its own packet file. The roles never see each other's work during Phase 2.

### Setup

For every framework the Phase 0 fan-out selected, instantiate:

- Packet skeleton from `templates/{rumelt-packet,wardley-packet,pr-faq-discovery,minto-outline}.md`.
- Work-log skeleton from `templates/worklog-skeleton.md` with role slot filled.

All start `Status: IN PROGRESS`.

### Launch

**One message, N `Agent` calls** with `run_in_background: true`. Parallel saves substantial wall clock — the frameworks are independent. For the full-memo fan-out, that's 4 `Agent` calls in one message.

```text
Agent (rumelt):
  subagent_type: "general-purpose"
  model: "opus"
  description: "Rumelt kernel"
  run_in_background: true
  prompt: <rumelt-architect role prompt — see below>

Agent (wardley):
  subagent_type: "general-purpose"
  model: "opus"
  description: "Wardley map"
  run_in_background: true
  prompt: <wardley-cartographer role prompt>

Agent (pr-faq):
  subagent_type: "general-purpose"
  model: "opus"
  description: "PR-FAQ discovery"
  run_in_background: true
  prompt: <pr-faq-discovery role prompt>

Agent (minto):
  subagent_type: "general-purpose"
  model: "opus"
  description: "Minto pyramid"
  run_in_background: true
  prompt: <minto-pyramid-builder role prompt>
```

### Role prompt shape (common to all four)

```text
You are the {{ role archetype }} for a strategy pipeline. Read the framing and any prior packets; produce your packet.

<scope>
Framing: {{ absolute_path }}/framing.md (read in full)
Sibling packets already in flight (read any that exist; don't wait for ones that don't):
  - {{ absolute_path }}/rumelt-packet.md
  - {{ absolute_path }}/wardley-packet.md
  - {{ absolute_path }}/pr-faq-packet.md
  - {{ absolute_path }}/minto-outline.md
Your work log: {{ absolute_path }}/work-log-{{ role }}.md
Your deliverable: {{ absolute_path }}/{{ role-specific packet file }} (skeleton seeded)
</scope>

<reference_material>
${CLAUDE_PLUGIN_ROOT}/skills/product-strategy/references/frameworks/<your-framework>.md — your framework's file (rumelt-kernel.md / wardley-maps.md / minto-pyramid.md / working-backwards.md). Load only yours.
${CLAUDE_PLUGIN_ROOT}/skills/product-strategy/references/roles/{{ role }}.md — full role reference with canonical section list and quality bar.
</reference_material>

<responsibilities>
Fill every section in the packet skeleton. Edit in place, don't overwrite. Each section has real content (not placeholder text) before moving to the next.

Cite inline for every non-obvious claim — framework file + heading, research syntheses, external URLs. Readers verify reasoning through these citations.

End with the Attribution Note — one paragraph the synthesizer drops into the memo verbatim.
</responsibilities>

<write_protocol>
{{ paste write-protocol.md verbatim }}
</write_protocol>

<quality_bar>
{{ role-specific quality bar — pull from the role reference }}
</quality_bar>

When every section has real content, flip Status to COMPLETE.
```

### Monitor

Escalating check-ins: ~30s → 2m → 5m → every 5m after.

At each check-in, run one `wc -l` across the packet files and work logs:

```bash
wc -l product-strategy/{{ slug }}/*-packet.md product-strategy/{{ slug }}/minto-outline.md
```

Report compactly:

```text
Phase 2 check-in #2:
- Rumelt:   184 lines, diagnosis + crux done, actions in progress
- Wardley:  142 lines, value chain + evolution table done, gameplay in progress
- PR-FAQ:    96 lines, press release done, external FAQ in progress
- Minto:    102 lines, SCQA done, supporting arguments in progress
```

Continue until every packet shows `Status: COMPLETE` at the top.

### Stuck detection

A packet file with identical line count across two consecutive check-ins is stuck. Launch a fresh `Agent` with the existing file state and a "skip completed sections" prompt; the original backgrounded agent can finish or timeout on its own. The recovery pattern mirrors `skills/research/references/orchestrator.md` — read that section rather than duplicating it here.

---

## Phase 3 — Synthesize

Foreground, single agent. The synthesizer reads every Phase 2 packet plus `framing.md` and composes the final `strategy-memo.md`.

### Setup

Instantiate:

- `product-strategy/{{ slug }}/strategy-memo.md` from `templates/strategy-memo.md`.
- `product-strategy/{{ slug }}/work-log-synthesizer.md` from `templates/worklog-skeleton.md` with role=strategy-synthesizer.

Both start `Status: IN PROGRESS`.

### Launch

One `Agent`, foreground, Opus.

### Role prompt template

```text
You are the strategy synthesizer. Read every Phase 2 packet and compose the final strategy memo.

<scope>
Framing: {{ absolute_path }}/framing.md
Phase 2 packets (read every one present):
  - {{ absolute_path }}/rumelt-packet.md
  - {{ absolute_path }}/wardley-packet.md
  - {{ absolute_path }}/pr-faq-packet.md
  - {{ absolute_path }}/minto-outline.md
Your work log: {{ absolute_path }}/work-log-synthesizer.md
Your deliverable: {{ absolute_path }}/strategy-memo.md (skeleton seeded)
</scope>

<reference_material>
${CLAUDE_PLUGIN_ROOT}/skills/product-strategy/references/frameworks/INDEX.md — cross-framework composition guidance for reconciling packets.
${CLAUDE_PLUGIN_ROOT}/skills/product-strategy/references/roles/strategy-synthesizer.md — full role reference.
</reference_material>

<responsibilities>
Compose the memo top-down (Minto). Executive Summary first, then Diagnosis, Guiding Policy, Coherent Actions, and the optional Customer Framing / Build-vs-Buy sections depending on which packets ran.

Attribute inline for every non-obvious claim — "The diagnosis (rumelt-packet §Diagnosis) is..." — so a reader can trace any claim back to its source packet.

Convergence Notes: name at least one convergence (packets agreed) and at least one divergence (packets disagreed; memo's voice picked). "Everything agreed" is a red flag.

Evidence bibliography: consolidate, deduplicate, order newest-first.
</responsibilities>

<write_protocol>
{{ paste write-protocol.md verbatim }}
</write_protocol>

<quality_bar>
- Every non-obvious claim has an inline attribution.
- The Executive Summary reads top-down (Minto).
- Convergence Notes name convergence AND divergence.
- The memo is prescriptive, not comparative.
- No framework body is reproduced — the memo uses packet outputs.
- Evidence bibliography is newest-first, deduplicated, with links.
- Flip Status to COMPLETE when every section has real content.
</quality_bar>
```

---

## Phase 3.5 — Critic review

Foreground, single agent. One evaluation axis (coherent + defensible) with a multi-dimensional rubric.

### Setup

Instantiate:

- `product-strategy/{{ slug }}/review-strategy.md` from a plain Markdown header (no fixed template — the critic's output format lives in `references/roles/strategy-critic.md`).
- `product-strategy/{{ slug }}/work-log-critic.md` from `templates/worklog-skeleton.md`.

Start `Status: IN PROGRESS`.

### Launch

One `Agent`, foreground, Opus.

### Role prompt template

```text
You are the strategy critic. Review the strategy memo for coherence and defensibility against a multi-dimensional rubric.

<scope>
Memo: {{ absolute_path }}/strategy-memo.md (read in full)
Phase 2 packets (read to cross-check claims):
  - {{ absolute_path }}/rumelt-packet.md
  - {{ absolute_path }}/wardley-packet.md (if present)
  - {{ absolute_path }}/pr-faq-packet.md (if present)
  - {{ absolute_path }}/minto-outline.md (if present)
Framing: {{ absolute_path }}/framing.md
Your work log: {{ absolute_path }}/work-log-critic.md
Your deliverable: {{ absolute_path }}/review-strategy.md
</scope>

<reference_material>
${CLAUDE_PLUGIN_ROOT}/skills/product-strategy/references/frameworks/ — per-framework validation checks (rumelt-kernel.md, wardley-maps.md, minto-pyramid.md, working-backwards.md). Pull only the files matching packets that ran.
${CLAUDE_PLUGIN_ROOT}/skills/product-strategy/references/roles/strategy-critic.md — full rubric, scoring, output format.
</reference_material>

<responsibilities>
Grade the memo on every rubric dimension: diagnosis-matches-evidence, guiding-policy-non-trivial, actions-coherent, Wardley-verifiable, customer-framing-specific, Minto-structure-holds, risks-honest, attribution-clean, bad-strategy-checks-pass.

Produce review-strategy.md with:
- Summary (2-3 sentences)
- Score (Strong / Needs revision / Needs rework)
- Dimension table (score + evidence per dimension)
- Critical issues, Warnings, Suggestions
- Specific revision recommendations (actionable — name the section and the fix)
</responsibilities>

<write_protocol>
{{ paste write-protocol.md verbatim }}
</write_protocol>

<quality_bar>
- Every rubric dimension is graded with specific evidence from the memo.
- Critical findings name a specific sentence or section and a specific problem.
- Recommendations are actionable: "add citation for the 40% margin claim" beats "improve citations."
- Flip Status to COMPLETE when every dimension has a graded score and every finding has a specific recommendation.
</quality_bar>
```

### Revise cycle

Read `review-strategy.md` inline when the critic flips to COMPLETE. Decision tree:

- **Strong** — skip to Phase 4.
- **Needs revision** — relaunch the synthesizer in revision mode with the critic's findings. Synthesizer applies revisions, flips memo back to COMPLETE. Relaunch critic (round 2). If still "Needs revision," surface remaining findings inline and hand the memo to the user.
- **Needs rework** — surface findings to the user first. Ask whether to proceed with revise-round-1 or reopen Phase 2 with different fan-out.

Cap at **2 revise rounds**. After round 2, remaining findings surface to the user for manual resolution rather than looping.

---

## Phase 4 — Deliver

Present inline to the user:

```markdown
## Strategy memo complete: {{ challenge_slug }}

**Files:**

- `product-strategy/{{ slug }}/strategy-memo.md` — the memo
- `product-strategy/{{ slug }}/framing.md` — framing document
- `product-strategy/{{ slug }}/rumelt-packet.md` — kernel (if ran)
- `product-strategy/{{ slug }}/wardley-packet.md` — map (if ran)
- `product-strategy/{{ slug }}/pr-faq-packet.md` — discovery PR-FAQ (if ran)
- `product-strategy/{{ slug }}/minto-outline.md` — argument pyramid (if ran)
- `product-strategy/{{ slug }}/review-strategy.md` — critic review

**Diagnosis:** {{ one-sentence diagnosis from the memo }}
**Crux:** {{ one sentence }}
**Guiding policy:** {{ one-sentence policy }}
**Critic score:** {{ Strong / Needs revision / Needs rework }}

**Handoff options:**

- Product discovery / PRD derivation: hand `strategy-memo.md` to `product-discovery` — it will derive HMW questions, job stories, and a PRD.
- Long-form narrative: hand `strategy-memo.md` + `pr-faq-packet.md` to whatever narrative-writing workflow your team uses — the Minto-shaped thinking is already done.
```

---

## Inline mode (no subagents)

For small strategy asks — "what's the crux of this problem," "help me sharpen this guiding policy," "is this a MECE pyramid" — the orchestrator edits directly in the main (forked) context. No subagents, no work logs, no packet files. The rhythm is still write-protocol: think → edit → think.

Use inline mode when:

- User asks one targeted framework question with a specific artifact in hand.
- User wants feedback on a sentence or a section, not a full memo.

Use the full pipeline when:

- User asks for a strategy memo.
- User asks to run one or more frameworks from scratch.
- User hands over raw material (research, transcripts, prior memos) and wants a synthesis.

---

## Parallel multi-memo sessions

When the user wants strategy from multiple angles at once ("the internal memo and the externally-facing PR-FAQ for the same bet"):

1. Plan the set — each deliverable's slug, audience, fan-out.
2. Run Phase 1 once if the framing is shared; per-deliverable if framings diverge.
3. Launch Phase 2 as parallel `Agent` calls — N deliverables × M frameworks in one message.
4. Phase 3 per deliverable; Phase 3.5 per deliverable.

`wc -l` across all packet files — stuck detection is unchanged.

---

## Handoff contracts

This skill's outputs are designed to compose with the rest of the bundle:

- **To `product-discovery`** — `strategy-memo.md` is the upstream input to PRD derivation. Discovery derives HMW questions, job stories, and user stories from the memo's customer framing and the coherent actions.
- **To narrative writing** — `strategy-memo.md` and `pr-faq-packet.md` carry Minto-shaped thinking that maps cleanly to SCQA or Working Backwards narrative arcs. The synthesizer's Executive Summary is already Minto-shaped — drop it into whatever long-form workflow your team uses.
