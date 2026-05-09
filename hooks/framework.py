"""Strongly-typed, stateful hook framework for Claude Code.

Provides Pydantic models for all 26 hook input types and their output types,
a session-scoped HookState class, and a run_hook() entry point that handles
stdin/stdout plumbing.

Usage from a UV shebang hook script:

    #!/usr/bin/env -S uv run --script
    # /// script
    # requires-python = ">=3.12"
    # dependencies = ["pydantic>=2"]
    # ///
    import os, sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from framework import run_hook, deny, PreToolUseInput, HookInput, HookState, SyncHookOutput

    def handle(input: HookInput, state: HookState) -> SyncHookOutput | None:
        ...

    if __name__ == "__main__":
        run_hook(handle, name="my_hook")
"""

from __future__ import annotations

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Annotated, Any, Callable, Literal, Union

from pydantic import BaseModel, ConfigDict, Field, TypeAdapter


# ---------------------------------------------------------------------------
# Input Models -- all 26 hook events per code.claude.com/docs/en/hooks.md
# ---------------------------------------------------------------------------

class BaseHookInput(BaseModel):
    """Fields common to all hook events."""

    model_config = ConfigDict(extra="allow")

    session_id: str
    transcript_path: str
    cwd: str
    hook_event_name: str
    permission_mode: str | None = None


# -- Session lifecycle events -----------------------------------------------

class SessionStartInput(BaseHookInput):
    hook_event_name: Literal["SessionStart"]
    source: Literal["startup", "resume", "clear", "compact"] | None = None
    model: str | None = None


class InstructionsLoadedInput(BaseHookInput):
    hook_event_name: Literal["InstructionsLoaded"]
    file_path: str
    memory_type: str  # User | Project | Local | Managed
    load_reason: str  # session_start | nested_traversal | path_glob_match | include | compact
    globs: list[str] | None = None
    trigger_file_path: str | None = None
    parent_file_path: str | None = None


class SessionEndInput(BaseHookInput):
    hook_event_name: Literal["SessionEnd"]


# -- User input events ------------------------------------------------------

class UserPromptSubmitInput(BaseHookInput):
    hook_event_name: Literal["UserPromptSubmit"]
    prompt: str


# -- Tool lifecycle events ---------------------------------------------------

class PreToolUseInput(BaseHookInput):
    hook_event_name: Literal["PreToolUse"]
    tool_name: str
    tool_input: dict[str, Any]
    tool_use_id: str
    agent_id: str | None = None
    agent_type: str | None = None


class PostToolUseInput(BaseHookInput):
    hook_event_name: Literal["PostToolUse"]
    tool_name: str
    tool_input: dict[str, Any]
    tool_response: Any = None
    tool_use_id: str
    agent_id: str | None = None
    agent_type: str | None = None


class PostToolUseFailureInput(BaseHookInput):
    hook_event_name: Literal["PostToolUseFailure"]
    tool_name: str
    tool_input: dict[str, Any]
    tool_use_id: str
    error: str
    is_interrupt: bool | None = None
    agent_id: str | None = None
    agent_type: str | None = None


class PermissionRequestInput(BaseHookInput):
    hook_event_name: Literal["PermissionRequest"]
    tool_name: str
    tool_input: dict[str, Any]
    permission_suggestions: list[Any] | None = None
    agent_id: str | None = None
    agent_type: str | None = None


class PermissionDeniedInput(BaseHookInput):
    hook_event_name: Literal["PermissionDenied"]
    tool_name: str
    tool_input: dict[str, Any]
    tool_use_id: str
    reason: str
    agent_id: str | None = None
    agent_type: str | None = None


# -- Agent/subagent events ---------------------------------------------------

class SubagentStartInput(BaseHookInput):
    hook_event_name: Literal["SubagentStart"]
    agent_id: str
    agent_type: str


class SubagentStopInput(BaseHookInput):
    hook_event_name: Literal["SubagentStop"]
    stop_hook_active: bool
    agent_id: str
    agent_transcript_path: str
    agent_type: str
    last_assistant_message: str | None = None


# -- Task/team events --------------------------------------------------------

class TaskCreatedInput(BaseHookInput):
    hook_event_name: Literal["TaskCreated"]
    task_id: str
    task_subject: str
    task_description: str | None = None
    teammate_name: str | None = None
    team_name: str | None = None


class TaskCompletedInput(BaseHookInput):
    hook_event_name: Literal["TaskCompleted"]
    task_id: str
    task_subject: str
    task_description: str | None = None
    teammate_name: str | None = None
    team_name: str | None = None


class TeammateIdleInput(BaseHookInput):
    hook_event_name: Literal["TeammateIdle"]


# -- Stop events --------------------------------------------------------------

class StopInput(BaseHookInput):
    hook_event_name: Literal["Stop"]
    assistant_response: str | None = None


class StopFailureInput(BaseHookInput):
    hook_event_name: Literal["StopFailure"]
    error_type: str  # rate_limit | authentication_failed | billing_error | etc.
    error_message: str | None = None


# -- Compaction events --------------------------------------------------------

class PreCompactInput(BaseHookInput):
    hook_event_name: Literal["PreCompact"]
    trigger: Literal["manual", "auto"]
    custom_instructions: str | None = None


class PostCompactInput(BaseHookInput):
    hook_event_name: Literal["PostCompact"]


# -- Notification events ------------------------------------------------------

class NotificationInput(BaseHookInput):
    hook_event_name: Literal["Notification"]
    message: str
    title: str | None = None
    notification_type: str


# -- Config/filesystem events -------------------------------------------------

class ConfigChangeInput(BaseHookInput):
    hook_event_name: Literal["ConfigChange"]
    source: str  # user_settings | project_settings | local_settings | policy_settings | skills


class CwdChangedInput(BaseHookInput):
    hook_event_name: Literal["CwdChanged"]
    new_cwd: str


class FileChangedInput(BaseHookInput):
    hook_event_name: Literal["FileChanged"]
    file_path: str


# -- Worktree events ----------------------------------------------------------

class WorktreeCreateInput(BaseHookInput):
    hook_event_name: Literal["WorktreeCreate"]
    worktree_id: str | None = None
    branch: str | None = None


class WorktreeRemoveInput(BaseHookInput):
    hook_event_name: Literal["WorktreeRemove"]
    worktree_id: str | None = None


# -- MCP elicitation events ---------------------------------------------------

class ElicitationInput(BaseHookInput):
    hook_event_name: Literal["Elicitation"]
    mcp_server: str | None = None
    input_schema: dict[str, Any] | None = None


class ElicitationResultInput(BaseHookInput):
    hook_event_name: Literal["ElicitationResult"]
    mcp_server: str | None = None
    user_input: dict[str, Any] | None = None


# Discriminated union -- TypeAdapter routes to the correct model automatically
HookInput = Annotated[
    Union[
        SessionStartInput,
        InstructionsLoadedInput,
        SessionEndInput,
        UserPromptSubmitInput,
        PreToolUseInput,
        PostToolUseInput,
        PostToolUseFailureInput,
        PermissionRequestInput,
        PermissionDeniedInput,
        SubagentStartInput,
        SubagentStopInput,
        TaskCreatedInput,
        TaskCompletedInput,
        TeammateIdleInput,
        StopInput,
        StopFailureInput,
        PreCompactInput,
        PostCompactInput,
        NotificationInput,
        ConfigChangeInput,
        CwdChangedInput,
        FileChangedInput,
        WorktreeCreateInput,
        WorktreeRemoveInput,
        ElicitationInput,
        ElicitationResultInput,
    ],
    Field(discriminator="hook_event_name"),
]

_hook_input_adapter: TypeAdapter[HookInput] = TypeAdapter(HookInput)


# ---------------------------------------------------------------------------
# Output Models -- mirror claude_agent_sdk/types.py lines 369-507
# ---------------------------------------------------------------------------

class PreToolUseSpecificOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    hookEventName: Literal["PreToolUse"] = "PreToolUse"
    permissionDecision: Literal["allow", "deny", "ask", "defer"] | None = None
    permissionDecisionReason: str | None = None
    updatedInput: dict[str, Any] | None = None
    additionalContext: str | None = None


class PostToolUseSpecificOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    hookEventName: Literal["PostToolUse"] = "PostToolUse"
    additionalContext: str | None = None
    updatedMCPToolOutput: Any | None = None


class PostToolUseFailureSpecificOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    hookEventName: Literal["PostToolUseFailure"] = "PostToolUseFailure"
    additionalContext: str | None = None


class PostToolBatchSpecificOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    hookEventName: Literal["PostToolBatch"] = "PostToolBatch"
    additionalContext: str | None = None


class UserPromptSubmitSpecificOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    hookEventName: Literal["UserPromptSubmit"] = "UserPromptSubmit"
    additionalContext: str | None = None
    sessionTitle: str | None = None


class UserPromptExpansionSpecificOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    hookEventName: Literal["UserPromptExpansion"] = "UserPromptExpansion"
    additionalContext: str | None = None


class SessionStartSpecificOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    hookEventName: Literal["SessionStart"] = "SessionStart"
    additionalContext: str | None = None


class SetupSpecificOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    hookEventName: Literal["Setup"] = "Setup"
    additionalContext: str | None = None


class PermissionRequestSpecificOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    hookEventName: Literal["PermissionRequest"] = "PermissionRequest"
    decision: dict[str, Any]


class PermissionDeniedSpecificOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    hookEventName: Literal["PermissionDenied"] = "PermissionDenied"
    retry: bool | None = None


class ElicitationSpecificOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    hookEventName: Literal["Elicitation"] = "Elicitation"
    action: Literal["accept", "decline", "cancel"] | None = None
    content: dict[str, Any] | None = None


class ElicitationResultSpecificOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    hookEventName: Literal["ElicitationResult"] = "ElicitationResult"
    action: Literal["accept", "decline", "cancel"] | None = None
    content: dict[str, Any] | None = None


class WorktreeCreateSpecificOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    hookEventName: Literal["WorktreeCreate"] = "WorktreeCreate"
    worktreePath: str | None = None


HookSpecificOutput = Union[
    PreToolUseSpecificOutput,
    PostToolUseSpecificOutput,
    PostToolUseFailureSpecificOutput,
    PostToolBatchSpecificOutput,
    UserPromptSubmitSpecificOutput,
    UserPromptExpansionSpecificOutput,
    SessionStartSpecificOutput,
    SetupSpecificOutput,
    PermissionRequestSpecificOutput,
    PermissionDeniedSpecificOutput,
    ElicitationSpecificOutput,
    ElicitationResultSpecificOutput,
    WorktreeCreateSpecificOutput,
]


class SyncHookOutput(BaseModel):
    """Top-level hook output. Serializes with by_alias=True so continue_ -> continue."""

    model_config = ConfigDict(populate_by_name=True, extra="forbid")

    continue_: bool | None = Field(None, alias="continue")
    suppressOutput: bool | None = None
    stopReason: str | None = None
    decision: Literal["block"] | None = None
    systemMessage: str | None = None
    reason: str | None = None
    hookSpecificOutput: HookSpecificOutput | None = None

    def to_json(self) -> str:
        return self.model_dump_json(by_alias=True, exclude_none=True)

    def to_dict(self) -> dict[str, Any]:
        return self.model_dump(by_alias=True, exclude_none=True)


# ---------------------------------------------------------------------------
# HookState -- session-scoped persistent state
# ---------------------------------------------------------------------------

class HookState:
    """JSON file-backed state at /tmp/claude-hook-{name}-{session_id}.json.

    Eagerly loads on init; writes on every mutation. No locking needed because
    Claude Code hooks execute synchronously per session.
    """

    def __init__(self, name: str, session_id: str) -> None:
        self._path = Path(f"/tmp/claude-hook-{name}-{session_id}.json")
        self._data: dict[str, Any] = self._load()

    def _load(self) -> dict[str, Any]:
        if self._path.exists():
            try:
                return json.loads(self._path.read_text())
            except (json.JSONDecodeError, OSError):
                return {}
        return {}

    def _save(self) -> None:
        self._path.write_text(json.dumps(self._data))

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self._data[key] = value
        self._save()

    def delete(self, key: str) -> bool:
        removed = key in self._data
        self._data.pop(key, None)
        self._save()
        return removed

    def increment(self, key: str) -> int:
        """Increment a counter and return the new value. Core loop-prevention primitive."""
        val = self._data.get(key, 0) + 1
        self._data[key] = val
        self._save()
        return val

    def has(self, key: str) -> bool:
        return key in self._data

    def clear(self) -> None:
        self._data = {}
        try:
            self._path.unlink(missing_ok=True)
        except OSError:
            pass

    def timestamp(self, key: str) -> None:
        """Set key to current UTC ISO timestamp. Useful for cooldown patterns."""
        self._data[key] = datetime.now(timezone.utc).isoformat()
        self._save()

    @property
    def path(self) -> Path:
        return self._path


# ---------------------------------------------------------------------------
# Helper functions -- ergonomic output constructors
# ---------------------------------------------------------------------------

def allow() -> SyncHookOutput:
    """Explicitly allow a PreToolUse action."""
    return SyncHookOutput(
        hookSpecificOutput=PreToolUseSpecificOutput(permissionDecision="allow"),
    )


def deny(reason: str) -> SyncHookOutput:
    """Deny a PreToolUse action. The reason is shown to Claude."""
    return SyncHookOutput(
        hookSpecificOutput=PreToolUseSpecificOutput(
            permissionDecision="deny",
            permissionDecisionReason=reason,
        ),
    )


def defer(reason: str | None = None) -> SyncHookOutput:
    """Defer a PreToolUse action (non-interactive -p mode only).

    Session pauses with stop_reason: tool_deferred.
    Resume later with: claude -p --resume <session-id>
    """
    return SyncHookOutput(
        hookSpecificOutput=PreToolUseSpecificOutput(
            permissionDecision="defer",
            permissionDecisionReason=reason,
        ),
    )


def add_context(message: str, event_name: Literal[
    "PreToolUse", "PostToolUse", "PostToolUseFailure", "PostToolBatch",
    "UserPromptSubmit", "UserPromptExpansion",
    "SessionStart", "Setup",
] = "PreToolUse") -> SyncHookOutput:
    """Inject additional context into Claude's conversation.

    Only events whose hookSpecificOutput accepts additionalContext per the
    authoritative hook schema are valid targets. Stop / SubagentStop /
    Notification / SubagentStart / InstructionsLoaded / SessionEnd do NOT
    support additionalContext — use block(reason) on Stop to feed Claude,
    or set systemMessage on SyncHookOutput to surface a user-facing note.

    NOTE: additionalContext is ADVISORY — Claude can see it but may ignore it.
    For guaranteed behavior control, use deny() or block() instead.
    """
    output_map: dict[str, type[BaseModel]] = {
        "PreToolUse": PreToolUseSpecificOutput,
        "PostToolUse": PostToolUseSpecificOutput,
        "PostToolUseFailure": PostToolUseFailureSpecificOutput,
        "PostToolBatch": PostToolBatchSpecificOutput,
        "UserPromptSubmit": UserPromptSubmitSpecificOutput,
        "UserPromptExpansion": UserPromptExpansionSpecificOutput,
        "SessionStart": SessionStartSpecificOutput,
        "Setup": SetupSpecificOutput,
    }
    cls = output_map[event_name]
    return SyncHookOutput(hookSpecificOutput=cls(additionalContext=message))


def block(reason: str) -> SyncHookOutput:
    """Block execution with a system message (for non-PreToolUse hooks)."""
    return SyncHookOutput(decision="block", reason=reason)


# ---------------------------------------------------------------------------
# run_hook() -- the entry point
# ---------------------------------------------------------------------------

def run_hook(
    handler: Callable[[Any, HookState], SyncHookOutput | None],
    *,
    name: str,
) -> None:
    """Read JSON from stdin, parse into typed input, call handler, write output to stdout.

    Fail-open by design: uncaught exceptions log to stderr and exit 0.
    """
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            sys.exit(0)

        data = json.loads(raw)
        parsed = _hook_input_adapter.validate_python(data)
        state = HookState(name, parsed.session_id)

        result = handler(parsed, state)

        if result is None:
            sys.exit(0)

        sys.stdout.write(result.to_json())
        sys.stdout.flush()
        sys.exit(0)

    except SystemExit:
        raise
    except Exception as exc:
        print(f"[hook:{name}] error: {exc}", file=sys.stderr)
        sys.exit(0)
