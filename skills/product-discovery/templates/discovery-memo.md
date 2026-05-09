---
slug: {{ slug }}
sequence: {{ NNN }}
route: discovery-round
status: draft
---

**Status:** IN PROGRESS

<write_protocol>
{{ paste ${CLAUDE_PLUGIN_ROOT}/skills/product-discovery/references/write-protocol.md verbatim }}
</write_protocol>

# Discovery Memo: {{ title }}

One-paragraph summary of what this round investigated and what the team should do next. Written last; assembled by the discovery-lead during Phase 3.

---

## Problem

Grounded in 3+ source citations. Not the solution; not a feature list. The observed friction, the trigger situation, the emotional texture, and what "fixed" looks like from the user's perspective.

- **Observed friction**: ...
- **Trigger situation**: ...
- **Emotional texture**: ...
- **Fixed feels like**: ...

### Sources

1. [source 1] — quote or observation
2. [source 2] — quote or observation
3. [source 3] — quote or observation

---

## Users

Who's affected. Not demographics alone — situations, contexts, workflows. Pulled from the source material in Problem. If JTBD interviews were run, the situations here match the situations in the job stories below.

- **Primary situation**: {{ who, when, what they're doing }}
- **Secondary situation**: {{ another context where the friction appears }}

---

## JTBD Job Stories

{{ If the jtbd-interviewer role ran; otherwise note "JTBD interviews not in scope for this round." }}

1. When [situation], I want [motivation], so I can [outcome].
   - Source: [ticket / quote / observation]
2. When [situation], I want [motivation], so I can [outcome].
   - Source: [ticket / quote / observation]
3. When [situation], I want [motivation], so I can [outcome].
   - Source: [ticket / quote / observation]

---

## HMW Set

{{ If the hmw-framer role ran; otherwise note "HMW reframing not in scope — problem already well-framed." }}

Strategies used: {{ strategy 1, strategy 2, strategy 3 }}

1. **HMW-1** [{{ strategy }}] How might we ... ?
2. **HMW-2** [{{ strategy }}] How might we ... ?
3. **HMW-3** [{{ strategy }}] How might we ... ?

NN/g validation passed on all HMWs (see `brainstorms/NNN-{{ slug }}-requirements.md` for the full validation table).

---

## Candidate Directions

Generated during Phase 3 of the discovery methodology. Each direction has a name, a concrete example, and a which-pain-point mapping. The point is not to pick one here — it's to surface the tradeoffs so the team can pick after reading.

### Direction 1 — {{ descriptive name }}

**Concept**: {{ one paragraph }}

**Concrete example**: {{ what the user would see or do }}

**Tradeoffs**: {{ what this direction gives up }}

**Addresses**: {{ which pain from Problem }}

### Direction 2 — {{ descriptive name }}

**Concept**: ...

**Concrete example**: ...

**Tradeoffs**: ...

**Addresses**: ...

### Direction 3 — {{ descriptive name }}

(Repeat for each direction; 4-6 total, per `discovery-rounds.md` Phase 3.)

---

## Data Model

Translates the strongest direction(s) into a concrete data model. Field names, types, status enums, relationships. Includes a decision-journal pattern if the product is agent-shaped.

```text
{{ Entity }}:
  id:          string
  {{ field }}: {{ type }}
  status:      {{ enum with explicit transitions }}
  created_at:  timestamp
```

Cross-references to existing models in the codebase (if any) — grounds the model in Vector 1 of landscape research.

---

## Vocabulary Mapping

Framework this round maps onto: {{ Twilio A2H / Levels of Autonomy / Double Diamond / other }}

Why this framework: {{ one paragraph }}

Mapping:

- [Concept] → [Framework category]
- [Concept] → [Framework category]

See `${CLAUDE_PLUGIN_ROOT}/skills/agent-ux-patterns/references/key-frameworks.md` for agent-system frameworks.

---

## Next Steps

- **Build first**: {{ what a first prototype or v0 would be; scoped to a sprint or less }}
- **Validate next**: {{ what uncertainty remains after this round; what experiment or interview would resolve it }}
- **Defer**: {{ directions worth revisiting but not now; explicit parking lot }}

Route forward:

- [ ] Proceed to PRD — spawn product-discovery with the discovery memo as the brief.
- [ ] Proceed to HMW-only — expand one direction via another HMW round.
- [ ] Proceed to prototype — skip PRD for a 1-sprint spike.
- [ ] Park — revisit after more data.

---

## Synthesis log

{{ the discovery-lead notes each routing call and each compose decision here }}

- Routing call: ran {{ framework or role }} because {{ rationale }}.
- Routing call: skipped {{ framework or role }} because {{ rationale }}.

---

When every section has real content, flip `Status: IN PROGRESS` → `Status: COMPLETE`.
