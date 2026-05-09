#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["pydantic>=2", "pyyaml"]
# ///
"""PostToolUse hook: validate `.erpaval/sessions/<id>/*.yaml` writes.

Early-exits for non-`.erpaval` paths and non-YAML files. On schema violation,
injects a systemMessage via additionalContext so Claude sees the error but is
not blocked (fail-open: bad validation must never wedge a session).

Per-task packets (`tasks/T-*.md`) are validated by parsing YAML frontmatter
(first `---` block). Body is intentionally unchecked.
"""

import os
import sys
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field, ValidationError

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from framework import (
    HookInput,
    HookState,
    PostToolUseInput,
    SyncHookOutput,
    add_context,
    run_hook,
)


# ---------- schemas mirroring tools/erpaval-validate.py ----------


class IntakeInferred(BaseModel):
    scope: Literal["coding", "non-coding"] | None = None
    complexity: Literal["1-file-fix", "multi-module", "rebuild"] | None = None
    dir_state: Literal["empty", "existing", "rebuild-in-place"] | None = None
    variant: Literal["greenfield", "brownfield", "rip-and-replace"] | None = None
    rigor_needed: list[Literal["hmw", "ears"]] | None = None


class IntakeGit(BaseModel):
    is_repo: bool
    branch: str | None = None
    dirty: bool | None = None


class IntakeSchema(BaseModel):
    session_id: str = Field(pattern=r"^session-[a-f0-9]{6,}$")
    working_dir: str
    raw_request: str
    inferred: IntakeInferred
    git: IntakeGit | None = None
    upstream_artifacts: dict | None = None
    env_snapshot: dict | None = None


class RecallSchema(BaseModel):
    applicable_lessons: list[dict] = Field(default_factory=list)
    injection_strategy: str | None = None


class ExploreSchema(BaseModel):
    agent_id: str
    scope: str
    findings: dict


class ResearchSchema(BaseModel):
    agent_id: str
    domain: str
    libraries: list[dict] = Field(default_factory=list)


class TaskFrontmatter(BaseModel):
    task_id: str
    ac_source: str | None = None
    agent_name: str | None = None
    model: Literal["haiku", "sonnet", "opus"] | None = None
    isolation: Literal["worktree"] | None = None
    status: Literal["IN_PROGRESS", "COMPLETE", "BLOCKED"] | None = None


class ValidationSchema(BaseModel):
    validation_id: str
    layers: dict
    auto_merge_eligible: bool | None = None
    disposition: str | None = None


class LessonsSchema(BaseModel):
    lessons_written: list[dict] = Field(default_factory=list)
    claude_md_updated: bool | None = None
    index_md_updated: bool | None = None


class SessionSchema(BaseModel):
    session_id: str = Field(pattern=r"^session-[a-f0-9]{6,}$")
    status: Literal["active", "completed", "abandoned"]
    variant: str | None = None
    classifier_trace: list = Field(default_factory=list)
    cycles_executed: dict = Field(default_factory=dict)
    packets: dict = Field(default_factory=dict)
    merge: dict | None = None


ERPAVAL_DOT_DIR = ".erpaval"
ERPAVAL_MARKER_PREFIX = "claude-erpaval-active-"


SCHEMAS: dict[str, type[BaseModel]] = {
    "intake": IntakeSchema,
    "recall": RecallSchema,
    "explore": ExploreSchema,
    "validation": ValidationSchema,
    "lessons": LessonsSchema,
    "session": SessionSchema,
}


def _schema_for_yaml(path: Path) -> type[BaseModel] | None:
    name = path.stem
    if name in SCHEMAS:
        return SCHEMAS[name]
    if name.startswith("research-"):
        return ResearchSchema
    return None


def _parse_frontmatter(text: str) -> dict | None:
    if not text.startswith("---\n"):
        return None
    try:
        end = text.index("\n---", 4)
    except ValueError:
        return None
    return yaml.safe_load(text[4:end]) or {}


def _validate(path: Path) -> list[str]:
    if not path.exists():
        return []

    if path.suffix in (".yaml", ".yml"):
        schema = _schema_for_yaml(path)
        if schema is None:
            return []
        try:
            data = yaml.safe_load(path.read_text())
        except yaml.YAMLError as e:
            return [f"{path}: YAML parse error: {e}"]
        if data is None:
            return [f"{path}: file is empty"]
    elif path.suffix == ".md" and path.parent.name == "tasks":
        schema = TaskFrontmatter
        data = _parse_frontmatter(path.read_text())
        if data is None:
            return []  # no frontmatter yet — skeleton being written
    else:
        return []

    try:
        schema.model_validate(data)
    except ValidationError as e:
        return [
            f"{path}: {'.'.join(str(x) for x in err['loc'])}: {err['msg']}"
            for err in e.errors()
        ]
    return []


def _mark_erpaval_active(session_id: str) -> None:
    """Drop a cross-hook marker so compound_nudge knows this Claude session
    actually wrote to .erpaval/. Prevents the nudge from firing when the user
    is working in some other repo that happens to have a stale .erpaval/.
    """
    marker = Path("/tmp") / f"{ERPAVAL_MARKER_PREFIX}{session_id}"
    try:
        marker.touch(exist_ok=True)
    except OSError:
        pass


def handle(input: HookInput, state: HookState) -> SyncHookOutput | None:
    if not isinstance(input, PostToolUseInput):
        return None
    file_path = input.tool_input.get("file_path", "")
    if f"/{ERPAVAL_DOT_DIR}/" not in file_path:
        return None
    path = Path(file_path)
    if path.suffix not in (".yaml", ".yml", ".md"):
        return None

    _mark_erpaval_active(input.session_id)

    errors = _validate(path)
    if not errors:
        return None

    message = "ERPAVal packet validation failed:\n" + "\n".join(errors)
    return add_context(message, event_name="PostToolUse")


if __name__ == "__main__":
    run_hook(handle, name="erpaval_validate_packet")
