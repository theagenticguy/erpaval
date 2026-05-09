# Rust Core Stack

Settled defaults for all Rust projects. These are health-check-only — no comparison research needed.

> **Rust 1.95.0** is the current stable toolchain. Bump MSRV pins older than ~1.80 to 1.77 (edition 2024 floor) at minimum; target 1.95 for new work.
> **SQL toolkit caveat:** `sqlx`'s release cadence has slowed. For new Rust projects, evaluate `diesel` (actively shipping at v2.3.x) alongside sqlx. Add a note in the recommendation if sqlx is selected.

## Package Management: Cargo

Cargo is the built-in build system and package manager. Use workspace manifests for multi-crate projects.

```toml
# Cargo.toml (workspace root)
[workspace]
resolver = "3"
members = ["crates/*"]

[workspace.package]
edition = "2024"
rust-version = "1.95"
license = "MIT OR Apache-2.0"

# Centralized lint configuration (inherited by all workspace members)
[workspace.lints.rust]
unsafe_code = "forbid"

[workspace.lints.clippy]
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

```toml
# crates/myapp/Cargo.toml
[package]
name = "myapp"
version = "0.1.0"
edition.workspace = true
rust-version.workspace = true
license.workspace = true

[lints]
workspace = true

[dependencies]
# ...
```

```bash
# Common commands
cargo build              # Debug build
cargo build --release    # Release build
cargo add tokio          # Add dependency
cargo remove tokio       # Remove dependency
cargo update             # Update Cargo.lock
```

Always commit both `Cargo.toml` and `Cargo.lock` (for binaries/applications; libraries omit `Cargo.lock`).

## Linting: clippy

Rust's official linter with 700+ lints organized into groups.

```bash
# Run with deny warnings (CI)
cargo clippy -- -D warnings

# Run with workspace lints applied
cargo clippy --workspace --all-targets

# Fix automatically
cargo clippy --fix --allow-dirty
```

### clippy.toml

```toml
# clippy.toml
msrv = "1.95"
cognitive-complexity-threshold = 15

disallowed-methods = [
    { path = "std::env::set_var", reason = "Not thread-safe; use a config struct" },
    { path = "std::thread::sleep", reason = "Use tokio::time::sleep in async code" },
]

disallowed-types = [
    { path = "std::collections::HashMap", reason = "Use indexmap::IndexMap for deterministic ordering" },
]
```

## Formatting: rustfmt

```toml
# rustfmt.toml (stable options only)
edition = "2024"
max_width = 100
use_field_init_shorthand = true
use_try_shorthand = true
```

```bash
# Format
cargo fmt

# Check (CI)
cargo fmt --check
```

## Testing: cargo-nextest

A next-generation test runner — faster than `cargo test`, with better output and retries.

```bash
# Install
cargo install cargo-nextest --locked

# Run tests
cargo nextest run

# Run with retries (flaky test handling)
cargo nextest run --retries 2

# Run specific test
cargo nextest run my_test_name

# List tests
cargo nextest list
```

### .config/nextest.toml

```toml
[profile.default]
retries = 0
slow-timeout = { period = "60s", terminate-after = 2 }
fail-fast = true

[profile.ci]
retries = 2
fail-fast = false
```

## Coverage: cargo-llvm-cov

```bash
# Install
cargo install cargo-llvm-cov --locked

# Run with coverage
cargo llvm-cov

# HTML report
cargo llvm-cov --html
open target/llvm-cov/html/index.html

# lcov format (CI integration)
cargo llvm-cov --lcov --output-path lcov.info

# With nextest
cargo llvm-cov nextest
```

## Security: cargo-audit + cargo-deny

### cargo-audit

Checks `Cargo.lock` against the RustSec Advisory Database.

```bash
# Install
cargo install cargo-audit --locked

# Audit
cargo audit

# JSON output
cargo audit --json
```

### cargo-deny

Comprehensive supply chain security: advisories, licenses, bans, and sources.

```toml
# deny.toml
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

```bash
# Install
cargo install cargo-deny --locked

# Check all
cargo deny check

# Check specific section
cargo deny check licenses
cargo deny check advisories
```

## Dead Code: cargo-machete

Finds unused dependencies in `Cargo.toml`.

```bash
# Install
cargo install cargo-machete --locked

# Run (fast, no compilation)
cargo machete

# More accurate (uses cargo metadata)
cargo machete --with-metadata
```

Ignore false positives in `Cargo.toml`:

```toml
[package.metadata.cargo-machete]
ignored = ["prost"]  # Used in build.rs
```

## Task Runner: just

The Rust ecosystem standard task runner (like `make` but better).

```justfile
# justfile
default: check

check: fmt lint test

fmt:
    cargo fmt --check

lint:
    cargo clippy --workspace --all-targets -- -D warnings

test:
    cargo nextest run

coverage:
    cargo llvm-cov nextest --lcov --output-path lcov.info

audit:
    cargo audit
    cargo deny check

machete:
    cargo machete

ci: fmt lint test audit machete
```

```bash
# Install
cargo install just --locked
# or: brew install just

# Run
just         # Runs default recipe
just test    # Runs specific recipe
just ci      # Runs full CI pipeline
```
