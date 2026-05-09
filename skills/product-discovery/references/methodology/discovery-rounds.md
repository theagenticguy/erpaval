# Discovery Rounds — Pain-Point-First Methodology

A six-phase methodology for product discovery sessions that start with a vague pain point and end with a concrete data model, prior-art landscape, and prioritized backlog. Absorbed from the retired `design-thinking` skill. The orchestrator's discovery-round route (see `orchestrator.md` Phase 2) fans out agents against these phases.

The shape maps cleanly onto Double Diamond: Phase 1-2 are Discover (problem-space divergence), Phase 3-4 are Define (problem-space convergence), Phase 5 is Develop (solution-space convergence for the data model), Phase 6 is Deliver (handoff).

---

## Phase 1 — Pain Point Excavation

Start with the user's stated friction, not the solution. Ask clarifying questions to find the root cause before generating options.

Pattern: "I'm juggling too many X" usually means the triage or prioritization layer is missing, not that X needs to be reduced. A solution framed as "build Y" almost always hides a deeper "because Y, then Z, then real problem."

Questions that open the space:

- What's the actual workflow today?
- Where does it break down?
- What's the emotional texture? (Overwhelm, boredom, anxiety, context-switching fatigue)
- What would "fixed" feel like from the user's perspective?

End of Phase 1 deliverable: one paragraph naming the observed friction, the trigger situation, and the desired outcome. Not a solution. Not a feature.

---

## Phase 2 — Landscape Research (Three Vectors)

Research three areas in parallel before proposing solutions. Each vector surfaces different constraints.

**Vector 1 — Internal codebase**: What data, models, events, and infrastructure already exist? What's the richest unexploited data source? What patterns has the team already established? Grep the codebase; read recent PRDs; list existing tables.

**Vector 2 — Prior art**: What have others built for this problem? Open-source projects, commercial products, academic papers, blog posts. Find the closest direct competitor and study it end-to-end. Cite URLs.

**Vector 3 — Adjacent platforms**: What native capabilities does the deployment platform offer (Slack features, GitHub Actions, AWS services, browser APIs)? Often the best solution is assembling existing primitives, not building from scratch.

Often the research-scout role (see `roles/research-scout.md`) owns Vector 2 and Vector 3; the discovery-lead owns Vector 1.

---

## Phase 3 — Multi-Direction Brainstorm

Generate 4-6 distinct directions, each with:

- A descriptive name ("Thread Command Center", "Delegation Dashboard").
- One-paragraph concept description.
- A concrete example showing what the user would see or do.
- Tradeoffs and constraints.
- Which pain point from Phase 1 it addresses.

Avoid converging too early. Present all directions before recommending. Let the user's reaction guide which to expand. The trap is picking the first plausible direction — then every downstream artifact is load-bearing on an unvalidated assumption.

This is where HMW reframing (see `frameworks/how-might-we.md`) earns its keep — an HMW-set converts the Phase-1 pain statement into 3-5 opportunity frames, each of which seeds one brainstorm direction.

---

## Phase 4 — Vocabulary Mapping

Map the emerging concept to an established framework or vocabulary. This is load-bearing for:

- Making the design legible to others.
- Avoiding reinventing terminology.
- Discovering gaps — if a framework has 5 categories and you only covered 3, what are the missing 2?

Sources of grounded vocabulary:

- Industry protocols (e.g., Twilio A2H: INFORM, COLLECT, AUTHORIZE, ESCALATE, RESULT — see `agent-ux-frameworks.md`).
- Academic frameworks (e.g., Levels of Autonomy: L0-L5 — see `agent-ux-frameworks.md`).
- Design pattern catalogs (e.g., agentic-design.ai).
- Existing product taxonomies (Double Diamond, JTBD, PR-FAQ — see `frameworks/INDEX.md`).

Good vocabulary is:

- **Exhaustive** — every instance of the concept maps to exactly one category.
- **Implies priority** — categories have a natural ordering.
- **Composable** — categories combine for complex cases.

---

## Phase 5 — Data Model Synthesis

Translate the concept into a concrete data model. Forces precision on what felt like vibes in Phase 3. Include:

- Field names and types.
- Status enums with clear transitions.
- Relationships to existing models.
- The "decision journal" pattern — always capture what the human decided, why, and how long they spent.

Example shape:

```text
Item:
  id:          string
  intent:      enum (from vocabulary)
  source:      reference to originating system
  title:       string (8-word summary)
  detail:      rich_text (expandable)
  artifacts:   [{type, ref, label}]
  status:      pending | acted_on | dismissed | expired
  created_at:  timestamp
  decision:    {action, reason, duration_s} | null
```

For PRD-route runs, this phase is where the system-architect role takes over (see `roles/system-architect.md`). For discovery-round runs, the discovery-lead sketches the model; the PRD comes later.

---

## Phase 6 — Delivery and Persistence

The discovery output is a `discovery-memo.md` (see `templates/discovery-memo.md`). Sections:

- Problem (from Phase 1).
- Users (from Phase 1, sharpened by Phase 2).
- JTBD Job Stories (if run — see `roles/jtbd-interviewer.md`).
- HMW Set (if run — see `roles/hmw-framer.md`).
- Candidate Directions (from Phase 3).
- Data Model (from Phase 5).
- Next Steps — what to build first, what to validate next, what to defer.

For Slack-based delivery, the memo is additionally posted as Block Kit sections. For everything else, the memo file on disk is the source of truth.

---

## Conversation discipline

When running a discovery round interactively:

- Start divergent (many ideas), converge gradually based on user reactions.
- Use concrete examples over abstract descriptions — show mock inbox items, not capability lists.
- Map to established frameworks early — it makes the design feel grounded.
- Always end with a data model — forces precision on what felt like vibes.
- Persist everything — the memo file is the artifact; nothing lives only in chat.
- Research before proposing — never skip Phase 2.
- Let the user drive convergence — present options, don't pick for them.
