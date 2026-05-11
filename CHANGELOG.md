# Changelog

## 1.1.0 — 2026-05-11 · initial public release

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
