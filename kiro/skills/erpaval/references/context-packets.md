# Context packets + review model

Every decision-bearing node writes a YAML packet to `.erpaval/sessions/<id>/`. Packets are read-only hints the orchestrator reads when composing each `/spawn` invocation. The per-task Markdown packets at `.erpaval/sessions/<id>/tasks/T-AC-X-Y.md` carry the authoritative `status:` (IN_PROGRESS / COMPLETE / BLOCKED) and `blocked_by:` frontmatter — they are how the orchestrator answers "what's next, what's blocked, what's stuck." Kiro's `/todo` slash command mirrors progress for the user but is advisory only. Per-task packets additionally double as research/ultraplan-style work logs — subagents edit them section-by-section using the `write-protocol.md` block.

Packets use session IDs (random hex, e.g., `session-a1b2c3`) and sequence numbers — no dates, no timestamps in filenames. Revisions append `-rev2`, `-rev3`.

**Reading convention for the YAML blocks below.** Each example shows a worked OAuth-PKCE session so fields line up across packets. Angle-bracket tokens (`<excerpt from CP-EXPLORE>`) are placeholders. Concrete values (`session-a1b2c3`, `003-oauth-pkce`, `src/auth`) are illustrative. Placeholder conventions (`<hex>`, `NNN`, `<slug>`, `<domain>`) live in `glossary.md`.

## Packet index

| Packet        | Path                                                                   | Written by             | Read by                             |
| ------------- | ---------------------------------------------------------------------- | ---------------------- | ----------------------------------- |
| CP-INTAKE     | `sessions/<id>/intake.yaml`                                            | Intake node            | All classifiers                     |
| CP-RECALL     | `sessions/<id>/recall.yaml`                                            | Recall node            | All Act context packets             |
| CP-HMW        | `brainstorms/NNN-slug-requirements.md` (committed)                     | Framing-HMW            | Framing-EARS, Plan                  |
| CP-EARS       | `specs/NNN-slug/spec.md` (committed)                                   | Framing-EARS           | Plan                                |
| CP-EXPLORE    | `sessions/<id>/explore.yaml`                                           | Explore subagent       | Plan, Act packets                   |
| CP-RESEARCH   | `sessions/<id>/research-<domain>.yaml`                                 | Research subagent      | Plan, Act packets                   |
| CP-PLAN       | `specs/NNN-slug/tasks.md` (committed, derived from EARS)               | Plan node              | Act                                 |
| CP-TASK-N     | `sessions/<id>/tasks/T-AC-X-Y.md`                                      | Orchestrator per task  | Subagent (edits in place); Validate |
| CP-VALIDATION | `sessions/<id>/validation.yaml`                                        | Validate               | CL-VALIDATE, Compound               |
| CP-LESSONS    | `sessions/<id>/lessons.yaml` + `solutions/<cat>/<slug>.md` (committed) | Compound               | Future sessions (Recall)            |
| CP-SESSION    | `sessions/<id>/session.yaml`                                           | Manifest (append-only) | Audit                               |

## CP-INTAKE

```yaml
session_id: session-a1b2c3
working_dir: /Users/.../project
git:
  is_repo: true
  branch: feat/oauth-pkce
  dirty: false
raw_request: |
  Users report that our mobile app's token exchange is slow and
  occasionally fails silently. We need PKCE + better error handling.
inferred:
  scope: coding
  complexity: multi-module
  dir_state: existing
  variant: brownfield
  rigor_needed: [hmw, ears]
upstream_artifacts:
  prd: null
  stack_decisions: null
env_snapshot:
  has_mise: true
  python: "3.12.4"
  node: "22.1.0"
```

## CP-RECALL

```yaml
applicable_lessons:
  - path: .erpaval/solutions/api-patterns/oauth-state-param-validation.md
    track: knowledge
    relevance: HIGH
    matched_on: [tags.oauth, module.src/auth]
  - path: .erpaval/solutions/test-failures/pytest-asyncio-scope-mismatch.md
    track: bug
    relevance: MEDIUM
    matched_on: [tags.pytest, module.tests]
injection_strategy: include_in_all_act_packets
```

## CP-EXPLORE

```yaml
agent_id: explore-1
scope: src/auth/**, src/users/**
findings:
  architecture: fastapi + sqlalchemy-async + alembic
  patterns:
    error_handling: custom APIError → middleware
    dependency_injection: FastAPI Depends + src/deps.py container
    test_style: pytest-asyncio + factoryboy
  touch_points:
    - src/auth/routes.py
    - src/auth/service.py
  toolchain: mise.toml defines lint/typecheck/test
```

## CP-RESEARCH

```yaml
agent_id: research-oauth
domain: OAuth + PKCE libraries
libraries:
  - name: authlib
    version_pin: "^1.3"
    docs_source: context7
    api_surface:
      - authlib.integrations.starlette_client.OAuth
    breaking_changes: 1.2 → 1.3 removed sync client; async-only
    security_notes:
      - Always validate state parameter (matches CP-RECALL lesson)
```

## CP-TASK-N

Per-task packets are Markdown, not YAML — they double as subagent work logs edited section-by-section via `write-protocol.md`. Seed from `assets/session/task-skeleton.md`; filename is `T-AC-X-Y.md`.

Structure:

- YAML frontmatter — `task_id`, `status` (IN_PROGRESS | COMPLETE | BLOCKED), `blocked_by` (list of upstream task_ids), `agent_name` (subagent target). Authoritative state for the orchestrator.
- `<write_protocol>` block verbatim.
- Sections 1-10: Objective · Scope · EARS requirement · Architecture context · API contracts · Conventions · Dependencies · Prior lessons · Success criteria · Anti-goals.
- Work log, Validation, Summary — filled by the subagent as it proceeds.

See `assets/session/task-skeleton.md` for the canonical skeleton.

## CP-VALIDATION

```yaml
validation_id: val-1
layers:
  l1_static:
    status: pass
    checks:
      - cmd: "uvx ruff check ."
        exit: 0
      - cmd: "uv run pyright"
        exit: 0
      - cmd: "uv run pytest"
        exit: 0
  l2_quality:
    status: pass
    agent: opus
    findings: []
  l3_security:
    status: findings
    tools:
      - cmd: "semgrep --config p/owasp-top-ten"
        findings: []
      - agent: opus-security
        findings:
          - severity: MEDIUM
            file: src/auth/oauth_service.py
            note: consider state parameter validation on callback
auto_merge_eligible: false
disposition: pending_human
```

## CP-LESSONS

```yaml
lessons_written:
  - path: .erpaval/solutions/test-failures/async-fixture-scope-oauth-tests.md
    track: bug
    category: test-failures
    severity: medium
    reason_captured: |
      Session hit this twice — once in Wave 2, once after validation.
      Worth persisting so next OAuth-related session doesn't repeat.
  - path: .erpaval/solutions/api-patterns/pkce-code-challenge-storage.md
    track: knowledge
    category: api-patterns
    severity: info
claude_md_updated: true
index_md_updated: true
```

## CP-SESSION

```yaml
session_id: session-a1b2c3
status: completed
variant: brownfield
classifier_trace:
  - CL-SCOPE: coding
  - CL-COMPLEXITY: multi-module
  - CL-DIR: existing
  - CL-RIGOR: [hmw, ears]
  - CL-SPEC: ready
  - CL-VALIDATE: findings
  - CL-DISP: accepted_with_followup
  - CL-LESSONS: wrote_2
cycles_executed:
  C1: 2
  C2: 3
  C4: 1
  C6: 3
packets:
  intake: .erpaval/sessions/session-a1b2c3/intake.yaml
  recall: .erpaval/sessions/session-a1b2c3/recall.yaml
  hmw: .erpaval/brainstorms/003-oauth-pkce-requirements.md
  ears: .erpaval/specs/003-oauth-pkce/spec.md
  explore: [.erpaval/sessions/session-a1b2c3/explore.yaml]
  research: [.erpaval/sessions/session-a1b2c3/research-oauth.yaml]
  plan_revisions: [.erpaval/specs/003-oauth-pkce/tasks.md]
  tasks: [.erpaval/sessions/session-a1b2c3/tasks/T-AC-*.md]
  validation: .erpaval/sessions/session-a1b2c3/validation.yaml
  lessons: .erpaval/sessions/session-a1b2c3/lessons.yaml
merge:
  auto: false
  disposition: accepted_with_followup
```

---

## Validation hook

The `postToolUse` hook with `matcher: fs_write` (`kiro/hooks/kiro_validate_packet.py`, configured inline in `kiro/agents/erpaval-orchestrator.json`) runs on every write, early-exits on non-`.erpaval/` paths, and Pydantic-checks YAML packets plus per-task `.md` frontmatter against their schemas. On failure the hook prints a warning to STDERR — advisory, not blocking. Fail-open by construction so a hook bug can never wedge a session.

Per-task Markdown packet bodies (the 10 sections + work log) are intentionally unchecked — they're narrative work logs. Only the YAML frontmatter at the top carries validated structured metadata. Committed HMW/EARS outputs under `brainstorms/` and `specs/` are not validated — they're human-readable durables. Secrets scanning is a separate concern — use `gitleaks`, `trufflehog`, or GitHub push protection at repo level.

## Zone rules

| Zone                    | Gitignored? | Why                                                    |
| ----------------------- | ----------- | ------------------------------------------------------ |
| `.erpaval/sessions/`    | yes         | Orchestrator-coupled, ephemeral, secrets surface       |
| `.erpaval/solutions/`   | no          | Durable compounding knowledge, benefits whole team     |
| `.erpaval/brainstorms/` | no          | HMW outputs — design intent, durable                   |
| `.erpaval/specs/`       | no          | EARS specs + derived tasks.md — traceable record       |
| `.erpaval/INDEX.md`     | no          | Discoverability pointer referenced from root CLAUDE.md |

Single `.gitignore` line: `.erpaval/sessions/`.

---

## Two-gate review model

### Gate 1 — Plan review (before Act)

The plan is the single highest-leverage artifact in the flow. A senior engineer reviews `specs/NNN-slug/{spec.md, tasks.md}`:

- Are the design decisions sound?
- Is task decomposition correct?
- Are interface contracts between parallel tasks compatible?
- Are there missing tasks or wrong dependencies?

This is the high-leverage review. If the plan is wrong, no amount of code review fixes it. If the plan is right and validation passes, the code is correct by construction. Expect 2-4 revision rounds (cycle C1).

Record `plan_approved_by` in `session.yaml` to note who approved.

### Gate 2 — Validation report review (before merge)

The reviewer reads the validation report, not the diff. Key questions:

- Did all three layers pass?
- Were any findings deferred? Are justifications reasonable?
- How many fix cycles were needed? (High count signals plan issues.)
- Were sensitive paths touched?

### Auto-merge criteria

A change qualifies for auto-merge (no human code review) when ALL of:

1. Plan was pre-approved at Gate 1 (`plan_approved_by` is set).
2. All three validation layers passed with zero CRITICAL/HIGH findings.
3. No files on the sensitive-paths list were touched.
4. Total files changed/created matches plan prediction (no scope creep).
5. Fix cycle count is 0 or 1 (low rework signals clean execution).

Changes that don't meet all five criteria route to Gate 2 human review. Even then, the reviewer reads the validation report and change narrative — line-by-line code review is the exception path for flagged findings only.
