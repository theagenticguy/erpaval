# Container Security & Dockerfiles

Multi-stage Dockerfile templates per language plus container security tooling.

## Base Image Hierarchy

From most to least secure:

1. **scratch** — Empty filesystem. Only for static binaries (Go, Rust). No shell, no package manager.
2. **Chainguard** (`cgr.dev/chainguard/...`) — Near-zero CVEs, daily rebuilds, SBOM included.
3. **Distroless** (`gcr.io/distroless/...`) — No shell, no package manager. Debian-based.
4. **Alpine** (`alpine:3.21`) — ~5 MB, musl libc. Good balance of size and utility.
5. **Debian Slim** (`debian:bookworm-slim`) — ~74 MB, glibc. Broadest compatibility.

## Dockerfile Templates

### Python (uv Multi-Stage)

```dockerfile
# syntax=docker/dockerfile:1

# --- Builder stage ---
FROM python:3.13-slim AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

WORKDIR /app

# Install dependencies (cached layer)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-editable --no-dev

# Copy application source
COPY . /app

# Install the project itself
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-editable --no-dev

# --- Runtime stage ---
FROM python:3.13-slim

RUN addgroup --system --gid 1001 app && \
    adduser --system --uid 1001 --ingroup app app

COPY --from=builder --chown=app:app /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH"

USER app
WORKDIR /app

CMD ["python", "-m", "myapp"]
```

Key env vars: `UV_COMPILE_BYTECODE=1` (pre-compile .pyc), `UV_LINK_MODE=copy` (required for Docker cache mounts).

### TypeScript (pnpm Multi-Stage)

```dockerfile
# syntax=docker/dockerfile:1

FROM node:22-slim AS base
ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable
WORKDIR /app

# --- Dependencies stage ---
FROM base AS deps
COPY package.json pnpm-lock.yaml ./
RUN --mount=type=cache,id=pnpm,target=/pnpm/store \
    pnpm install --frozen-lockfile --prod

# --- Build stage ---
FROM base AS build
COPY package.json pnpm-lock.yaml ./
RUN --mount=type=cache,id=pnpm,target=/pnpm/store \
    pnpm install --frozen-lockfile
COPY . .
RUN pnpm run build

# --- Runtime stage ---
FROM node:22-slim

RUN addgroup --system --gid 1001 app && \
    adduser --system --uid 1001 --ingroup app app

WORKDIR /app
COPY --from=deps --chown=app:app /app/node_modules ./node_modules
COPY --from=build --chown=app:app /app/dist ./dist
COPY --from=build --chown=app:app /app/package.json ./

USER app
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

### Go (Static Binary to scratch)

```dockerfile
# syntax=docker/dockerfile:1

FROM golang:1.22-alpine AS builder
WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 \
    go build -ldflags="-s -w" -o server ./cmd/server

# --- Runtime stage (zero attack surface) ---
FROM scratch

COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
USER 1001:1001
COPY --from=builder /app/server /server

EXPOSE 8080
ENTRYPOINT ["/server"]
```

For debug builds needing a shell, use `gcr.io/distroless/static-debian12:nonroot` instead of `scratch`.

### Rust (Multi-Stage with BuildKit Cache)

```dockerfile
# syntax=docker/dockerfile:1

FROM rust:1.77-slim AS builder
WORKDIR /app

COPY Cargo.toml Cargo.lock ./

# Dependency caching: build with dummy source
RUN mkdir src && echo "fn main() {}" > src/main.rs
RUN --mount=type=cache,target=/usr/local/cargo/registry \
    --mount=type=cache,target=/usr/local/cargo/git \
    --mount=type=cache,target=/app/target \
    cargo build --release

# Build real application
RUN rm -rf src target/release/deps/myapp* target/release/myapp*
COPY src ./src
RUN --mount=type=cache,target=/usr/local/cargo/registry \
    --mount=type=cache,target=/usr/local/cargo/git \
    --mount=type=cache,target=/app/target \
    cargo build --release && \
    cp target/release/myapp /usr/local/bin/myapp

# --- Runtime stage ---
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

For fully static musl binary:

```dockerfile
FROM rust:1.77-alpine AS builder
RUN apk add --no-cache musl-dev
WORKDIR /app
COPY . .
RUN cargo build --release --target x86_64-unknown-linux-musl

FROM scratch
COPY --from=builder /app/target/x86_64-unknown-linux-musl/release/myapp /myapp
USER 1001:1001
ENTRYPOINT ["/myapp"]
```

## Container Security Tools

### hadolint (Dockerfile Linting)

```bash
# Install
brew install hadolint         # or: mise use hadolint
```

```yaml
# .hadolint.yaml
ignored:
  - DL3008    # Pin versions in apt-get — too noisy for dev
  - SC2086    # Double quote to prevent globbing — Dockerfile false positives
override:
  error:
    - DL3007  # Using latest tag in FROM
    - DL3013  # Pin versions in pip install
    - DL3018  # Pin versions in apk add
trustedRegistries:
  - docker.io
  - ghcr.io
  - public.ecr.aws
failure-threshold: warning
```

```bash
hadolint Dockerfile
hadolint -f sarif Dockerfile > hadolint.sarif
```

### grype (Container Vulnerability Scanning)

```bash
# Install
brew install grype            # or: mise use grype
```

```yaml
# .grype.yaml
fail-on-severity: high
ignore:
  - vulnerability: CVE-2023-XXXX
    reason: "Not reachable in our code path"
match:
  python:
    using-cpes: false         # Reduce false positives
  javascript:
    using-cpes: false
```

```bash
grype myapp:latest                              # Scan image
grype sbom:sbom.cdx.json --fail-on high         # Scan SBOM (re-scannable)
grype myapp:latest -o sarif > grype.sarif        # SARIF output
```

**SBOM-first workflow** (recommended): Generate SBOM with syft once, then re-scan with grype as the vulnerability database updates — no need to rebuild.

```bash
syft myapp:latest -o cyclonedx-json=sbom.cdx.json
grype sbom:sbom.cdx.json --fail-on high
```

### cosign (Container Image Signing)

Keyless signing using OIDC identity (GitHub Actions, Google, Microsoft).

```bash
# Install
brew install cosign           # or: mise use cosign
```

```yaml
# In GitHub Actions
- uses: sigstore/cosign-installer@v3
- name: Sign the image
  run: |
    cosign sign --yes \
      ghcr.io/${{ github.repository }}@${{ steps.build.outputs.digest }}
```

Always sign **digests** (immutable), not tags (mutable).

Attach SBOM attestation:

```bash
cosign attest --predicate sbom.cdx.json --type cyclonedx --yes \
  ghcr.io/org/myapp@sha256:abc123...
```

## .dockerignore Template

```text
.git
.gitignore
.venv
__pycache__
*.pyc
.pytest_cache
.ruff_cache
.mypy_cache
node_modules
dist
build
target
*.egg-info
.env
.env.*
*.md
!README.md
Dockerfile
docker-compose*.yml
.dockerignore
.github
.gitlab-ci.yml
lefthook.yml
mise.toml
```

## Best Practices

- **Multi-stage builds**: Separate build dependencies from runtime. Final image should only contain artifacts.
- **Non-root user**: Always create and switch to a non-root user. Use numeric UIDs for scratch images.
- **Pin base images**: Use specific tags (e.g., `python:3.13-slim`), never `latest`.
- **Minimal final image**: Prefer scratch/distroless for static binaries, slim variants for interpreted languages.
- **BuildKit cache mounts**: Use `--mount=type=cache` for package manager caches to speed rebuilds.
- **Layer ordering**: Copy dependency manifests first (cached), then source code (changes frequently).
- **SHELL pipefail**: Set `SHELL ["/bin/bash", "-o", "pipefail", "-c"]` before RUN commands with pipes.
