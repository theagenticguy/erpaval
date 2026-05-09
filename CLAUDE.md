# erpaval-plugin

Development context for the erpaval-plugin repo. This CLAUDE.md is project-level memory — it is NOT shipped as a plugin component.

## Repo structure

```text
.claude-plugin/plugin.json    # plugin manifest
.mcp.json                     # MCP servers used by the researcher agent
skills/
  erpaval/                    # the core skill
    SKILL.md
    references/               # flow, classifiers, glossary, orchestrator, etc.
    templates/                # session YAML/MD skeletons, lesson templates, EARS/HMW stubs
    tools/                    # PEP 723 scripts: erpaval-new, erpaval-recall, erpaval-validate
  product-discovery/          # hard dependency — HMW and EARS substeps
    references/frameworks/    # ears.md, how-might-we.md
    references/roles/         # hmw-framer.md, ears-specifier.md
    templates/                # hmw-skeleton.md, ears-spec-skeleton.md
agents/
  researcher.md               # Research-phase agent (context7, deepwiki, brave, exa)
hooks/
  framework.py                # Pydantic hook framework — do not edit without testing
  hooks.json                  # hook event bindings
  session_start_bootstrap.py  # SessionStart — emits prior-lesson summary
  validate_packet.py          # PostToolUse(Write|Edit) — Pydantic-checks .erpaval/ writes
  compound_nudge.py           # Stop — one-shot nudge when Compound is pending
```

## Version management

Bump `plugin.json` `.version` manually or with `mise run bump -- <major|minor|patch>` if you add a `mise.toml`.

## Tools

All three tools under `skills/erpaval/tools/` are PEP 723 scripts. Run with `uv run`. No venv needed.

- `erpaval-new.py --request "<text>"` — scaffold a new session dir
- `erpaval-recall.py bootstrap` — session-start summary
- `erpaval-recall.py search --module <path> --tags <csv>` — per-task retrieval
- `erpaval-validate.py <path>` — schema-check a YAML packet

## Hooks

All hooks are fail-open. A broken hook exits 0 and logs to stderr — it cannot wedge a session. The `framework.py` module handles stdin/stdout plumbing and `HookState` for session-scoped persistence.

## Adding skills

Add new skills under `skills/<name>/SKILL.md` following the two-tier pattern (SKILL.md ≤ 300 lines, heavy content in `references/`).
