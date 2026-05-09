# Code Quality Tools

## 7-Layer Defense Model (Overview)

Quality and security tools compose across 7 layers, catching issues at increasing cost:

1. **Editor** — Instant feedback (ruff, biome, clippy, rust-analyzer)
2. **Pre-commit** — Catches issues before they enter the commit (lefthook)
3. **Commit-msg** — Enforces conventional commit format
4. **Pre-push** — Full lint + test + SAST before code leaves the machine
5. **CI** — Authoritative checks on every PR
6. **Nightly** — Deep scans too slow for PR (mutation testing, full dep updates)
7. **Release** — SBOM generation, image signing, provenance

See `references/stacks/shared/security.md` for the full per-language tool mapping and configuration guide.

## semgrep (Static Analysis)

Language-agnostic static analysis for security and code quality. Runs locally, no account required for basic usage.

```bash
# Install
uv tool install semgrep
# or: brew install semgrep

# Run with default rulesets
semgrep scan --config auto

# Run specific rulesets
semgrep scan --config p/python --config p/typescript
```

### Recommended Rulesets

| Ruleset           | Coverage                      |
| ----------------- | ----------------------------- |
| `p/python`        | Python security + quality     |
| `p/typescript`    | TypeScript security + quality |
| `p/golang`        | Go security + quality         |
| `p/rust`          | Rust security (community)     |
| `p/react`         | React-specific patterns       |
| `p/owasp-top-ten` | OWASP Top 10 vulnerabilities  |
| `p/secrets`       | Hardcoded secrets detection   |
| `p/docker`        | Dockerfile best practices     |

### mise.toml Integration

```toml
[tasks.security]
description = "Run security scan"
run = "semgrep scan --config auto --error"

[tasks.build]
depends = ["lint", "security"]
run = "..."
```

## hadolint (Dockerfile Linting)

Lints Dockerfiles against best practices. Integrates ShellCheck for RUN instruction validation.

```bash
# Install
brew install hadolint         # or: mise use hadolint

# Run
hadolint Dockerfile
hadolint -f sarif Dockerfile > hadolint.sarif
```

## ast-grep (Structural Pattern Matching)

Fast AST-based code search, linting, and rewriting using tree-sitter. Complements semgrep for structural patterns and automated refactoring.

```bash
# Install
brew install ast-grep         # or: cargo install ast-grep

# Ad-hoc search
sg run --pattern 'console.log($A)' --lang ts

# Rewrite
sg run --pattern 'var $X = $Y' --rewrite 'const $X = $Y' --lang js

# Lint with rules
sg scan --rule rules/
```

## knip (Dead Code Detection)

Finds unused files, dependencies, and exports in JavaScript/TypeScript projects.

```bash
# Install
pnpm add -D knip

# Run
pnpm knip

# Fix (remove unused exports)
pnpm knip --fix
```

### knip.json

```json
{
  "$schema": "https://unpkg.com/knip@5/schema.json",
  "entry": ["src/index.ts"],
  "project": ["src/**/*.ts"],
  "ignore": ["**/*.test.ts"],
  "ignoreDependencies": ["@types/*"]
}
```
