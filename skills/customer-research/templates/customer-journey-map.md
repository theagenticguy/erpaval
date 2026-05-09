# Customer Journey Map

A visualization of the customer's end-to-end experience across a scenario, with friction points + emotions + opportunities surfaced per phase. Each row should map back to at least one MECE sub-question from the research plan — no rows invented without evidence.

**Scenario**: [FILL — a specific task the customer is trying to complete]
**Customer segment**: [FILL — from the problem statement]
**Date**: [FILL]
**Source research**: [link to `research-plan.md`]

## The grid

Rows = phases of the experience. Columns = what's observable + what's felt + where we could help.

| # | Phase                 | Customer action | Touchpoint                           | Customer thought                        | Customer feeling     | Opportunity         | Sub-question evidence             |
| - | --------------------- | --------------- | ------------------------------------ | --------------------------------------- | -------------------- | ------------------- | --------------------------------- |
| 1 | [e.g., Awareness]     | [what they do]  | [where — mobile app / store / email] | [verbatim or paraphrased from research] | [emotion, 1-2 words] | [how we could help] | [Q-ID from research plan, source] |
| 2 | [e.g., Discovery]     | ...             | ...                                  | ...                                     | ...                  | ...                 | ...                               |
| 3 | [e.g., Consideration] | ...             | ...                                  | ...                                     | ...                  | ...                 | ...                               |
| 4 | [e.g., First use]     | ...             | ...                                  | ...                                     | ...                  | ...                 | ...                               |
| 5 | [e.g., Ongoing use]   | ...             | ...                                  | ...                                     | ...                  | ...                 | ...                               |
| 6 | [e.g., Completion]    | ...             | ...                                  | ...                                     | ...                  | ...                 | ...                               |

### Column definitions

- **Phase** — a named stage of the experience. Typical counts: 4-8 phases.
- **Customer action** — what they are doing, verb-led. Specific.
- **Touchpoint** — where the action happens (mobile app, store, email, phone call, chat, physical store).
- **Customer thought** — what they are thinking, preferably as a verbatim quote. If no quote, paraphrase from research.
- **Customer feeling** — the emotion. 1-2 words. Avoid vague words like "frustrated" — prefer "overwhelmed by options" or "anxious about delivery date".
- **Opportunity** — the unmet need or friction. This is where design work can help. One sentence.
- **Sub-question evidence** — which MECE sub-question produced the evidence for this row. Keeps the journey grounded in research, not fabrication.

## The emotional arc

Plot the customer's emotion across phases. Even a rough ASCII sketch clarifies where the experience cracks:

```text
Awareness  Discovery  Consideration  First use  Ongoing  Completion
   😊          🙂           😐           😟         😊         😊
  hopeful    curious    overwhelmed   anxious    relieved   proud
```

Look for:

- **Cliff drops** — a phase where the emotion tanks. That's the root-cause opportunity.
- **Long flat stretches** — either the experience is fine (good) or our research missed something (suspect).
- **False peaks** — a customer enjoys early interactions but abandons later. The *why* matters more than the drop.

## Anti-patterns

| Failure                                          | Fix                                                                                                                                                   |
| ------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Inventing rows without evidence**              | Every row needs a sub-question citation. If there's no evidence, go research it                                                                       |
| **Too many phases**                              | 8 phases maximum. If you need more, you're describing a workflow, not a journey                                                                       |
| **"Frustrated" on every row**                    | Specific emotions ("overwhelmed by options", "anxious about time"). Generic "frustrated" is a tell that the research was shallow                      |
| **Opportunities that name solutions**            | Opportunity = the unmet need, not the feature. "Reduce cognitive load at checkout" not "add a progress bar"                                           |
| **Mixing customer segments**                     | One journey per primary segment. If you need multiple, produce multiple maps                                                                          |
| **Current state + future state in the same map** | Keep them separate. The current-state map is what's real today; future-state is what you propose (belongs in a storyboard or PR, not the journey map) |

## What happens next

Once the journey map is tight:

- Use the "Opportunity" column to seed Invent (`skills/working-backwards/` Stage 3).
- Pick the biggest emotional drop and visualize it as the Refine-stage storyboard.
- Hand off to `skills/working-backwards/` for the 5CQ's Q5 (customer experience).

## Connection to Pyramid

The journey map is a structured view of the evidence gathered in the Pyramid base — one row per evidence-cluster. Rows that share an "opportunity" cluster on a shared "so what" in `research-plan.md` step 7. This means the journey map is a visual slice of the Pyramid base, not a separate artifact.
