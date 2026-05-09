# Product strategy work log — {{ role }}

**Status:** IN PROGRESS
**Role:** {{ cpo | cso | vp-design | rumelt-architect | wardley-cartographer | pr-faq-discovery | minto-pyramid-builder | strategy-synthesizer | strategy-critic }}
**Slug:** {{ slug }}
**Working directory:** `product-strategy/{{ slug }}/`
**Your output file:** `product-strategy/{{ slug }}/{{ framing.md | framing-cso.md | framing-design.md | rumelt-packet.md | wardley-packet.md | pr-faq-packet.md | minto-outline.md | strategy-memo.md | review-strategy.md }}`

<write_protocol>
Your output file is the single source of truth for your work. Edit it after every meaningful step, before starting the next one. Partial progress written to disk survives timeouts, SendMessage interrupts, and orchestrator context pressure; state held in working memory does not.

The rhythm is: one unit of thought → edit the file with the outcome → next unit. One decision at a time.

Work through your sections in numbered order. For each section:

1. Think through the decision or draft. Read adjacent files, run a web search, or consult the framework reference when the answer is not in your head.
2. Edit the file under that section — the claim you are making, the evidence behind it, the tradeoff accepted. Cite sources inline.
3. If the section needs more depth, do another unit of thought and edit again.
4. Move to the next section only after the current one has real content.

Name the tradeoff on every non-obvious call. "Chose diagnosis X over Y because X names the actual bottleneck rather than the symptom" beats "went with X." The critic reads these attributions when composing the final memo.

Cite adjacent material inline when a decision depends on source evidence — framework file + heading, research synthesis line number, or external URL. Reviewers read the citations to verify your reasoning.

When every section has real content, change the `Status:` line at the top of the file from `IN PROGRESS` to `COMPLETE`.
</write_protocol>

## 1. Objective

{{ one-sentence objective — what this role is producing for this run }}

## 2. Scope

- **Input**: {{ framing.md, specific packets, prior memos — whatever this role reads }}
- **Output**: {{ exact file path this role writes to }}
- **Role reference**: the matching file in `${CLAUDE_PLUGIN_ROOT}/skills/product-strategy/references/roles/`

Sections to complete in the output file (varies by role — see the role reference for the full list):

- {{ section 1 }}
- {{ section 2 }}

Out of scope:

- {{ what this role should NOT do — e.g., synthesizer does not re-run frameworks, critic does not rewrite the memo }}

## 3. Inputs

Files to read in full before writing:

- `product-strategy/{{ slug }}/framing.md` (always, once it exists)
- {{ packet files this role depends on, per the role reference }}

Reference material:

- `${CLAUDE_PLUGIN_ROOT}/skills/product-strategy/references/frameworks/INDEX.md` — framework routing guide (decision table + cross-framework composition). Per-framework files live in the same `frameworks/` directory — `rumelt-kernel.md`, `wardley-maps.md`, `minto-pyramid.md`, `working-backwards.md`.
- The matching file under `${CLAUDE_PLUGIN_ROOT}/skills/product-strategy/references/roles/` (cpo.md, cso.md, vp-design.md, rumelt-architect.md, wardley-cartographer.md, pr-faq-discovery.md, minto-pyramid-builder.md, strategy-synthesizer.md, strategy-critic.md).

Load progressively — read `frameworks/INDEX.md` first, pull the specific per-framework file(s) only when the section you are writing needs them.

## 4. Success criteria

Baseline:

- Output file populated with real content in every required section.
- `Status:` flipped from `IN PROGRESS` to `COMPLETE` when done.
- Every non-obvious claim cites its source inline.
- Write protocol followed — edit after every section, not at the end.

Role-specific (see the role reference for the full list):

- **cpo / cso / vp-design**: framing challenge is specific, audience is specific, framework fan-out plan is committed.
- **rumelt-architect**: three-part kernel plus the Crux, four bad-strategy checks passed.
- **wardley-cartographer**: value chain, evolution stages with cited evidence, gameplay moves, build-vs-buy read.
- **pr-faq-discovery**: five customer questions answered specifically, evidence gaps flagged.
- **minto-pyramid-builder**: SCQA at top, 3–5 MECE supporting groups, cross-reference to source packets.
- **strategy-synthesizer**: memo reads top-down, attribution inline, convergence notes name convergence and divergence.
- **strategy-critic**: every rubric dimension graded with specific evidence, revision recommendations actionable.

## 5. Anti-goals

- Don't re-run a framework that has already produced a packet — compose from what's on disk.
- Don't produce generic advice. Every claim is specific and attributed.
- Don't leave empty sections. Write the finding or note explicitly "not applicable because X."
- Don't rewrite the memo from a reviewer role (critic). Reviewers review; the synthesizer applies.
- Don't silently reshape scope. If you disagree with the ask, note it in the work log and continue with what was asked.

---

## Work log

{{ the agent fills this per the write protocol — one entry per meaningful action }}

### {{ timestamp-or-step }}: {{ what was done }}

{{ what changed, which section of the output file was edited, any source consulted, any tradeoff named }}

---

## Validation

### Self-checks

- [ ] Every required section of the output file has real content
- [ ] Every non-obvious claim has an inline citation
- [ ] Tradeoffs named on non-obvious calls
- [ ] `Status:` flipped to `COMPLETE`

---

## Summary

{{ one paragraph — what this run produced, where it lives, and any decisions worth calling out for the next role to see. Example: "chose commodity positioning for the eval harness component over custom-build because three commercial providers (cited) now cover the feature surface we'd build — the synthesizer should lean on this when composing the build-vs-buy section of the memo." }}
