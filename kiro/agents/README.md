# Kiro custom agents — ERPAVal

Three custom agent JSONs that port the ERPAVal methodology onto Kiro CLI.

## The three agents

| Agent | Role | Invoke |
|---|---|---|
| `erpaval-orchestrator` | Main entry point. Runs ERPAVal phases (Explore/Research/Plan/Act/Validate/Compound), spawns subagents, hosts the three hooks. | `kiro-cli chat --agent erpaval-orchestrator` |
| `erpaval-researcher` | Library / API / framework research. Used by the orchestrator's Research phase; spawnable directly for ad-hoc lookups. | `kiro-cli chat --agent erpaval-researcher` (or via `subagent` from the orchestrator) |
| `erpaval-explorer` | Read-only codebase reconnaissance. Replaces Claude Code's built-in Explore subagent (Kiro has no equivalent). | Spawned via `subagent` from the orchestrator; standalone with `kiro-cli chat --agent erpaval-explorer` |

System prompts live as sibling Markdown files under `prompts/` and are pulled in via `file://` URIs in each agent JSON.

## Install flow

The agent JSONs in this directory use `${ERPAVAL_HOME}` placeholders for paths to the bundled SKILL.md, references, and hook scripts. **Kiro's documented agent JSON schema does not specify `${VAR}` interpolation** (only `KIRO_HOME`, which is user-global, not bundle-scoped). The install script handles this by string-substituting `${ERPAVAL_HOME}` with the resolved absolute install path before writing each JSON to its destination:

- `~/.kiro/agents/erpaval-orchestrator.json`
- `~/.kiro/agents/erpaval-researcher.json`
- `~/.kiro/agents/erpaval-explorer.json`
- `~/.kiro/agents/prompts/erpaval-*.md` (referenced by `prompt: file://./prompts/...`)

Install also copies `${ERPAVAL_HOME}/hooks/kiro_*.py` into place and copies `kiro/settings/mcp.json` to `~/.kiro/settings/mcp.json` (or the workspace `.kiro/settings/mcp.json`).

If you install by hand, replace every `${ERPAVAL_HOME}` in the JSONs with the absolute path to your clone of the bundle (e.g. `/Users/you/.kiro/skills/erpaval-bundle`).

## Hooks (orchestrator only)

The orchestrator hosts the three ERPAVal hooks inline (Kiro stores hooks per-agent rather than in a global `hooks.json`):

- `agentSpawn` → `kiro_session_start_bootstrap.py` (emits prior-lesson summary)
- `postToolUse` (matcher: `fs_write`) → `kiro_validate_packet.py` (Pydantic-checks `.erpaval/` writes)
- `stop` → `kiro_compound_nudge.py` (one-shot Compound-pending nudge)

The researcher and explorer agents inherit no hooks — they are leaf subagents and don't drive the session loop.
