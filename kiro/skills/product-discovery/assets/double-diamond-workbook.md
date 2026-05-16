---
slug: {{ slug }}
sequence: {{ NNN }}
framework: double-diamond
status: draft
---

**Status:** IN PROGRESS

<write_protocol>
{{ paste ${ERPAVAL_HOME}/skills/product-discovery/references/write-protocol.md verbatim }}
</write_protocol>

# Double Diamond Workbook: {{ title }}

Four stages, two diamonds. Each stage gets its own section with activities, timebox, sources consulted, and the observable output.

- **Diamond 1 — Problem space** (Discover → Define)
- **Diamond 2 — Solution space** (Develop → Deliver)

See `${ERPAVAL_HOME}/skills/product-design-shared/references/double-diamond.md` for the full framework reference.

---

## Diamond 1 — Problem space

### Stage 1 — Discover (diverge)

**Timebox**: {{ e.g., week 1 }}

**Goal**: Explore the problem landscape. Surface the right problem before picking a solution.

**Activities**:

- [ ] {{ e.g., 8 customer interviews }}
- [ ] {{ e.g., support-ticket mining }}
- [ ] {{ e.g., funnel / retention analysis }}
- [ ] {{ adjacent platform scan }}
- [ ] {{ competitive audit (see research-scout role) }}

**Sources consulted** (cite each):

1. {{ source 1 }}
2. {{ source 2 }}
3. {{ source 3 }}

**Observable output**: {{ e.g., "raw insight set — 40+ observations in insights.md" }}

**Decisions logged**:

- {{ what you observed that surprised the team }}
- {{ what assumptions you invalidated }}

---

### Stage 2 — Define (converge)

**Timebox**: {{ e.g., week 2 }}

**Goal**: Synthesize insights into a sharp problem statement. Output of this stage is usually a single problem statement plus an HMW set.

**Activities**:

- [ ] Affinity-map the Discover output.
- [ ] Draft the customer problem statement — see `frameworks/how-might-we.md` Step 1.
- [ ] Generate HMW candidates via the `hmw-framer` role.
- [ ] NN/g-validate every HMW.

**Observable output**:

- **Problem statement**: {{ one paragraph grounded in citations }}
- **HMW set**: 3-5 candidates in `brainstorms/NNN-{{ slug }}-requirements.md`.

**Transition check — is the team converged?**

- [ ] The team can recite the problem statement from memory.
- [ ] The HMW set is agreed on (not just approved — actually agreed).
- [ ] No one is advocating a solution yet.

Proceed to Diamond 2 only when the team passes this check. If not, loop back into Discover.

---

## Diamond 2 — Solution space

### Stage 3 — Develop (diverge)

**Timebox**: {{ e.g., week 3-4 }}

**Goal**: Generate multiple solution concepts. Prototype widely, test early, fail cheaply.

**Activities**:

- [ ] Multi-direction brainstorm (4-6 directions, see `discovery-rounds.md` Phase 3).
- [ ] Crazy 8s / brainwriting / SCAMPER against each HMW.
- [ ] Prototype 3 directions at low fidelity.
- [ ] Test prototypes with 5 users each.

**Observable output**:

- {{ e.g., "3 solution concepts, each tested with 5 users, in prototypes/NNN/" }}
- {{ e.g., "user reactions log" }}

**Decisions logged**:

- Which prototype converted best.
- What each prototype taught about user mental models.
- What new constraints emerged from testing.

---

### Stage 4 — Deliver (converge)

**Timebox**: {{ e.g., week 5-6 }}

**Goal**: Narrow to one solution. Build at higher fidelity. Test at small scale. Ship.

**Activities**:

- [ ] Pick the winning prototype based on Develop-stage data.
- [ ] Build hi-fi prototype or MVP.
- [ ] A/B or small-scale rollout.
- [ ] Measurement plan: what metric decides "this shipped."

**Observable output**:

- {{ e.g., "shipped v0 behind a feature flag to 100 users" }}
- {{ e.g., "measurement plan — metric, target, decision date" }}
- {{ e.g., "retro notes — what the round taught the team for next time" }}

---

## Synthesis summary

{{ written after all four stages complete — one paragraph capturing what the round delivered and what the team learned about the problem and the solution space }}

---

## Route forward

- [ ] Full discovery round complete — hand off to PRD (product-discovery PRD route).
- [ ] Discovery incomplete — loop back to Discover or Define.
- [ ] Solution shipped; start measurement.

When every stage has real content and an observable output, flip `Status: IN PROGRESS` → `Status: COMPLETE`.
