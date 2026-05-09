# Output Templates

Defines the structure and format for all generated artifacts. The `/build-stack` command uses these patterns to produce consistent outputs.

## Generated Artifacts

| Artifact     | Filename                 | Description                                                     |
| ------------ | ------------------------ | --------------------------------------------------------------- |
| Stack Report | `tech-stack-report.md`   | Full analysis with comparison matrices and architecture diagram |
| ADR files    | `adr/NNN-{topic}.md`     | One per significant technology decision (3-5 total)             |
| Python deps  | `pyproject.toml` snippet | If Python is in the stack                                       |
| JS/TS deps   | `package.json` snippet   | If JavaScript/TypeScript is in the stack                        |
| Dev tools    | `mise.toml` snippet      | Tool versions and task definitions                              |

## Stack Report Structure

The report follows this outline (see `templates/stack-report.md` for the full template):

1. **Executive Summary** — 3-5 sentence overview of the recommended stack
2. **Requirements Recap** — Normalized requirements from intake phase
3. **Unified Stack Table** — Single table with all recommended technologies
4. **Per-Layer Analysis** — Detailed breakdown per architectural layer
5. **Comparison Matrices** — Side-by-side evaluations for researched categories
6. **Architecture Diagram** — Mermaid diagram showing component relationships
7. **Health Report** — Consolidated health checks for all recommendations
8. **Trade-offs and Risks** — Known limitations and mitigation strategies
9. **Dependency Manifests** — Ready-to-use config file snippets
10. **Sources** — Links to docs, repos, benchmarks cited

## Comparison Matrix Format

Used for every 🔬 RESEARCH category. See `templates/comparison-matrix.md` for the full template.

`````markdown
### {Category Name}

| Criteria (weight)     | Candidate A | Candidate B     | Candidate C |
| --------------------- | ----------- | --------------- | ----------- |
| Performance (0.2)     | ⭐⭐⭐      | ⭐⭐            | ⭐⭐⭐      |
| DX / Ergonomics (0.2) | ⭐⭐        | ⭐⭐⭐          | ⭐⭐        |
| Ecosystem (0.15)      | ⭐⭐⭐      | ⭐⭐⭐          | ⭐⭐        |
| Learning Curve (0.15) | ⭐⭐        | ⭐⭐⭐          | ⭐⭐        |
| Health (0.15)         | ✅ HEALTHY  | ✅ HEALTHY      | ⚠️ CAUTION   |
| Team Fit (0.15)       | ⭐⭐⭐      | ⭐⭐            | ⭐⭐        |
| **Weighted Score**    | **2.55**    | **2.65**        | **2.30**    |
| **Recommendation**    |             | ✅ **Selected** |             |

````text
Star ratings: ⭐ (1) = Poor, ⭐⭐ (2) = Adequate, ⭐⭐⭐ (3) = Excellent

## ADR Format

See `templates/adr-template.md` for the full template. Each ADR covers:

- Status (Proposed/Accepted)
- Context (why this decision matters)
- Decision (what was chosen and why)
- Alternatives table (what else was considered)
- Consequences (positive and negative)
- Health check snapshot

## Mermaid Diagram Patterns

### System Architecture (Primary)

```mermaid
graph TB
    subgraph Client
        A[Browser / Mobile App]
    end
    subgraph API Layer
        B[API Gateway]
        C[Application Server]
    end
    subgraph Data Layer
        D[(Primary DB)]
        E[(Cache)]
    end
    subgraph Infrastructure
        F[CDN]
        G[Message Queue]
        H[Object Storage]
    end
    A --> F
    A --> B
    B --> C
    C --> D
    C --> E
    C --> G
    G --> C
    F --> H
````
`````

### Deployment Architecture

````mermaid
graph LR
    subgraph CI/CD
        A[GitHub Actions]
    end
    subgraph Container Runtime
        B[Container Registry]
        C[Compute Service]
    end
    subgraph Observability
        D[Traces]
        E[Metrics]
        F[Logs]
    end
    A --> B
    B --> C
    C --> D
    C --> E
    C --> F
```text

Adapt the diagram based on actual stack choices. Include:

- All major components from the unified stack
- Data flow arrows with labels
- Subgraphs for logical layers
- External service integrations

## Dependency File Formats

### pyproject.toml Snippet

```toml
[project]
name = "{project-name}"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = [
    # Web framework
    "{framework}>=x.y",
    # ... grouped by purpose with comments
]

[dependency-groups]
dev = [
    "pytest>=8.0",
    "ruff>=0.8",
    # ...
]
````

### package.json Snippet

````json
{
  "name": "{project-name}",
  "type": "module",
  "dependencies": {
    "{framework}": "^x.y.z"
  },
  "devDependencies": {
    "vitest": "^x.y.z",
    "biome": "^x.y.z"
  }
}
```markdown

### mise.toml Snippet

```toml
[tools]
python = "3.12"
node = "22"

[env]
_.python.venv = { path = ".venv", create = true }

[tasks]
install = "uv sync"
dev = "uv run {dev_command}"
test = "uv run pytest"
lint = "uvx ruff check ."
format = "uvx ruff format ."
````
