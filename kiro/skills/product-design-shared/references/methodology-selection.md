# Methodology selection — which framework when

Shared router guide. For any orchestrator picking between Pyramid, Working Backwards, Double Diamond, or research-design — or chaining them — this file is the decision tree.

## Quick-pick matrix

| Your situation                                                                | Reach for                                                                    | Why                                                                                                          |
| ----------------------------------------------------------------------------- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| Starting from a vague product idea; need customer-first framing and alignment | **Working Backwards** (`working-backwards.md`) + `skills/working-backwards/` | Artifact-first discipline. 5CQ → PR/FAQ forces customer clarity before build.                                |
| Wicked / ambiguous problem; risk is premature convergence                     | **Double Diamond** (`double-diamond.md`)                                     | Diamond 1 forces real problem framing. Divergent/convergent shape protects against jumping to solutions.     |
| Evidence in hand; need to persuade a skeptical reader                         | **Pyramid Principle** (`pyramid-principle.md`)                               | Composition discipline: research bottom-up, present top-down. SCQA for slides; long-form structure for docs. |
| Fuzzy question; don't know what to research first                             | **Research design** (`research-design.md`)                                   | Hypothesis + null + MECE questions + methods. Produces Pyramid-base-shaped output by construction.           |
| Big strategic project; all of the above                                       | **Chain them** (see below)                                                   | The disciplines compose cleanly.                                                                             |

## Decision tree

```text
Do you know what problem you're solving?
├── No → Start with Double Diamond Diamond-1 (Discover → Define) OR Working Backwards Listen → Define
│         Both work; WB is artifact-first (5CQ), DD is process-first (divergent/convergent).
│         → Once you have a framed problem, return here.
│
├── Yes, but you don't know how to test your assumption
│   → research-design
│     Frame hypothesis + null → MECE sub-questions → gather → synthesize findings
│     → Feed findings into Pyramid Phase 1.
│
└── Yes, and you have evidence
    └── What are you producing?
        ├── A product-definition artifact (PR, Dear Customer Letter, 5CQ)
        │   → Working Backwards (`skills/working-backwards/`) — uses Pyramid as its composition spine
        │
        ├── A strategy / proposal / resource-request document
        │   → Pyramid composition (`pyramid-principle.md`) — hand the pyramid to your team's narrative-writing workflow
        │
        ├── A slide deck for an audience
        │   → Pyramid via SCQA — Pyramid arc applied to slides
        │
        ├── An engineering PRD
        │   → `skills/product-discovery/` — Pyramid is used at the executive-summary stage
        │
        └── A storyboard / visual vignette
            → Storyboarding (panel-by-panel customer vignettes) — the visual top of the pyramid
```

## How the disciplines compose

These are not alternatives; they stack.

### The canonical chain

```text
research-design      →   produces Pyramid-base-shaped findings
   ↓
Double Diamond        →   (optional) Diamond 1 provides the problem-framing ritual
   ↓
Working Backwards     →   Listen + Define consume findings; Invent + Refine produce artifacts
   ↓
Pyramid Principle     →   composes the PR/FAQ, long-form narrative, deck from the WB output
   ↓
Artifacts             →   PR/FAQ, Dear Customer Letter, storyboard, deck, PRD
```

### Which pieces to skip

You do not always need every step:

- **Small iteration on a known product?** Skip DD, skip the full WB. A 5CQ + a storyboard is often enough.
- **Engineering-heavy feature with a clear customer need?** WB Listen + Define → `skills/product-discovery/` directly. Skip the PR/FAQ unless you need alignment broadly.
- **A proposal for a known audience (e.g., your manager)?** Skip WB. Go straight to Pyramid-composed long-form narrative.
- **Pure technical deep-dive with no customer-facing surface?** research-design + Pyramid. WB is overhead.
- **Wicked cross-org problem?** DD Diamond-1 is load-bearing. Do not skip.

### Which pieces to add

- **Stakeholder alignment is the bottleneck?** Add DD's 2019 engagement layer or a WB PR/FAQ review cycle.
- **Antagonistic reviewer?** The Pyramid antagonist test (read as skeptic) + WB's FAQ mechanism are complementary — do both.
- **Need to quantify an opinion-laden claim?** Add a research-design pass with an explicit null hypothesis *before* writing the Pyramid.

## By audience

| Audience                                         | Primary discipline          | Secondary                    |
| ------------------------------------------------ | --------------------------- | ---------------------------- |
| Leadership (PR/FAQ review, executive memo)       | Working Backwards           | Pyramid (for composition)    |
| External design-led stakeholders                 | Double Diamond              | Pyramid (for the final deck) |
| Engineering team (need to implement)             | `skills/product-discovery/` | Working Backwards upstream   |
| Mixed audience — executive + designer + engineer | Pyramid + WB chain          | DD as translation anchor     |

## By artifact

| Artifact             | Primary composition discipline             | Typical upstream                           |
| -------------------- | ------------------------------------------ | ------------------------------------------ |
| PR/FAQ               | Pyramid (PR = top; FAQ = antagonist test)  | Working Backwards Listen + Define          |
| Long-form narrative  | Pyramid                                    | research-design if claim-heavy             |
| Dear Customer Letter | Pyramid (5-paragraph form)                 | Working Backwards Refine                   |
| 5 Customer Questions | Pyramid (mini — Q1–Q4 = base, Q5 = answer) | Working Backwards Listen                   |
| Slide deck           | Pyramid via SCQA                           | Any of the above                           |
| Storyboard           | Pyramid via SCQA (visual)                  | Working Backwards Refine                   |
| PRD                  | Pyramid at the exec summary                | Working Backwards Define + research-design |
| Customer journey map | MECE decomposition from research-design    | Working Backwards Listen                   |

## Anti-patterns

- **Picking the heaviest framework by default.** Not every small change deserves a PR/FAQ. 5CQ is often enough; sometimes a 1-sentence customer-problem note is enough. Match the framework weight to the decision weight.
- **Stacking all four without reason.** If research-design → DD → WB → Pyramid is the default for every project, you have ceremony without judgment.
- **Using WB where the artifact doesn't fit.** WB's force comes from the PR/FAQ ritual. In a setting with no equivalent review, its value drops and DD or a lighter discovery process may be better.
- **Using Pyramid without evidence.** The Pyramid is a composition discipline, not a substitute for research. A MECE-looking pyramid built on unsupported claims is just a prettier way to be wrong.

## Upstream / downstream summary

| File                   | Upstream                                    | Downstream                                                                |
| ---------------------- | ------------------------------------------- | ------------------------------------------------------------------------- |
| `research-design.md`   | Vague question                              | `pyramid-principle.md` Phase 1                                            |
| `pyramid-principle.md` | Evidence from research-design               | Any composed artifact                                                     |
| `working-backwards.md` | Customer insight (research-design + Listen) | PR/FAQ, 5CQ, storyboard (composed via Pyramid)                            |
| `double-diamond.md`    | Wicked / ambiguous problem                  | Any of the above; often Diamond 1 feeds Working Backwards Listen + Define |
