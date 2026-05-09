# Rust Project Scaffold

Complete project configuration with full quality gates and security pipeline.

## Cargo.toml

```toml
[package]
name = "myapp"
version = "0.1.0"
edition = "2024"
rust-version = "1.95"
license = "MIT OR Apache-2.0"

[dependencies]

[dev-dependencies]

# Centralized lint configuration
[lints.rust]
unsafe_code = "forbid"

[lints.clippy]
pedantic = { level = "warn", priority = -1 }
nursery = { level = "warn", priority = -1 }
cargo = { level = "warn", priority = -1 }
# Cherry-pick restriction lints
unwrap_used = "warn"
dbg_macro = "warn"
print_stdout = "warn"
print_stderr = "warn"
todo = "warn"
unimplemented = "warn"
# Allow common pedantic false positives
module_name_repetitions = "allow"
must_use_candidate = "allow"
missing_errors_doc = "allow"
missing_panics_doc = "allow"
```

For workspaces, move `[lints]` to `[workspace.lints]` and add `[lints] workspace = true` in each member crate.

## rustfmt.toml

```toml
edition = "2024"
max_width = 100
use_field_init_shorthand = true
use_try_shorthand = true
```

## clippy.toml

```toml
msrv = "1.95"
cognitive-complexity-threshold = 15

disallowed-methods = [
    { path = "std::env::set_var", reason = "Not thread-safe; use a config struct" },
    { path = "std::thread::sleep", reason = "Use tokio::time::sleep in async code" },
]
```

## deny.toml

```toml
[advisories]
vulnerability = "deny"
unmaintained = "warn"
yanked = "warn"
notice = "warn"

[licenses]
unlicensed = "deny"
allow = [
    "MIT",
    "Apache-2.0",
    "BSD-2-Clause",
    "BSD-3-Clause",
    "ISC",
    "Unicode-3.0",
    "Unicode-DFS-2016",
    "Zlib",
]

[bans]
multiple-versions = "warn"
wildcards = "deny"
deny = [
    { crate = "openssl", wrappers = ["openssl-sys"] },
]

[sources]
unknown-registry = "deny"
unknown-git = "deny"
allow-registry = ["https://github.com/rust-lang/crates.io-index"]
```

## .config/nextest.toml

```toml
[profile.default]
retries = 0
slow-timeout = { period = "60s", terminate-after = 2 }
fail-fast = true

[profile.ci]
retries = 2
fail-fast = false
```

## justfile

```justfile
default: check

# Run all checks
check: fmt lint test

# Check formatting
fmt:
    cargo fmt --check

# Run clippy
lint:
    cargo clippy --workspace --all-targets -- -D warnings

# Run tests with nextest
test:
    cargo nextest run

# Run tests with coverage
coverage:
    cargo llvm-cov nextest --lcov --output-path lcov.info

# Security audit
audit:
    cargo audit
    cargo deny check

# Find unused dependencies
machete:
    cargo machete

# Full CI pipeline
ci: fmt lint test audit machete
```

## mise.toml

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
run = "just test"

[tasks.coverage]
description = "Run tests with coverage"
run = "just coverage"

[tasks.security]
description = "Run all security scans"
depends = ["security:audit", "security:deny", "security:secrets", "security:sast", "security:machete"]

[tasks."security:audit"]
description = "Audit advisories"
run = "cargo audit"

[tasks."security:deny"]
description = "Check licenses, bans, sources"
run = "cargo deny check"

[tasks."security:secrets"]
description = "Scan for secrets"
run = "betterleaks git --no-banner"

[tasks."security:sast"]
description = "SAST scan with semgrep"
run = "semgrep scan --config p/rust --config p/owasp-top-ten --error src/"

[tasks."security:machete"]
description = "Find unused dependencies"
run = "cargo machete"

[tasks.ci]
description = "Full CI pipeline"
run = "just ci"
```

## lefthook.yml

```yaml
pre-commit:
  parallel: true
  jobs:
    - name: cargo-fmt
      glob: "*.rs"
      run: cargo fmt --check

    - name: cargo-clippy
      glob: "*.rs"
      run: cargo clippy --workspace --all-targets -- -D warnings

    - name: betterleaks
      run: git diff --staged | betterleaks stdin --no-banner

pre-push:
  parallel: true
  jobs:
    - name: test
      run: cargo nextest run

    - name: cargo-deny
      run: cargo deny check

    - name: betterleaks
      run: betterleaks git --no-banner

    - name: semgrep
      run: semgrep scan --config p/rust --config p/owasp-top-ten --error src/
```

## .github/workflows/ci.yml

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:

jobs:
  fmt:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
        with:
          components: rustfmt
      - run: cargo fmt --check

  clippy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
        with:
          components: clippy
      - uses: Swatinem/rust-cache@v2
      - run: cargo clippy --workspace --all-targets -- -D warnings

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
      - uses: Swatinem/rust-cache@v2
      - uses: taiki-e/install-action@v2
        with:
          tool: cargo-nextest,cargo-llvm-cov
      - run: cargo llvm-cov nextest --lcov --output-path lcov.info
      - uses: actions/upload-artifact@v4
        with:
          name: coverage
          path: lcov.info

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@stable
      - uses: Swatinem/rust-cache@v2
      - uses: taiki-e/install-action@v2
        with:
          tool: cargo-audit,cargo-deny,cargo-machete
      - run: cargo audit
      - run: cargo deny check
      - run: cargo machete
      - name: Semgrep
        run: |
          pip install semgrep
          semgrep scan --config p/rust --config p/owasp-top-ten --error src/
      - name: Betterleaks
        run: |
          docker run --rm -v "$PWD:/src" ghcr.io/betterleaks/betterleaks:latest \
            git --no-banner --report-format sarif --report-path /src/betterleaks.sarif /src
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

  msrv:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@master
        with:
          toolchain: "1.77"
      - uses: Swatinem/rust-cache@v2
      - run: cargo check --workspace
```

## Dockerfile

```dockerfile
# syntax=docker/dockerfile:1

FROM rust:1.77-slim AS builder
WORKDIR /app

COPY Cargo.toml Cargo.lock ./
RUN mkdir src && echo "fn main() {}" > src/main.rs
RUN --mount=type=cache,target=/usr/local/cargo/registry \
    --mount=type=cache,target=/usr/local/cargo/git \
    --mount=type=cache,target=/app/target \
    cargo build --release

RUN rm -rf src target/release/deps/myapp* target/release/myapp*
COPY src ./src
RUN --mount=type=cache,target=/usr/local/cargo/registry \
    --mount=type=cache,target=/usr/local/cargo/git \
    --mount=type=cache,target=/app/target \
    cargo build --release && \
    cp target/release/myapp /usr/local/bin/myapp

FROM debian:bookworm-slim
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates && \
    rm -rf /var/lib/apt/lists/* && \
    adduser --system --uid 1001 app
USER app
COPY --from=builder /usr/local/bin/myapp /usr/local/bin/myapp
EXPOSE 8080
CMD ["myapp"]
```

## .gitignore

```text
/target/
Cargo.lock
*.sarif
.env
```

Note: Remove `Cargo.lock` from `.gitignore` for binary/application projects. Only libraries should ignore it.

## .editorconfig

```ini
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true
indent_style = space
indent_size = 4

[*.{toml,yaml,yml,json}]
indent_size = 2

[*.md]
trim_trailing_whitespace = false
```

## Setup Commands

```bash
# Initialize
cargo init myapp && cd myapp
mise install && lefthook install

# Verify
just check
mise run security
```
