# Kiro CLI Compatibility — design notes

How the Claude Code `erpaval-plugin` ports to Kiro CLI. Capability mapping,
gap shims, and migration playbook.

## Headline

Two of erpaval's primitives are clean 1:1 with Kiro: Skills (the open Agent
Skills standard) and MCP. Subagents map closely (the `subagent` tool, the 4-per-
DAG-level cap, the `summary` return channel). Hooks map by event name but
**lose capability**: Kiro hooks are shell-only (no prompt-based hooks), only
`preToolUse` can block (via exit code 2), and `postToolUse`/`stop` are
advisory. All gaps have shipped shims documented below.

The hook event mapping is: `SessionStart` → `agentSpawn` (1:1),
`UserPromptSubmit` → `userPromptSubmit` (1:1), `PreToolUse` → `preToolUse`
(block via exit 2 only), `PostToolUse` → `postToolUse` (cannot block —
packet validation is advisory), `Stop` → `stop` (advisory channel).

The gaps are: `${CLAUDE_PLUGIN_ROOT}` env var, plugin manifest, plugin
namespacing, prompt-based hooks, blocking `PostToolUse`/`Stop` channels,
built-in `Explore` subagent, and `addBlockedBy` task deps. Four Claude Code
hook events — `SessionEnd`, `SubagentStop`, `PreCompact`, `Notification` —
have no Kiro equivalent (erpaval uses none of them).

> Verified against Kiro CLI docs as of 2026-05-29. Kiro CLI is on a fast
> minor-version cadence (v2.2 → v2.5 in May 2026 alone) — re-check
> [kiro.dev/changelog](https://kiro.dev/changelog/) before each refresh.

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

| Capability                                         | Status                  |
| -------------------------------------------------- | ----------------------- |
| SessionStart → agentSpawn                          | 1:1                     |
| PostToolUse → postToolUse                          | partial, cannot block   |
| Stop → stop                                        | partial, advisory only  |
| PreToolUse → preToolUse                            | partial, exit-2 only    |
| UserPromptSubmit → userPromptSubmit                | 1:1                     |
| SessionEnd, SubagentStop, PreCompact, Notification | gap, unused by erpaval  |
| Hook config location                               | inline in agent JSON    |
| Hook trigger model (prompt-based hooks)            | gap, shell-only on Kiro |
| Plugin-root env var                                | gap, shimmed            |

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
tools (`read`, `grep`, `glob`, `shell` with a deny list for destructive
commands) and a system prompt that mirrors Claude Code's Explore behavior.
Kiro's read-only **Plan Agent** (`/plan`, v1.23.0) is an alternative for
structured read-only planning.

### `addBlockedBy` task dependencies

Kiro's `/todo` has no dependency wiring or rich status workflow. We replace
it with filesystem-driven gating. The orchestrator reads task-packet
`status:` frontmatter (`IN_PROGRESS`, `COMPLETE`, `BLOCKED`) before
launching dependent waves. Kiro's `/todo` is exposed for user-visible
progress only. The packets remain the source of truth.

### `Edit` tool separate from `Write`

Kiro has no separate `Edit` tool — the `write` tool (canonical name; `fs_write`
is the deprecated Q-era alias) overwrites. Hook matchers target `write` only,
not `Write|Edit|MultiEdit` like Claude Code. Skills that document file edits
use `write` semantics: rewrite the file with the new content.

> Tool-name modernization: this distribution emits the current canonical
> built-in names (`read`, `write`, `shell`, `aws`) in every agent JSON and hook
> matcher, not the deprecated Q-era aliases (`fs_read`, `fs_write`,
> `execute_bash`, `use_aws`). The old names still resolve as aliases, but the
> canonical names are forward-safe.

### `postToolUse` cannot block — packet validation is advisory

Claude Code's `PostToolUse` hook can reject a write. Kiro's `postToolUse`
**cannot block** — any non-zero exit surfaces a warning but the write stands.
`kiro_validate_packet.py` therefore runs as an advisory schema check: it warns
on a malformed `.erpaval/` packet but does not reject it. If hard rejection is
ever required, move the check to `preToolUse` on `write` and return exit code 2
(the single blocking path in Kiro's hook model). The fail-open design is
unchanged — `framework.run_hook` still catches exceptions and exits 0.

## Migration playbook

If you fork this plugin and want to maintain both distributions:

1. Author the methodology in `skills/erpaval/` at the repo root. That is
   the Claude Code distribution.
2. Mirror updates into `kiro/skills/erpaval/` with the documented surface
   rewrites. `${CLAUDE_PLUGIN_ROOT}` becomes `${ERPAVAL_HOME}`. `templates/`
   becomes `assets/`. `tools/` becomes `scripts/`. Task tool refs become
   filesystem state plus `/todo`. Built-in tool names use the canonical
   forms (`read`/`write`/`shell`/`aws`), not the Q-era aliases.
3. Run `bash kiro/install.sh --dry-run` to verify the install path.
4. Install into a workspace `.kiro/` and run `kiro-cli chat --agent
   erpaval-orchestrator`.

A future enhancement: a `kiro/sync.sh` that automates the surface rewrites
by reading `skills/` and emitting `kiro/skills/`.

## Known issues

Kiro's documented agent JSON schema does not specify `${VAR}` interpolation
on field values. The installer sidesteps this by `sed`-substituting at
install time. If Kiro ever adds first-class env-var expansion, the JSONs
can be shipped verbatim. (Kiro's `mcp.json` *does* expand `${VAR}` in `env`
and `headers`; agent-JSON field values do not, which is why `${ERPAVAL_HOME}`
is resolved at install time, not by Kiro.) To relocate the whole Kiro home,
Kiro honors `KIRO_HOME` (v2.3.0) — the installer's `--workspace`/default
target is the analogue here.

`kiro-cli` does not have a `kiro install` subcommand. Install is via
cloning the repo and running `install.sh`.

The Compound nudge is advisory. Users or agents may end a session without
writing lessons. The `.nudged` ledger logs this as a one-shot dismiss.
Future sessions still bootstrap normally.
