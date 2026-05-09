# Python CLI Stack

For building command-line tools and interactive terminal applications.

## CLI Framework: cyclopts (Recommended) or typer

| Feature          | cyclopts            | typer                   |
| ---------------- | ------------------- | ----------------------- |
| Type annotations | Full Python typing  | Full Python typing      |
| Nested commands  | Native              | Native                  |
| Pydantic support | Built-in            | Via extension           |
| Validators       | Pydantic validators | click callbacks         |
| Completion       | Built-in            | Built-in                |
| Maintenance      | Active, modern      | Active, large community |

Default to **cyclopts** for new projects. Use **typer** when the team already knows it.

```python
# cyclopts example
import cyclopts

app = cyclopts.App(help="My CLI tool")

@app.command
def greet(name: str, count: int = 1):
    """Greet someone."""
    for _ in range(count):
        print(f"Hello, {name}!")

if __name__ == "__main__":
    app()
```

## Rich Terminal Output: rich

For styled terminal output, tables, progress bars, and logging.

```python
from rich.console import Console
from rich.table import Table
from rich.progress import track

console = Console()

# Styled output
console.print("[bold green]Success![/] Operation completed.")

# Tables
table = Table(title="Results")
table.add_column("Name", style="cyan")
table.add_column("Score", justify="right")
table.add_row("Alice", "95")
console.print(table)

# Progress bars
for item in track(range(100), description="Processing..."):
    process(item)
```

## Recommended Stack

```toml
# pyproject.toml
[project]
dependencies = [
    "cyclopts>=4",        # v4 is the current stable line; v5 in alpha
    "rich>=15",           # v15 is current — bumps v13/v14 baselines
    "pydantic>=2.13",
]

[project.scripts]
my-tool = "my_tool.cli:app"
```
