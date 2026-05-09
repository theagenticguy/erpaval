---
name: tech-stack-builder
description: >
  Opinionated tech stack recommendations and settled library references. Two
  modes: (1) `/build-stack` runs parallel researcher agents to compare
  candidates and emit a stack report + ADRs for greenfield projects; (2)
  direct reference routing for coding with settled defaults. Use when the user
  asks to recommend a stack, choose between frameworks, compare open-source
  tools, scaffold a project with quality gates, set up a security pipeline, or
  asks how to wire TanStack Router/Query/Table/Form, Motion, Recharts, D3,
  React Three Fiber, dnd-kit, XY Flow, shadcn/blocks.so, Hono, tRPC, Litestar,
  FastAPI, cyclopts, polars, DuckDB, Biome, pnpm, Vite, uv, ruff, ty, pyright,
  mise, lefthook, golangci-lint, clippy, cargo-nextest, cargo-deny,
  betterleaks, semgrep, osv-scanner, trivy, grype, hadolint, cosign, checkov,
  CDK, or Amplify Gen 2 + Aurora. Do NOT use for product definition or PRD drafting
  (use `product-discovery`); do NOT invoke directly when `erpaval` is running
  — `erpaval` drives `/build-stack` through `CL-SPEC`.
arguments:
  - name: context
    description: Optional initial project context (e.g., "Python API for payments on AWS")
    required: false
user_facing: true
---

## Contents

| File                                  | When to load                                                           |
| ------------------------------------- | ---------------------------------------------------------------------- |
| `references/orchestrator.md`          | Running `/build-stack` — intake → parallel research → synthesis → ADRs |
| `references/opinionated-defaults.md`  | Deciding health-check vs full-research per category                    |
| `references/search-strategies.md`     | Configuring researcher agent tool use (Context7, exa, nova, etc.)      |
| `references/health-check-criteria.md` | HEALTHY / CAUTION / WARNING classification for recommendations         |
| `references/output-templates.md`      | Format specs for the stack report, ADRs, comparison matrices           |
| `references/domains/backend.md`       | Backend researcher domain config                                       |
| `references/domains/frontend.md`      | Frontend researcher domain config                                      |
| `references/domains/infra.md`         | Infrastructure researcher domain config                                |
| `references/domains/aws.md`           | AWS researcher domain config                                           |
| `references/domains/devtools.md`      | Dev-tooling researcher domain config                                   |
| `references/stacks/typescript/`       | Settled TypeScript/React patterns — 15 library references              |
| `references/stacks/python/`           | Settled Python patterns — core, CLI, API, data pipeline                |
| `references/stacks/go/`               | Settled Go patterns — modules, golangci-lint, govulncheck, chi         |
| `references/stacks/rust/`             | Settled Rust patterns — cargo, clippy, nextest, cargo-deny             |
| `references/stacks/shared/`           | Cross-language tooling — mise, lefthook, security, CI/CD, containers   |
| `templates/stack-report.md`           | Full report skeleton (instantiated by orchestrator)                    |
| `templates/adr-template.md`           | ADR format for significant choices                                     |
| `templates/comparison-matrix.md`      | Comparison matrix format                                               |
| `templates/scaffold/`                 | Ready-to-copy project scaffolds — python, typescript, go, rust         |

# Tech Stack Builder

Two-mode skill: `/build-stack` runs parallel researcher agents to produce a stack report + ADRs, and standalone reference routing teaches settled coding patterns when the user is already building.

## Mode 1 — `/build-stack` orchestration

Runs a forked orchestrator that launches the plugin `researcher` agent in parallel across up to five domain configs (`backend`, `frontend`, `infra`, `aws`, `devtools`). Each instance researches its slice, scores candidates against `health-check-criteria.md`, and writes a comparison matrix. The orchestrator synthesizes, resolves conflicts via explicit priority (user constraints → avoid list → ecosystem coherence → health → familiarity), and emits:

| Artifact               | Description                                                                        |
| ---------------------- | ---------------------------------------------------------------------------------- |
| `tech-stack-report.md` | Unified stack table, per-layer analysis, comparison matrices, architecture diagram |
| `adr/NNN-*.md`         | 3–5 ADRs for non-obvious or long-horizon decisions                                 |
| Dependency snippets    | `pyproject.toml`, `package.json`, `mise.toml` scoped to the recommended stack      |
| Scaffold (optional)    | Phase 5 generates real config files via `templates/scaffold/` if the user opts in  |

Hybrid defaults philosophy: ~60% of categories have opinionated winners (ruff, uv, biome, mise) — the researcher runs a **health check only** on those. The remaining ~40% (web framework, ORM, IaC, component library) get full comparison research, because the landscape actively shifts. See `references/opinionated-defaults.md` for the split.

To start: `/build-stack` with optional context (e.g., `/build-stack Python API for payments on AWS`). Full runbook in `references/orchestrator.md`.

## Mode 2 — Reference routing for settled defaults

When the user is already coding and needs a specific library pattern, route them to one reference file. Don't pre-load everything — each reference carries real weight, and loading all of them doubles the active context for no gain.

### React + TypeScript web app

Start with the stack overview (`references/stacks/typescript/webapp.md`), then load one library reference on demand:

| Library / layer           | Reference                                           |
| ------------------------- | --------------------------------------------------- |
| TanStack Router           | `references/stacks/typescript/tanstack-router.md`   |
| TanStack Query            | `references/stacks/typescript/tanstack-query.md`    |
| TanStack Table            | `references/stacks/typescript/tanstack-table.md`    |
| TanStack Form             | `references/stacks/typescript/tanstack-form.md`     |
| Motion (ex framer-motion) | `references/stacks/typescript/motion.md`            |
| Recharts + D3             | `references/stacks/typescript/visualization.md`     |
| React Three Fiber + Drei  | `references/stacks/typescript/react-three-fiber.md` |
| dnd-kit                   | `references/stacks/typescript/dnd-kit.md`           |
| XY Flow (React Flow)      | `references/stacks/typescript/xy-flow.md`           |
| blocks.so + shadcn/ui     | `references/stacks/typescript/ui-blocks.md`         |
| Amplify Gen 2 + Aurora    | `references/stacks/typescript/amplify-aurora.md`    |

### Core setups per language

| Scenario                                          | Reference                                   |
| ------------------------------------------------- | ------------------------------------------- |
| TypeScript core (pnpm, biome, zod, vitest)        | `references/stacks/typescript/core.md`      |
| Node API (Hono, tRPC, Fastify)                    | `references/stacks/typescript/node-api.md`  |
| AWS CDK (TypeScript)                              | `references/stacks/typescript/cdk.md`       |
| Python core (uv, ruff, ty/pyright, pytest)        | `references/stacks/python/core.md`          |
| Python CLI (cyclopts, rich)                       | `references/stacks/python/cli.md`           |
| Python API (FastAPI, Litestar)                    | `references/stacks/python/api.md`           |
| Data pipeline (polars, DuckDB, Parquet)           | `references/stacks/python/data-pipeline.md` |
| Go project (modules, golangci-lint, govulncheck)  | `references/stacks/go/core.md`              |
| Rust project (cargo, clippy, nextest, cargo-deny) | `references/stacks/rust/core.md`            |

### Cross-language tooling

| Scenario                                         | Reference                                  |
| ------------------------------------------------ | ------------------------------------------ |
| mise versions + tasks                            | `references/stacks/shared/mise-config.md`  |
| lefthook + conventional commits                  | `references/stacks/shared/git-hooks.md`    |
| Security pipeline (7-layer shift-left)           | `references/stacks/shared/security.md`     |
| CI/CD (GitHub Actions per language)              | `references/stacks/shared/ci-cd.md`        |
| Container security (Dockerfile, hadolint, grype) | `references/stacks/shared/containers.md`   |
| Code-quality configs                             | `references/stacks/shared/code-quality.md` |

### Scaffolds

When the user asks to scaffold a project with quality gates pre-wired, load the matching file from `templates/scaffold/` — `python.md`, `typescript.md`, `go.md`, or `rust.md`. Each scaffold contains concrete, ready-to-copy files: dependency manifests, linter configs, `mise.toml`, `lefthook.yml`, CI workflow, Dockerfile, `.gitignore`, `.editorconfig` — wired to the full security pipeline.

## Ecosystem fit

- **Upstream of `erpaval`.** `erpaval`'s `CL-SPEC` classifier invokes `/build-stack` when the stack is missing. Don't call both; `erpaval` drives.
- **Downstream of `product-discovery`.** Product-discovery owns PRD, HMW, and EARS — those skills explicitly exclude tech choices. When they hand off a PRD, Section 15 maps directly to `/build-stack` intake.
- **Uses `researcher` agent** (defined in `${CLAUDE_PLUGIN_ROOT}/agents/researcher.md`). Do not define a custom researcher here.
