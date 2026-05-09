# Python Project Scaffold

Complete project configuration with full quality gates and security pipeline. Based on production-proven configuration from code-context-agent.

## pyproject.toml

```toml
[build-system]
requires = ["uv_build>=0.10.5,<0.11.0"]
build-backend = "uv_build"

[project]
name = "myapp"
version = "0.1.0"
description = ""
readme = "README.md"
license = { text = "MIT" }
requires-python = ">=3.13"
dependencies = []

[project.scripts]
myapp = "myapp.cli:app"

[dependency-groups]
dev = [
    "commitizen>=4.13.8",
    "pytest>=9.0.2",
    "pytest-cov>=7.0.0",
    "ruff>=0.15.2",
]
security = [
    "bandit[sarif]>=1.9.3",
]

# ---- Ruff (Linting & Formatting) ----

[tool.ruff]
line-length = 120
indent-width = 4
target-version = "py313"
exclude = [".git", ".venv", "__pycache__", "build", "dist"]

[tool.ruff.lint]
select = [
    "E",      # pycodestyle errors
    "W",      # pycodestyle warnings
    "F",      # Pyflakes
    "I",      # isort
    "B",      # flake8-bugbear
    "C4",     # flake8-comprehensions
    "C90",    # mccabe complexity
    "BLE",    # flake8-blind-except
    "COM",    # flake8-commas
    "UP",     # pyupgrade
    "ARG",    # flake8-unused-arguments
    "SIM",    # flake8-simplify
    "TCH",    # flake8-type-checking
    "PTH",    # flake8-use-pathlib
    "ERA",    # eradicate (commented-out code)
    "PL",     # pylint
    "RUF",    # Ruff-specific
    "D",      # pydocstyle
    "S",      # flake8-bandit (security)
]
ignore = [
    "D100",    # Allow missing module docstrings
    "D104",    # Allow missing package docstrings
]
fixable = ["ALL"]

[tool.ruff.lint.pydocstyle]
convention = "google"

[tool.ruff.lint.mccabe]
max-complexity = 10

[tool.ruff.lint.per-file-ignores]
"tests/**/*.py" = ["D", "S101", "ARG"]

[tool.ruff.format]
quote-style = "double"
indent-style = "space"
docstring-code-format = true

# ---- ty (Type Checking) ----

[tool.ty.rules]
possibly-unresolved-reference = "error"
invalid-argument-type = "error"
missing-argument = "error"
unsupported-operator = "error"
division-by-zero = "error"
unused-ignore-comment = "warn"

[tool.ty.environment]
python-version = "3.13"

[tool.ty.src]
include = ["src"]

# ---- Bandit (SAST) ----

[tool.bandit]
exclude_dirs = ["tests", ".venv", "build", "dist"]
skips = [
    "B101",  # assert_used — tests use assert
]

# ---- Coverage ----

[tool.coverage.run]
branch = true
source = ["myapp"]
omit = ["*/tests/*", "*/__main__.py"]

[tool.coverage.report]
precision = 2
show_missing = true
fail_under = 80
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
    "@overload",
]

[tool.coverage.xml]
output = "coverage.xml"

# ---- Pytest ----

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --tb=short"

# ---- pip-licenses (License Compliance) ----

[tool.pip-licenses]
from = "mixed"
fail-on = "GPL;AGPL;SSPL;EUPL"
partial-match = true
ignore-packages = ["myapp"]

# ---- Commitizen (Conventional Commits) ----

[tool.commitizen]
name = "cz_conventional_commits"
version_provider = "pep621"
tag_format = "v$version"
update_changelog_on_bump = true
```

## mise.toml

```toml
[tools]
python = "3.13"
betterleaks = "latest"
osv-scanner = "latest"
semgrep = "latest"
syft = "latest"

[env]
_.python.venv = { path = ".venv", create = true }

[tasks]
install = "uv sync --all-groups"

[tasks.lint]
description = "Lint with ruff"
run = "uvx ruff check src/"

[tasks."lint:fix"]
description = "Lint and auto-fix"
run = "uvx ruff check src/ --fix"

[tasks.format]
description = "Format with ruff"
run = "uvx ruff format src/"

[tasks."format:check"]
description = "Check formatting"
run = "uvx ruff format --check src/"

[tasks.typecheck]
description = "Type check with ty"
run = "uvx ty check src/"

[tasks.test]
description = "Run tests"
run = "uv run pytest"

[tasks."test:coverage"]
description = "Run tests with coverage"
run = "uv run pytest --cov --cov-report=term-missing:skip-covered --cov-report=xml:coverage.xml --cov-branch"

[tasks.security]
description = "Run all security scans"
depends = ["security:secrets", "security:sast", "security:bandit", "security:deps", "security:licenses"]

[tasks."security:secrets"]
description = "Scan for secrets with betterleaks"
run = "betterleaks git --no-banner"

[tasks."security:sast"]
description = "SAST scan with semgrep"
run = "semgrep scan --config auto --config p/owasp-top-ten --error --quiet src/"

[tasks."security:bandit"]
description = "SAST scan with bandit"
run = "uv run bandit -c pyproject.toml -r src/"

[tasks."security:deps"]
description = "Audit dependencies for vulnerabilities"
run = "osv-scanner scan --lockfile uv.lock"

[tasks."security:licenses"]
description = "Check dependency licenses"
run = "uv run --with pip-licenses pip-licenses"

[tasks."security:sbom"]
description = "Generate SBOMs"
run = "syft . -o cyclonedx-json=sbom.cdx.json -o spdx-json=sbom.spdx.json"

[tasks.check]
description = "Run all checks"
depends = ["lint", "format:check", "typecheck", "test"]

[tasks.commit]
description = "Interactive conventional commit"
run = "uv run cz commit"

[tasks.bump]
description = "Bump version"
run = "uv run cz bump"
```

## lefthook.yml

```yaml
commit-msg:
  jobs:
    - name: conventional-commit
      run: uv run cz check --commit-msg-file {1}

pre-commit:
  parallel: true
  jobs:
    - name: ruff-check
      run: uvx ruff check --fix {staged_files}
      glob: "*.py"
      stage_fixed: true

    - name: ruff-format
      run: uvx ruff format {staged_files}
      glob: "*.py"
      stage_fixed: true

    - name: ty-check
      run: uvx ty check src/

    - name: betterleaks
      run: git diff --staged | betterleaks stdin --no-banner

pre-push:
  parallel: true
  jobs:
    - name: lint
      run: uvx ruff check src/

    - name: format-check
      run: uvx ruff format --check src/

    - name: typecheck
      run: uvx ty check src/

    - name: test
      run: uv run pytest

    - name: betterleaks
      run: betterleaks git --no-banner

    - name: semgrep
      run: semgrep scan --config auto --config p/owasp-top-ten --error --quiet src/
```

## .github/workflows/ci.yml

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

## Dockerfile

```dockerfile
# syntax=docker/dockerfile:1

FROM python:3.13-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-editable --no-dev

COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-editable --no-dev

FROM python:3.13-slim
RUN addgroup --system --gid 1001 app && \
    adduser --system --uid 1001 --ingroup app app
COPY --from=builder --chown=app:app /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"
USER app
WORKDIR /app
CMD ["python", "-m", "myapp"]
```

## .gitignore

```text
__pycache__/
*.py[cod]
*.egg-info/
dist/
build/
.venv/
.ruff_cache/
.pytest_cache/
.coverage
coverage.xml
*.sarif
sbom.*.json
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

[*.{toml,yaml,yml}]
indent_size = 2

[*.md]
trim_trailing_whitespace = false
```

## Setup Commands

```bash
# Initialize
uv init myapp && cd myapp
mise install && uv sync --all-groups
lefthook install

# Verify
mise run check
mise run security
```
