# Double Diamond — UK Design Council framework

Shared reference for the Double Diamond design process model. Canonical owner: the **UK Design Council** (designcouncil.org.uk), created 2004, expanded into the **Framework for Innovation** in 2019, complemented by the **Systemic Design Framework** thereafter.

This file explains the discipline so other skills can compose against it without duplicating the method.

## The principle

The Double Diamond describes design thinking as two back-to-back diamonds:

- **Diamond 1 — Problem space**: *Discover* (diverge to understand the problem) → *Define* (converge to the framed brief).
- **Diamond 2 — Solution space**: *Develop* (diverge across candidate solutions) → *Deliver* (converge on a tested launch).

The shape is load-bearing. The implicit discipline is *"Are we building the right thing?"* before *"Are we building the thing right?"* Teams that skip straight to ideation solve the wrong problem well.

```text
Discover           Define            Develop           Deliver
(diverge)         (converge)        (diverge)         (converge)
   ◆                  ◆                 ◆                  ◆
    \                / \               / \                /
     \   problem   /   \   solution  /   \   solution  /
      \   space   /     \    space   /    \   space   /
       \        /        \          /      \        /
        problem-framed    solution-found   solution-tested
        (brief)           (prototypes)     (launch)
```

## The four phases

Each phase alternates divergent (expand options) and convergent (narrow down) thinking.

| Phase        | Space    | Thinking   | Activities                                                                                                                                                         | Primary output                                            |
| ------------ | -------- | ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ | --------------------------------------------------------- |
| **Discover** | Problem  | Divergent  | "Understanding rather than assuming the problem through direct engagement with affected people." User research, ethnography, stakeholder interviews, market scans. | Raw insights, qualitative + quantitative data             |
| **Define**   | Problem  | Convergent | "Reframing the challenge based on insights from discovery." Synthesis, affinity mapping, problem-statement and "How might we" framing.                             | A tightly framed design brief                             |
| **Develop**  | Solution | Divergent  | "Generating multiple solutions through inspiration-seeking and co-design." Ideation, sketching, prototyping, co-creation workshops.                                | A portfolio of prototypes and candidate concepts          |
| **Deliver**  | Solution | Convergent | "Testing solutions at small-scale, rejecting failures, and improving viable options." Usability testing, pilots, iterative refinement, launch.                     | A tested, shipped solution (or a validated kill decision) |

The phases are iterative in practice, not strictly linear. The Council's own 2019 update notes: "making and testing very early stage ideas can be part of discovery" and "no idea is ever 'finished'".

## The 2019 Framework for Innovation additions

The 2004 diagram described the *process*. The 2019 refresh describes what an organization needs *around* the process to actually use it. Three new layers:

### 1. Four design principles (applied in every phase)

- **Put people first** — user needs and aspirations
- **Communicate visually and inclusively** — shared understanding across stakeholders
- **Collaborate and co-create** — work with diverse partners, not for them
- **Iterate, iterate, iterate** — test early to reduce risk

### 2. Methods bank

Organized into three families:

- **Explore** — challenges and opportunities
- **Shape** — prototypes and insights
- **Build** — ideas and expertise

### 3. Organizational conditions

- **Leadership** — creates the conditions for innovation and experimentation
- **Engagement** — connects stakeholders and partners around the work

The rationale: process alone is not enough. Without leadership that tolerates ambiguity and engagement that brings in the right voices, even rigorous process stalls.

## The Systemic Design Framework (complementary)

Post-2019 the Council added a **Systemic Design Framework** for wicked problems (climate, public health, systemic inequities). It keeps the divergent/convergent core of the Double Diamond while adding a systems orientation. The Double Diamond remains the "essential guide" for product-scoped design work; Systemic Design is an umbrella methodology for cross-cutting challenges.

## Common misuses and critiques

- **Treating it as waterfall.** The visual is easy to read as a stage-gate. The Council and practitioners emphasize iteration and cycling back. Single most common misuse.
- **Skipping Diamond 1.** Teams jump to Develop because ideation is fun and problem-framing is uncomfortable. Result: a well-executed wrong solution.
- **Weak coverage of delivery/operations.** "Deliver" ends near launch. Post-launch ops, measurement, scaling, and lifecycle are not first-class; teams typically bolt on agile/DevOps or service-design blueprints.
- **Weak on stakeholder politics and funding.** The 2019 leadership/engagement layer acknowledges this but does not prescribe methods.
- **Ambiguous at enterprise scale.** The Council itself judged the Double Diamond insufficient for systemic problems and built the Systemic Design Framework on top.

## Comparison with other disciplines

### vs Working Backwards (Amazon)

| Dimension                  | Double Diamond                                    | Working Backwards                                                |
| -------------------------- | ------------------------------------------------- | ---------------------------------------------------------------- |
| Primary forcing function   | Process shape (divergence / convergence)          | **Artifact** (PR/FAQ, Dear Customer Letter)                      |
| Problem-space depth        | Large by construction (Diamond 1)                 | Compressed into 5CQ Q1–Q4; the PR simulates the "done" end-state |
| Solution-space depth       | Large (Diamond 2: Develop + Deliver)              | Invent stage is brief; Refine pins to customer-visible CX        |
| Iteration posture          | Implicit — "iterate" added as a principle in 2019 | Explicit — process is circular, Stage 5 feeds Stage 1            |
| Stakeholder alignment      | Weak in base; added in 2019 engagement layer      | First-class: PR/FAQ reviews *are* the alignment mechanism        |
| Metrics / launch           | "Deliver" ends near launch                        | Stage 5 + experimentation + post-launch quality scorecard       |
| Customer-research pipeline | Methods bank (abstract)                           | Concrete VoC tooling per organization                            |

### vs other design-thinking variants

- **Stanford d.school** (Empathize → Define → Ideate → Prototype → Test) — same spirit, five named stages instead of two diamonds. Foregrounds *empathy* as a named stage; DD folds empathy into Discover and foregrounds the divergent/convergent shape.
- **IDEO 3 I's** (Inspiration → Ideation → Implementation) — three-space model that maps cleanly onto DD (Inspiration ≈ Discover + Define; Ideation ≈ Develop; Implementation ≈ Deliver). IDEO is more narrative; DD is more diagrammatic.
- **IBM Enterprise Design Thinking** — continuous *Loop* (Observe, Reflect, Make) plus *Keys* (Hills, Playbacks, Sponsor Users). Explicitly non-linear and enterprise-governance-aware. Stronger on stakeholder alignment than DD; weaker on the problem/solution-space distinction.
- **Lean / Agile discovery** (Dual-track, Lean Startup Build–Measure–Learn) — continuous and hypothesis-driven rather than phase-shaped. Closer cousin to Diamond 2 alone. Often laid *over* DD so discovery (Diamond 1 + early Diamond 2) runs parallel to delivery (late Diamond 2), not sequentially.

## How DD maps to other disciplines in this repo

| DD phase | Working Backwards       | Pyramid                                     | Research design                          |
| -------- | ----------------------- | ------------------------------------------- | ---------------------------------------- |
| Discover | Listen                  | Evidence assembly (Phase 1)                 | Gather evidence via chosen methods       |
| Define   | Define                  | MECE grouping + argument construction       | Findings synthesis in Pyramid-base shape |
| Develop  | Invent + early Refine   | — (solution generation)                     | —                                        |
| Deliver  | Refine + Test & Iterate | Answer derivation + draft + antagonist test | —                                        |

See `working-backwards.md`, `pyramid-principle.md`, and `research-design.md` for the deep dives. See `methodology-selection.md` for when to pick which.

## When to reach for the Double Diamond

- Contexts where Working Backwards terminology would feel awkward to the team.
- Design-led teams where the divergent/convergent discipline is the point.
- Early-stage wicked problems where Diamond 1 (real problem framing) is load-bearing and premature convergence is the biggest risk.
- As a comparison anchor — when explaining Working Backwards to someone steeped in design-thinking vocabulary, pointing at the DD equivalent collapses a lot of translation work.

## Key sources

- Design Council, "The Double Diamond" — [designcouncil.org.uk/our-resources/the-double-diamond/](https://www.designcouncil.org.uk/our-resources/the-double-diamond/)
- Design Council, "Framework for Innovation" — [designcouncil.org.uk/our-resources/framework-for-innovation/](https://www.designcouncil.org.uk/our-resources/framework-for-innovation/)
- Design Council, "Systemic Design Framework" — [designcouncil.org.uk/our-resources/systemic-design-framework/](https://www.designcouncil.org.uk/our-resources/systemic-design-framework/)
- Wikipedia — "Double Diamond (design process model)"
- Origin: 2004, UK Design Council in-house team under Richard Eisermann; public launch 2005 via the "Eleven Lessons" study; visual model adapted from Béla H. Bánáthy (1996).
- License: Double Diamond visual re-released under CC BY 4.0 around its 20th anniversary (2023).
