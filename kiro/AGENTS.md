# erpaval — Kiro CLI distribution

Project-level memory for the Kiro CLI port of erpaval-plugin. Kiro reads
`AGENTS.md` natively — see https://kiro.dev/docs/cli/steering/.

This file is **NOT** the methodology — that lives in `skills/erpaval/SKILL.md`.
This file is the install map and the "where things are" pointer.

## Bundle layout

```text
kiro/
├── AGENTS.md                          # this file
├── README.md                          # user-facing entry point
├── KIRO-COMPATIBILITY.md              # design notes + gap inventory
├── install.sh                         # bash installer (--workspace, --dry-run, --uninstall)
├── settings/
│   └── mcp.json                       # mirrors root .mcp.json (4 research servers)
├── skills/
│   ├── erpaval/                       # core methodology (SKILL.md + references/ + assets/ + scripts/)
│   ├── product-discovery/             # HMW + EARS substeps (hard-dep for CL-RIGOR)
│   └── product-design-shared/         # shared design references
├── agents/
│   ├── erpaval-orchestrator.json      # main agent — hosts hooks inline
│   ├── erpaval-researcher.json        # research delegate
│   ├── erpaval-explorer.json          # read-only codebase explorer (replaces built-in Explore)
│   └── prompts/                       # system prompt bodies referenced via file://
└── hooks/
    ├── framework.py                   # Pydantic framework for Kiro's 5 hook events
    ├── kiro_session_start_bootstrap.py
    ├── kiro_validate_packet.py
    └── kiro_compound_nudge.py         # advisory-only — Kiro stop hooks cannot block
```

## Install

```bash
./install.sh                # user scope: ~/.kiro/
./install.sh --workspace    # workspace scope: <cwd>/.kiro/
./install.sh --dry-run      # preview only
./install.sh --uninstall    # remove installer-created symlinks
```

## Run

```bash
kiro-cli chat --agent erpaval-orchestrator --trust-all-tools
```

`--trust-all-tools` auto-approves every tool call so subagents can write,
shell out, and call MCP servers without prompting. For unattended runs add
`--no-interactive` and set `KIRO_API_KEY`. For least-privilege scoping use
`--trust-tools=read,grep,glob,write,shell` instead. (Trusted-command matching
is a prefix string match, so prefer scoped `allowedTools` + `toolsSettings` in
the agent JSON over a blanket `--trust-all-tools` for anything beyond dev/test.)

All three agents pin `model: claude-opus-4-7`. Override per-invocation with
`--model <id>` or edit the JSONs.

## ERPAVAL_HOME

The installer substitutes `${ERPAVAL_HOME}` into the agent JSONs at install
time, pointing at `<target>/erpaval`. Skills, hooks, and assets resolve
relative to it. This is the Kiro-distribution analogue of Claude Code's
`${CLAUDE_PLUGIN_ROOT}` (which doesn't exist in Kiro).

## Hooks

Three of Kiro's five hook events are wired (per the orchestrator agent JSON):

- `agentSpawn` → `kiro_session_start_bootstrap.py` — emits prior-lesson summary on session start
- `postToolUse` (matcher: `write`) → `kiro_validate_packet.py` — **advisory** Pydantic schema check on `.erpaval/` writes; Kiro `postToolUse` cannot block, so a malformed packet is warned, not rejected (move to `preToolUse` + exit 2 if hard rejection is ever needed)
- `stop` → `kiro_compound_nudge.py` — **advisory only**; Kiro stop hooks cannot block-and-re-prompt the agent the way Claude Code's `Stop` channel does

All hooks are fail-open (`framework.run_hook` catches exceptions and exits 0).

## Tools

PEP 723 Python scripts under `kiro/skills/erpaval/scripts/`. Run with `uv run`:

- `erpaval-new.py --request "<text>"` — scaffold a session
- `erpaval-recall.py bootstrap` — session-start summary
- `erpaval-recall.py search --module <p> --tags <csv>` — per-task lesson retrieval
- `erpaval-validate.py <path>` — schema-check a packet

## Differences from the Claude Code distribution

| Concern             | Claude Code                                        | Kiro                                             |
| ------------------- | -------------------------------------------------- | ------------------------------------------------ |
| Plugin root env var | `${CLAUDE_PLUGIN_ROOT}`                            | `${ERPAVAL_HOME}` (set by installer)             |
| Hook config         | `hooks/hooks.json` (plugin-global)                 | `hooks` field inside the orchestrator agent JSON |
| Stop channel        | `decision: "block" + reason` (re-prompts)          | STDOUT to context (advisory)                     |
| Built-in Explore    | `subagent_type: "Explore"`                         | bundled `erpaval-explorer` custom agent          |
| Task deps           | `addBlockedBy` enforced by `TaskCreate/TaskUpdate` | filesystem-driven; `/todo` is advisory UI        |

See `KIRO-COMPATIBILITY.md` for the full 30-row capability mapping table.

## Adding skills

Same two-tier pattern as Claude Code: SKILL.md ≤ 500 lines (Kiro spec), heavy
content in `references/`. Layout: `SKILL.md` + `references/` + `assets/` +
`scripts/`. Drop new skills under `kiro/skills/<name>/`.
