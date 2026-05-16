# Jobs to Be Done (job stories)

Clayton Christensen's JTBD theory posits that customers "hire" products to make progress in a specific life situation. Alan Klement and Intercom formalized the "job story" format that replaces persona-led framing with situation-led framing.

## Canonical structure

**Job story format** (Klement / Intercom):

> When **[situation]**, I want **[motivation]**, so I can **[outcome]**.

Example:

> When an important customer signs up, I want to be notified, so I can start a conversation promptly.

Key distinctions from a user story:

- **No persona** — situations, not demographics. The same person behaves differently in different contexts.
- **Emphasis on motivation and outcome** — not role and feature.
- **Progress-oriented** — captures the change in state the customer wants.

## JTBD interview technique — four forces

JTBD interviewers probe four forces around a purchase or adoption moment:

1. **Push of the current situation** — what's broken about how things are now?
2. **Pull of the new solution** — what made the new product attractive?
3. **Anxiety of the new solution** — what made the user hesitate?
4. **Habit of the current solution** — what made the old way sticky?

The interviewer rewinds to the moment of decision and walks forward. "Switch interview" technique: ask about the last time they switched how they did this, not how they do it today.

## When to use

Upstream in discovery — especially when writing PRDs, defining problem space, or reframing a "we need feature X" request into its underlying customer progress. Useful for new products or new user segments. Also the right move when the team is stuck on persona demographics that don't explain the behavior ("women 25-45" doesn't predict anything).

## When to skip

- Backlog items ready to build (use user stories from `user-stories-invest.md`).
- When the team hasn't done any JTBD interviews. Writing job stories from assumptions is worse than writing user stories from assumptions, because it feels more grounded than it is.
- Internal tools for a known team where the "situation" is obvious.

## Template

Seeded from `assets/jtbd-skeleton.md`. One file per interview subject or per observed situation. The `jtbd-interviewer` role (see `roles/jtbd-interviewer.md`) generates candidates from PM-provided source material (notes, quotes, tickets) — not from synthetic personas.

## Worked example

Source: support ticket cluster around a PM missing a critical customer signup in a long Slack channel.

Job story:

> When I'm triaging a noisy Slack channel at the start of my day, I want to see the 3 messages that require action, so I can respond before the morning standup.

What this buys over a user story: the situation ("noisy Slack at start of day") bounds the design space — the solution doesn't have to work in other contexts. The motivation ("see 3 messages requiring action") is the acceptance test. The outcome ("respond before standup") anchors the metric.

## Validation checks

- Every job story follows the literal shape "When X, I want Y, so I can Z."
- Situation is specific (time, place, trigger), not demographic.
- Motivation describes a change in the user's state, not a feature they want.
- Outcome is observable — the user would know if they got it.
- At least one source (interview quote, support ticket, observed workflow) is cited per job story.

## Citations

- [Alan Klement, *When Coffee and Kale Compete*](https://www.alanklement.com/) — 2018 canonical CC-licensed book.
- [Intercom, "Designing Features Using Job Stories"](https://www.intercom.com/blog/using-job-stories-design-features-mvps-mastermind/) — canonical job-story shape.
- [JTBD Toolkit, "Job Stories Revisited"](https://jtbdtoolkit.medium.com/job-stories-revisited-13ad0b54eb3c) — 2023 practitioner refresh.
- [LearningLoop, "Jobs to Be Done Framework"](https://learningloop.io/glossary/jobs-to-be-done-framework-jtbd) — glossary.
- [Product School, "Using the Jobs to Be Done Framework"](https://productschool.com/blog/skills/using-the-jobs-to-be-done-framework-for-product-management) — 2024 practitioner guide.
