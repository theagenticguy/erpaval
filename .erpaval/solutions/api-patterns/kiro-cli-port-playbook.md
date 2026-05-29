---
title: Kiro CLI port playbook for Claude Code Agent Skills
track: knowledge
category: api-patterns
module: kiro/
component: kiro-cli
severity: info
tags: [kiro, claude-code, agent-skills, hooks, subagents, mcp, port]
applies_when:
  - porting a Claude Code plugin that ships skills + agents + hooks + MCP
  - Kiro CLI is a target runtime for an existing Agent Skills bundle
  - need a checklist for what's 1:1 vs gap with shims
pattern: |
  Kiro CLI implements the open Agent Skills standard. Three folder renames
  + path-substitution + hook-channel awareness are the bulk of the work.

  ### 1:1 mappings (no shim needed)
  - Skills: `.kiro/skills/<n>/SKILL.md` (same frontmatter: name, description,
    license, compatibility, allowed-tools)
  - MCP: `.kiro/settings/mcp.json` (same `{mcpServers: {<n>: {command, args, env}}}`)
  - Hook events: SessionStart→agentSpawn, PostToolUse→postToolUse, Stop→stop,
    PreToolUse→preToolUse, UserPromptSubmit→userPromptSubmit
  - Subagents: `.kiro/agents/<n>.json` + `subagent` built-in tool, max 4 parallel
  - Tools (emit the canonical Kiro names; `fs_*`/`execute_bash`/`use_aws` are
    deprecated Q-era aliases that still resolve): read↔Read, write↔Write+Edit,
    shell↔Bash, aws↔(no CC equiv), glob↔Glob, grep↔Grep, web_fetch↔WebFetch,
    web_search↔WebSearch

  ### Folder renames (3 of them)
  - `templates/` → `assets/`
  - `tools/` → `scripts/`
  - `references/` stays

  ### Surface rewrites
  - `${CLAUDE_PLUGIN_ROOT}` → custom env var (e.g. `${ERPAVAL_HOME}`); Kiro has
    no plugin-scoped equivalent. Set via install.sh sed-substitution at install
    time, since Kiro doesn't document `${VAR}` interpolation in agent JSON.
  - Hook config moves from a global `hooks/hooks.json` to inline `hooks` field
    inside the orchestrator agent JSON. Hooks are per-agent in Kiro.
  - Replace `mcp__plugin_<plugin>_<server>__<tool>` namespace with Kiro's
    `@<server>/<tool>` notation.
  - Replace `subagent_type: "Explore"` (built-in) with a custom read-only
    explorer agent (Kiro has no built-in Explore).

  ### Gaps with shims
  - Stop hook re-prompt: Kiro stop hooks cannot block-and-re-prompt. Compound
    nudge becomes advisory STDOUT. The agent SEES the message but isn't forced
    to act. Acceptable degradation.
  - Task dependencies: Kiro `/todo` lacks `addBlockedBy` / status workflow.
    Use filesystem state in task packets as authoritative, `/todo` for UI mirror.
  - `Edit` tool: Kiro has no separate Edit. The `write` tool overwrites. Hook
    matchers target `write` only.
  - `postToolUse` cannot block: a `postToolUse` validation hook can only warn,
    not reject a write. For hard rejection, move the check to `preToolUse` +
    exit code 2 (Kiro's single blocking path).
  - SessionEnd / SubagentStop / PreCompact / Notification hooks: not present
    in Kiro. erpaval doesn't use them, so no shim needed.

  ### Frontmatter cleanup
  - Drop Claude-Code-specific fields like `arguments:` and `user_facing:` from
    SKILL.md (not in Agent Skills spec). Document slash-command exposure in body
    via `$ARGUMENTS` / `${N}` Kiro substitution syntax.

  ### Install bug to avoid
  `mkdir -p` then `ln -sfn` against an empty target directory creates the
  symlink INSIDE the directory. Either skip the mkdir for paths that become
  symlinks, or remove empty dirs before ln. (See install.sh step 1/2 split.)
example_files:
  - kiro/skills/erpaval/SKILL.md
  - kiro/agents/erpaval-orchestrator.json
  - kiro/hooks/framework.py
  - kiro/install.sh
---

# Why this matters

Without this checklist, every Claude Code plugin port to Kiro repeats the
same discovery cycle: which features are 1:1, which need shims, which gaps
are acceptable. The mapping table in `kiro/KIRO-COMPATIBILITY.md` is the
canonical reference.

# Example

See the file paths above. The whole port lives at
`/Users/lalsaado/Projects/erpaval-plugin/kiro/` — three SKILL.md rewrites, three
agent JSONs, four hook scripts (framework + three event handlers), one
install.sh, three Markdown user docs.
