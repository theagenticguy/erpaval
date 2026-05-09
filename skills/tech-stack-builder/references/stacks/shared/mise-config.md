# mise Configuration Patterns

mise is the default tool for managing dev tool versions, environment variables, and project tasks. It replaces nvm, pyenv, asdf, direnv, and Makefile/justfile for task running.

> mise ships on a CalVer cadence (daily releases). Notable capabilities:
>
> - **GitLab & Forgejo token resolution** — multi-source (env vars, per-host files, CLI), plus `mise token` subcommands for debugging auth.
> - **Lockfile provenance verification** — cryptographic verification for the current platform; Cosign + GitHub Artifact Attestations integrated for supply-chain trust.
> - **Tool `depends` field** — enforce install order inside `mise.toml` (e.g., Elixir after Erlang).
> - **Global `libc` preference** (`MISE_LIBC=musl` / `glibc`) — threads through every precompiled-binary path (Node, Bun, Python, aqua registry).
> - **Per-tool `prerelease = true`** — for `github:`/`aqua:` backends, include pre-release tags in `latest` and `ls-remote`.
> - **.NET runtime-only installs** — skip the full SDK when you only need the runtime.
> - **Task argument forwarding** via `{{usage.*}}` templates in `depends`.
> - **Offline `mise prune`** — no longer hits npm / Go proxy / GitHub for tracked-config resolution.

## Standard mise.toml for Python Projects

```toml
[tools]
python = "3.12"

[env]
_.python.venv = { path = ".venv", create = true }

[tasks]
install = "uv sync"
run = "uv run python app.py"
test = "uv run pytest"
lint = "uvx ruff check ."
format = "uvx ruff format ."
```

## Standard mise.toml for TypeScript Projects

```toml
[tools]
node = "24"

[tasks]
install = "pnpm install"
dev = "pnpm dev"
build = "pnpm build"
test = "pnpm test"
lint = "pnpm biome check ."
format = "pnpm biome format . --write"
```

## Standard mise.toml for Polyglot / Monorepo Projects

```toml
[tools]
python = "3.12"
node = "24"

[env]
_.python.venv = { path = ".venv", create = true }

[tasks.install]
description = "Install all dependencies"
run = ["uv sync", "pnpm install"]

[tasks.build]
description = "Build everything"
depends = ["lint"]
run = ["uv run python -m build", "pnpm build"]

[tasks.lint]
description = "Lint all code"
run = ["uvx ruff check .", "pnpm biome check ."]
```

## Standard mise.toml for Go Projects

```toml
[tools]
go = "1.26"
golangci-lint = "latest"
betterleaks = "latest"
osv-scanner = "latest"
semgrep = "latest"

[tasks.lint]
description = "Lint with golangci-lint"
run = "golangci-lint run"

[tasks.fmt]
description = "Format with gofumpt"
run = "gofumpt -l -w ."

[tasks.test]
description = "Run tests"
run = "go test -v -race ./..."

[tasks.security]
description = "Run security scans"
depends = ["security:vuln", "security:secrets"]

[tasks."security:vuln"]
run = "govulncheck ./..."

[tasks."security:secrets"]
run = "betterleaks git --no-banner"
```

## Standard mise.toml for Rust Projects

```toml
[tools]
rust = "stable"
just = "latest"
cargo-nextest = "latest"
cargo-deny = "latest"
cargo-audit = "latest"
cargo-llvm-cov = "latest"
cargo-machete = "latest"
lefthook = "latest"
betterleaks = "latest"
semgrep = "latest"

[tasks.check]
description = "Run all checks"
run = "just check"

[tasks.test]
description = "Run tests"
run = "cargo nextest run"

[tasks.security]
description = "Run security scans"
run = ["cargo audit", "cargo deny check", "betterleaks git --no-banner"]
```

## Key Patterns

- `mise.toml` at project root, committed to version control
- `mise.local.toml` for personal overrides, `.gitignore`'d
- Use `mise run <task>` instead of Makefiles
- Tasks support `depends`, `sources`/`outputs` (skip if unchanged), `env`, `dir`
- File-based tasks in `mise-tasks/` directory for complex scripts
- `mise sync python --uv` to keep mise + uv Python versions aligned
