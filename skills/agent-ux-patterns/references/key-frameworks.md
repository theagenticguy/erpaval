# Key Frameworks

Reference material for established frameworks used in design thinking sessions.

## Twilio A2H Protocol

Five intent types for agent-to-human communication:

| Intent    | Purpose                          | User Action              |
| --------- | -------------------------------- | ------------------------ |
| INFORM    | Awareness only                   | Read and acknowledge     |
| COLLECT   | Gather structured input          | Provide requested data   |
| AUTHORIZE | Gate approval                    | Approve or reject        |
| ESCALATE  | Agent is stuck, needs human help | Take over the task       |
| RESULT    | Completed work for review        | Review and accept/revise |

The inbox composition is itself a trust metric: early on it's AUTHORIZE-heavy (agent asks permission), over time it shifts to INFORM-heavy (agent reports what it did).

## Levels of Autonomy

From arxiv.org/abs/2506.12469 — L0-L5 scale from human-does-everything to full autonomy:

- **L0** — Human does all work, no agent involvement
- **L1** — Agent suggests, human executes
- **L2** — Agent executes with human approval (AUTHORIZE-heavy inbox)
- **L3** — Agent executes, human reviews after (RESULT-heavy inbox)
- **L4** — Agent executes, human spot-checks (INFORM-heavy inbox)
- **L5** — Full autonomy, human only intervenes on exceptions

## OpenHands "Outer Loop"

Human moves from inner loop (doing work) to outer loop (reviewing work). The transition is gradual and task-dependent.

## LangChain Agent Inbox

Open-source React app for human-in-the-loop agent review. Provides a reference implementation of the inbox pattern with support for approve/reject/edit workflows.

## Key Slack Primitives

Platform capabilities relevant to agent UX delivery:

- **App Home Tab** — per-user persistent interactive surface (100 blocks, all Block Kit elements)
- **Slack Lists** — structured data with typed fields, table + Kanban views, full CRUD API
- **`plan` + `task_card` blocks** — purpose-built Block Kit blocks for agent task display
- **Workflow Builder** — conditional branching, interactive buttons, webhook triggers, custom functions
- **Canvas** — persistent collaborative documents with markdown, checklists, embedded workflows
