# Write Protocol

Canonical write-protocol block. The orchestrator copies it verbatim into every Act-phase context packet and into every per-task skeleton. One source of truth keeps all subagents on the same discipline.

Adapted from `skills/research/references/write-protocol.md` for code-writing work: the rhythm is "read → edit code → run check → edit packet with outcome", not "search → edit brief".

---

<write_protocol>
Your task packet file is the single source of truth for what you've done, decided, and verified. Edit it after every meaningful step, before starting the next one. Partial progress written to disk survives subagent timeouts, mid-turn interrupts, and orchestrator context pressure; state held in working memory does not.

The rhythm is: one action → edit the packet with the outcome → next action. One exchange at a time.

Work through your sections in numbered order. For each section:

1. Do one unit of work — read a file, write a code change, run a check, capture a finding.
2. Edit your packet file under that section with what happened — the exact files touched, the check output, the decision made, any surprises.
3. If the section needs more depth, do another unit and edit again.
4. Move to the next section only after the current one has real content.

If a check fails (lint, type, test, semgrep): write the failure to the packet, then fix, then edit again with the fix. Keep the file ahead of your working memory at all times.

**Cite every code change with file:line.** "Added `verify_pkce` at `src/auth/oauth_service.py:142-168`" beats "Added the PKCE helper." Citations let the orchestrator and future reviewers trace every line back to the task.

When every section has real content and every success criterion is checked off, change the `status:` field in the packet's YAML frontmatter from `IN_PROGRESS` to `COMPLETE`, then call the built-in `summary` tool with a 1-2 paragraph result.
</write_protocol>
