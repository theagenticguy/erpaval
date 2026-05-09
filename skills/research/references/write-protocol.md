# Write Protocol

This file is the canonical write-protocol block. The orchestrator copies it verbatim into every research agent's prompt and into every agent-file skeleton. A single source of truth keeps all agents on the same discipline.

---

<write_protocol>
Your output file is the single source of truth for what you've learned. Edit it after every search or fetch, before starting the next one. Partial findings written to disk survive 403 errors, timeouts, and early termination; findings held in working memory do not.

The rhythm is: one search or fetch → edit the file with what you found → next search. One exchange at a time.

Work through your sections in numbered order. For each section:

1. Run one search or fetch.
2. Edit the file under that section with what you learned — specific facts, quoted evidence, inline source URLs.
3. If the section needs more depth, run another search and edit again.
4. Move to the next section only after the current one has real content.

If a fetch returns 403, 404, or similar: write what you already have to the file, then try an alternative URL, then edit again with the new finding. Keep the file ahead of your working memory at all times.

**Cite every quantitative claim inline** with a Markdown link that includes the publication date when the source shows one: `[Source Name, 2026-04-15](https://url.com)`. Keep sources next to the claims they support — a trailing Sources section gets built later at synthesis time.

Order citations newest-first when you list more than one for the same point. Recency matters for a research brief; the reader weights the top-listed source most heavily.

Recency scope: concentrate on sources from the last 6 months. Reach further back only when the question is historical, recent literature is thin, or the older source is canonical (e.g., a foundational paper or an official spec). Flag older sources with their date so the reader can judge.

When every section has real content, change the `Status:` line at the top of the file from `IN PROGRESS` to `COMPLETE`.
</write_protocol>
