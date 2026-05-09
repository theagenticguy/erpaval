# /build-stack — Tech Stack Research Orchestrator

You are orchestrating a tech stack research workflow. You will guide the user through requirements intake, launch parallel research agents, synthesize results, and produce structured outputs.

## Reference Files

Load these for context:

- `${CLAUDE_PLUGIN_ROOT}/skills/tech-stack-builder/references/opinionated-defaults.md`
- `${CLAUDE_PLUGIN_ROOT}/skills/tech-stack-builder/references/output-templates.md`
- `${CLAUDE_PLUGIN_ROOT}/skills/tech-stack-builder/references/health-check-criteria.md`

## Templates

- `${CLAUDE_PLUGIN_ROOT}/skills/tech-stack-builder/templates/stack-report.md`
- `${CLAUDE_PLUGIN_ROOT}/skills/tech-stack-builder/templates/adr-template.md`
- `${CLAUDE_PLUGIN_ROOT}/skills/tech-stack-builder/templates/comparison-matrix.md`

---

## Phase tracking

Before Phase 1, create 5 todo items — Requirements intake, Parallel research, Synthesis, Output generation, Scaffolding (optional). During Phase 2, additionally `TaskCreate` one item per domain researcher launched (backend / frontend / infra / aws / devtools, as applicable) and flip each to `completed` when its domain output returns. Flip phase items to `in_progress` on entry, `completed` on exit.

---

## Phase 1: Requirements Intake

First, parse any provided context from `$ARGUMENTS`: `{{ context }}`

If context was provided, extract what you can and only ask about missing pieces. If no context was provided, ask all questions.

Use `AskUserQuestion` to gather the following requirements interactively. Group related questions together (max 4 per call). Be conversational, not robotic.

### Required Information

1. **Application Type**: What are you building?
   - Options: API service, Full-stack web app, CLI tool, Data pipeline, Mobile backend, Library/SDK, Other

2. **Stack Layers**: Which layers do you need?
   - Options: Backend, Frontend, Infrastructure, AWS Services, All of the above
   - (Multi-select)

3. **Primary Language(s)**: What language(s) will you use?
   - Options: Python, TypeScript, Go, Rust, Other
   - (Multi-select)

4. **Deployment Target**: Where will this run?
   - Options: AWS, GCP, Azure, Self-hosted, Vercel/Netlify, Other

5. **Compute Model**: How should it run?
   - Options: Containers (ECS/Docker), Serverless (Lambda), VMs (EC2), Hybrid, Not sure yet

6. **Expected Scale**: What's the expected load?
   - Options: Low (< 100 req/s), Medium (100-1000 req/s), High (1000-10000 req/s), Very High (10000+ req/s)

7. **Team Size**: How many engineers?
   - Options: Solo, Small (2-5), Medium (6-15), Large (15+)

8. **Must-Haves**: Any non-negotiable requirements? (Free text)
   - e.g., "Must support WebSockets", "Need GraphQL", "Real-time updates required"

9. **Already Decided**: Any technologies already locked in? (Free text)
   - e.g., "Using PostgreSQL", "React is non-negotiable", "Already on ECS"

10. **Avoid List**: Anything explicitly off the table? (Free text)
    - e.g., "No Kubernetes", "No MongoDB", "No Angular"

### After Intake

Summarize the normalized requirements back to the user in a clean table format and ask for confirmation before proceeding. Example:

```text
| Requirement | Value |
|-------------|-------|
| App Type | API service |
| Layers | Backend, Infrastructure, AWS |
| Language | Python |
| Deployment | AWS |
| Compute | Containers (ECS) |
| Scale | Medium (100-1000 req/s) |
| Team Size | Small (3 engineers) |
| Must-Haves | WebSocket support, async task processing |
| Locked In | PostgreSQL, GitHub for CI/CD |
| Avoid | Kubernetes, MongoDB |
```

Wait for user confirmation before moving to Phase 2.

---

## Phase 2: Parallel Research

Based on the confirmed requirements, determine which agents to launch.

### Agent Selection Logic

All research is performed by the `researcher` agent, launched once per applicable domain:

| Domain     | Launch If                                                                             |
| ---------- | ------------------------------------------------------------------------------------- |
| `backend`  | "Backend" in layers OR app type is API/web app                                        |
| `frontend` | "Frontend" in layers AND app type is NOT "API service" / "CLI tool" / "Data pipeline" |
| `infra`    | Always (every project needs infra)                                                    |
| `aws`      | Deployment target is "AWS"                                                            |
| `devtools` | Always (every project needs dev tools)                                                |

### Launching Agents

**CRITICAL**: Launch ALL applicable domain instances in a SINGLE message using multiple `Agent` tool calls. This runs them in parallel.

For each domain, use the `Agent` tool with:

- `subagent_type`: `researcher` (the plugin's dedicated researcher agent — already pinned to Opus)
- `description`: short label (e.g., `"Backend stack research"`)
- `run_in_background`: `true` when spawning 2+ domains so they run in parallel

**Prompt template for each domain instance:**

```text
You are a tech stack researcher specializing in the {domain} domain.

Read your domain configuration from: ${CLAUDE_PLUGIN_ROOT}/skills/tech-stack-builder/references/domains/{domain}.md

Also read these reference files:
- ${CLAUDE_PLUGIN_ROOT}/skills/tech-stack-builder/references/opinionated-defaults.md
- ${CLAUDE_PLUGIN_ROOT}/skills/tech-stack-builder/references/search-strategies.md
- ${CLAUDE_PLUGIN_ROOT}/skills/tech-stack-builder/references/health-check-criteria.md

## Project Requirements

{paste the requirements table here}

## Constraints
- Locked-in decisions: {list}
- Avoid list: {list}
- Team size: {size} — adjust learning curve expectations accordingly
- Scale target: {scale} — factor into performance evaluations

## Your Task

Research your domain categories following both your base agent instructions and domain config. You have 7 search tools — use them strategically:

- **context7**: Library API docs and code examples (resolve library ID first, then query)
- **deepwiki**: GitHub repo health, architecture, community (read structure first, then sections)
- **exa**: Comparative research, benchmarks, "best of" lists (`web_search_exa`)
- **brave-search**: Recent news, release announcements, broad web (`brave_web_search`)
- **tavily**: In-depth research with content extraction (`tavily_search`, `tavily_extract`)
- **nova-web-search**: Quick cited fact lookups — latest versions, release dates, benchmarks (`nova_web_grounding` with `recency: "latest"` and `output_style: "bullets"`)
- **awsknowledge**: AWS service selection, architecture patterns, CDK guidance (topics: `general`, `amplify_docs`, `cdk_docs`, `cdk_constructs`)

Produce your output in the exact format specified in your agent and domain instructions. Include comparison matrices for all RESEARCH categories, health checks for all recommendations, and domain-specific artifacts.
```

---

## Phase 3: Synthesis

After all agents return their results:

### 3.1 Collect and Organize

Gather all agent outputs and organize by layer:

- Backend recommendations
- Frontend recommendations (if applicable)
- Infrastructure recommendations
- AWS service recommendations (if applicable)
- Developer tooling recommendations

### 3.2 Resolve Conflicts

If agents recommend conflicting technologies, resolve using this priority order:

1. **User constraints** — Must-haves and locked-in decisions always win
2. **Avoid list** — Excluded technologies are never recommended
3. **Ecosystem coherence** — Technologies that integrate natively with each other
4. **Health status** — Prefer HEALTHY over CAUTION over WARNING
5. **Team familiarity** — Prefer technologies the team already knows (based on team size and context)

If a conflict can't be resolved automatically (e.g., two equally valid approaches), present the options to the user via `AskUserQuestion` for tiebreaking.

### 3.3 Cross-Cutting Validation

Verify:

- [ ] All recommended technologies work together (no incompatibilities)
- [ ] Deployment model is consistent across layers (e.g., if containers, everything containerizes well)
- [ ] Language versions are consistent (e.g., Python 3.12 throughout)
- [ ] No license conflicts (all permissive licenses)
- [ ] Observability stack covers all layers
- [ ] Auth approach is consistent between backend and frontend

### 3.4 Build Unified Stack Table

Create a single table with ALL recommended technologies across all layers:

`````markdown
| Layer   | Technology | Version | Role          | Health     |
| ------- | ---------- | ------- | ------------- | ---------- |
| Backend | FastAPI    | 0.115   | Web framework | ✅ HEALTHY |
| ...     | ...        | ...     | ...           | ...        |

````text
---

## Phase 4: Output Generation

Generate all artifacts in the user's current working directory.

### 4.1 Stack Report

Write `tech-stack-report.md` using the template from `${CLAUDE_PLUGIN_ROOT}/skills/tech-stack-builder/templates/stack-report.md`.

Fill in all `[FILL]` markers with:

- Executive summary synthesized from all agent outputs
- Requirements recap from Phase 1
- Unified stack table from Phase 3
- Per-layer analysis from agent outputs
- All comparison matrices from agents that did full research
- Mermaid architecture diagram showing all components and data flows
- Consolidated health report
- Trade-offs and risks
- Dependency manifests

### 4.2 Dependency Files

Write applicable dependency snippets:

**If Python in stack**: Write a `pyproject.toml` snippet section in the report with all Python dependencies grouped by purpose.

**If JS/TS in stack**: Write a `package.json` snippet section in the report with all JS/TS dependencies grouped by purpose.

**Always**: Write a `mise.toml` snippet with tool versions and project tasks.

### 4.3 ADR Files

Create an `adr/` directory and write 3-5 ADR files using the template from `${CLAUDE_PLUGIN_ROOT}/skills/tech-stack-builder/templates/adr-template.md`.

Write one ADR per significant decision. Prioritize decisions where:

- Multiple strong candidates existed (non-obvious choice)
- The choice has significant long-term implications
- The choice constrains future options

Name files: `adr/001-{topic}.md`, `adr/002-{topic}.md`, etc.

### 4.4 Architecture Diagram

Include a Mermaid diagram in the stack report showing:

- All major components from the unified stack
- Data flow arrows with labels
- Subgraphs for logical layers (Client, API, Data, Infrastructure)
- External service integrations (AWS services, third-party APIs)

### 4.5 Final Summary

After writing all files, present a summary to the user:

```markdown
## Stack Research Complete

### Files Generated

- `tech-stack-report.md` — Full analysis with comparison matrices and architecture diagram
- `adr/001-{topic}.md` — {brief description}
- `adr/002-{topic}.md` — {brief description}
- ... (list all ADR files)

### Recommended Stack (Quick View)

{Unified stack table}

### Next Steps

1. Review the full report and ADRs
2. Copy dependency snippets into your project
3. Use the mise.toml to set up your development environment
4. Revisit any ⚠️ CAUTION items in the health report
````
`````

---

## Phase 5: Project Scaffolding (Optional)

After presenting the stack report, ask the user:

> "Would you like me to scaffold the project with these tools pre-configured? I can generate all config files (dependency manifests, linter configs, mise.toml, lefthook.yml, CI workflow, Dockerfile) ready to run."

If yes:

1. Load the appropriate scaffold template(s) from `${CLAUDE_PLUGIN_ROOT}/skills/tech-stack-builder/templates/scaffold/{language}.md`
2. Load `${CLAUDE_PLUGIN_ROOT}/skills/tech-stack-builder/references/stacks/shared/security.md` for security tool config
3. Generate actual project files (not snippets) into the user's working directory, adapting the templates:
   - Replace `myapp` with the project name from Phase 1
   - Adjust dependency lists based on the researched stack
   - Include only the CI/security tools recommended in the report
4. Run setup commands: `mise install && lefthook install`

This bridges "here's what you should use" to "here's your ready-to-run project."
