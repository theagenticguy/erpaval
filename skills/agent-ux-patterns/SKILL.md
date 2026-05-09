---
name: agent-ux-patterns
description: >
  Agent UX patterns and human-in-the-loop design: Twilio A2H protocol, Levels of Autonomy
  (L0-L5), inbox pattern, progressive trust, decision journal, gate reviews, autonomous
  work reports. Six-phase methodology from vague pain point to concrete data model via
  landscape research and multi-direction brainstorming. Use when the user asks to design
  agent UX, pick an autonomy level, build a human-in-the-loop flow, structure an agent
  inbox, design approval gates, or mentions A2H, autonomy level, progressive trust,
  inbox pattern, approval gate, decision journal, or agentic design. Do NOT use for PRD
  drafting — use product-discovery. Do NOT use for frontend components — use
  frontend-design. Do NOT use for building agents with a specific SDK — use
  claude-agent-sdk, strands-sdk, langgraph-langchain, or mastra-vercel-ai.
---

# Agent UX Patterns

A structured methodology for designing agent user experiences — particularly the human-in-the-loop surfaces (inbox, gates, reviews, trust) where agents and humans collaborate. Optimized for conversations that start with a vague pain point ("users feel overwhelmed by the agent's outputs") and end with a concrete data model, interaction vocabulary, and prioritized backlog.

This skill focuses on the *agent-side* design problem: how agents surface work for review, how autonomy levels shift over time, how trust accrues through observation of human responses. For *product-discovery* disciplines (customer research, problem framing, PR/FAQ authoring), see the shared references in `${CLAUDE_PLUGIN_ROOT}/skills/product-design-shared/references/` and the consumer skills that wrap them (`working-backwards`, `customer-research`).

## The Process

### Phase 1: Pain Point Excavation

Start with the user's stated friction, not the solution. Ask clarifying questions to find the root cause.

Pattern: "I'm juggling too many X" usually means the triage/prioritization layer is missing, not that X needs to be reduced.

- What's the actual workflow today?
- Where does it break down?
- What's the emotional texture? (Overwhelm, boredom, anxiety, context-switching fatigue)
- What would "fixed" feel like from the user's perspective?

### Phase 2: Landscape Research (Three Vectors)

Research three areas in parallel before proposing solutions:

**Vector 1: Internal codebase** — What data, models, events, and infrastructure already exist? What's the richest unexploited data source? What patterns has the team already established?

**Vector 2: Prior art** — What have others built for this problem? Open-source projects, commercial products, academic papers, blog posts. Find the closest direct competitor and study it.

**Vector 3: Adjacent platforms** — What native capabilities does the deployment platform offer? (Slack features, GitHub Actions, AWS services, browser APIs). Often the best solution is assembling existing primitives, not building from scratch.

### Phase 3: Multi-Direction Brainstorm

Generate 4-6 distinct directions, each with:

- A descriptive name (e.g., "Thread Command Center", "Delegation Dashboard")
- One-paragraph concept description
- A concrete example showing what the user would see/do
- Tradeoffs and constraints
- Which pain point it addresses

Avoid converging too early. Present all directions before recommending. Let the user's reaction guide which to expand.

### Phase 4: Vocabulary Mapping

Map the emerging concept to an established framework or vocabulary. This is critical for:

- Making the design legible to others
- Avoiding reinventing terminology
- Discovering gaps in the design (if a framework has 5 categories and you only covered 3, what are the missing 2?)

Sources of good vocabulary:

- Industry protocols (e.g., Twilio A2H: INFORM, COLLECT, AUTHORIZE, ESCALATE, RESULT)
- Academic frameworks (e.g., Levels of Autonomy: L0-L5)
- Design pattern catalogs (e.g., agentic-design.ai)
- Existing product taxonomies

The vocabulary should be:

- **Exhaustive** — every instance of the concept maps to exactly one category
- **Implies priority** — categories have a natural ordering
- **Composable** — categories can combine for complex cases

### Phase 5: Data Model Synthesis

Translate the concept into a concrete data model. Include:

- Field names and types
- Status enums with clear transitions
- Relationships to existing models
- The "decision journal" pattern — always capture what the human decided, why, and how long they spent

Example pattern:

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

### Phase 6: Delivery and Persistence

For Slack-based conversations:

- Use Block Kit for structured messages (headers, sections, dividers, context blocks)
- Save to Canvas for living documents that evolve over session boundaries
- Create backlog items for all concrete implementation work
- Link everything: canvas URL in backlog items, backlog IDs in canvas

## Agent-Specific Design Patterns

### The Inbox Pattern

Every agent-to-human interaction is one of five types (A2H vocabulary):

| Intent    | User Action               | Priority | Color |
| --------- | ------------------------- | -------- | ----- |
| ESCALATE  | Take over, agent is stuck | Highest  | Red   |
| AUTHORIZE | Approve/reject a gate     | High     | Amber |
| COLLECT   | Provide structured input  | Medium   | Blue  |
| RESULT    | Review completed work     | Low      | Green |
| INFORM    | Awareness only            | Lowest   | Grey  |

The inbox composition is itself a trust metric: early on it's AUTHORIZE-heavy (agent asks permission), over time it shifts to INFORM-heavy (agent reports what it did).

### Progressive Trust

Trust is learned, not configured. The mechanism:

1. Agent completes work → item appears in inbox
2. Human acts (fast rubber-stamp vs. slow deep review)
3. Memory system observes review depth and outcomes
4. Next time: fast-approved categories auto-advance, slow-reviewed categories stay blocking
5. Inbox gets quieter over time as trust builds

Maps to Levels of Autonomy:

- L2 (approve before execution) = AUTHORIZE-heavy inbox
- L3 (review after execution) = RESULT-heavy inbox
- L4 (spot-check only) = INFORM-heavy inbox

### The Decision Journal

Every human action on an inbox item is recorded:

- What action was taken (approve, reject, redirect, escalate)
- Why (free-text reason, optional)
- How long the review took (timestamp delta)
- What artifacts were viewed

This journal feeds the progressive trust engine and provides an audit trail.

### Gate Reviews (Phase/Gate Pattern)

Projects decompose into phases with gates between them:

- Each phase produces typed artifacts
- Gates can be blocking (human must act) or auto-advance (learned from history)
- Optimistic locking prevents two agents from claiming the same phase
- The gate type migrates from blocking → auto as trust builds

### Autonomous Work Reports

For sandboxed agent execution:

- Budget tracking (turns used/max, cost used/max)
- Artifact links (PRs, docs, analysis)
- Session replay link for deep-dive
- "Stop and report" fallback when budget exhausted

## Conversation Style

When running a design thinking session:

- Start divergent (many ideas), converge gradually based on user reactions
- Use concrete examples over abstract descriptions — show mock inbox items, not capability lists
- Map to established frameworks early — it makes the design feel grounded
- Always end with a data model — forces precision on what felt like vibes
- Persist everything — canvas for living docs, backlog for implementation work
- Use rich formatting — Block Kit for Slack, structured tables, clear visual hierarchy
- Research before proposing — never skip the landscape research phase
- Let the user drive convergence — present options, don't pick for them

## Reference Material

See `${CLAUDE_PLUGIN_ROOT}/skills/agent-ux-patterns/references/key-frameworks.md` for detailed framework descriptions (Twilio A2H Protocol, Levels of Autonomy, Slack primitives).

## References

| File                           | Contents                                                                                                       |
| ------------------------------ | -------------------------------------------------------------------------------------------------------------- |
| `references/key-frameworks.md` | Twilio A2H Protocol, Levels of Autonomy (L0-L5), OpenHands Outer Loop, LangChain Agent Inbox, Slack primitives |
