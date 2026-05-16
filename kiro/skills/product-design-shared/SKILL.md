---
name: product-design-shared
description: >
  Shared canonical references for product-design frameworks — Pyramid Principle,
  Working Backwards, Double Diamond, research design, methodology selection.
  Consumed by `product-discovery`, `product-strategy`, `working-backwards`, and
  `customer-research` via `${ERPAVAL_HOME}/skills/product-design-shared/references/`.
  Do NOT invoke this skill directly — it has no orchestrator and no assets.
  Load the upstream skill that owns your task (`product-discovery` for PRD /
  HMW / EARS, `product-strategy` for Rumelt / Wardley / Minto, etc.) and let
  it pull from this pool as needed.
license: MIT
compatibility: Designed for Kiro CLI (open Agent Skills standard). References-only — no SKILL behavior, no slash command surface.
---

# product-design-shared — references-only pool

This skill exists so the four product-design skills above can share one
canonical copy of each framework reference. It has **no SKILL behavior**:
no role prompts, no orchestrator, no assets, no slash command.

## What lives here

| File                                  | What it covers                                                    |
| ------------------------------------- | ----------------------------------------------------------------- |
| `references/pyramid-principle.md`     | Minto Pyramid composition discipline                              |
| `references/working-backwards.md`     | Amazon Working Backwards 5-stage flow + PR/FAQ                    |
| `references/double-diamond.md`        | Discover / Define / Develop / Deliver, divergent-convergent shape |
| `references/research-design.md`       | Hypothesis · null · MECE questions · methods · findings           |
| `references/methodology-selection.md` | Decision tree for which framework to reach for                    |

## Who consumes this skill

- `product-discovery` — for PRD drafting, HMW framing, EARS specs, Jobs-to-be-Done
- `product-strategy` — for Rumelt kernel, Wardley maps, Minto-structured argument
- `working-backwards` — for the 5-stage flow (Listen, Define, Invent, Refine, Test)
- `customer-research` — for hypothesis-driven research design

If you're trying to "use" `product-design-shared`, you probably want one of
those four skills instead. Pick from `references/methodology-selection.md`.
