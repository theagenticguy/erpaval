---
title: Kiro subagent dispatch — `subagent` tool vs `/spawn` slash command (and the `summary` return-path trap)
track: knowledge
category: best-practices
module: .kiro/agents/, ERPAVal SKILL.md
component: Kiro CLI subagent runtime
severity: info
tags: [kiro, kiro-cli, subagent, spawn, summary-tool, erpaval, methodology, orchestration]
applies_when:
  - Building or invoking a Kiro CLI orchestrator agent that delegates to subagents
  - Writing or revising a methodology that uses Kiro subagents (ERPAVal, multi-agent skills, etc.)
  - Diagnosing "No result" / empty subagent return in a parent session
pattern: |
  Kiro provides two distinct subagent-shaped primitives that are NOT
  interchangeable:

  ### 1. The `subagent` built-in tool — agent-driven delegation
  - Triggered when the main agent decides to delegate, typically via NL:
    `> Use the X agent to do Y`
  - Bounded task within the parent's task graph (DAG, max 4 parallel)
  - Subagent's only return path is the **built-in `summary` tool** (auto-
    added to every subagent — do not declare it in the agent's `tools`)
  - `is_interactive: false`. If a tool needs approval and isn't pre-allowed,
    the subagent **fails fast** (no hang). Mitigation: subagent config has
    `allowedTools: ["*"]` (or specific globs); parent has
    `toolsSettings.subagent.trustedAgents: [...]` to skip approval on
    dispatch.
  - Subagent session records the parent session ID. Traceable via
    `kiro-cli chat --resume-id <id>`.

  ### 2. The `/spawn` slash command — user-driven parallel session
  - Started by the *user* in the chat, e.g.
    `> /spawn --name analysis Review failing tests`
  - Fresh long-running session that can be returned to via the **crew
    monitor** (Ctrl+G) or `/chat resume`
  - Quote from the docs: *"Unlike subagents, which are spawned by the
    main agent to delegate focused work within a task graph, `/spawn` is
    a user-driven command that starts a fresh long-running session you
    can return to later."*
  - **Not for orchestrator-driven delegation.**

  ### Failure mode: silent "No result"
  Symptoms: a subagent dispatch returns `Pipeline completed ... No result`
  or an empty summary, even though the configs look correct.

  Common causes:
  1. **Subagent finished without calling `summary`.** The summary tool is
     the only return mechanism. If the subagent wrote all output to disk
     (a file, a packet) and exited without summary-calling, the parent
     gets nothing. Always include in the subagent prompt: "Final step:
     call the built-in `summary` tool with a 1-2 paragraph result; return
     nothing else."
  2. **Subagent fail-fast on an approval prompt.** Look for missing tools
     in the subagent's `allowedTools`. Fix: `allowedTools: ["*"]` on
     trusted internal subagents, or add the specific tool names.
  3. **Parent didn't list the subagent in `availableAgents` / `trustedAgents`.**
     Without `availableAgents`, the spawn is rejected. Without
     `trustedAgents`, the user is prompted to approve every spawn — and
     in headless/pipeline contexts this surfaces as an empty result.
  4. **Pipeline-shape vs NL-shape difference.** Aggregating subagents via
     a structured pipeline tool (e.g., the MCP-style `subagent` invocation
     with `stages`) may serialize results differently than native NL
     dispatch. NL dispatch is the canonical shape; reserve the pipeline
     form for genuine DAG fan-out where stage results need to be
     correlated programmatically.

  ### Permission contract — minimum viable orchestrator config
  ```json
  {
    "tools": ["...", "subagent"],
    "allowedTools": ["*"],
    "toolsSettings": {
      "subagent": {
        "availableAgents": ["explorer", "researcher", "act-*"],
        "trustedAgents":   ["explorer", "researcher", "act-*"]
      }
    }
  }
  ```

  And on each subagent:
  ```json
  {
    "tools": ["fs_read", "grep", "glob", "execute_bash", "..."],
    "allowedTools": ["*"]
  }
  ```

  ### ERPAVal SKILL.md corrections surfaced by reading the docs
  1. Replace `/spawn --name <id> "..."` in the orchestrator runbook with
     NL invocation: `> Use the erpaval-explorer agent to <task>`. The
     `subagent` tool is what fires under the hood; the pipeline-style
     `subagent` invocation is a niche escape hatch, not the default.
  2. Emphasize "subagent must end with a `summary` call" in every
     subagent prompt template — including the per-task packet skeleton.
  3. Use **Ctrl+G crew monitor** as the primary observability tool for
     interactive sessions; keep `wc -l` packet polling as the
     non-interactive / headless fallback.
  4. Note that subagent sessions persist with parent ID; failed delegations
     can be inspected via `kiro-cli chat --resume-id <subagent-session-id>`.
example_files:
  - /Users/lalsaado/.kiro/agents/erpaval-orchestrator.json
  - /Users/lalsaado/.kiro/agents/erpaval-explorer.json
  - /Users/lalsaado/.kiro/agents/erpaval-researcher.json
---

# Why this matters

Kiro's subagent semantics differ from Claude Code's in three ways that
ERPAVal currently glosses over:
- `/spawn` is user-driven (not the agent's delegation primitive)
- Subagents fail-fast instead of hanging on approval prompts
- The `summary` tool is the ONLY return path

Getting any of these wrong produces silent-empty subagent dispatches —
which, mid-session, looks like "the subagent ran but did nothing."
Methodology that depends on subagent fan-out (Wave 2-3 of Act, L2 +
L3 validation) is broken at the contract level until these are
addressed.

# Example

Wrong (per docs):
```
/spawn --name validate-quality "Code quality review per validation-playbook.md..."
```

Right (per docs):
```
> Use the erpaval-explorer agent to do an L2 code-quality review per
  validation-playbook.md. Read all files under blog/, apply the L2
  checklist, and call the built-in `summary` tool with the Markdown
  report as your final step.
```

Verification when a subagent returns empty:
1. Confirm the subagent's prompt explicitly demanded a `summary` call
2. Check parent's `trustedAgents` includes the subagent name
3. Check subagent's `allowedTools` covers everything the task needs
4. Open Ctrl+G monitor mid-run to see if the subagent is actually doing
   work or fail-fasting on a missing tool
5. Find the subagent session via `kiro-cli chat --list-sessions` and
   inspect with `--resume-id` to see what actually happened
