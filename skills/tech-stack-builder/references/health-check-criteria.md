# Health Check Criteria

Every technology recommendation must include a health assessment. This file defines the classification system and how to gather the data.

## Health Classifications

### ✅ HEALTHY

All of the following must be true:

- **Release recency**: Stable release within the last 6 months
- **Commit activity**: Active commits in the last 3 months (not just dependency bumps)
- **Not archived**: GitHub repo is not archived or marked read-only
- **No critical CVEs**: No unpatched critical or high-severity vulnerabilities
- **Community**: 1,000+ GitHub stars (for libraries) or strong corporate backing
- **Maintenance**: 2+ active maintainers OR corporate sponsor with dedicated team
- **Documentation**: Up-to-date docs covering current version

### ⚠️ CAUTION

One or more of the following:

- **Release gap**: Last stable release 6-12 months ago
- **Single maintainer**: Bus factor of 1 with no corporate backing
- **Slowing activity**: Commit frequency declining over last 6 months
- **Open security issues**: Known vulnerabilities with patches pending
- **Version gap**: Major version behind with migration path unclear
- **Competing successor**: A clear successor project is gaining traction

### 🚨 WARNING

One or more of the following:

- **Stale**: Last release more than 12 months ago
- **Archived**: Repository is archived or marked as unmaintained
- **EOL announced**: End-of-life or deprecation officially announced
- **Unresolved CVEs**: Critical vulnerabilities with no patch timeline
- **Abandoned**: No maintainer response to issues/PRs for 6+ months
- **License change**: Recent license change to non-permissive terms
- **Fork dominance**: Community has moved to a fork

## Data Collection Checklist

For each technology, gather:

| Data Point              | Where to Find                                      |
| ----------------------- | -------------------------------------------------- |
| Latest release date     | GitHub releases page, npm/PyPI                     |
| Last commit date        | GitHub repo, DeepWiki                              |
| Open/closed issue ratio | GitHub issues tab                                  |
| Number of maintainers   | GitHub contributors page (filter to last 6mo)      |
| GitHub stars            | GitHub repo                                        |
| Known CVEs              | `{library} CVE` search, GitHub security advisories |
| License                 | GitHub repo, package registry                      |
| Download trends         | npm trends, PyPI stats, crates.io                  |
| Breaking changes        | CHANGELOG, migration guides                        |
| Corporate backing       | About page, sponsors, governance docs              |

## Health Check Output Format

For each technology in the recommendation, include:

```markdown
### {Technology Name} — {Health Status Emoji} {HEALTHY|CAUTION|WARNING}

- **Version**: {latest_stable_version} (released {date})
- **Activity**: {commits_last_3mo} commits in last 3 months
- **Maintainers**: {count} active ({names_or_org})
- **Stars**: {count} | **License**: {license}
- **Issues**: {open_count} open / {closed_count} closed
- **Notes**: {any relevant flags, e.g. "Major v4 rewrite in progress"}
```

## Escalation Rules

- If an **opinionated default** scores CAUTION: include a note but keep the recommendation
- If an **opinionated default** scores WARNING: escalate to full research, find alternatives
- If a **user-locked choice** scores WARNING: flag prominently in the report with migration suggestions
- If ALL candidates in a category score CAUTION or worse: note the ecosystem maturity concern in the ADR

## Health Trends to Watch

Flag these patterns even if current health is GREEN:

- **Governance drama**: Public maintainer conflicts, CoC disputes
- **Corporate acquisition**: Recent acquisition of the backing company
- **Rewrite in progress**: Major version rewrite that may break ecosystem
- **Funding concerns**: Open Collective/GitHub Sponsors declining
- **AI-driven churn**: Tool being rapidly replaced by AI-native alternatives
