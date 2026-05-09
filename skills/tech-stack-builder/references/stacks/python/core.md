# Python Core Stack

Settled defaults for all Python projects. These are health-check-only — no comparison research needed.

> **Current versions**: Python 3.13 as the runtime floor, `uv` 0.11.x, `ruff` 0.15.x (2026 style guide), `ty` 0.0.32, `pytest` 9.x.

## Package Management: uv

`uv` is the default for everything Python. Never use pip, pip-tools, pipx, virtualenv, pyenv, or poetry.

> **uv 0.11** swapped to [`rustls-platform-verifier`](https://github.com/rustls/rustls-platform-verifier) and `aws-lc` for TLS/crypto. Most users are unaffected, but if a previously trusted certificate chain is suddenly rejected, check your system trust store — uv now delegates to `Security.framework` / system APIs instead of eagerly loading keychain certs. `--native-tls` is deprecated in favor of `--system-certs` (identical behavior). The change improves macOS startup time by skipping bulk keychain reads.

| Task                   | Command                                |
| ---------------------- | -------------------------------------- |
| Run a script           | `uv run script.py`                     |
| Init a project         | `uv init my-app`                       |
| Init a library         | `uv init --lib my-lib`                 |
| Add dependency         | `uv add httpx`                         |
| Add dev dependency     | `uv add --dev pytest`                  |
| Sync from lockfile     | `uv sync`                              |
| Run in project env     | `uv run pytest`                        |
| One-off with extra dep | `uv run --with httpx python script.py` |
| CLI tool (no install)  | `uvx ruff check .`                     |

Always commit both `pyproject.toml` and `uv.lock`.

## Linting & Formatting: ruff

Replaces black, isort, flake8, pylint in a single tool.

> **ruff 0.15** shipped the **2026 style guide** and **block suppression comments** (`# ruff: disable[N803]` / `# ruff: enable[N803]`). Formatter changes include: lambda parameters stay on one line, parentheses around `except` exception tuples removed on Python 3.14+, a single blank line permitted at the start of function bodies, no parentheses around long `as` captures in `match`. Many security/async/pytest rules have stabilized out of preview (see the [0.15.0 release notes](https://github.com/astral-sh/ruff/releases/tag/0.15.0)). **Preview feature**: markdown code-block formatting.

```toml
# pyproject.toml
[tool.ruff]
target-version = "py313"
line-length = 120

[tool.ruff.lint]
select = [
    "E", "W", "F", "I", "B", "C4", "C90", "BLE", "COM",
    "UP", "ARG", "SIM", "TCH", "PTH", "ERA", "PL", "RUF",
    "D",   # pydocstyle (docstrings)
    "S",   # flake8-bandit (security) — inline SAST
]
ignore = ["D100", "D104"]

[tool.ruff.lint.pydocstyle]
convention = "google"

[tool.ruff.lint.mccabe]
max-complexity = 10

[tool.ruff.lint.per-file-ignores]
"tests/**/*.py" = ["D", "S101", "ARG"]
```

The `S` rules (flake8-bandit) provide inline security scanning that **covers most of what standalone bandit checks**. For new Python projects, default to ruff `S` only + semgrep for cross-language SAST; keep standalone `bandit` only for legacy CI continuity or specific checks ruff hasn't ported.

### Bandit (Standalone SAST — legacy / optional)

```toml
# pyproject.toml
[dependency-groups]
security = ["bandit[sarif]>=1.9.3"]

[tool.bandit]
exclude_dirs = ["tests", ".venv", "build", "dist"]
skips = ["B101"]  # assert_used — tests use assert
```

```bash
uv run bandit -c pyproject.toml -r src/
uv run bandit -c pyproject.toml -r src/ -f sarif -o bandit.sarif
```

## Type Checking: ty (or pyright)

ty (from the ruff/astral team) is the emerging default. pyright remains a solid alternative with better VSCode integration.

```toml
# pyproject.toml — ty configuration
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
```

```bash
uvx ty check src/
```

### pyright (alternative)

```toml
# pyproject.toml
[tool.pyright]
pythonVersion = "3.13"
typeCheckingMode = "standard"
```

## Coverage: pytest-cov

```toml
# pyproject.toml
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
```

```bash
uv run pytest --cov --cov-report=term-missing:skip-covered --cov-report=xml --cov-branch
```

## Data Validation: pydantic v2

De facto standard for Python data models with runtime validation.

```python
from pydantic import BaseModel, Field

class Config(BaseModel):
    name: str
    port: int = Field(default=8080, ge=1, le=65535)
    debug: bool = False
```

## Testing: pytest v9

`pytest` v9 is the current stable line (v8 → v9 transition happened in 2025). Check the release notes for any deprecated fixtures/APIs when migrating v8 projects.

```toml
# pyproject.toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --tb=short"

[dependency-groups]
dev = [
    "pytest>=9",
    "pytest-cov>=7",
]
```

## HTTP Client: httpx

Async-native replacement for requests.

```python
import httpx

# Sync
resp = httpx.get("https://api.example.com/data")

# Async
async with httpx.AsyncClient() as client:
    resp = await client.get("https://api.example.com/data")
```

## Tabular Data: polars

Faster and more ergonomic than pandas.

```python
import polars as pl

df = pl.read_csv("data.csv")
result = df.filter(pl.col("age") > 30).group_by("city").agg(pl.col("salary").mean())
```
