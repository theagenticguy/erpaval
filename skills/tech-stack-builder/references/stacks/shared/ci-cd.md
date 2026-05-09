# CI/CD Pipeline Templates

Ready-to-use CI/CD templates per language. Each includes lint, test, and security scan jobs.

## GitHub Actions

### Python

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v7
        with:
          enable-cache: true
      - run: uv sync --locked
      - run: uvx ruff check src/
      - run: uvx ruff format --check src/
      - run: uvx ty check src/

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v7
        with:
          enable-cache: true
      - run: uv sync --locked
      - run: uv run pytest --cov --cov-report=xml --cov-branch
      - uses: actions/upload-artifact@v4
        with:
          name: coverage
          path: coverage.xml

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v7
        with:
          enable-cache: true
      - run: uv sync --locked --group security
      - name: Semgrep
        run: |
          uv tool install semgrep
          semgrep scan --config auto --config p/owasp-top-ten --error --quiet src/
      - name: Bandit
        run: uv run bandit -c pyproject.toml -r src/
      - name: OSV-Scanner
        uses: google/osv-scanner-action/osv-scanner-action@v2
        with:
          scan-args: --lockfile uv.lock
      - name: Betterleaks
        run: |
          docker run --rm -v "$PWD:/src" ghcr.io/betterleaks/betterleaks:latest \
            git --no-banner --report-format sarif --report-path /src/betterleaks.sarif /src
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      - name: License check
        run: uv run --with pip-licenses pip-licenses
```

### TypeScript

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 24
          cache: pnpm
      - run: pnpm install --frozen-lockfile
      - run: pnpm biome ci .
      - run: pnpm tsc --noEmit
      - run: pnpm knip

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 24
          cache: pnpm
      - run: pnpm install --frozen-lockfile
      - run: pnpm vitest run --coverage

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 24
          cache: pnpm
      - run: pnpm install --frozen-lockfile
      - name: Semgrep
        run: |
          pip install semgrep
          semgrep scan --config p/typescript --config p/owasp-top-ten --error src/
      - name: OSV-Scanner
        uses: google/osv-scanner-action/osv-scanner-action@v2
        with:
          scan-args: --lockfile pnpm-lock.yaml
      - name: Betterleaks
        run: |
          docker run --rm -v "$PWD:/src" ghcr.io/betterleaks/betterleaks:latest \
            git --no-banner --report-format sarif --report-path /src/betterleaks.sarif /src
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      - name: License check
        run: npx license-checker-rseidelsohn --failOn "GPL-3.0;AGPL-3.0" --production
```

### Go

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
        with:
          go-version-file: go.mod
          cache: true
      - name: gofumpt check
        run: |
          go install mvdan.cc/gofumpt@latest
          test -z "$(gofumpt -l .)"
      - name: golangci-lint
        uses: golangci/golangci-lint-action@v6
        with:
          version: latest

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
        with:
          go-version-file: go.mod
          cache: true
      - run: go test -v -race -coverprofile=coverage.out ./...
      - uses: actions/upload-artifact@v4
        with:
          name: coverage
          path: coverage.out

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
        with:
          go-version-file: go.mod
          cache: true
      - name: govulncheck
        run: |
          go install golang.org/x/vuln/cmd/govulncheck@latest
          govulncheck ./...
      - name: Semgrep
        run: |
          pip install semgrep
          semgrep scan --config p/golang --config p/owasp-top-ten --error .
      - name: OSV-Scanner
        uses: google/osv-scanner-action/osv-scanner-action@v2
        with:
          scan-args: --recursive .
      - name: Betterleaks
        run: |
          docker run --rm -v "$PWD:/src" ghcr.io/betterleaks/betterleaks:latest \
            git --no-banner --report-format sarif --report-path /src/betterleaks.sarif /src
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Rust

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
          toolchain: "1.77"  # Match rust-version in Cargo.toml
      - uses: Swatinem/rust-cache@v2
      - run: cargo check --workspace
```

## GitLab CI

Based on production GitLab CI configuration with security scanning, coverage, and artifact reports.

```yaml
stages:
  - lint
  - test
  - security
  - build

variables:
  UV_IMAGE: ghcr.io/astral-sh/uv:latest-python3.13-bookworm-slim
  UV_CACHE_DIR: .uv-cache

# Shared install job (builds .venv once, passed as artifact)
install:
  stage: .pre
  image: $UV_IMAGE
  script:
    - uv sync --locked --all-groups
  artifacts:
    paths: [.venv/]
    expire_in: 1 hour
  cache:
    key:
      files: [uv.lock]
    paths: [$UV_CACHE_DIR]

lint:
  stage: lint
  image: $UV_IMAGE
  dependencies: [install]
  script:
    - uv run ruff check --output-format=gitlab --output-file=gl-code-quality-report.json src/ || true
    - uv run ruff check src/
    - uv run ruff format --check src/
    - uv run ty check src/
  artifacts:
    when: always
    reports:
      codequality: gl-code-quality-report.json

test:
  stage: test
  image: $UV_IMAGE
  dependencies: [install]
  script:
    - uv run pytest --junitxml=report.xml --cov --cov-report=xml:coverage.xml --cov-branch
  coverage: '/TOTAL\s+\d+\s+\d+\s+\d+\s+\d+\s+(\d+(?:\.\d+)?%)\s*$/'
  artifacts:
    when: always
    reports:
      junit: report.xml
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml

.security-base:
  stage: security
  allow_failure: true

sast:semgrep:
  extends: .security-base
  image: semgrep/semgrep:latest
  script:
    - semgrep scan --config auto --config p/owasp-top-ten --gitlab-sast
        --gitlab-sast-output gl-sast-semgrep.json --error src/ || true
  artifacts:
    when: always
    reports:
      sast: gl-sast-semgrep.json

secrets:betterleaks:
  extends: .security-base
  image:
    name: ghcr.io/betterleaks/betterleaks:latest
    entrypoint: [""]
  variables:
    GIT_DEPTH: 0
  script:
    - betterleaks git --no-banner --report-format sarif
        --report-path betterleaks.sarif --exit-code 0
  artifacts:
    when: always
    paths: [betterleaks.sarif]

sbom:
  extends: .security-base
  before_script:
    - curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh
        | sh -s -- -b /usr/local/bin
  script:
    - syft . -o cyclonedx-json=gl-sbom.cdx.json -o spdx-json=sbom.spdx.json
  artifacts:
    when: always
    reports:
      cyclonedx: [gl-sbom.cdx.json]
    paths: [sbom.spdx.json]
```

## Caching Best Practices

| Ecosystem   | Action / Setup                                   | Cache Path                           | Cache Key                        |
| ----------- | ------------------------------------------------ | ------------------------------------ | -------------------------------- |
| Python (uv) | `astral-sh/setup-uv@v7`                          | `~/.cache/uv`                        | Auto (uv.lock)                   |
| Node (pnpm) | `pnpm/action-setup@v4` + `actions/setup-node@v4` | `~/.pnpm-store`                      | `hashFiles('**/pnpm-lock.yaml')` |
| Go          | `actions/setup-go@v5`                            | `~/go/pkg/mod` + `~/.cache/go-build` | `hashFiles('**/go.sum')`         |
| Rust        | `Swatinem/rust-cache@v2`                         | `~/.cargo` + `target/`               | `hashFiles('**/Cargo.lock')`     |

## Key GitHub Actions

| Action                                            | Purpose                                                                                         |
| ------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| `astral-sh/setup-uv@v7`                           | Python (uv) with built-in caching                                                               |
| `pnpm/action-setup@v4`                            | pnpm setup                                                                                      |
| `actions/setup-go@v5`                             | Go with module caching                                                                          |
| `dtolnay/rust-toolchain@stable`                   | Rust toolchain                                                                                  |
| `Swatinem/rust-cache@v2`                          | Rust cargo + target caching                                                                     |
| `taiki-e/install-action@v2`                       | Install Rust CLI tools (cargo-nextest, etc.)                                                    |
| `golangci/golangci-lint-action@v6`                | golangci-lint with caching                                                                      |
| `ghcr.io/betterleaks/betterleaks:latest`          | Secret scanning (successor to gitleaks) — run via `docker run` in CI; no first-party action yet |
| `google/osv-scanner-action/osv-scanner-action@v2` | Dependency vulnerability scan                                                                   |
| `bridgecrewio/checkov-action@v12`                 | IaC security scan                                                                               |
| `aquasecurity/trivy-action@master`                | Container/filesystem vulnerability scan                                                         |
