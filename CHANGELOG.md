# Changelog

## 1.1.1 — 2026-05-11 · launch polish

- Self-installing marketplace at `.claude-plugin/marketplace.json` —
  `/plugin marketplace add theagenticguy/erpaval` + `/plugin install
  erpaval@erpaval` works out of the box
- README install section with three paths: Claude Code marketplace
  (full plugin), `npx skills add` via skills.sh (skills-only,
  multi-agent), and local `--plugin-dir` (development)
- Framing polish: drop "Adaptive" from the README tagline + plugin
  description + GitHub repo description; "methodology" → "workflow"
  on user-facing surfaces (the upstream `product-discovery` and
  `agent-ux-patterns` skills keep their own framing)
- Researcher: tighten Step-0 recency window to 6 months for API/SDK
  docs; explicit "always start with `context7`" callout
- Strong-prose parallel-subagent nudges for Explore + Research and
  Act in `skills/erpaval/SKILL.md` and the orchestrator runbook
- `hooks/hooks.json`: extend `PostToolUse` matcher to include
  `MultiEdit`
- `scripts/validate-plugin.sh`: parse `marketplace.json`, AST-check
  `framework.py`, new I4 invariant for plugin/marketplace version sync
- Top-level `README.md` now in the lint scope; markdownlint-cli2
  config allows GitHub-style `[!NOTE]` callout blank lines
- New `product-design-shared/SKILL.md` reference-pool stub

## 1.1.0 — 2026-05-09 · initial public release

First public release of the `erpaval` Claude Code plugin and marketplace.

- Six-phase autonomous-coding workflow: Explore · Research · Plan · Act ·
  Validate · Compound
- Classifier-driven routing (`CL-SCOPE`, `CL-COMPLEXITY`, `CL-RESUME`,
  `CL-DIR`, `CL-RIGOR`, `CL-SPEC`, `CL-VALIDATE`, `CL-C2`, `CL-LESSONS`)
  decides which phases run on a given request
- Compounding lessons store at `.erpaval/solutions/` so each session
  inherits what prior sessions learned
- Three Pydantic-typed, fail-open hooks (`SessionStart` recall bootstrap,
  `PostToolUse` packet validation, `Stop` Compound nudge)
- 11 vendored skills so classifier routes resolve in-bundle:
  `erpaval`, `product-discovery`, `research`, `ultraplan`,
  `tech-stack-builder`, `product-strategy`, `working-backwards`,
  `customer-research`, `meta-prompt-optimizer`, `product-design-shared`,
  `agent-ux-patterns`
- Self-installing marketplace at `.claude-plugin/marketplace.json` —
  `/plugin marketplace add theagenticguy/erpaval` + `/plugin install
  erpaval@erpaval` works out of the box
- Skill-only multi-agent install path via `npx skills add
  theagenticguy/erpaval` (Claude Code, Cursor, Codex, Windsurf, …)
