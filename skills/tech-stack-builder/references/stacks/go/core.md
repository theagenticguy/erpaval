# Go Core Stack

Settled defaults for all Go projects. These are health-check-only — no comparison research needed.

> **Go 1.26.x** is the current stable toolchain (supported: 1.26 / 1.25 / 1.24). Bump any `go 1.22` or `go 1.23` pins.
> **golangci-lint v2** uses a new config schema — the v1 YAML format will NOT parse. All examples below are v2-format.

## Package Management: Go Modules

Go modules are the built-in package management system. No external tool needed.

```bash
# Initialize a new module
go mod init github.com/org/project

# Add dependencies (auto-detected from imports)
go mod tidy

# Verify dependency integrity
go mod verify

# Download dependencies for offline use
go mod download

# List all dependencies
go list -m all

# Upgrade a specific dependency
go get -u github.com/some/package@latest

# Upgrade all dependencies
go get -u ./...
```

Always commit both `go.mod` and `go.sum`.

## Linting: golangci-lint v2

The meta-linter that runs 30+ linters in parallel. v2 uses a new `.golangci.yml` format.

```yaml
# .golangci.yml (v2 format)
version: "2"

linters:
  enable:
    - gosec          # Security rules
    - revive         # Superset of golint
    - staticcheck    # Go vet on steroids
    - errcheck       # Unchecked errors
    - exhaustive     # Exhaustive switch/map checks
    - govet          # Go vet checks
    - ineffassign    # Ineffective assignments
    - unused         # Unused code
    - gofumpt        # Stricter gofmt
    - misspell       # Spelling mistakes
    - prealloc       # Slice preallocation hints
    - unconvert      # Unnecessary type conversions
    - unparam        # Unused function parameters
    - copyloopvar    # Loop variable capture (Go 1.22+)

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
      - G104    # Audit errors not checked (too noisy for some projects)
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

```bash
# Install
brew install golangci-lint
# or: go install github.com/golangci/golangci-lint/v2/cmd/golangci-lint@latest

# Run
golangci-lint run
golangci-lint run ./...
golangci-lint run --fix    # Auto-fix where possible
```

## Formatting: gofumpt

Stricter superset of `gofmt`. Enforces additional formatting rules (grouped imports, unnecessary blank lines removed).

```bash
# Install
go install mvdan.cc/gofumpt@latest

# Format
gofumpt -l -w .

# Check only (CI)
gofumpt -l -d .
```

Integrated into golangci-lint as a formatter — no need to run separately if using golangci-lint.

## Testing: go test

```bash
# Run all tests
go test ./...

# Verbose with race detection
go test -v -race ./...

# With coverage
go test -cover ./...

# Generate coverage profile
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out -o coverage.html
go tool cover -func=coverage.out

# Run specific test
go test -run TestMyFunction ./pkg/...

# Benchmarks
go test -bench=. -benchmem ./...
```

For assertions, use `testify`:

```go
import "github.com/stretchr/testify/assert"

func TestAdd(t *testing.T) {
    result := Add(2, 3)
    assert.Equal(t, 5, result)
}
```

## Vulnerability Scanning: govulncheck

Official Go vulnerability scanner from the Go team. Checks compiled code paths (not just dependencies).

```bash
# Install
go install golang.org/x/vuln/cmd/govulncheck@latest

# Scan
govulncheck ./...

# JSON output
govulncheck -format json ./...
```

## HTTP Frameworks

| Framework           | When to Use                                        |
| ------------------- | -------------------------------------------------- |
| `net/http` (stdlib) | Simple APIs, minimal dependencies                  |
| `chi`               | RESTful APIs needing middleware and routing        |
| `echo`              | Full-featured with built-in middleware, validation |

For most projects, `net/http` with `chi` router is the settled default:

```go
import "github.com/go-chi/chi/v5"

r := chi.NewRouter()
r.Use(middleware.Logger)
r.Get("/health", healthHandler)
```
