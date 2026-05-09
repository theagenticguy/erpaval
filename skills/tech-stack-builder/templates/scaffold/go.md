# Go Project Scaffold

Complete project configuration with full quality gates and security pipeline.

## go.mod

```go
module github.com/org/myapp

go 1.26
```

## .golangci.yml

```yaml
version: "2"

linters:
  enable:
    - gosec
    - revive
    - staticcheck
    - errcheck
    - exhaustive
    - govet
    - ineffassign
    - unused
    - gofumpt
    - misspell
    - prealloc
    - unconvert
    - unparam
    - copyloopvar

linters-settings:
  revive:
    rules:
      - name: exported
        arguments: [checkPrivateReceivers]
      - name: blank-imports
      - name: context-as-argument
      - name: error-return
      - name: error-naming
      - name: increment-decrement
      - name: var-naming
      - name: unreachable-code
  gosec:
    excludes:
      - G104
  govet:
    enable-all: true
  gofumpt:
    extra-rules: true
  exhaustive:
    default-signifies-exhaustive: true

formatters:
  enable:
    - gofumpt

issues:
  exclude-dirs:
    - vendor
    - testdata
  exclude-rules:
    - path: "_test\\.go"
      linters:
        - gosec
        - errcheck
```

## mise.toml

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

[tasks."fmt:check"]
description = "Check formatting"
run = 'test -z "$(gofumpt -l .)"'

[tasks.test]
description = "Run tests"
run = "go test -v -race ./..."

[tasks."test:coverage"]
description = "Run tests with coverage"
run = "go test -coverprofile=coverage.out ./... && go tool cover -func=coverage.out"

[tasks.vet]
description = "Run go vet"
run = "go vet ./..."

[tasks.security]
description = "Run all security scans"
depends = ["security:secrets", "security:vuln", "security:sast", "security:deps"]

[tasks."security:secrets"]
description = "Scan for secrets"
run = "betterleaks git --no-banner"

[tasks."security:vuln"]
description = "Scan for Go vulnerabilities"
run = "go install golang.org/x/vuln/cmd/govulncheck@latest && govulncheck ./..."

[tasks."security:sast"]
description = "SAST scan with semgrep"
run = "semgrep scan --config p/golang --config p/owasp-top-ten --error ."

[tasks."security:deps"]
description = "Audit dependencies"
run = "osv-scanner scan -r ."

[tasks.check]
description = "Run all checks"
depends = ["fmt:check", "lint", "vet", "test"]
```

## lefthook.yml

```yaml
pre-commit:
  parallel: true
  jobs:
    - name: golangci-lint
      glob: "*.go"
      run: golangci-lint run --new-from-rev HEAD

    - name: gofumpt-check
      glob: "*.go"
      run: 'test -z "$(gofumpt -l {staged_files})"'

    - name: betterleaks
      run: git diff --staged | betterleaks stdin --no-banner

commit-msg:
  jobs:
    - name: conventional-commit
      run: |
        MSG=$(head -1 {1})
        echo "$MSG" | grep -qE '^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\(.+\))?: .+' \
          || (echo "Commit message must follow Conventional Commits format" && exit 1)

pre-push:
  parallel: true
  jobs:
    - name: test
      run: go test -race ./...

    - name: lint
      run: golangci-lint run

    - name: govulncheck
      run: govulncheck ./...

    - name: betterleaks
      run: betterleaks git --no-banner

    - name: semgrep
      run: semgrep scan --config p/golang --config p/owasp-top-ten --error .
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
      - uses: actions/setup-go@v5
        with:
          go-version-file: go.mod
          cache: true
      - name: gofumpt check
        run: |
          go install mvdan.cc/gofumpt@latest
          test -z "$(gofumpt -l .)"

  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-go@v5
        with:
          go-version-file: go.mod
          cache: true
      - uses: golangci/golangci-lint-action@v6
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

## Dockerfile

```dockerfile
# syntax=docker/dockerfile:1

FROM golang:1.22-alpine AS builder
WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 \
    go build -ldflags="-s -w" -o server ./cmd/server

FROM scratch
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
USER 1001:1001
COPY --from=builder /app/server /server
EXPOSE 8080
ENTRYPOINT ["/server"]
```

## .gitignore

```text
/bin/
/vendor/
coverage.out
*.sarif
.env
```

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

[*.go]
indent_style = tab
indent_size = 4

[*.{yaml,yml,json,toml}]
indent_size = 2

[Makefile]
indent_style = tab

[*.md]
trim_trailing_whitespace = false
```

## Setup Commands

```bash
# Initialize
go mod init github.com/org/myapp
mise install && lefthook install

# Verify
mise run check
mise run security
```
