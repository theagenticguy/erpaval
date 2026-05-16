# Kiro CLI Compatibility — design notes

Distribution mapping summary, gap inventory, and migration playbook for porting
the Claude Code `erpaval-plugin` to Kiro CLI.

## Headline

**Three of erpaval's primitives are 1:1 with Kiro:** Skills (open Agent Skills
standard), MCP, and the three hook events erpaval uses (`SessionStart` →
`agentSpawn`, `PostToolUse` → `postToolUse`, `Stop` → `stop`).

The remaining gaps — `${CLAUDE_PLUGIN_ROOT}` env var, plugin manifest, plugin
namespacing, Stop-hook re-prompt channel, built-in `Explore` subagent,
`addBlockedBy` task deps — all have shipped shims documented below.

## Capability mapping (30 rows)

| Capability | Claude Code | Kiro | Status |
| --- | --- | --- | --- |
| Skill bundle (workflow knowledge) | `skills/<n>/SKILL.md` | `.kiro/skills/<n>/SKILL.md` (open Agent Skills spec) | **1:1** |
| Skill subfolders | `references/`, `templates/`, `tools/` | `references/`, `assets/`, `scripts/` (3 renames) | **1:1** |
| Skill triggering | desc-based auto + slash command | desc-based auto + slash command (auto-exposed) | **1:1** |
| Skill argument substitution | `$ARGUMENTS`, `$1` | `$ARGUMENTS`, `${N}` | **1:1** |
| Plugin namespacing | `plugin:skill-name` | (none) | **gap** |
| Plugin manifest | `.claude-plugin/plugin.json` | (none for Skills); POWER.md only for MCP-bundle Powers | **gap** |
| Plugin marketplace | Anthropic plugin marketplace | Powers marketplace (MCP bundles only) | **partial** |
| Subagent | `agents/<n>.md` + Task tool, max 4 parallel | `.kiro/agents/<n>.json` + `subagent` tool, max 4 parallel | **1:1** |
| Subagent invocation | `Task(subagent_type, prompt)` | `/spawn [--name X] task...` or NL "Use the X agent to ..." | **1:1** |
| Subagent return | Task return value | built-in `summary` tool | **1:1** |
| Subagent allowlist | per-agent frontmatter | `toolsSettings.subagent.{availableAgents, trustedAgents}` glob | **1:1** |
| Hooks: SessionStart | `SessionStart` | `agentSpawn` | **1:1** |
| Hooks: PostToolUse | `PostToolUse` | `postToolUse` (with `matcher`) | **1:1** |
| Hooks: Stop | `Stop` | `stop` | **1:1 (channel-different)** |
| Hooks: PreToolUse / UserPromptSubmit | both supported | both supported | **1:1** |
| Hooks: SessionEnd / SubagentStop / PreCompact / Notification | supported | (none) | **gap** (unused by erpaval) |
| Hook config location | `.claude-plugin/hooks.json` (plugin-global) | per-agent `hooks` field in agent JSON | **partial** (semantically equivalent) |
| Plugin-root env var | `${CLAUDE_PLUGIN_ROOT}` | (none); `KIRO_HOME` is user-global | **gap** (shimmed via `${ERPAVAL_HOME}`) |
| MCP config | `.mcp.json` at plugin root | `.kiro/settings/mcp.json` workspace + `~/.kiro/settings/mcp.json` user + per-agent inline | **1:1** |
| MCP schema | `{mcpServers: {<n>: {command, args, env}}}` | identical | **1:1** |
| Task management | `TaskCreate / TaskUpdate / TaskList` (deps + statuses) | `/todo` add/complete + `.kiro/cli-todo-lists/*.json` | **partial** (no deps, no rich status) |
| Plan / spec mode | `ExitPlanMode` | `/plan` agent — read-only | **partial** |
| Read tool | `Read` | `fs_read` (`read`) | **1:1** |
| Write tool | `Write` | `fs_write` (`write`) | **1:1** |
| Edit tool | `Edit` | (none — `fs_write` overwrites) | **partial** |
| Bash | `Bash` | `execute_bash` (`shell`) | **1:1** |
| Glob / Grep | `Glob` / `Grep` | `glob` / `grep` | **1:1** |
| WebFetch / WebSearch | `WebFetch` / `WebSearch` | `web_fetch` / `web_search` | **1:1** |
| Settings file | `~/.claude/settings.json` | `~/.kiro/settings/cli.json` | **1:1** |
| Per-project settings | `.claude/settings.json` | (none documented) | **gap** |
| Steering / always-on context | `CLAUDE.md`, `AGENTS.md` | `.kiro/steering/*.md`, `AGENTS.md` | **1:1** |

## Concrete file mapping

| Claude Code | Kiro |
| --- | --- |
| `.claude-plugin/plugin.json` | `kiro/AGENTS.md` + `kiro/install.sh` (no manifest equivalent) |
| `.mcp.json` | `kiro/settings/mcp.json` |
| `agents/researcher.md` | `kiro/agents/erpaval-researcher.json` + `kiro/agents/prompts/erpaval-researcher.md` |
| (built-in `Explore`) | `kiro/agents/erpaval-explorer.json` + `kiro/agents/prompts/erpaval-explorer.md` |
| `hooks/hooks.json` | `hooks` field inside `kiro/agents/erpaval-orchestrator.json` |
| `hooks/framework.py` | `kiro/hooks/framework.py` (5 events instead of 26) |
| `hooks/session_start_bootstrap.py` | `kiro/hooks/kiro_session_start_bootstrap.py` |
| `hooks/validate_packet.py` | `kiro/hooks/kiro_validate_packet.py` |
| `hooks/compound_nudge.py` | `kiro/hooks/kiro_compound_nudge.py` (advisory-only) |
| `skills/erpaval/SKILL.md` | `kiro/skills/erpaval/SKILL.md` |
| `skills/erpaval/references/` | `kiro/skills/erpaval/references/` |
| `skills/erpaval/templates/` | `kiro/skills/erpaval/assets/` |
| `skills/erpaval/tools/` | `kiro/skills/erpaval/scripts/` |
| `skills/product-discovery/` | `kiro/skills/product-discovery/` |
| `skills/product-design-shared/` | `kiro/skills/product-design-shared/` |
| `CLAUDE.md` | `kiro/AGENTS.md` |

## Gap shims

### `${CLAUDE_PLUGIN_ROOT}` — env var injected by Claude Code's plugin loader

**Shim**: `${ERPAVAL_HOME}` env var. The installer (`kiro/install.sh`) substitutes
this into the agent JSONs at install time, resolving it to the absolute path of
`<target>/erpaval`. References inside skills (which Kiro reads from disk by path)
use `${ERPAVAL_HOME}` literally; the installer does NOT mutate skill file
content. Documentation in skills tells the user to read these references via
the orchestrator agent, which has `${ERPAVAL_HOME}` available in its hook env.

### Plugin manifest — `.claude-plugin/plugin.json`

**Shim**: `kiro/AGENTS.md` documents the bundle. `kiro/install.sh` is the install
mechanism. Kiro's "Powers" primitive (POWER.md + `mcp.json` + `steering/`) is
intended for MCP-tool bundles, not generic workflow distributions, so we don't
ship as a Power.

### Plugin namespacing — `plugin:skill-name`

**Shim**: flat dirs under `<target>/skills/` with `erpaval-*` prefixes on agent
names (`erpaval-orchestrator`, `erpaval-researcher`, `erpaval-explorer`). Skills
keep their bare names (`erpaval`, `product-discovery`, `product-design-shared`).

### Stop-hook re-prompt channel

**Shim**: `kiro_compound_nudge.py` calls `emit_context(reason)` on STDOUT — the
agent SEES the message but is not forced to act. The reason text explicitly
asks the agent to run Compound now. The same one-shot dismiss-once mechanics
(`HookState.compound_nudged`, `.erpaval/sessions/.nudged` ledger) prevent
re-firing. If the agent ignores the nudge, lessons aren't written for that
session — the cost of a softer channel.

### Built-in `Explore` subagent

**Shim**: `kiro/agents/erpaval-explorer.json` — a custom agent with read-only
tools (`read`, `grep`, `glob`, `execute_bash` with a deny-list for destructive
commands) and a system prompt mirroring Claude Code's Explore agent.

### `addBlockedBy` task dependencies

**Shim**: filesystem-driven gating. The orchestrator reads task-packet
`status:` frontmatter (`IN_PROGRESS` / `COMPLETE` / `BLOCKED`) before launching
dependent waves. Kiro's `/todo` is exposed for user-visible progress, but
the authoritative state lives in the packets.

### `Edit` tool separate from `Write`

**Shim**: Kiro has no separate `Edit` tool; `fs_write` overwrites. Hook matchers
target `fs_write` only (not `Write|Edit|MultiEdit` like Claude Code). Skills
that document file edits use `fs_write` semantics ("rewrite the file with the
new content") rather than `Edit`'s search-and-replace pattern.

## Migration playbook for forkers

If you fork this plugin and want to maintain both distributions:

1. Author the methodology in `skills/erpaval/` (root, Claude Code distribution).
2. Mirror updates into `kiro/skills/erpaval/` with the documented surface
   rewrites (`${CLAUDE_PLUGIN_ROOT}` → `${ERPAVAL_HOME}`, `templates/` →
   `assets/`, `tools/` → `scripts/`, Task tool refs → filesystem state +
   `/todo`).
3. Run `bash kiro/install.sh --dry-run` to verify the install path is intact.
4. Test by installing into a workspace `.kiro/` and running `kiro-cli chat
   --agent erpaval-orchestrator`.

A future enhancement: a `kiro/sync.sh` that automates the surface rewrites by
reading `skills/` and emitting `kiro/skills/` deterministically.

## Known issues

- Kiro's documented agent JSON schema does not specify `${VAR}` interpolation
  on field values. The installer sidesteps this by `sed`-substituting at
  install time. If Kiro ever adds first-class env-var expansion, the JSONs can
  be shipped verbatim.
- `kiro-cli` does not have a `kiro install` subcommand — install is via cloning
  the repo + running `install.sh`.
- The Compound nudge is advisory; users / agents may end a session without
  writing lessons. The `.nudged` ledger logs this as a one-shot dismiss; future
  sessions still bootstrap normally.
