# Role — Strategy Critic

The strategy-critic reviews the synthesized `strategy-memo.md` against a single evaluation axis — *coherent and defensible* — with a multi-dimensional rubric. One foreground `general-purpose` `Agent`. Cap at 2 revise rounds.

## Archetype

Strategy and discovery artifacts have one evaluation axis (is this coherent and defensible) with multiple dimensions (diagnosis matches evidence, guiding policy is non-trivial, actions are coherent with each other, Wardley claims are verifiable, PR-FAQ framing is specific). A single critic produces one report; the synthesizer applies revisions. This differs from `presentation`'s two-reviewer pattern because slides have two orthogonal quality axes; strategy has one.

## Scope

- **Input**: `strategy-memo.md` (full), every Phase 2 packet for cross-checks, `framing.md` for intent.
- **Output**: `review-strategy.md` — the review report with a score, findings, and specific revision recommendations. The synthesizer reads this and revises.
- **Work log**: `work-log-critic.md`.

Out of scope: rewriting the memo (synthesizer), re-running any framework (Phase 2 roles), handing off to downstream skills (orchestrator).

## Task at hand

Read `strategy-memo.md` and every Phase 2 packet. Produce `review-strategy.md` with a multi-dimensional rubric:

### Rubric dimensions

1. **Diagnosis matches evidence** — does the diagnosis section cite real evidence from the packets? Is the Crux named as a surmountable challenge, not a fact of life? Do symptoms map to a coherent root cause?
2. **Guiding policy is non-trivial** — does the policy rule out at least one defensible alternative? If every competitor would adopt the same policy, flag it.
3. **Actions are coherent** — do the actions reinforce each other? Is any action cutting against another? Are they specific (who, what, by when)?
4. **Wardley claims are verifiable** — every evolution-stage claim has cited evidence. Build-vs-buy reads correspond to evolution stages.
5. **Customer framing is specific** — if the PR-FAQ section is present, the customer archetype is specific, the quote is realistic, the five customer questions are answered specifically.
6. **Minto structure holds** — executive summary is top-down; supporting arguments are MECE; a reader stopping at any level has a coherent view.
7. **Risks are honest** — real risks with real mitigations. Evidence gaps are flagged. "Risks we already handled" is flagged.
8. **Attribution is clean** — every non-obvious claim traces to its source packet inline. No hand-wavy synthesis.
9. **Bad-strategy checks pass** — Rumelt's four hallmarks (fluff, face-the-challenge, goals-vs-strategy, scattered-objectives) have explicit answers in the memo, not just in the packet.

### Scoring

- **Strong** — 0 critical, ≤3 warnings, all dimensions pass.
- **Needs revision** — 0 critical, 4–8 warnings, or 1–2 dimensions marginal.
- **Needs rework** — any critical issue, 9+ warnings, or 3+ dimensions failing.

**Critical**: diagnosis unsupported, guiding policy is a slogan, actions contradict each other, factual claims without evidence, Minto pyramid is broken (no MECE), memo contradicts a Phase 2 packet.

**Warning**: attribution missing on non-obvious claims, risk section incomplete, convergence notes generic, bibliography not newest-first.

**Suggestion**: phrasing tweaks, stronger transitions, alternative framings worth considering.

## Reference material

- `${CLAUDE_PLUGIN_ROOT}/skills/product-strategy/references/frameworks/INDEX.md` — routing guide. Per-framework validation checks live in the same `frameworks/` directory (`rumelt-kernel.md`, `wardley-maps.md`, `minto-pyramid.md`, `working-backwards.md`); load only the files matching packets that ran.
- Every Phase 2 packet — to cross-check the memo's claims against the packets.

## Quality bar

- Every dimension is graded pass / warn / fail with specific evidence. "Seems fine" fails.
- Critical findings name a specific sentence or section in the memo and a specific problem.
- Revision recommendations are actionable — "add citation for the 40% margin claim" beats "improve citations."
- The critic's voice is direct. Hedge only when the evidence itself is ambiguous.

## Revise cycle

The synthesizer can apply your revisions and flip the memo back to `IN PROGRESS` → `COMPLETE` for a second review. Cap at 2 rounds. After round 2, surface remaining findings to the user inline rather than looping.

## Write-protocol reference

Paste `${CLAUDE_PLUGIN_ROOT}/skills/product-strategy/references/write-protocol.md` into your task prompt's `<write_protocol>` tags. Edit `review-strategy.md` after every dimension is assessed.

## Output format

```markdown
# Strategy Review — {{ slug }}

**Status:** IN PROGRESS
**Round:** {{ 1 or 2 }}

## Summary

[2–3 sentences: overall coherence, strongest aspects, top revision priorities.]

**Score:** [Strong / Needs revision / Needs rework]
**Critical:** [N] **Warnings:** [N] **Suggestions:** [N]

## Dimension scores

| Dimension                     | Score                    | Evidence   |
| ----------------------------- | ------------------------ | ---------- |
| Diagnosis matches evidence    | Pass / Warn / Fail       | [specific] |
| Guiding policy is non-trivial | Pass / Warn / Fail       | [specific] |
| Actions are coherent          | Pass / Warn / Fail       | [specific] |
| Wardley claims verifiable     | Pass / Warn / Fail / N/A | [specific] |
| Customer framing specific     | Pass / Warn / Fail / N/A | [specific] |
| Minto structure holds         | Pass / Warn / Fail       | [specific] |
| Risks are honest              | Pass / Warn / Fail       | [specific] |
| Attribution is clean          | Pass / Warn / Fail       | [specific] |
| Bad-strategy checks pass      | Pass / Warn / Fail       | [specific] |

## Critical issues

[Must-fix with memo section references and specific problems.]

## Warnings

[Should-fix with memo section references.]

## Suggestions

[Nice-to-have.]

## Specific revision recommendations

1. [Section X, line Y: change Z because W.]
2. ...
```

Flip `Status:` to `COMPLETE` when every dimension has a graded score and every finding has a specific recommendation.
