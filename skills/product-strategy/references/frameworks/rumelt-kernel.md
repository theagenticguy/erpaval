# Rumelt Kernel

## Canonical structure

Three elements. All three must be present for the artifact to count as strategy rather than a wishlist [1, 2].

1. **Diagnosis** — a clear-eyed read of the situation that identifies the central challenge and separates symptoms from root causes. "Our revenue is declining" is a symptom; "our distribution channel has commoditized while our cost structure assumes the old margins" is a diagnosis.
2. **Guiding policy** — the overall approach to overcoming the challenge. Guardrails on a highway: they direct and constrain action without fully defining it. Not a goal, not a slogan — a chosen angle of attack.
3. **Coherent actions** — coordinated, feasible moves that carry out the guiding policy. These are the substance of strategy, not "implementation." Every action must fit the guiding policy, and the actions must fit each other.

**The Crux (2022 refinement)** [3, 4]: the crux is the *single most important, surmountable, high-impact* challenge — the one pitch on the climb where the whole route hinges. Name it, concentrate resources, resist distraction. In practice, the Crux sits inside the diagnosis and sharpens it from "here's what's going on" to "here's the one thing that must be solved first."

**Four hallmarks of bad strategy** [1]:

- **Fluff** — buzzwords that mask substance ("customer-focused intermediation" = banking).
- **Failure to face the challenge** — plans that avoid naming the real obstacle.
- **Mistaking goals for strategy** — aspirational targets without a plan to overcome obstacles.
- **Bad strategic objectives** — long scattered lists that dilute focus, or "blue-sky" goals.

## When to use

Any decision point where a team is generating lists of goals without a diagnosis — roadmap prioritization, portfolio bets, reorganizations, "should we build this" questions. Especially effective when a strategy doc exists but reads as aspiration, not direction. The Crux variant specifically fits "we have too many fires — which one actually matters?"

## When to skip

Skip when the diagnosis is already agreed and the team is in execution. Skip when the decision is tactical — "which font should the button use" does not earn a kernel. Skip when a long-form narrative process is already doing the same job via SCQA and customer-problem framing; duplicate kernels add friction without insight.

## Template / worked example

Fill in inline; this is the raw shape of a Rumelt packet.

```markdown
## Challenge

[One paragraph: what problem is on the table, who's asking, and what "solving it" would look like.]

## Diagnosis

[The one claim about the situation that, if true, changes what we do. Cite evidence inline.
Distinguish: symptoms we see vs root cause we claim.
Name the crux: the single pivotal challenge this strategy resolves around.]

## Guiding policy

[The angle of attack. A policy is a chosen approach, not a list of goals.
It constrains future action without fully defining it.
Example shape: "Compete on [X] by concentrating [Y], because [Z]."]

## Coherent actions

1. [Action — specific, coordinated, feasible. Says who does what by when.]
2. [Action — must reinforce action 1, not cut against it.]
3. [Action — every action carries the guiding policy forward.]

## Bad-strategy checks

- Fluff: [any buzzwords masking substance? Name them.]
- Face the challenge: [did we name the real obstacle, or dance around it?]
- Goals vs strategy: [are any actions just restated aspirations?]
- Scattered objectives: [is the action set focused, or a kitchen-sink list?]
```

**Worked example — diagnosis excerpt**:

> Symptoms: five teams are each building their own LLM eval harness. Root-cause diagnosis: there is no shared contract for what "correct agent behavior" means, and every team encodes its own implicit contract in code. The crux is not "we need an eval tool" — it is "we need a contract before we can have a tool."

## Validation checks

- Diagnosis names a challenge, not a state. "Declining revenue" is a state; "our cost structure assumed margins that commoditization killed" is a diagnosis.
- Guiding policy is non-trivial — it rules out at least one defensible alternative. If every competitor would adopt the same policy, it isn't a policy.
- Actions are coherent — no action cuts against another.
- The crux is named explicitly.
- None of the four hallmarks of bad strategy apply.
- Evidence is cited inline, not dumped in a footer.

## Citations

- [3] Rumelt, R. *The Crux: How Leaders Become Strategists.* Public Affairs, 2022.
- [41] [BCG Henderson Institute podcast with Rumelt on The Crux](https://bcghendersoninstitute.com/the-crux-with-richard-rumelt/) (2022).
- [2] [Digital Rebel, "Good Strategy Has Three Parts. Most Have Zero."](https://digitalrebel.fi/blog/good-strategy-has-three-parts-most-have-zero) (2025).
- [38] [Alex Murrell, "Richard Rumelt: Good Strategy Bad Strategy."](https://www.alexmurrell.co.uk/summaries/richard-rumelt-good-strategy-bad-strategy) (2024).
- [1] Rumelt, R. *Good Strategy / Bad Strategy.* Crown Business, 2011.
