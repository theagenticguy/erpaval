# EARS

Easy Approach to Requirements Syntax — Mavin, Wilkinson, Harwood, Novak at Rolls-Royce (IEEE RE'09). Five structured templates plus a Complex composite. Adopted by AWS Kiro (2025) and GitHub Spec Kit (2025 RFC) as the canonical format for AI-assisted specification.

## Canonical structure — five templates + Complex

| # | Pattern           | Template                                             | Example                                                               |
| - | ----------------- | ---------------------------------------------------- | --------------------------------------------------------------------- |
| 1 | Ubiquitous        | `The <system> shall <response>`                      | *The system shall log all user activity.*                             |
| 2 | Event-driven      | `When <trigger>, the <system> shall <response>`      | *When a user submits the form, the system shall validate inputs.*     |
| 3 | State-driven      | `While <state>, the <system> shall <response>`       | *While charging, the device shall display a battery icon.*            |
| 4 | Optional feature  | `Where <feature>, the <system> shall <response>`     | *Where biometric login is enabled, the system shall use fingerprint.* |
| 5 | Unwanted behavior | `If <condition>, then the <system> shall <response>` | *If the payment gateway fails, then the system shall retry once.*     |
| 6 | Complex           | Composition of any of the above                      | *While logged in, when a user submits, the system shall validate.*    |

The `shall` is intentional and load-bearing — it's the normative verb from IEEE 29148. Do not replace with "must", "will", "should".

**GEARS (2024-2025)** generalizes `<system>` to any subject — agent, service, CLI, user. Use classic EARS by default; reach for GEARS when multiple subjects are involved in the same flow.

## AC numbering and dependency annotation

Each AC gets a stable ID: `AC-<story>-<n>` (e.g., `AC-1-3` = 3rd AC of User Story 1).

Two annotation markers:

- `[P]` — parallel-safe. Can run in isolated worktree with other `[P]` ACs.
- `Dependencies: AC-X-Y, AC-X-Z` — must wait for those ACs.

Derivation rules:

- Two ACs touch the same file → cannot both be `[P]`.
- AC-B calls code from AC-A → AC-B has `Dependencies: AC-A`.
- AC-B tests behavior from AC-A → AC-B has `Dependencies: AC-A`.
- Same story, disjoint files → both can be `[P]`.

When uncertain, prefer `Dependencies:` over `[P]`. Missed dependency corrupts the task graph; missed `[P]` only costs parallelism.

## When to use

- Specs destined for AI coders (Kiro, Spec Kit, or any Agent Skills runtime that consumes structured prompts).
- Safety-critical or regression-sensitive paths (auth, billing, data integrity).
- Requirements that must be testable at the invariant level (not just example-based).
- Systems where multiple teams implement against the same contract.

## When to skip

- User-value framing — write a user story instead (`user-stories-invest.md`).
- Exploratory discovery — HMW / JTBD (`how-might-we.md`, `jtbd-job-stories.md`).
- Communication with non-technical stakeholders who prefer prose.
- Trivial features where EARS would be overkill.

## Template / worked example

Seeded from `assets/ears-spec-skeleton.md`. See `roles/ears-specifier.md` for the full authoring process.

Worked example — a biometric sign-in story:

```text
## User Story 1 — Android biometric sign-in

AC-1-1 [P]
Ubiquitous: The login screen shall offer a biometric sign-in option when
the device reports biometric capability.

AC-1-2 [P]
State-driven: While biometric enrollment is unavailable on the device,
the login screen shall hide the biometric affordance.

AC-1-3
Dependencies: AC-1-1
Event-driven: When the user taps the biometric affordance, the system
shall prompt the OS biometric dialog within 250ms.

AC-1-4
Dependencies: AC-1-3
Unwanted behavior: If biometric authentication fails 3 consecutive times,
then the system shall fall back to password entry with no lockout.
```

## Validation checks

- Every AC uses one of the five templates literally. No paraphrases of "shall".
- Every AC is testable — a test-writer can derive pass/fail from the AC text alone.
- No AC embeds a solution ("the system shall use Redis").
- `[P]` and `Dependencies:` are present on every AC, never both.
- Every story has at least one Unwanted-behavior AC on a failure-sensitive path.
- Every `Dependencies:` references an existing AC ID.

## Citations

- Mavin, A., Wilkinson, P., Harwood, A., Novak, M. "Easy Approach to Requirements Syntax (EARS)." *17th IEEE International Requirements Engineering Conference*, 2009.
- [AWS Kiro Documentation, Spec-Driven Development](https://kiro.directory/blog/getting-started-kiro-spec-driven/) — 2025 launch; EARS canonical format.
- [GitHub Spec Kit, "Feature Request: EARS Integration" (issue #1356)](https://github.com/github/spec-kit/issues/1356) — 2025 RFC.
- [Wikipedia, "Easy Approach to Requirements Syntax"](https://en.wikipedia.org/wiki/Easy_Approach_to_Requirements_Syntax) — canonical templates.
- [Visure Solutions, "Adopting EARS Notation for Requirements Specification"](https://visuresolutions.com/alm-guide/adopting-ears-notation/) — 2024 practitioner guide.
- [Makerneo, "Understanding EARS and How to Write Better AI Prompts"](https://makerneo.com/en/articles/what-is-ears-requirements-syntax-how-to-write-better-ai-prompts.html) — 2024 AI-coder framing.
