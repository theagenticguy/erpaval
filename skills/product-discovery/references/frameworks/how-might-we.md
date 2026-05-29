# How Might We

Reframes research-grounded problem statements into 3-5 outcome-level "How might we..." questions. Originally Stanford d.school / IDEO; popularized by NN/g for UX research integration.

## Contents

- Canonical structure
- d.school nine reframing strategies
- NN/g validation (all five must pass)
- When to use
- When to skip
- Template
- Worked example
- Validation checks
- Citations

## Canonical structure

NN/g template:

> How might we **[action]** for **[user segment]** to **[achieve outcome]**?

Each word earns its place:

- **How** — assumes a solution exists (optimism).
- **Might** — signals possibility, not commitment.
- **We** — collaborative framing.

Three-step process (NN/g):

1. Identify insights from research (not assumption).
2. Define needs — what change is the user seeking?
3. Formulate HMW — outcome-oriented, not solution-shaped.

## d.school nine reframing strategies

When a first-pass HMW is too narrow or too broad, the Bootcamp Bootleg suggests nine transformation moves:

1. **Amp up the good** — magnify an existing positive aspect.
2. **Remove the bad** — strip away what causes friction.
3. **Explore the opposite** — reverse the obvious assumption.
4. **Question an assumption** — challenge what "must" be true.
5. **Go after adjectives** — reframe the qualitative feel.
6. **ID unexpected resources** — use what's already there differently.
7. **Create an analogy** — borrow from an unrelated domain.
8. **Play against the challenge** — reframe constraint as feature.
9. **Change a status quo** — provoke by inverting the default.

Pick three strategies per run, not nine — see `roles/hmw-framer.md` for the starting-point heuristic.

## NN/g validation (all five must pass)

| Check                                    | Fix if violated                                      |
| ---------------------------------------- | ---------------------------------------------------- |
| Grounded in research (not imagined)      | Cite the error rate, user report, or incident        |
| No embedded solutions                    | Restate at the outcome level                         |
| Broad enough to admit multiple solutions | Widen scope — don't constrain to one technique       |
| Targets desired outcomes, not symptoms   | Ask "why does this matter?" until you hit an outcome |
| Positive framing                         | Flip negatives to their positive counterpart         |

## When to use

After user research, at the Define → Develop transition of Double Diamond. Pair with Crazy 8s, brainwriting, or SCAMPER for ideation. Also the default route when the user's ask is solution-shaped ("build a dashboard" → HMW reframes to "How might we help ops staff see the system's state at a glance?").

## When to skip

- Before any research is done — HMW with no grounding is just brainstorming with extra steps.
- Executional questions with a known answer.
- Mature products where the problem is already sharp.

## Template

Seeded from `templates/hmw-skeleton.md`. Shape:

```text
# Problem
Today, <users> have to <workaround> when <trigger>.
Customers need a way to <desired outcome>.

# How Might We
- HMW-1 [<strategy>] How might we <verb> <object> <for whom> <when>?
- HMW-2 [<strategy>] ...
- HMW-3 [<strategy>] ...

# NN/g validation
- grounded: yes — [citation]
- no embedded solutions: yes
- broad: yes
- targets outcome not symptom: yes
- positive framing: yes
```

## Worked example

Before HMW: "Users hate our login screen."

After HMW (strategy: Remove the bad):

> HMW-1 [Remove the bad] How might we reduce the friction of returning Android users signing in for the second time, so they reach the feed without retyping credentials?

After HMW (strategy: Question an assumption):

> HMW-2 [Question an assumption] How might we let power users skip the username step entirely, given that 82% of login attempts come from a trusted device?

After HMW (strategy: Explore the opposite):

> HMW-3 [Explore the opposite] How might we turn the login screen into a useful surface — a check-in, a digest preview — instead of a gate to pass through?

## Validation checks

- All 5 NN/g guardrails pass on every HMW.
- At least 3 HMWs written; at most 5. More fatigue review; fewer under-explore.
- Each HMW references a different d.school strategy.
- `strategies_used:` in frontmatter lists the three strategies picked.

## Citations

- [NN/g, "Problem Statements in UX Discovery"](https://www.nngroup.com/articles/problem-statements/) — Maria Rosala on HMW guardrails.
- [Stanford d.school, Design Thinking Bootleg](https://dschool.stanford.edu/resources/the-bootcamp-bootleg) — 2018 update (2010 Bootcamp Bootleg remains canonical).
- [User Research Strategist, "A Guide to How Might We Statements"](https://www.userresearchstrategist.com/p/a-guide-to-how-might-we-statements) — 2024 practitioner write-up.
