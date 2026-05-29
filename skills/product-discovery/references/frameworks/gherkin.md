# Gherkin (Given-When-Then)

Behavior-Driven Development scenario format. Dan North, ~2006. Executable by Cucumber, SpecFlow, Behave. The native language of modern BDD test suites.

## Contents

- Canonical structure
- Better Gherkin guidelines (Cucumber)
- When to use
- When to skip
- Template / worked example
- Validation checks
- EARS vs. Gherkin — when to use which
- Citations

## Canonical structure

```gherkin
Feature: Android biometric sign-in

  Scenario: Returning user signs in with biometric
    Given a returning Android user with biometric enrolled
    And the app is freshly launched
    When the user taps the biometric affordance
    Then the biometric prompt shall appear within 250ms
    And on success, the feed shall render within 5 seconds

  Scenario: Biometric fails three times, falls back to password
    Given a returning Android user with biometric enrolled
    When biometric authentication fails 3 consecutive times
    Then the login screen shall offer password entry
    And no account lockout shall be triggered
```

Keywords:

- **Feature** — the overarching capability (matches a user story or feature group).
- **Scenario** — one concrete path through the feature.
- **Given** — preconditions; state of the world at scenario start.
- **When** — the action under test.
- **Then** — the observable outcome.
- **And / But** — continuation of any of the above.

## Better Gherkin guidelines (Cucumber)

- Write declarative, not imperative — "the user signs in", not "the user clicks the button at (350, 480)".
- One scenario = one path through the feature.
- Keep Given/When/Then lean — long scenarios are test maintenance debt.
- Reuse Given clauses via Background.
- Tag scenarios (`@smoke`, `@regression`) for selective runs.

## When to use

- Happy path + named edge cases that need automated acceptance tests.
- Feature-level behavior where QA, product, and engineering need a shared vocabulary.
- Any system already running Cucumber, SpecFlow, Behave, or a compatible runner.
- Paired with EARS: EARS for invariants, Gherkin for the concrete examples that prove the invariant holds. See `ears.md`.

## When to skip

- Invariants that don't fit the "given/when/then" shape — use EARS (`ears.md`).
- Exploratory testing — Gherkin adds ceremony without adding coverage.
- Teams without a BDD runner — the scenarios turn into dead prose.

## Template / worked example

Gherkin lives inside the user story or spec file as a nested block. For a story with 3 scenarios:

```gherkin
Feature: <feature name matching the user story>

  Background:
    Given <shared precondition>

  Scenario: <happy path>
    When <action>
    Then <observable outcome>

  Scenario: <named edge case 1>
    When <action>
    Then <observable outcome>

  Scenario: <named edge case 2>
    When <action>
    Then <observable outcome>
```

For a Kiro/Spec Kit flow, the EARS spec drives the invariants and Kiro auto-generates Gherkin scenarios from them. Both formats coexist on the same story.

## Validation checks

- Every scenario has exactly one When clause (split if more than one action).
- Every Then clause names an observable outcome — not an internal state.
- Feature name matches the user story or feature group.
- Background is used when 3+ scenarios share a Given.
- Every scenario passes when run against the built feature; scenarios that skip or x-fail are flagged.

## EARS vs. Gherkin — when to use which

| Dimension   | Gherkin (Given-When-Then)        | EARS (5 templates)                    |
| ----------- | -------------------------------- | ------------------------------------- |
| Origin      | BDD / Cucumber, Dan North ~2006  | Rolls-Royce / Mavin 2009              |
| Primary use | Executable acceptance scenarios  | System behavior specification         |
| Granularity | Per-scenario, concrete examples  | Per-requirement, general rules        |
| Audience    | Developers + QA + product        | Engineers + requirements + AI agents  |
| Tooling     | Cucumber, SpecFlow, Behave       | Text — AI-parseable via Kiro/Spec Kit |
| Best for    | Happy path + specific edge cases | Invariants, unwanted behaviors, NFRs  |
| Weakness    | Verbose for invariants           | Not directly executable               |

Modern teams use **both** — EARS at the requirement level, Gherkin at the scenario level. Kiro explicitly generates Given/When/Then from EARS specs.

## Citations

- [Cucumber, "Better Gherkin"](https://cucumber.io/docs/bdd/better-gherkin/) — canonical guidelines.
- [Automation Panda, "BDD 101: The Gherkin Language"](https://automationpanda.com/2017/01/26/bdd-101-the-gherkin-language/) — practitioner primer.
- Dan North, "Introducing BDD" (2006) — original BDD essay.
