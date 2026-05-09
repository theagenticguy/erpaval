# Explorer: {{ vector_name }} — {{ problem_title }}

**Status:** IN PROGRESS
**Vector:** {{ vector_name }}
**Last updated:** {{ timestamp }}

---

## Protocol

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

---

## 1. Problem Framing

*How you're reading the problem. One or two sentences.*

## 2. Chosen Approach

*The high-level approach you're taking, shaped by your vector. Name the shape (e.g., "event-driven with a durable queue" or "synchronous in-process with a retry loop").*

## 3. Key Decisions

*Each decision as a short block: what you'd do, why, and the tradeoff. Cite adjacent code paths where relevant.*

### Decision A

### Decision B

### Decision C

## 4. Implementation Steps

*Ordered list of concrete steps. Each step: what file or module, what the change is, what verifies it.*

1.
2.
3.

## 5. Risks and Tradeoffs

*What you're giving up with this approach. What could go wrong. What you'd watch for.*

## 6. Verification Criteria

*How you'd know this plan worked: tests, observable outputs, smoke tests.*
