# Opinionated Defaults

These are known-good, battle-tested tools that are the clear leaders in their category. When a category has an opinionated default, the researcher agent should **health-check only** (verify it's still active, no critical issues) rather than doing a full comparison.

Categories marked with `🔬 RESEARCH` always require fresh comparison research because the landscape is actively evolving or highly context-dependent.

Version hints below reflect the current stable line. The researcher agent re-verifies via nova/GitHub Releases at run time; treat listed versions as a starting point, not a floor.

## Python Ecosystem

| Category           | Default               | Notes                                                                                                                 |
| ------------------ | --------------------- | --------------------------------------------------------------------------------------------------------------------- |
| Linter + Formatter | `ruff` (0.15.x)       | Replaces black, isort, flake8, pylint, and most of bandit via the `S` ruleset                                         |
| Package Manager    | `uv` (0.11.x)         | Replaces pip, pip-tools, poetry, pipx. Still pre-1.0 but production-grade                                             |
| Type Checker       | `ty` / `basedpyright` | Astral's `ty` for new projects; `basedpyright` (community fork) if VSCode OSS is a constraint. Pyright remains valid. |
| Data Validation    | `pydantic` v2.13.x    | v2 line is stable; no v3 on the horizon                                                                               |
| Task Queue         | `dramatiq`            | Simpler than celery, better defaults                                                                                  |
| HTTP Client        | `httpx`               | Async-native replacement for requests                                                                                 |
| Testing            | `pytest` v9.x         | v9 stable (post v8→v9 transition); check for deprecated fixtures                                                      |
| CLI Framework      | `cyclopts` v4.x       | Modern typed CLI framework; v4 is stable, v5 in alpha                                                                 |
| Terminal UI        | `rich` v15.x          | v15 is current; bump any v13/v14 references                                                                           |
| Tabular Data       | `polars` v1.40.x      | v1 line mature                                                                                                        |
| OLAP / embedded    | `DuckDB` v1.5.x       | v1 stable                                                                                                             |
| Viz (declarative)  | `altair` v6.x         | v6 is current; v5 references are stale                                                                                |
| 🔬 RESEARCH        | Web Framework         | FastAPI vs Litestar vs Django vs Flask — depends on project type                                                      |
| 🔬 RESEARCH        | ORM / Query Builder   | SQLAlchemy vs SQLModel vs Tortoise vs raw SQL — depends on complexity                                                 |
| 🔬 RESEARCH        | Auth Library          | Depends heavily on auth model (OAuth, JWT, session, etc.)                                                             |

## JavaScript / TypeScript Ecosystem

| Category             | Default           | Notes                                                                                                                                                                |
| -------------------- | ----------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Language             | TypeScript 6.x    | Check `verbatimModuleSyntax` and stricter `noUncheckedIndexedAccess` interactions                                                                                    |
| Runtime              | Node.js 24 LTS    | Current LTS (prior: 22 maintenance). AWS Lambda supports `nodejs24.x`.                                                                                               |
| Linter + Formatter   | `biome` v2.4.x    | Replaces eslint + prettier; 97% Prettier parity                                                                                                                      |
| Package Manager      | `pnpm` v10.x      | v11 in late RC — v10 is the stable pick                                                                                                                              |
| Bundler / Dev Server | `vite` v8.x       | **Vite 8 ships Rolldown as the single default bundler** — replaces the esbuild+Rollup split                                                                          |
| Testing              | `vitest` v4.x     | v4 stable (post v3 → v4 bump); v5 in beta                                                                                                                            |
| Schema Validation    | `zod` v4.x        | **v4 introduced breaking changes** — unified `error` param, `z.email()`/`z.uuid()` as standalone, `.merge/.format/.flatten` deprecated. Migration codemod available. |
| React Compiler       | `react-compiler`  | v1.0 stable — enable by default on new React 19 projects                                                                                                             |
| 🔬 RESEARCH          | Meta-Framework    | Next.js vs TanStack Start vs Astro vs Remix — depends on rendering model                                                                                             |
| 🔬 RESEARCH          | Component Library | shadcn/ui (migrating toward `base-ui`) vs Ark UI vs Mantine — evolving rapidly                                                                                       |
| 🔬 RESEARCH          | State Management  | Zustand vs Jotai vs TanStack vs signals — depends on app complexity                                                                                                  |
| 🔬 RESEARCH          | CSS Approach      | Tailwind v4 (CSS-first config) vs vanilla-extract vs Panda CSS vs CSS Modules                                                                                        |

## Infrastructure

| Category            | Default                  | Notes                                                              |
| ------------------- | ------------------------ | ------------------------------------------------------------------ |
| Containerization    | `docker` (with BuildKit) | Universal standard                                                 |
| CI/CD               | `github-actions`         | Default for GitHub-hosted repos                                    |
| Observability       | `opentelemetry`          | Vendor-neutral telemetry standard                                  |
| Dev Tool Management | `mise`                   | Replaces nvm, pyenv, asdf, direnv                                  |
| 🔬 RESEARCH         | IaC                      | CDK v2 vs Pulumi vs Terraform/OpenTofu — depends on cloud and team |
| 🔬 RESEARCH         | Orchestration            | ECS vs EKS vs Lambda vs App Runner — depends on workload           |
| 🔬 RESEARCH         | Service Mesh             | Depends on whether microservices architecture is needed            |

## AWS Services

| Category       | Default      | Notes                                                                                                        |
| -------------- | ------------ | ------------------------------------------------------------------------------------------------------------ |
| Object Storage | `S3`         | Universal standard                                                                                           |
| CDN            | `CloudFront` | Native S3 integration                                                                                        |
| Message Queue  | `SQS`        | Simple, reliable, serverless                                                                                 |
| DNS            | `Route 53`   | Native AWS integration                                                                                       |
| Lambda runtime | `nodejs24.x` | Current default for Node Lambdas. Also `python3.13`.                                                         |
| 🔬 RESEARCH    | Compute      | Lambda vs ECS Fargate vs App Runner vs EC2 — depends on workload pattern                                     |
| 🔬 RESEARCH    | Database     | Aurora DSQL is GA — weigh as a serverless-Postgres default alongside Aurora Serverless v2, DynamoDB, and RDS |
| 🔬 RESEARCH    | Auth         | Cognito vs custom vs third-party — depends on requirements                                                   |
| 🔬 RESEARCH    | API Gateway  | API Gateway vs ALB vs AppSync — depends on API style                                                         |
| 🔬 RESEARCH    | AI/ML        | Bedrock vs SageMaker vs custom — depends on use case                                                         |

## Go Ecosystem

| Category              | Default               | Notes                                                                                                                      |
| --------------------- | --------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Go toolchain          | `go` 1.26.x           | Latest stable (supported: 1.24+). Bump references pinned to 1.22/1.23.                                                     |
| Linter                | `golangci-lint` v2.x  | **v2 changed the config schema** — v1 YAML won't parse. Bundles gosec, revive, staticcheck, errcheck, exhaustive, gofumpt. |
| Formatter             | `gofumpt`             | Stricter superset of gofmt (also runs inside golangci-lint v2)                                                             |
| Testing               | `go test` + `testify` | Stdlib test runner + assertion library                                                                                     |
| Vulnerability Scanner | `govulncheck`         | Official Go team tool, checks compiled code paths                                                                          |
| HTTP Router           | `chi`                 | Lightweight, stdlib-compatible router                                                                                      |
| Task Runner           | `mise`                | Cross-language task runner                                                                                                 |

## Rust Ecosystem

| Category       | Default          | Notes                                                                                            |
| -------------- | ---------------- | ------------------------------------------------------------------------------------------------ |
| Rust toolchain | `rustc` 1.95.x   | Current stable. Bump references pinned to the 1.80 era.                                          |
| Linter         | `clippy`         | Pedantic + nursery + cargo groups, restriction cherry-picks                                      |
| Formatter      | `rustfmt`        | Stable options only                                                                              |
| Testing        | `cargo-nextest`  | Faster than `cargo test`, retries, profiles                                                      |
| Coverage       | `cargo-llvm-cov` | lcov/HTML output                                                                                 |
| Security Audit | `cargo-audit`    | RustSec Advisory Database                                                                        |
| Supply Chain   | `cargo-deny`     | Licenses, advisories, bans, sources                                                              |
| Dead Code      | `cargo-machete`  | Unused Cargo.toml dependencies                                                                   |
| Task Runner    | `just`           | Rust ecosystem standard                                                                          |
| 🔬 RESEARCH    | SQL Toolkit      | sqlx cadence has slowed; Diesel v2.3.x is shipping actively — weigh based on sync vs async needs |

## Security Tooling (Cross-Language)

| Category             | Default                                    | Notes                                                                                                                                                                                                                                                                                  |
| -------------------- | ------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Secret Detection     | `betterleaks` v1.x                         | Successor to `gitleaks`, built by Zach Rice (original gitleaks author) and Aikido Security. Drop-in config-compatible (`.gitleaks.toml` still works). Adds CEL-based secret validation, token-efficiency filter, parallelized git scanning. 98.6% CredData recall vs. gitleaks' 70.4%. |
| SAST                 | `semgrep` v1.x                             | p/python, p/typescript, p/golang, p/rust, p/owasp-top-ten. Very active release cadence.                                                                                                                                                                                                |
| Python SAST          | `ruff S` rules                             | Covers most of `bandit`'s checks — drop bandit as a separate step on new projects unless legacy CI requires it                                                                                                                                                                         |
| Dep Vulnerabilities  | `osv-scanner` v2.x                         | Supports uv.lock, pnpm-lock.yaml, go.sum, Cargo.lock, package-lock.json                                                                                                                                                                                                                |
| SBOM Generation      | `syft` v1.x                                | CycloneDX + SPDX output                                                                                                                                                                                                                                                                |
| Git Hooks            | `lefthook` v2.x                            | Fast, zero-dependency, parallel. `husky` is in maintenance mode.                                                                                                                                                                                                                       |
| Image Signing        | `cosign` v3.x                              | v3 is current — bump references pinned to v2                                                                                                                                                                                                                                           |
| Conventional Commits | `commitizen` (Python) or `commitlint` (JS) | Commit message enforcement                                                                                                                                                                                                                                                             |

## Container Tooling

| Category                 | Default                  | Notes                                               |
| ------------------------ | ------------------------ | --------------------------------------------------- |
| Container Runtime        | `docker` (with BuildKit) | Multi-stage builds, cache mounts                    |
| Dockerfile Linting       | `hadolint`               | Best practices + ShellCheck for RUN instructions    |
| Image Vulnerability Scan | `grype`                  | Composite risk scoring (CVSS + EPSS + KEV)          |
| Multi-Scanner            | `trivy`                  | Vulns + misconfig + secrets + licenses in one tool  |
| Image Signing            | `cosign`                 | Keyless signing via Sigstore OIDC                   |
| IaC Security             | `checkov`                | 1000+ policies, graph-based cross-resource analysis |

## How Agents Use This File

1. **Check if the category has an opinionated default** — if yes, run a health check only (see `health-check-criteria.md`)
2. **If marked 🔬 RESEARCH** — do full comparison research using search tools
3. **If user has a locked-in choice** — skip entirely, just validate compatibility
4. **If user explicitly says "evaluate X"** — override the default and do full research even for defaulted categories
