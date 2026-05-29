# ERPAVal — Kiro CLI distribution

Adaptive autonomous software development workflow ported to Kiro CLI. Same
methodology as the Claude Code distribution — Explore / Research / Plan / Act /
Validate / Compound — packaged as Kiro Agent Skills + custom agents + per-agent
hooks.

The Claude Code distribution lives at the repo root (`/skills`, `/agents`,
`/hooks`). The Kiro distribution lives in this `kiro/` directory and installs
into a Kiro home (`~/.kiro/` or workspace `.kiro/`).

## Install

From the repo root:

```bash
./kiro/install.sh             # user scope: ~/.kiro/
./kiro/install.sh --workspace # workspace scope: <cwd>/.kiro/
```

The installer:

- creates the target Kiro directory tree
- symlinks `kiro/skills/*` into `<target>/skills/`
- symlinks `kiro/hooks/` into `<target>/erpaval/hooks/`
- renders `kiro/agents/*.json` into `<target>/agents/` with `${ERPAVAL_HOME}`
  substituted to the install path
- offers to wire `kiro/settings/mcp.json` into `<target>/settings/mcp.json`

Re-running is idempotent. Run `./kiro/install.sh --uninstall` to remove the
symlinks (user data preserved).

## Run

```bash
kiro-cli chat --agent erpaval-orchestrator --trust-all-tools
```

The `--trust-all-tools` flag auto-approves every tool call, so subagents can
write files, run shell commands, and call MCP servers without prompting. For
unattended overnight runs, also pass `--no-interactive` and set
`KIRO_API_KEY`. For tighter scoping, use `--trust-tools=read,grep,glob,write,shell`
instead of `--trust-all-tools` — trusted-command matching is a prefix string
match, so least-privilege scoping in the agent JSON is safer than a blanket flag.

Then state your request. The orchestrator runs the classifiers (CL-SCOPE,
CL-COMPLEXITY, CL-RESUME, CL-DIR, CL-RIGOR, CL-SPEC) to decide which phases
apply, scaffolds a `.erpaval/sessions/session-<hex>/` directory, and routes
implementation through `erpaval-explorer` (read-only Explore replacement) and
`erpaval-researcher` (research delegate) plus general-purpose subagents for Act.

All three bundled agents pin `model: claude-opus-4-7` (Anthropic's latest
coding model). To override, edit the JSONs or pass `--model <id>` to
`kiro-cli chat`.

## Same methodology, different runtime

The methodology is unchanged. What's different on Kiro:

- Hooks live inside the orchestrator agent JSON (Kiro convention)
- Compound nudges at session end are **advisory** — Kiro stop hooks cannot
  block-and-re-prompt the way Claude Code can. Run `/erpaval` (or just ask the
  orchestrator) to invoke Compound mid-session.
- Task dependencies are tracked by filesystem state in
  `.erpaval/sessions/<id>/tasks/T-AC-X-Y.md` packets. `/todo` is exposed for
  user-visible progress only.

See `KIRO-COMPATIBILITY.md` for the full design notes + gap inventory.

## License

MIT — same as the parent repo.
