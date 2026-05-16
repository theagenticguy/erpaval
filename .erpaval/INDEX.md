# ERPAVal lessons index

Lessons learned from prior ERPAVal sessions. Claude reads this at
session start and greps `.erpaval/solutions/**` for relevant
lessons before starting work.

## By category

### knowledge / architecture-patterns
- [cross-runtime-skill-distribution](solutions/architecture-patterns/cross-runtime-skill-distribution.md) — Sibling-dir + install.sh pattern for shipping one Agent Skills bundle to multiple runtimes (Claude Code + Kiro CLI).

### knowledge / api-patterns
- [kiro-cli-port-playbook](solutions/api-patterns/kiro-cli-port-playbook.md) — Concrete checklist + capability matrix for porting Claude Code plugins to Kiro CLI: 1:1 mappings, folder renames, surface rewrites, gap shims.

### knowledge / best-practices
- [install-mkdir-vs-symlink](solutions/best-practices/install-mkdir-vs-symlink.md) — `mkdir -p` then `ln -sfn` against an empty directory creates the symlink INSIDE the dir, not as a replacement. Two safe install-script patterns documented.

## Recent additions

- 2026-05-16 — three lessons from session-554486 (Kiro CLI compatibility port)
