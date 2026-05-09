# Search Strategies

Tool inventory and priority order for research agents. Load this file before running the first search.

## Time awareness

Run `date +"%Y-%m-%d"` before the first search to ground yourself in the current date. Include the current year in queries — e.g., `best python ORM 2026`, not `best python ORM`.

Primary focus: sources from the last 6 months. Reach further back only when the question is historical, recent coverage is thin, or the older source is canonical (e.g., a foundational paper or an official spec). Flag older sources with their date so the reader can judge.

Set `recency: "latest"` on `nova_web_grounding` calls by default. Use date qualifiers on `brave_web_search` queries when the topic is time-sensitive.

## Tool inventory

| Tool                                                                    | Best for                                                          | Use when                                                                            |
| ----------------------------------------------------------------------- | ----------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| `web_search_exa`                                                        | Comparative content, expert analyses, "best of" lists, benchmarks | You're comparing options, exploring a category, or hunting for thoughtful long-form |
| `brave_web_search`                                                      | Recent news, release announcements, community discussions         | You need broad web coverage or very recent information                              |
| `tavily_search` + `tavily_extract`                                      | In-depth research where full page content matters                 | You need to analyze a source deeply or extract structured data                      |
| `tavily_research`                                                       | Extended investigation on complex multi-part topics               | The scope is broad and exploratory                                                  |
| Context7 (`resolve-library-id` → `query-docs`)                          | Official API docs, type signatures, code examples                 | You're writing code against a specific library. First choice for library work.      |
| DeepWiki (`read_wiki_structure` → `read_wiki_contents`, `ask_question`) | GitHub repo architecture, community health, code patterns         | You're evaluating a project's structure or checking repo activity                   |
| `nova_web_grounding`                                                    | Cited quick facts with source URLs                                | You need a narrow, specific answer — version numbers, dates, specific statistics    |
| AWS Knowledge (`search_documentation` → `read_documentation`)           | AWS service selection, architecture patterns, CDK/IaC             | Any AWS-specific question. First choice before falling back to web search.          |
| `WebFetch`                                                              | Reading a specific URL found via search                           | A search result returned a promising URL worth full-reading                         |

## Priority by research type

| Research type    | Priority order                           |
| ---------------- | ---------------------------------------- |
| General topic    | exa → brave → tavily → WebFetch → nova   |
| Code / library   | context7 → deepwiki → exa → nova → brave |
| AWS-specific     | awsknowledge → brave → nova              |
| Market / product | brave → exa → tavily → nova              |

Move to the next tool when the current one lacks sufficient information. Don't run everything — two or three well-chosen sources usually beat a sprawl.

## Quality guidelines

- Prefer primary sources: official docs, release notes, GitHub repos, academic papers. Blog posts are useful for synthesis but shouldn't carry a factual claim alone.
- Cross-reference: any factual claim goes in with at least two independent sources when possible.
- Record the URL, title, and publication date for every citation. The write protocol requires inline URLs with dates — keep that rhythm.
- Be specific: data points, version numbers, dates, benchmarks over vague paraphrase.
- Note confidence: distinguish verified fact vs. likely true vs. uncertain. The synthesis step uses these signals.
- Acknowledge gaps: say so explicitly when a fact isn't findable. Don't fill the hole with a guess.
