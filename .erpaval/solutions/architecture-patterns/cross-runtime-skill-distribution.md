---
title: Cross-runtime skill distribution via sibling-dir + install.sh
track: knowledge
category: architecture-patterns
module: kiro/
component: distribution
severity: info
tags: [agent-skills, kiro, claude-code, distribution, install]
applies_when:
  - porting an existing Agent Skills bundle to a new runtime
  - one bundle needs to support multiple agentic runtimes simultaneously
  - the runtimes share the open Agent Skills format but diverge on hooks/agents/manifest
pattern: |
  Keep the original distribution at the repo root (untouched). Add a sibling
  directory (e.g. `kiro/`) that is a parallel distribution containing only
  the files that diverge: forked SKILL.md (with surface rewrites for the new
  runtime's tool / hook / env-var vocabulary), forked agent definitions,
  forked hook scripts, and an install.sh that wires the bundle into the
  target runtime's home (`~/.kiro/`, `~/.claude/`, etc.).

  Symlink runtime-agnostic content (PEP 723 tool scripts, methodology
  references) from the sibling distribution back into the original tree
  at install time so they're shared.

  Document the divergence in a `KIRO-COMPATIBILITY.md` (or equivalent) at
  the new distribution's root with a capability mapping table.
example_files:
  - kiro/install.sh
  - kiro/AGENTS.md
  - kiro/KIRO-COMPATIBILITY.md
---

# Why this matters

Forking the whole repo doubles the maintenance cost. Inlining runtime
detection inside SKILL.md pollutes the methodology with conditionals.
Sibling-dir + install.sh keeps each distribution self-contained and lets the
shared methodology files (references/, scripts/) stay singular at the source.

# Example

```text
erpaval-plugin/
├── .claude-plugin/         # Claude Code distribution (root)
├── .mcp.json
├── agents/
├── hooks/
├── skills/
├── CLAUDE.md
└── kiro/                   # Kiro CLI distribution (sibling)
    ├── install.sh          # symlinks shared content + sed-substitutes JSONs
    ├── AGENTS.md           # Kiro-shaped project memory
    ├── KIRO-COMPATIBILITY.md
    ├── settings/mcp.json   # mirrors root .mcp.json
    ├── skills/             # forked SKILL.md; references/ kept aligned
    ├── agents/             # Kiro JSON shape, not Markdown frontmatter
    └── hooks/              # 5-event Pydantic framework (Kiro emits 5)
```

The install script substitutes `${ERPAVAL_HOME}` (custom env var) into the
agent JSONs at install time, providing the path-resolution shim that
replaces Claude Code's `${CLAUDE_PLUGIN_ROOT}`.
