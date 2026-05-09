# Search Strategies

Guidelines for how researcher agents should use available search tools to gather current, accurate information about open-source technologies.

## Tool Priority Order

Use tools in this order. Move to the next tool when the current one doesn't have sufficient information.

### 1. Context7 (First Choice for Libraries)

- **Best for**: Official API docs, code examples, getting started guides
- **Use when**: You know the exact library name and need usage details
- **Pattern**: Resolve library ID first, then query docs
- **Limitation**: Only covers libraries in its index

### 2. DeepWiki (First Choice for GitHub Repos)

- **Best for**: Understanding repo architecture, contribution patterns, community health
- **Use when**: Evaluating a specific GitHub project's structure and activity
- **Pattern**: Read wiki structure first, then drill into relevant sections
- **Limitation**: Only GitHub repos, may lag behind very recent changes

### 3. Exa (Best for Comparative Research)

- **Best for**: Finding blog posts, comparisons, benchmarks, "best of" lists
- **Use when**: Comparing multiple tools in a category
- **Pattern**: Use `web_search_exa` with comparative queries
- **Strength**: Excellent at finding high-quality technical content

### 4. Brave Search (General Web Search)

- **Best for**: Recent news, release announcements, community discussions
- **Use when**: Need broad web coverage or very recent information
- **Pattern**: Use `brave_web_search` with specific queries

### 5. Tavily (Research-Oriented Search)

- **Best for**: In-depth research with extracted content
- **Use when**: Need to deeply analyze search results
- **Pattern**: Use `tavily_search` for discovery, `tavily_extract` for content

### 6. Nova Web Search (Live Web Grounding with Citations)

- **Best for**: Quick, focused fact-checking with cited sources. Getting current data points (latest version numbers, release dates, benchmark results).
- **Use when**: You need a specific, narrow answer with source URLs — not broad discovery.
- **Tool**: `nova_web_grounding`
- **Pattern**: Each call is a single focused search. For broad topics, make **multiple parallel calls** with different specific queries rather than one large request.
- **Parameters**:
  - `topic`: Specific, focused question (narrow queries work best)
  - `num_sources`: 1-5 (default 3)
  - `recency`: `"latest"` (last month), `"recent"` (last year), `"any"` (all time)
  - `output_style`: `"summary"` (2-3 paragraphs), `"detailed"` (full analysis), `"bullets"` (key points)
- **Example queries**:
  - `topic: "FastAPI latest stable release version and date", recency: "latest"`
  - `topic: "Litestar vs FastAPI performance benchmarks 2025", recency: "recent", output_style: "bullets"`
- **Strength**: Returns cited answers — every claim has a source URL. Great for health checks.

### 7. AWS Knowledge (AWS Best Practices and Architecture)

- **Best for**: AWS service selection, architecture patterns, CDK/IaC guidance, AWS best practices
- **Use when**: Evaluating AWS services, choosing between AWS options, validating architecture decisions
- **Tool**: `awsknowledge` MCP server
- **Key topics to query**:
  - `general` — Architecture decisions, service comparisons, "what's the right AWS service for X?"
  - `amplify_docs` — Static sites, SPAs, framework-specific deployment (React, Next.js, Vue)
  - `cdk_docs` — CDK patterns, construct library usage
  - `cdk_constructs` — Specific CDK construct references and examples
- **Pattern**: Consult awsknowledge first for any AWS-related decision before falling back to web search. It has authoritative, curated AWS guidance.
- **Limitation**: AWS services only — not useful for evaluating non-AWS alternatives

## Query Templates by Domain

### Finding Top Libraries in a Category

```text
"best {category} libraries {language} {current_year}"
"top 10 {category} {language} {current_year}"
"{language} {category} comparison {current_year}"
"awesome-{category} github"
```

### Evaluating a Specific Library

```text
"{library_name} production review {current_year}"
"{library_name} vs {competitor} benchmark"
"{library_name} github stars contributors activity"
"{library_name} breaking changes migration"
```

### Checking Health and Activity

```text
"{library_name} latest release"
"{library_name} github archived deprecated"
"{library_name} security vulnerability CVE"
"{library_name} roadmap future plans"
```

### AWS Service Evaluation

```text
"AWS {service} best practices {current_year}"
"AWS {service} vs {alternative} when to use"
"AWS {service} pricing calculator {workload_type}"
"AWS {service} limitations gotchas"
```

### Framework Comparison

```text
"{framework_a} vs {framework_b} performance benchmark {current_year}"
"{framework_a} vs {framework_b} developer experience"
"{framework_a} production case study"
"migrating from {framework_a} to {framework_b}"
```

## Search Workflow Per Category

### For 🔬 RESEARCH Categories (Full Comparison)

1. **Discovery**: Search for top candidates in the category (2-3 queries via exa/brave)
2. **Shortlist**: Identify 3-5 viable candidates from results
3. **Deep Dive**: For each candidate, check docs (context7) and repo health (deepwiki)
4. **AWS decisions**: If comparing AWS services, query awsknowledge first for authoritative guidance
5. **Compare**: Find head-to-head comparisons and benchmarks (exa/brave/nova)
6. **Health Check**: Verify each candidate against `health-check-criteria.md` — use nova_web_grounding for quick version/release date lookups
7. **Synthesize**: Build comparison matrix with weighted criteria

### For Opinionated Defaults (Health Check Only)

1. **Verify Active**: Check latest release date and commit activity (deepwiki or nova_web_grounding with `recency: "latest"`)
2. **Check Issues**: Search for critical CVEs or deprecation notices (brave/nova)
3. **Confirm Recommendation**: Ensure still the clear category leader
4. **Flag if Changed**: If health check fails, escalate to full research

### For User-Locked Choices (Validation Only)

1. **Compatibility Check**: Verify it works with other stack choices
2. **Version Check**: Confirm latest stable version (nova_web_grounding is fast for this)
3. **Note Constraints**: Document any limitations for other choices

### For AWS Service Categories

1. **Consult awsknowledge first**: Query with the architecture decision or service comparison
2. **Supplement with web search**: Use nova/brave/exa for pricing updates, recent announcements, community experiences
3. **Cross-reference**: Validate awsknowledge recommendations against real-world production reports

## Search Quality Guidelines

- **Prefer primary sources**: Official docs, GitHub repos, release notes over blog posts
- **Check dates**: Ignore results older than 18 months for fast-moving categories
- **Cross-reference**: Don't rely on a single source for any claim
- **Stars aren't everything**: A 500-star focused library may be better than a 10k-star abandoned one
- **Benchmark skepticism**: Note benchmark methodology and whether it's from a neutral source
- **License awareness**: Always check license compatibility (prefer MIT, Apache 2.0, BSD)
