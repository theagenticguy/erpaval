# Developer Tooling Domain

## Categories

### Per-Language Tooling

**Python**:

- **Linter + Formatter**: ruff (default)
- **Type Checker**: ty (default, Astral) — pyright is the mature alternative for VSCode-centric teams
- **Package Manager**: uv (default)
- **Testing**: pytest (default)

**JavaScript / TypeScript**:

- **Linter + Formatter**: biome (default)
- **Package Manager**: pnpm (default)
- **Testing**: vitest (default)
- **Schema Validation**: zod (default)

**Go**:

- **Linter**: golangci-lint v2 (default) — meta-linter running gosec, revive, staticcheck, errcheck, exhaustive, gofumpt
- **Formatter**: gofumpt (default) — stricter superset of gofmt
- **Testing**: `go test` + testify (default)
- **Vulnerability Scanner**: govulncheck (default) — checks compiled code paths

**Rust**:

- **Linter**: clippy (default) — pedantic + nursery + cargo groups, restriction cherry-picks
- **Formatter**: rustfmt (default) — stable options only
- **Testing**: cargo-nextest (default) — faster than `cargo test`, retries, profiles
- **Coverage**: cargo-llvm-cov (default)
- **Security**: cargo-audit + cargo-deny (default) — advisories, licenses, bans, sources
- **Dead Code**: cargo-machete (default) — unused dependency detection
- **Task Runner**: just (default) — Rust ecosystem standard

### Cross-Language Tooling

- **Dev Tool Management**: mise (default)
- **Monorepo Tools** (RESEARCH if applicable): Turborepo, Nx, moon, Bazel — only if monorepo architecture
- **Documentation** (RESEARCH if applicable): Astro Starlight, VitePress, Docusaurus, Mintlify, MkDocs — if docs site needed
- **API Documentation** (RESEARCH if applicable): Scalar, Swagger UI, Redoc, Stoplight — if API docs needed
- **AI Development Tools** (RESEARCH): Claude Code, Cursor, GitHub Copilot, Codeium, aider — evaluate based on team workflow
- **Git Hooks**: lefthook (default for all languages) — fast, zero-dependency, parallel execution
- **Secret Detection**: betterleaks (default) — successor to gitleaks from the original author, drop-in config-compatible; adds CEL-based live-secret validation and token-efficiency filtering
- **SAST**: semgrep (default) — language-agnostic, p/python, p/typescript, p/golang, p/rust rulesets
- **Container Dev**: Docker Desktop, OrbStack, Podman Desktop — if containers in stack

## Conditional Logic

| Condition                                 | Action                                              |
| ----------------------------------------- | --------------------------------------------------- |
| Single language project                   | Only research tools for that language               |
| Monorepo mentioned                        | Research monorepo tools                             |
| "docs" or "documentation" in requirements | Research documentation tools                        |
| API project                               | Research API documentation tools                    |
| Team size > 3                             | Research collaboration tools (PR bots, code review) |
| No frontend                               | Skip JS/TS tooling unless backend uses Node         |

## Domain-Specific Artifacts

Provide ready-to-use config snippets:

- `mise.toml` with all tool versions and project tasks
- Linter/formatter config (e.g., `ruff.toml`, `biome.json`)
- Pre-commit or git hooks config
- `.editorconfig` if multi-language

Also include a **Developer Workflow** section:

- How to onboard a new developer (setup steps)
- Daily development loop (edit, lint, test, commit)
- CI/CD integration points for tooling

## Additional Quality Checks

- [ ] Config snippets are syntactically valid
- [ ] Only tools relevant to the project's languages are included
