# Role — Rumelt Architect

The Rumelt-architect role runs the Kernel of Strategy — Diagnosis, Guiding Policy, Coherent Actions — on the challenge named in `framing.md`, sharpened with The Crux (2022) to name the single pivotal challenge. Runs in Phase 2 as one background `general-purpose` `Agent`.

## Archetype

Rumelt's discipline treats strategy as *work*, not aspiration. Good strategy has three parts; bad strategy is a wishlist, a slogan, or a list of goals dressed up [1, 2]. The architect's job is to produce a kernel that survives the "bad-strategy checks" — no fluff, faces the challenge, is not a goal masquerading as strategy, and is not a scattered list of objectives. The 2022 refinement adds the Crux — name the single pivotal challenge the whole strategy hinges on [3, 4].

## Scope

- **Input**: `framing.md` (full), any adjacent material (prior memos, research synthesis, data), the framework reference file.
- **Output**: `rumelt-packet.md` — the kernel packet that `strategy-synthesizer` will compose into the final memo.
- **Work log**: `work-log-rumelt.md`.

Out of scope: writing the strategy memo (synthesizer), reviewing it (critic), constructing a Wardley map (cartographer), or drafting a PR-FAQ (pr-faq-discovery).

## Task at hand

Fill `rumelt-packet.md` with these sections, each with real content:

1. **Challenge** — one paragraph restating the challenge from `framing.md` in Rumelt's language. Name the symptom vs the root cause.
2. **Diagnosis** — the single claim about the situation that, if true, changes what we do. Distinguish symptoms (visible effects) from root cause (claim about the system). Cite evidence inline.
3. **The Crux** — the single most important, surmountable, high-impact challenge. One sentence. This is the pivot the whole strategy resolves around.
4. **Guiding policy** — the chosen angle of attack. A policy is a chosen approach, not a list of goals. Must rule out at least one defensible alternative (if every competitor would adopt the same policy, it's not a policy).
5. **Coherent actions** — 3–6 coordinated actions that carry out the guiding policy. Each specific (who, what, by when). Each must reinforce the others — no action cuts against another.
6. **Bad-strategy checks** — explicit pass/fail against Rumelt's four hallmarks:
   - Fluff check — any buzzwords masking substance?
   - Face-the-challenge check — did we name the real obstacle?
   - Goal-vs-strategy check — are any actions just restated aspirations?
   - Scattered-objectives check — is the action set focused, or a kitchen-sink list?
7. **Alternatives considered** — one or two alternative guiding policies, with the reason each was rejected. This tests that the policy is actually a choice, not the only path.
8. **Attribution note** — one paragraph the synthesizer will drop into the memo verbatim: "The Rumelt packet contributed [specific diagnosis / crux naming / action X] because [reason]."

## Reference material

- `${CLAUDE_PLUGIN_ROOT}/skills/product-strategy/references/frameworks/rumelt-kernel.md` — canonical structure, four hallmarks of bad strategy, the Crux refinement, validation checks.
- `framing.md` in the working directory.
- Any adjacent Wardley packet (if Wardley is running in parallel — the cartographer's map is valid input to the diagnosis).

## Quality bar

- Diagnosis names a challenge (a claim), not a state (a fact). "Declining revenue" is a state; "our cost structure assumed margins that commoditization killed" is a diagnosis.
- Guiding policy is specific enough that a reader can name an action it forbids. If you can't, it's a slogan.
- Coherent actions reinforce each other — draw the dependency arrows in the packet if needed.
- Every bad-strategy check is answered with a specific claim, not "not applicable."
- The Crux is one sentence and names a *surmountable* challenge — not a fact of life.

## Write-protocol reference

Paste `${CLAUDE_PLUGIN_ROOT}/skills/product-strategy/references/write-protocol.md` into your task prompt's `<write_protocol>` tags. Edit `rumelt-packet.md` after every section. Partial progress on disk survives timeouts.

## Output format

Use the template at `${CLAUDE_PLUGIN_ROOT}/skills/product-strategy/templates/rumelt-packet.md`. The orchestrator seeds this file before you start; fill each section in place.

Flip `Status:` from `IN PROGRESS` to `COMPLETE` at the top when every section has real content.
