# Security & Quality Pipeline

A 7-layer shift-left defense model for comprehensive project security. Each layer catches different classes of issues at increasing cost — the earlier you catch, the cheaper the fix.

## The 7-Layer Defense Model

```text
Layer 1: Editor        — Instant feedback while typing (ruff, biome, clippy, rust-analyzer)
Layer 2: Pre-commit    — Catches issues before they enter the commit (lefthook)
Layer 3: Commit-msg    — Enforces conventional commit format (commitizen/commitlint)
Layer 4: Pre-push      — Full lint + test + SAST before code leaves the machine
Layer 5: CI            — Authoritative checks on every PR (SAST, SCA, secrets, licenses)
Layer 6: Nightly       — Deep scans too slow for PR (mutation testing, full dep updates)
Layer 7: Release       — SBOM generation, image signing, provenance attestation
```

## Per-Language Tool Mapping

| Layer               | Python                | TypeScript                   | Go                        | Rust                     | Cross-Language                 |
| ------------------- | --------------------- | ---------------------------- | ------------------------- | ------------------------ | ------------------------------ |
| Inline SAST         | ruff S rules          | biome security domain        | gosec (via golangci-lint) | clippy restriction lints | --                             |
| Deep SAST           | bandit                | semgrep p/typescript         | semgrep p/golang          | semgrep p/rust           | semgrep auto + p/owasp-top-ten |
| Secret detection    | --                    | --                           | --                        | --                       | betterleaks                    |
| Dep vulnerabilities | osv-scanner (uv.lock) | osv-scanner (pnpm-lock.yaml) | govulncheck + osv-scanner | cargo-audit + cargo-deny | osv-scanner, trivy fs          |
| License compliance  | pip-licenses          | license-checker-rseidelsohn  | go-licenses               | cargo-deny [licenses]    | --                             |
| SBOM generation     | syft                  | syft                         | syft                      | syft                     | syft (CycloneDX + SPDX)        |
| IaC scanning        | --                    | --                           | --                        | --                       | checkov, trivy config          |
| Container scanning  | --                    | --                           | --                        | --                       | grype, trivy image, hadolint   |

## Tool Configuration Quick Reference

### betterleaks (Secret Detection)

Successor to `gitleaks`, built by the original gitleaks author (Zach Rice) with Aikido Security — better detection (98.6% CredData recall vs. 70.4% for gitleaks), CEL-based live-secret validation, and parallelized git scanning. Config files and `.gitleaksignore` are accepted as-is; env vars `BETTERLEAKS_CONFIG` and `GITLEAKS_CONFIG` both work.

```bash
# Install
brew install betterleaks                        # or: brew install betterleaks/tap/betterleaks
# mise:    mise use betterleaks
# docker:  docker pull ghcr.io/betterleaks/betterleaks:latest
```

```toml
# .betterleaks.toml (or .gitleaks.toml — both are honored)
[extend]
useDefault = true                               # default ruleset from the binary

[[allowlists]]
paths = [
  '''(.*?)\.test\.\w+''',
  '''fixtures/''',
]
```

```bash
betterleaks git                                 # Scan current git repo
betterleaks dir .                               # Scan files/directories (non-git)
git diff --staged | betterleaks stdin           # Pre-commit-style: scan staged changes
betterleaks git --report-format sarif --report-path betterleaks.sarif
betterleaks git --validation                    # Fire HTTP requests to verify secrets are live (opt-in)
```

Inline suppression: add `betterleaks:allow` (or legacy `gitleaks:allow`) as a comment on the line.

### semgrep (Deep SAST)

```bash
# Install
uv tool install semgrep        # or: brew install semgrep
```

```bash
# Auto-detect language and apply relevant rules
semgrep scan --config auto --error src/

# Specific rulesets
semgrep scan --config p/python --config p/owasp-top-ten src/

# Available rulesets per language
# p/python, p/typescript, p/javascript, p/golang, p/rust
# p/react, p/docker, p/owasp-top-ten, p/secrets
```

SARIF output: `semgrep scan --config auto --sarif > semgrep.sarif`

### bandit (Python SAST)

```bash
# Install
uv add --group security "bandit[sarif]"
```

```toml
# pyproject.toml
[tool.bandit]
exclude_dirs = ["tests", ".venv", "build", "dist"]
skips = [
    "B101",  # assert_used — tests use assert
]
```

```bash
uv run bandit -c pyproject.toml -r src/
uv run bandit -c pyproject.toml -r src/ -f sarif -o bandit.sarif
```

### osv-scanner (Dependency Vulnerabilities)

```bash
# Install
brew install osv-scanner       # or: mise use osv-scanner
```

Supported lockfiles: `uv.lock`, `pnpm-lock.yaml`, `go.sum`, `Cargo.lock`, `requirements.txt`, `poetry.lock`, `package-lock.json`, `yarn.lock`.

```bash
osv-scanner scan --lockfile uv.lock
osv-scanner scan -r .                          # Recursive directory scan
osv-scanner scan --format sarif -r . > osv.sarif
```

### syft (SBOM Generation)

```bash
# Install
brew install syft              # or: mise use syft
```

```bash
# Directory SBOM (CycloneDX + SPDX)
syft dir:. -o cyclonedx-json=sbom.cdx.json -o spdx-json=sbom.spdx.json

# Container image SBOM
syft myapp:latest -o cyclonedx-json=sbom.cdx.json
```

### trivy (Multi-Scanner)

```bash
# Install
brew install trivy             # or: mise use trivy
```

```bash
trivy fs --severity HIGH,CRITICAL .            # Filesystem vuln scan
trivy config .                                 # IaC misconfig scan
trivy image --severity HIGH,CRITICAL myapp:latest  # Container scan
trivy fs --format sarif --output trivy.sarif . # SARIF output
```

### checkov (IaC Security)

```bash
# Install
uvx checkov -d .               # One-shot, no install
# or: uv add --dev checkov
```

```yaml
# .checkov.yml
framework:
  - terraform
  - dockerfile
  - kubernetes
skip-check:
  - CKV_AWS_18  # S3 encryption — handled by org SCP
skip-path:
  - .terraform/
  - node_modules/
soft-fail-on:
  - LOW
  - MEDIUM
```

## SARIF Integration

Most security tools produce SARIF (Static Analysis Results Interchange Format) for unified reporting.

**GitHub**: Upload via `github/codeql-action/upload-sarif@v3` — results appear in Security tab.

**GitLab**: Convert SARIF to GitLab format via `sarif-converter` or use native report types (`sast`, `dependency_scanning`, `container_scanning`).

**Tools with native SARIF output**: semgrep, bandit, betterleaks, trivy, checkov, grype, hadolint, osv-scanner.

## Dependabot / Renovate

### Dependabot (GitHub)

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    groups:
      production-dependencies:
        dependency-type: "production"
        update-types: ["minor", "patch"]
      dev-dependencies:
        dependency-type: "development"
        patterns: ["*"]

  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    groups:
      all-minor-patch:
        patterns: ["*"]
        update-types: ["minor", "patch"]

  - package-ecosystem: "gomod"
    directory: "/"
    schedule:
      interval: "weekly"

  - package-ecosystem: "cargo"
    directory: "/"
    schedule:
      interval: "weekly"

  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"

  - package-ecosystem: "docker"
    directory: "/"
    schedule:
      interval: "weekly"
```

### Renovate (Alternative)

Use Renovate over Dependabot when you need: multi-platform support (GitLab, Bitbucket), complex grouping, auto-merge with merge confidence, or 90+ package manager support.

```json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": ["config:recommended", ":semanticCommits", "group:allNonMajor"],
  "packageRules": [
    { "matchUpdateTypes": ["patch"], "automerge": true },
    {
      "matchDepTypes": ["devDependencies"],
      "matchUpdateTypes": ["minor", "patch"],
      "automerge": true
    }
  ]
}
```

## Composing the Full Pipeline

### Pre-commit (lefthook)

```yaml
# In lefthook.yml — see git-hooks.md for full patterns
pre-commit:
  parallel: true
  jobs:
    - name: betterleaks
      run: git diff --staged | betterleaks stdin --no-banner
    # ... plus language-specific linters
```

### CI (GitHub Actions)

```yaml
# Minimal security job — add to your CI workflow
security:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4

    - name: Semgrep SAST
      run: |
        pip install semgrep
        semgrep scan --config auto --config p/owasp-top-ten --error --sarif > semgrep.sarif src/

    - name: Betterleaks
      run: |
        docker run --rm -v "$PWD:/src" ghcr.io/betterleaks/betterleaks:latest \
          git --no-banner --report-format sarif --report-path /src/betterleaks.sarif /src
      env:
        GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}

    - name: OSV-Scanner
      uses: google/osv-scanner-action/osv-scanner-action@v2
      with:
        scan-args: |-
          --recursive
          .

    - name: Upload SARIF
      if: always()
      uses: github/codeql-action/upload-sarif@v3
      with:
        sarif_file: semgrep.sarif
```

### Nightly (Scheduled)

Run expensive scans on a schedule rather than every PR:

- Dependency updates: `uv lock --upgrade` / `cargo update` / `pnpm update`
- Mutation testing: `mutmut run` / `cargo mutants` / Stryker
- Full CodeQL analysis with `security-extended` queries
- SBOM regeneration with `syft`
