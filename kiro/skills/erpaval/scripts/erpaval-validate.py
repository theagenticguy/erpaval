# /// script
# requires-python = ">=3.12"
# dependencies = ["pydantic>=2", "pyyaml", "cyclopts"]
# ///
"""erpaval-validate — schema-check a .erpaval/ YAML packet.

Invoked by the PostToolUse(Write|Edit) hook after any write under
`.erpaval/**/*.yaml`. Reads the file and validates against the matching
Pydantic schema. Exits non-zero with an error message on failure so the
hook can surface it to Claude.

Secret-scanning is intentionally out of scope — that belongs to gitleaks,
trufflehog, or GitHub push protection at the repo level.

Usage:
  uv run erpaval-validate.py <path>
  uv run erpaval-validate.py --stdin-json  # reads {"tool_input": {"file_path": "..."}}
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Literal

import yaml
from cyclopts import App
from pydantic import BaseModel, Field, ValidationError

app = App()

# ---------- schemas (one per packet type) ----------


class IntakeInferred(BaseModel):
    """Scaffolded with all-null; classifiers fill each field on first run.

    Plan blocks on null complexity, so fail-fast if classifiers skipped.
    """

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
    """Validates the YAML frontmatter at the top of `tasks/T-*.md` packets.

    The Markdown body (10 sections + work log) is intentionally unchecked —
    it's a narrative work log edited section-by-section by the subagent.
    """

    task_id: str
    ac_source: str | None = None
    agent_name: str | None = None
    model: Literal["haiku", "sonnet", "opus"] | None = None
    isolation: Literal["worktree"] | None = None
    status: Literal["IN_PROGRESS", "COMPLETE", "BLOCKED"] | None = None


class ValidationLayer(BaseModel):
    status: Literal["pass", "fail", "findings"]


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


SCHEMAS: dict[str, type[BaseModel]] = {
    "intake": IntakeSchema,
    "recall": RecallSchema,
    "explore": ExploreSchema,
    "validation": ValidationSchema,
    "lessons": LessonsSchema,
    "session": SessionSchema,
}


def schema_for(path: Path) -> type[BaseModel] | None:
    name = path.stem
    if name in SCHEMAS:
        return SCHEMAS[name]
    if name.startswith("research-"):
        return ResearchSchema
    if path.parent.name == "tasks" and path.suffix == ".md" and name.startswith("T-"):
        return TaskFrontmatter
    return None


# ---------- entry points ----------


def _is_erpaval_packet(path: Path) -> bool:
    if ".erpaval" not in path.parts:
        return False
    if path.suffix in (".yaml", ".yml"):
        return True
    if path.suffix == ".md" and path.parent.name == "tasks":
        return True
    return False


def _parse_frontmatter(text: str) -> dict | None:
    """Split --- frontmatter YAML from markdown body."""
    if not text.startswith("---\n"):
        return None
    try:
        end = text.index("\n---", 4)
    except ValueError:
        return None
    return yaml.safe_load(text[4:end]) or {}


def _validate(path: Path) -> list[str]:
    errors: list[str] = []
    if not path.exists():
        return [f"{path}: does not exist"]

    schema = schema_for(path)
    if schema is None:
        return errors  # unknown packet type — nothing to check

    content = path.read_text()
    if path.suffix == ".md":
        data = _parse_frontmatter(content)
        if data is None:
            return errors  # no frontmatter yet — skeleton being written
    else:
        try:
            data = yaml.safe_load(content)
        except yaml.YAMLError as e:
            errors.append(f"{path}: YAML parse error: {e}")
            return errors
        if data is None:
            errors.append(f"{path}: file is empty")
            return errors

    try:
        schema.model_validate(data)
    except ValidationError as e:
        for err in e.errors():
            loc = ".".join(str(x) for x in err["loc"])
            errors.append(f"{path}: {loc}: {err['msg']}")

    return errors


@app.default
def validate(path: Path | None = None, stdin_json: bool = False) -> None:
    """Validate a .erpaval/ YAML packet against its schema and scan for secrets."""
    target: Path | None
    if stdin_json:
        payload = json.loads(sys.stdin.read())
        file_path = payload.get("tool_input", {}).get("file_path")
        if not file_path:
            sys.exit(0)  # not a file-write event, nothing to validate
        target = Path(file_path)
    elif path is not None:
        target = path
    else:
        print("error: pass <path> or --stdin-json", file=sys.stderr)
        sys.exit(2)

    if not _is_erpaval_packet(target):
        sys.exit(0)  # not a .erpaval packet, skip

    errors = _validate(target)
    if errors:
        for err in errors:
            print(err, file=sys.stderr)
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    app()
