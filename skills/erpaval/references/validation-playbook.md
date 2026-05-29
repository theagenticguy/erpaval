# Validation playbook + closed-loop toolchain

Validation is three layers, each catching different defect classes. Layer 1 is fast and catches surface issues before spending Opus tokens on deeper analysis. Run them in order.

Underneath the layers is the closed-loop toolchain — the reason Layer 1 can be sub-second and why fix cycles stay cheap. Keep every local check **fast, deterministic, and reachable from `mise run`** so subagents get feedback in seconds, not minutes.

---

## Contents

- Why the loop is closed-loop
  - Recommended toolchain
  - Why mise for agents
  - Targeted test execution
- Layer 1 — Static checks
  - Python
  - TypeScript / JavaScript
  - Go
  - Rust
  - Interpreting results
- Layer 2 — Code-quality review (Opus agent)
  - Review prompt
  - Handling findings
- Layer 3 — Security scanning
  - SAST commands
  - Opus security review
  - Interpreting results
- Validation flow summary
- Fix-cycle protocol (C4 / C5)

## Why the loop is closed-loop

```text
Tight loop (seconds):            Loose loop (minutes):
  Agent writes code                Agent writes code
  → runs lint (0.3s)               → pushes to CI
  → gets error                     → waits for runner + deps
  → fixes immediately              → waits for lint
  → runs lint (0.3s)               → gets error
  → passes                         → context has moved on
  → runs tests (2s) → done         → re-reads code → fixes → repeat
```

Rust-based tools (ruff, ty, uv, biome, oxc, dprint, turbo) are 10-100× faster than their predecessors — the difference between linting in 200ms and waiting 5 seconds. Every tool the agent runs most often should hit sub-second or low-single-digit seconds.

### Recommended toolchain

```text
Python     : uv · ruff · ty (or pyright --strict) · pytest · bandit · pip-audit · semgrep
TypeScript : pnpm (or bun) · biome · tsc --strict · vitest · npm audit · semgrep
Go         : go vet · golangci-lint · go test · govulncheck
Rust       : cargo clippy · cargo test · cargo fmt --check · cargo audit
Task runner: mise (unified interface across languages)
Git hooks  : lefthook (runs mise tasks — no abstraction gap with the agent)
Cross-lang : dprint (markdown/JSON format) · semgrep (SAST across 30+ languages)
```

### Why mise for agents

Subagents don't need to know whether the project uses ruff or eslint, pytest or vitest, uv or pnpm. They run `mise run check` and get pass/fail. The project's `mise.toml` encodes all toolchain knowledge. An agent exploring a new codebase reads `mise.toml` during Explore and immediately knows how to lint, test, and validate.

```toml
# mise.toml skeleton the agent can count on
[tasks.lint]
run = "uvx ruff check . && uvx ruff format --check ."

[tasks.typecheck]
run = "uv run pyright"

[tasks.test]
run = "uv run pytest"

[tasks.test-module]
run = "uv run pytest tests/${1}/"

[tasks.security]
run = "uvx bandit -r src/ -ll && uv run pip-audit"

[tasks.check]
depends = ["lint", "typecheck", "test"]

[tasks.validate]
depends = ["check", "security"]
```

### Targeted test execution

Running the full suite on every change is the single biggest bottleneck. Layer the strategy:

1. **During Act (per-task)**: only the tests for the module being changed. The context packet specifies which test files to run.
2. **Between phases (gate check)**: tests for all modules touched in the phase — catches integration issues between parallel tasks.
3. **Final validation (Layer 1)**: full suite once at the end.

```text
Task 1A: tests/models/test_user.py       (2s)
Task 1B: tests/schemas/test_auth.py      (1s)
Phase 1 gate: tests/models/ + tests/schemas/ (3s)
Task 2A: tests/services/test_auth.py     (3s)
Phase 2 gate: tests/services/            (3s)
Final validation: full suite             (30s) — once
```

Total: ~42s vs. 6 × full-suite = ~180s.

---

## Layer 1 — Static checks

The goal is a clean bill of health from every tool the project already uses.

### Python

```bash
uvx ruff format --check .
uvx ruff check .
uv run pyright
uv run pytest
uvx pip-audit
```

If `mise.toml` defines tasks, prefer those — they encode project-specific flags:

```bash
mise run lint
mise run test
mise run typecheck
```

### TypeScript / JavaScript

```bash
pnpm lint         # or: bunx biome check .
pnpm typecheck    # or: npx tsc --noEmit
pnpm test         # or: bun test
pnpm audit        # or: npm audit
```

### Go

```bash
go vet ./...
golangci-lint run
go test ./...
govulncheck ./...
```

### Rust

```bash
cargo clippy -- -D warnings
cargo test
cargo fmt --check
cargo audit
```

### Interpreting results

| Result                       | Action                                                                |
| ---------------------------- | --------------------------------------------------------------------- |
| All checks pass              | Proceed to Layer 2                                                    |
| Formatting issues            | Auto-fix with `ruff format .` / `biome check --write .` / `cargo fmt` |
| Lint warnings (non-blocking) | Fix if in changed files; ignore if pre-existing                       |
| Lint errors                  | Fix before proceeding                                                 |
| Type errors                  | Fix — often interface mismatches from parallel agents                 |
| Test failures                | Diagnose and fix — loop back to Act with specific fix instructions    |
| Audit findings               | Assess severity — critical/high must be addressed; low can be noted   |

---

## Layer 2 — Code-quality review (parallel Opus dimension agents)

Layer 2 fans out. Instead of one agent carrying the whole checklist, launch a set
of read-only Opus reviewers in **one message** — each owns one axis and reads
only what that axis needs. The five quality axes below map to 2–3 agents
depending on changeset size (e.g. `tech-debt + coupling`, `DRY + dead code`,
`API surface + convention drift`). Counts are in `fan-out.md`.

```text
Model: opus (each agent)
Tools: Read, Glob, Grep (read-only — these agents do NOT write code)
Launch: one message, run_in_background=true, one agent per dimension group
```

Each agent runs the checklist for its axis only. The orchestrator merges their
findings before the severity pass. Splitting the axes keeps each agent's context
small and surfaces more issues than one agent stretched across all five.

### Review prompt (per dimension — give each agent only its axis)

```text
You are a senior code reviewer analyzing a changeset for quality issues
on ONE dimension: {{ dimension }}. Find problems, be specific and actionable.

## What Changed
[git diff summary or list of modified files]

## Codebase Context
[Key patterns and conventions from Explore phase]

## Review Checklist

1. **Tech debt creep**
   - Complexity vs. functionality added
   - New coupling points between modules that shouldn't be coupled
   - Layering boundaries respected (data → service → interface)
   - Magic numbers, hardcoded values, implicit assumptions

2. **DRY violations**
   - Duplicated logic within the changeset
   - Duplicated logic between changeset and existing code
   - Repeated patterns that should be extracted
   (Premature abstraction is worse than duplication — flag clear cases only.)

3. **Dead code**
   - Unused imports, unreachable branches, orphaned helpers

4. **Convention drift**
   - New code follows codebase patterns (errors, naming, file org)

5. **API surface**
   - New public exports necessary or should be internal
   - Signatures consistent with existing APIs
   - Return types consistent (no mixing None returns with exceptions)

## Output
For each issue:
- **File**: path/to/file.py:line
- **Severity**: CRITICAL / WARNING / NOTE
- **Category**: tech-debt | dry | dead-code | convention | api-surface
- **Description**: What's wrong and why it matters
- **Suggestion**: Specific fix (code snippet if helpful)

If no issues, say so. Do not manufacture issues.
```

### Handling findings

| Severity | Action                                                          |
| -------- | --------------------------------------------------------------- |
| CRITICAL | Must fix before shipping. Loop back to Act.                     |
| WARNING  | Fix if straightforward (< 5 min). Otherwise, log as known debt. |
| NOTE     | Informational. No action required.                              |

---

## Layer 3 — Security scanning

Run cheapest/fastest scanners first:

```text
1. ruff (includes some security rules)     — 0.2s
2. bandit -r src/ -ll                      — 1-2s
3. pip-audit / npm audit                   — 2-3s
4. semgrep --config auto                   — 5-10s
5. semgrep --config p/owasp-top-ten        — 5-10s
6. Opus security review (agentic)          — 30-60s
```

### SAST commands

**Python**:

```bash
semgrep --config auto --error .
semgrep --config p/owasp-top-ten --error .
bandit -r src/ -ll
uvx pip-audit
```

**JavaScript/TypeScript**:

```bash
npm audit --audit-level=moderate    # or pnpm audit
semgrep --config p/owasp-top-ten .
```

**Go**: `govulncheck ./...`

**Rust**: `cargo audit`

Semgrep rule categories to weight heavily: injection, auth/authz, crypto, data exposure, deserialization.

### Opus security review (parallel dimension agents)

After static scanners, read-only Opus agents review for logic-level issues
pattern-matching tools miss. Like Layer 2, this fans out — launch the security
axes (injection · auth/authz · crypto · data exposure · dangerous-API /
deserialization) as parallel agents in one message, grouped into 2–3 agents by
changeset size. Counts are in `fan-out.md`.

```text
Model: opus (each agent)
Tools: Read, Glob, Grep
Launch: one message, run_in_background=true, one agent per dimension group
```

Prompt template (per dimension — give each agent only its axis):

```text
You are a security engineer reviewing a changeset for vulnerabilities
that static analysis tools typically miss, focused on ONE area:
{{ dimension }}.

## What Changed
[git diff summary]

## Application Context
[What the app does, what data it handles, trust boundaries]

## Review Focus

1. Authentication & authorization logic — bypasses, TOCTOU races, missing checks
2. Input validation & sanitization — boundary validation, type confusion
3. Data flow — secrets in URLs/logs/errors, PII scoping
4. Business logic — race conditions, replay/reorder attacks, fail-closed vs fail-open
5. Dependency usage — dangerous API calls (eval/exec/shell=True), path traversal

## Output
For each finding:
- **File**: path/to/file.py:line
- **Severity**: CRITICAL / HIGH / MEDIUM / LOW
- **CWE**: CWE-ID if applicable
- **Description**: The vulnerability + attack scenario
- **Fix**: Specific remediation with code
```

### Interpreting results

| Source                      | Severity        | Action                       |
| --------------------------- | --------------- | ---------------------------- |
| Semgrep CRITICAL/HIGH       | Any             | Must fix. Loop back to Act.  |
| Semgrep MEDIUM              | In changed code | Fix. In unchanged code: log. |
| Bandit HIGH                 | In changed code | Fix.                         |
| Dependency audit (CRITICAL) | Any             | Upgrade or find alternative. |
| Opus review CRITICAL        | Any             | Fix immediately.             |
| Opus review HIGH            | In changed code | Fix before shipping.         |
| Opus review MEDIUM/LOW      | Any             | Note and assess risk.        |

---

## Validation flow summary

```text
Layer 1: Static checks
  ├── Pass → Layer 2
  └── Fail → Fix → Re-run Layer 1

Layer 2: Code-quality review (Opus)
  ├── No CRITICAL → Layer 3
  └── CRITICAL found → Fix → Re-run from Layer 1

Layer 3: Security scanning
  ├── SAST (semgrep, bandit, audit)
  │   ├── Clean → Opus security review
  │   └── Findings → Fix → Re-run Layer 3
  └── Opus security review
      ├── No CRITICAL/HIGH → Done
      └── Findings → Fix → Re-run from Layer 1
```

## Adversarial verification of findings

A finding from a single reviewer can be a false positive — and chasing false
positives back through Act (cycle C4) is the most expensive way to waste a fix
cycle. Before a CRITICAL or HIGH finding counts, verify it with one or more
independent skeptic agents, launched in parallel (one message):

```text
Model: opus (each verifier)
Tools: Read, Glob, Grep
Prompt: "Try to REFUTE this finding: {{ finding }}. Read the cited code and its
         call sites. Default to refuted=true unless the issue clearly holds.
         Return {refuted: bool, reason}."
```

Drop a finding when a majority of verifiers refute it. This runs after the
dimension reviewers return and before the severity pass that feeds Gate 2. Keep
it proportional — verify CRITICAL/HIGH findings; let MEDIUM/LOW through to the
report without a separate verification pass.

## Fix-cycle protocol (C4 / C5)

1. **Be specific**: don't re-run the whole task. Give the agent the exact issue, file, line, and expected fix.
2. **Include validator output**: paste the error/finding verbatim.
3. **Scope the fix**: "Fix this one issue in this one file" — not "review and fix any issues."
4. **Re-validate from Layer 1**: even for targeted fixes, re-run all layers. Fixes can introduce new issues.
5. **Max 3 fix cycles**: if the same issue persists after 3 attempts, the plan likely has a structural problem. Return to Plan.
