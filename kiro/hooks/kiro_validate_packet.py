#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["pydantic>=2", "pyyaml"]
# ///
"""postToolUse hook: validate `.erpaval/sessions/<id>/*.yaml` writes.

Kiro fires `postToolUse` after each tool execution. This hook is intended
to be wired with `matcher: "fs_write"` in the agent JSON, so it runs only
after Kiro's canonical write tool. We still defensive-check `tool_name`.

Early-exits for non-`.erpaval` paths and non-YAML/MD files. On schema
violation, emits the error to STDOUT (Kiro's context channel) so the agent
sees the problem; the tool itself has already run, so this is advisory.
Fail-open: a parser bug must never wedge a session.

Per-task packets (`tasks/T-*.md`) are validated by parsing YAML frontmatter
(first `---` block). Body is intentionally unchecked.

Side effect: drops a `/tmp/kiro-erpaval-active-<session_id>` marker file so
`kiro_compound_nudge.py` knows this Kiro session actually wrote into
`.erpaval/`. Marker prefix `kiro-` avoids collision with the analogous
Claude Code distribution running on the same host.
"""

import os
import sys
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field, ValidationError

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from framework import (  # noqa: E402
    HookState,
    PostToolUseInput,
    emit_context,
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
ERPAVAL_MARKER_PREFIX = "kiro-erpaval-active-"


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
    """Drop a cross-hook marker so kiro_compound_nudge knows this Kiro
    session actually wrote to .erpaval/. Prevents the nudge from firing
    when the user is working in some other repo that happens to have a
    stale .erpaval/.
    """
    marker = Path("/tmp") / f"{ERPAVAL_MARKER_PREFIX}{session_id}"
    try:
        marker.touch(exist_ok=True)
    except OSError:
        pass


def handle(input, state: HookState) -> None:
    if not isinstance(input, PostToolUseInput):
        return
    # Defensive: agent JSON should already gate this with matcher: "fs_write",
    # but accept the canonical name and the `write` alias.
    if input.tool_name not in ("fs_write", "write"):
        return

    file_path = input.tool_input.get("file_path") or input.tool_input.get("path") or ""
    if f"/{ERPAVAL_DOT_DIR}/" not in file_path:
        return
    path = Path(file_path)
    if path.suffix not in (".yaml", ".yml", ".md"):
        return

    _mark_erpaval_active(input.session_id)

    errors = _validate(path)
    if not errors:
        return

    message = "ERPAVal packet validation failed:\n" + "\n".join(errors)
    emit_context(message)


if __name__ == "__main__":
    run_hook(handle, name="erpaval_validate_packet")
