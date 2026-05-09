# ERPAVal lessons index

Lessons learned from prior ERPAVal sessions. Claude reads this at session start and greps `.erpaval/solutions/**` for relevant lessons before starting work.

## By category

Categories are enumerated in `${CLAUDE_PLUGIN_ROOT}/skills/erpaval/references/solution-categories.yaml`. Counts are populated as the Compound phase writes new lessons.

## Recent additions

*None yet.*

## How to use

- At session start, the `session_start_bootstrap.py` hook emits category counts
- Per Act task, `erpaval-recall` surfaces relevant lessons by module + tag match
- The Compound phase writes new lessons after merge and updates this file
