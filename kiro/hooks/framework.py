"""Strongly-typed, stateful hook framework for Kiro CLI.

Models Kiro's 5 hook events (agentSpawn, userPromptSubmit, preToolUse,
postToolUse, stop) per /docs/cli/hooks/. STDIN is a flat JSON object;
output channel is STDOUT (captured into context for agentSpawn /
userPromptSubmit / stop) plus exit-code-driven STDERR semantics:

    exit 0  -> success; STDOUT captured
    exit 2  -> (preToolUse only) block tool execution; STDERR returned to LLM
    exit 1+ -> show warning, allow execution; STDERR shown as warning

Critically, Kiro `stop` hooks CANNOT block-and-re-prompt the way Claude Code's
`Stop` hook can. STDOUT on `stop` is added to context as advisory only. Do
not rely on it to gate the assistant.

Usage from a UV shebang hook script:

    #!/usr/bin/env -S uv run --script
    # /// script
    # requires-python = ">=3.12"
    # dependencies = ["pydantic>=2"]
    # ///
    import os, sys
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from framework import run_hook, emit_context, HookState, PostToolUseInput

    def handle(input, state):
        if isinstance(input, PostToolUseInput) and input.tool_name == "fs_write":
            emit_context("noted")  # exits 0

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
# Input Models -- 5 hook events per Kiro /docs/cli/hooks/
# ---------------------------------------------------------------------------


class BaseHookInput(BaseModel):
    """Fields common to every Kiro hook payload."""

    model_config = ConfigDict(extra="allow")

    hook_event_name: str
    cwd: str
    session_id: str


class AgentSpawnInput(BaseHookInput):
    """Fires when an agent is activated; no tool context.

    STDOUT is added to the conversation as starting context.
    Closest Claude Code equivalent: SessionStart.
    """

    hook_event_name: Literal["agentSpawn"]


class UserPromptSubmitInput(BaseHookInput):
    """Fires when the user submits a prompt.

    STDOUT is added to the conversation context (advisory).
    """

    hook_event_name: Literal["userPromptSubmit"]
    prompt: str


class PreToolUseInput(BaseHookInput):
    """Fires before tool execution.

    Exit code 2 blocks the tool; STDERR is returned to the LLM as the reason.
    Other non-zero exit codes show a warning and allow execution.
    """

    hook_event_name: Literal["preToolUse"]
    tool_name: str
    tool_input: dict[str, Any]


class PostToolUseInput(BaseHookInput):
    """Fires after tool execution; carries the tool response.

    STDOUT is captured but is informational; the tool already ran.
    """

    hook_event_name: Literal["postToolUse"]
    tool_name: str
    tool_input: dict[str, Any]
    tool_response: Any = None


class StopInput(BaseHookInput):
    """Fires when the assistant finishes responding.

    STDOUT is added to context as advisory only. Kiro stop hooks CANNOT
    block-and-re-prompt the assistant — there is no decision: block channel.
    """

    hook_event_name: Literal["stop"]


# Discriminated union -- TypeAdapter routes to the correct model automatically.
HookInput = Annotated[
    Union[
        AgentSpawnInput,
        UserPromptSubmitInput,
        PreToolUseInput,
        PostToolUseInput,
        StopInput,
    ],
    Field(discriminator="hook_event_name"),
]

_hook_input_adapter: TypeAdapter[HookInput] = TypeAdapter(HookInput)


# ---------------------------------------------------------------------------
# HookState -- session-scoped persistent state
# ---------------------------------------------------------------------------


class HookState:
    """JSON file-backed state at /tmp/kiro-hook-{name}-{session_id}.json.

    The `kiro-` prefix avoids collision with Claude Code's analogous
    `claude_hook` state files when both runtimes execute on the same host.

    Eagerly loads on init; writes on every mutation. No locking needed because
    Kiro hooks execute synchronously per session.
    """

    def __init__(self, name: str, session_id: str) -> None:
        self._path = Path(f"/tmp/kiro-hook-{name}-{session_id}.json")
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
        """Increment a counter and return the new value. Loop-prevention primitive."""
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
# Output helpers -- exit-code-driven, no JSON output protocol on Kiro
# ---------------------------------------------------------------------------


def emit_context(message: str) -> None:
    """Print message to STDOUT and exit 0.

    Kiro captures STDOUT into the agent's context for agentSpawn,
    userPromptSubmit, and stop events. For preToolUse / postToolUse,
    STDOUT is captured but does not influence tool execution.
    """
    sys.stdout.write(message)
    if not message.endswith("\n"):
        sys.stdout.write("\n")
    sys.stdout.flush()
    sys.exit(0)


def block_tool(reason: str) -> None:
    """Block tool execution. Only valid for preToolUse hooks.

    Prints reason to STDERR and exits 2. Kiro returns the STDERR text to the
    LLM as the block reason. On any other event, exit 2 is treated as a
    generic warning by Kiro — there is no block channel.
    """
    sys.stderr.write(reason)
    if not reason.endswith("\n"):
        sys.stderr.write("\n")
    sys.stderr.flush()
    sys.exit(2)


def warn(message: str) -> None:
    """Emit a non-blocking warning. Prints to STDERR, exits 1.

    Kiro shows STDERR as a warning to the user but allows tool execution
    or assistant flow to continue.
    """
    sys.stderr.write(message)
    if not message.endswith("\n"):
        sys.stderr.write("\n")
    sys.stderr.flush()
    sys.exit(1)


# ---------------------------------------------------------------------------
# run_hook() -- the entry point
# ---------------------------------------------------------------------------


def run_hook(
    handler: Callable[[Any, HookState], None],
    *,
    name: str,
) -> None:
    """Read JSON from stdin, parse into typed input, call handler.

    The handler signature is `(input, state) -> None`. Return values are
    ignored; handlers signal outcomes by calling emit_context() / block_tool()
    / warn() directly, each of which exits the process.

    Fail-open by design: uncaught exceptions log to STDERR and exit 0 so a
    broken hook cannot wedge a Kiro session.
    """
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            sys.exit(0)

        data = json.loads(raw)
        parsed = _hook_input_adapter.validate_python(data)
        state = HookState(name, parsed.session_id)

        handler(parsed, state)

        # Handler returned without calling a helper — treat as no-op success.
        sys.exit(0)

    except SystemExit:
        raise
    except Exception as exc:
        print(f"[hook:{name}] error: {exc}", file=sys.stderr)
        sys.exit(0)
