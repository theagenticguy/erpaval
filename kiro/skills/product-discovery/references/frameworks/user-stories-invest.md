# User stories + INVEST

The agile backlog baseline. Kent Beck introduced user stories in XP (late 1990s); Rachel Davies at Connextra defined the current three-part template (early 2000s); Mike Cohn popularized it in *User Stories Applied* (2004). Bill Wake added INVEST as the quality rubric in 2003.

## Canonical structure

> **As a** [role], **I want** [goal], **so that** [benefit].

The three parts do different work:

- **Role** — who needs this (persona name or archetype).
- **Goal** — what outcome they're trying to reach.
- **Benefit** — the "why it matters" — not a restatement of the goal.

## INVEST criteria (Wake 2003)

Every story meets all six:

- **I**ndependent — can be built in any order, without blocking other stories.
- **N**egotiable — a placeholder for conversation, not a contract.
- **V**aluable — delivers value to a user or buyer.
- **E**stimable — the team can roughly size the effort. (Wake later noted he'd replace this with "External" if redesigning today.)
- **S**mall — fits in a single sprint; preferably a few days of work.
- **T**estable — has verifiable acceptance criteria.

## Composing with acceptance criteria

Modern practice: one user story carries multiple acceptance criteria. The criteria can be:

- **Gherkin scenarios** — best for "here's a concrete example that proves it." See `gherkin.md`.
- **EARS statements** — best for "here's an invariant or unwanted-behavior rule." See `ears.md`.
- **Plain bullet checklists** — fine for simple internal tools.

They don't conflict; use what fits the AC.

## When to use

Backlog items ready for development. The agile unit of work. Pairs with sprint planning, story-point estimation, and acceptance-test writing.

## When to skip

- Upstream discovery — use JTBD job stories (`jtbd-job-stories.md`).
- Pure system or technical requirements with no user-facing value — use EARS directly, no user-story wrapper needed.
- Research spikes or non-deliverable tasks — use a task or spike, not a user story.

## Template / worked example

Story:

> As a returning Android user, I want to sign in without retyping my password, so that I can reach my feed in under 5 seconds.

INVEST pass:

- Independent — doesn't block other stories.
- Negotiable — placeholder for a conversation about biometric vs. SSO vs. magic link.
- Valuable — reduces churn at the login gate.
- Estimable — scoped to "Android biometric" — team can size in points.
- Small — fits in a sprint.
- Testable — 5-second timer; biometric prompt observed; feed renders.

Acceptance criteria (EARS form, mixed with Gherkin for the happy path):

- **AC-1-1** [Ubiquitous] The login screen shall offer a biometric sign-in option when the device reports biometric capability.
- **AC-1-2** [Unwanted] If biometric authentication fails 3 consecutive times, then the system shall fall back to password entry with no lockout.
- **AC-1-3** Given a returning Android user with biometric enrolled, when they open the app, then the biometric prompt shall display within 1 second.

## Validation checks

- Story follows the three-part "As a / I want / so that" shape literally.
- Role is specific (not "user").
- Goal is outcome, not feature ("see my notifications at a glance", not "use the notifications panel").
- Benefit is separate from the goal (not a tautology).
- At least one AC per story, with at least one testable condition.
- P0/P1/P2 priority label set (see PRD template section 5.1).

## Citations

- [Bill Wake, "INVEST in Good Stories, and SMART Tasks"](https://xp123.com/articles/invest-in-good-stories-and-smart-tasks/) — 2003 canonical source.
- [Mountain Goat Software, "Why the Three-Part User Story Template Works So Well"](https://www.mountaingoatsoftware.com/blog/why-the-three-part-user-story-template-works-so-well) — Mike Cohn on the template.
- Cohn, M. *User Stories Applied for Agile Software Development.* Addison-Wesley, 2004.
- [Wikipedia, "INVEST (mnemonic)"](https://en.wikipedia.org/wiki/INVEST_(mnemonic)) — includes Wake's later reconsideration of "Estimable".
