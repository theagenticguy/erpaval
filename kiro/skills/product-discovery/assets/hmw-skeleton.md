---
slug: <slug>
sequence: NNN
status: draft
strategies_used: []
---

**Status:** IN PROGRESS

<write_protocol>
{{ paste ${ERPAVAL_HOME}/skills/product-discovery/references/write-protocol.md verbatim }}
</write_protocol>

# Problem

Today, <users> have to <workaround>
when <trigger / situation>.
Customers need a way to <desired outcome>.

# How Might We

- HMW-1 [<strategy>] How might we ... ?
- HMW-2 [<strategy>] How might we ... ?
- HMW-3 [<strategy>] How might we ... ?

# NN/g validation

- grounded: yes / no — <citation>
- no embedded solutions: yes / no
- broad: yes / no
- targets outcome not symptom: yes / no
- positive framing: yes / no

---

## Instructions

Seed this file before launching the `hmw-framer` subagent. The agent edits it in place per the write protocol.

- `<users>` names a specific segment, not "users" generically.
- `<workaround>` describes what they do today that's painful.
- `<trigger>` is the situation that creates the pain.
- `<desired outcome>` is the outcome, not a solution.

Strategies (pick 3 of 9 d.school moves — see `${ERPAVAL_HOME}/skills/product-discovery/references/roles/hmw-framer.md` for the full list and starting-point heuristic):

1. Amp up the good · 2. Remove the bad · 3. Explore the opposite · 4. Question an assumption · 5. Go after adjectives · 6. ID unexpected resources · 7. Create an analogy · 8. Play against the challenge · 9. Change a status quo.

When every HMW passes NN/g validation and every field is filled, flip `Status: IN PROGRESS` → `Status: COMPLETE`.
