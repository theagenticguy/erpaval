# Write Protocol

Canonical write-protocol block for explorers. The orchestrator copies it verbatim into every explorer's Task prompt and into every explorer-file skeleton. Single source of truth.

---

<write_protocol>
Your output file is the single source of truth for your plan. Edit it as each decision crystallizes, before moving to the next one. Decisions written to disk survive timeouts and early termination; thinking held in working memory does not.

The rhythm is: think through one decision → edit the file with your call and your reasoning → move to the next decision.

Work through your sections in numbered order. For each section:

1. Consider the decision. Read adjacent code or search when the answer isn't in your head.
2. Edit the file with your call: what you'd do, why, and the tradeoff you're accepting.
3. If the section needs more depth, think again and edit again.
4. Move to the next section only after the current one has real content.

Your divergence vector shapes every decision. When two answers both work, pick the one your vector prefers — that's your job. A plan that looks like the default "balanced" plan is a failed explorer; the critic needs your genuine bias to have something to pick from.

**Name the tradeoff** on every non-obvious call. "Chose X over Y because X is cheaper to reverse / faster to ship / has fewer moving parts" — the critic reads these attributions and uses them to compose the final plan.

Cite adjacent code inline when a decision depends on existing structure: `src/auth/session.py:42` style. The critic will read these to verify your reasoning.

When every section has real content, change the `Status:` line at the top of the file from `IN PROGRESS` to `COMPLETE`.
</write_protocol>
