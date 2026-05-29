# Kiro CLI Compatibility — design notes

How the Claude Code `erpaval-plugin` ports to Kiro CLI. Capability mapping,
gap shims, and migration playbook.

## Headline

Three of erpaval's primitives are 1:1 with Kiro: Skills (the open Agent
Skills standard), MCP, and the three hook events erpaval uses. Six gaps
exist. All have shipped shims documented below.

The 1:1 hook mapping is: `SessionStart` → `agentSpawn`, `PostToolUse` →
`postToolUse`, `Stop` → `stop`.

The six gaps are: `${CLAUDE_PLUGIN_ROOT}` env var, plugin manifest, plugin
namespacing, Stop-hook re-prompt channel, built-in `Explore` subagent, and
`addBlockedBy` task deps.

## Capability mapping

### Skills

| Capability                              | Status  |
| --------------------------------------- | ------- |
| Skill bundle (workflow knowledge)       | 1:1     |
| Skill subfolders (3 renames)            | 1:1     |
| Skill triggering (auto + slash command) | 1:1     |
| Skill argument substitution             | 1:1     |
| Plugin namespacing                      | gap     |
| Plugin manifest                         | gap     |
| Plugin marketplace                      | partial |

### Subagents

| Capability                           | Status |
| ------------------------------------ | ------ |
| Subagent definition (4 parallel cap) | 1:1    |
| Subagent invocation                  | 1:1    |
| Subagent return channel              | 1:1    |
| Subagent allowlist                   | 1:1    |

### Hooks

| Capability                                         | Status                 |
| -------------------------------------------------- | ---------------------- |
| SessionStart → agentSpawn                          | 1:1                    |
| PostToolUse → postToolUse                          | 1:1                    |
| Stop → stop                                        | 1:1, channel-different |
| PreToolUse, UserPromptSubmit                       | 1:1                    |
| SessionEnd, SubagentStop, PreCompact, Notification | gap, unused by erpaval |
| Hook config location                               | partial                |
| Plugin-root env var                                | gap, shimmed           |

### MCP

| Capability          | Status |
| ------------------- | ------ |
| MCP config location | 1:1    |
| MCP schema          | 1:1    |

### Task management

| Capability       | Status           |
| ---------------- | ---------------- |
| Task list        | partial, no deps |
| Plan / spec mode | partial          |

### Tools

| Capability                    | Status                    |
| ----------------------------- | ------------------------- |
| Read, Write, Bash, Glob, Grep | 1:1                       |
| WebFetch, WebSearch           | 1:1                       |
| Edit                          | partial, no separate tool |

### Settings and steering

| Capability           | Status |
| -------------------- | ------ |
| User settings file   | 1:1    |
| Per-project settings | gap    |
| Steering, AGENTS.md  | 1:1    |

## Concrete file mapping

### Top-level

| Claude Code                  | Kiro                                    |
| ---------------------------- | --------------------------------------- |
| `.claude-plugin/plugin.json` | `kiro/AGENTS.md` plus `kiro/install.sh` |
| `.mcp.json`                  | `kiro/settings/mcp.json`                |
| `CLAUDE.md`                  | `kiro/AGENTS.md`                        |

### Agents

| Claude Code            | Kiro                                  |
| ---------------------- | ------------------------------------- |
| `agents/researcher.md` | `kiro/agents/erpaval-researcher.json` |
| Built-in `Explore`     | `kiro/agents/erpaval-explorer.json`   |

### Hooks

| Claude Code                        | Kiro                                          |
| ---------------------------------- | --------------------------------------------- |
| `hooks/hooks.json`                 | `hooks` field in orchestrator JSON            |
| `hooks/framework.py`               | `kiro/hooks/framework.py`, 5 events           |
| `hooks/session_start_bootstrap.py` | `kiro/hooks/kiro_session_start_bootstrap.py`  |
| `hooks/validate_packet.py`         | `kiro/hooks/kiro_validate_packet.py`          |
| `hooks/compound_nudge.py`          | `kiro/hooks/kiro_compound_nudge.py`, advisory |

### Skill subfolders

| Claude Code                  | Kiro                              |
| ---------------------------- | --------------------------------- |
| `skills/erpaval/references/` | `kiro/skills/erpaval/references/` |
| `skills/erpaval/templates/`  | `kiro/skills/erpaval/assets/`     |
| `skills/erpaval/tools/`      | `kiro/skills/erpaval/scripts/`    |

## Gap shims

### `${CLAUDE_PLUGIN_ROOT}`

Claude Code injects this env var. Kiro does not. The installer
(`kiro/install.sh`) substitutes `${ERPAVAL_HOME}` into the agent JSONs at
install time. The path resolves to `<target>/erpaval`.

References inside skills use `${ERPAVAL_HOME}` literally. The installer does
not mutate skill file content. The orchestrator agent has the env var
available when it reads those references.

### Plugin manifest

`kiro/AGENTS.md` documents the bundle. `kiro/install.sh` is the install
mechanism. Kiro's "Powers" primitive is intended for MCP-tool bundles, not
generic workflow distributions, so we do not ship as a Power.

### Plugin namespacing

Kiro skills are flat directories with no namespace prefix. We use `erpaval-*`
prefixes on agent names: `erpaval-orchestrator`, `erpaval-researcher`,
`erpaval-explorer`. Skills keep bare names: `erpaval`, `product-discovery`,
`product-design-shared`.

### Stop-hook re-prompt channel

Claude Code's Stop hook can return `decision: "block"` and re-prompt the
agent. Kiro's stop hook cannot. `kiro_compound_nudge.py` calls
`emit_context(reason)` on STDOUT instead. The agent sees the message but is
not forced to act. The same one-shot dismiss mechanics from the Claude Code
distribution still apply: `HookState.compound_nudged` and the
`.erpaval/sessions/.nudged` ledger prevent re-firing.

If the agent ignores the nudge, lessons are not written for that session.
This is the cost of a softer channel.

### Built-in `Explore` subagent

Claude Code provides a built-in read-only Explore subagent. Kiro does not.
`kiro/agents/erpaval-explorer.json` ships a custom agent with read-only
tools (`read`, `grep`, `glob`, `execute_bash` with a deny list for
destructive commands) and a system prompt that mirrors Claude Code's Explore
behavior.

### `addBlockedBy` task dependencies

Kiro's `/todo` has no dependency wiring or rich status workflow. We replace
it with filesystem-driven gating. The orchestrator reads task-packet
`status:` frontmatter (`IN_PROGRESS`, `COMPLETE`, `BLOCKED`) before
launching dependent waves. Kiro's `/todo` is exposed for user-visible
progress only. The packets remain the source of truth.

### `Edit` tool separate from `Write`

Kiro has no separate `Edit` tool. `fs_write` overwrites. Hook matchers
target `fs_write` only, not `Write|Edit|MultiEdit` like Claude Code. Skills
that document file edits use `fs_write` semantics: rewrite the file with
the new content.

## Migration playbook

If you fork this plugin and want to maintain both distributions:

1. Author the methodology in `skills/erpaval/` at the repo root. That is
   the Claude Code distribution.
2. Mirror updates into `kiro/skills/erpaval/` with the documented surface
   rewrites. `${CLAUDE_PLUGIN_ROOT}` becomes `${ERPAVAL_HOME}`. `templates/`
   becomes `assets/`. `tools/` becomes `scripts/`. Task tool refs become
   filesystem state plus `/todo`.
3. Run `bash kiro/install.sh --dry-run` to verify the install path.
4. Install into a workspace `.kiro/` and run `kiro-cli chat --agent
   erpaval-orchestrator`.

A future enhancement: a `kiro/sync.sh` that automates the surface rewrites
by reading `skills/` and emitting `kiro/skills/`.

## Known issues

Kiro's documented agent JSON schema does not specify `${VAR}` interpolation
on field values. The installer sidesteps this by `sed`-substituting at
install time. If Kiro ever adds first-class env-var expansion, the JSONs
can be shipped verbatim.

`kiro-cli` does not have a `kiro install` subcommand. Install is via
cloning the repo and running `install.sh`.

The Compound nudge is advisory. Users or agents may end a session without
writing lessons. The `.nudged` ledger logs this as a one-shot dismiss.
Future sessions still bootstrap normally.
