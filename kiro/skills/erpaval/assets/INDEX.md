# ERPAVal lessons index

Lessons learned from prior ERPAVal sessions. The orchestrator agent reads this at session start and greps `.erpaval/solutions/**` for relevant lessons before starting work.

## By category

Categories are enumerated in `${ERPAVAL_HOME}/skills/erpaval/references/solution-categories.yaml`. Counts are populated as the Compound phase writes new lessons.

## Recent additions

*None yet.*

## How to use

- At session start, the `kiro_session_start_bootstrap.py` hook (Kiro `agentSpawn` event) emits category counts to STDOUT
- Per Act task, `erpaval-recall` surfaces relevant lessons by module + tag match
- The Compound phase writes new lessons after merge and updates this file
