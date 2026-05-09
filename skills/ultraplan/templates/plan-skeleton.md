# Plan: {{ problem_title }}

**Status:** IN PROGRESS
**Last updated:** {{ timestamp }}
**Explorers:** {{ list_of_explorer_file_paths }}

---

## Protocol

<critic_protocol>
Your job is to compose a single final plan from three independent explorer plans. Do not average — pick per-decision. Each decision in your final plan should come from the explorer whose vector best fits this specific decision, and you should say which one.

Read every explorer file in full before drafting. Note where explorers converged (strong signal) and where they diverged (explicit tradeoff worth naming).

Write section by section, editing this file after each explorer you process. Partial progress written to disk survives termination; plans held in working memory do not.

The final plan is prescriptive, not comparative. The "which explorer" attribution belongs inline as short parentheticals, not as a separate comparison section. The user wants a plan to execute, not a survey.

When every section has real content, change the `Status:` line at the top from `IN PROGRESS` to `COMPLETE`.
</critic_protocol>

---

## Problem

*Crisp statement of what this plan solves. One paragraph.*

## Chosen Approach

*The composed approach. Name its shape. Explicitly call out where the explorers agreed (signal the approach is sound) and where they disagreed (name the tradeoff you resolved).*

## Decisions

*Each major decision, with the choice, the explorer it came from, and the reason. Format:*

### Decision: {{ short name }}

**Call:** {{ what you'd do }}
**Source:** {{ Architectural | Speed-first | Simple-first | Composed from multiple }}
**Reason:** {{ why this call beats the alternatives for this problem }}
**Tradeoff accepted:** {{ what you're giving up }}

---

### Decision: {{ short name }}

...

## Implementation Order

*Ordered list of steps. Each step: file or module, the change, what verifies it. This is the execution plan — a developer should be able to work top-to-bottom.*

1.
2.
3.

## Risks

*What could go wrong with the composed approach. Where the explorers disagreed most — those are the load-bearing tradeoffs to watch.*

## Verification Criteria

*How you'd know the plan worked: tests, observable outputs, smoke tests. Copy the strongest criteria from the explorers.*

## Convergence Notes

*One short paragraph: where all three explorers agreed (high confidence), where they diverged (explicit tradeoffs resolved above).*
