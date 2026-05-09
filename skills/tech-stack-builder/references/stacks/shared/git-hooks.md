# Git Hooks & Conventional Commits

## lefthook (Git Hook Manager)

lefthook is the recommended git hook manager — fast, zero-dependency, and supports parallel execution.

### lefthook.yml

```yaml
pre-commit:
  parallel: true
  commands:
    lint:
      glob: "*.{py,pyi}"
      run: uvx ruff check --fix {staged_files}
      stage_fixed: true
    format:
      glob: "*.{py,pyi}"
      run: uvx ruff format {staged_files}
      stage_fixed: true
    typecheck:
      glob: "*.{py,pyi}"
      run: uv run pyright {staged_files}
    biome:
      glob: "*.{ts,tsx,js,jsx,json}"
      run: pnpm biome check --write {staged_files}
      stage_fixed: true

commit-msg:
  commands:
    commitlint:
      run: pnpm commitlint --edit {1}
```

### Setup

```bash
# Install
mise use lefthook
# or: brew install lefthook

# Initialize (creates lefthook.yml if missing)
lefthook install
```

### Go lefthook.yml

```yaml
pre-commit:
  parallel: true
  commands:
    golangci-lint:
      glob: "*.go"
      run: golangci-lint run --new-from-rev HEAD
    gofumpt-check:
      glob: "*.go"
      run: 'test -z "$(gofumpt -l {staged_files})"'
    betterleaks:
      run: git diff --staged | betterleaks stdin --no-banner

commit-msg:
  commands:
    conventional:
      run: |
        MSG=$(head -1 {1})
        echo "$MSG" | grep -qE '^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\(.+\))?: .+' \
          || (echo "Must follow Conventional Commits" && exit 1)

pre-push:
  parallel: true
  commands:
    test:
      run: go test -race ./...
    lint:
      run: golangci-lint run
    govulncheck:
      run: govulncheck ./...
    betterleaks:
      run: betterleaks git --no-banner
```

### Rust lefthook.yml

```yaml
pre-commit:
  parallel: true
  commands:
    cargo-fmt:
      glob: "*.rs"
      run: cargo fmt --check
    cargo-clippy:
      glob: "*.rs"
      run: cargo clippy --workspace --all-targets -- -D warnings
    betterleaks:
      run: git diff --staged | betterleaks stdin --no-banner

pre-push:
  parallel: true
  commands:
    test:
      run: cargo nextest run
    cargo-deny:
      run: cargo deny check
    betterleaks:
      run: betterleaks git --no-banner
    semgrep:
      run: semgrep scan --config p/rust --config p/owasp-top-ten --error src/
```

## Conventional Commits (commitizen + commitlint)

### .czrc

```json
{
  "path": "cz-conventional-changelog"
}
```

### commitlint.config.js

```javascript
export default {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [2, 'always', [
      'feat', 'fix', 'docs', 'style', 'refactor',
      'perf', 'test', 'build', 'ci', 'chore', 'revert'
    ]],
    'subject-case': [2, 'never', ['start-case', 'pascal-case', 'upper-case']],
  },
}
```

### Usage

```bash
# Interactive commit
pnpm cz
# or: npx cz

# Format: <type>(<scope>): <subject>
# Examples:
# feat(auth): add OAuth2 login flow
# fix(api): handle null response from /users endpoint
# docs: update README with deployment steps
```
