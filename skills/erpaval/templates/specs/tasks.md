# Task graph — derived from spec.md

**Do not hand-edit this file.** Regenerated from `spec.md` whenever the spec is revised.

## Wave 1 — parallel

- T-AC-1-1 `[P]` — <summary> · `addBlockedBy: []`
- T-AC-1-2 `[P]` — <summary> · `addBlockedBy: []`
- T-AC-2-1 `[P]` — <summary> · `addBlockedBy: []`

## Wave 2

- T-AC-1-3 — <summary> · `addBlockedBy: [T-AC-1-1, T-AC-1-2]`
- T-AC-2-2 — <summary> · `addBlockedBy: [T-AC-2-1]`

## Wave 3

- T-AC-1-4 — <summary> · `addBlockedBy: [T-AC-1-3]`

## Success criteria baseline

- `ruff check` clean
- `pyright` clean on touched files
- `pytest` passes

## Anti-goals

- No refactoring of existing code
- Stay within scope files listed per-task
