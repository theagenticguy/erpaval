# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml", "cyclopts"]
# ///
"""erpaval-new — scaffold a new `.erpaval/sessions/session-<hex>/` directory.

Creates the session dir, writes an intake.yaml stub from the template,
and ensures `.erpaval/` is gitignored for `sessions/`. Does not commit.

Usage:
  uv run erpaval-new.py --request "Add PKCE to OAuth flow"
  uv run erpaval-new.py  # stubs raw_request empty for Claude to fill
"""
from __future__ import annotations

import secrets
import subprocess
import sys
from pathlib import Path
from textwrap import dedent

import yaml
from cyclopts import App

app = App()

CATEGORIES_YAML = Path(__file__).parent.parent / "references" / "solution-categories.yaml"


def _load_categories() -> list[str]:
    """Return `solutions/<name>` subdirs from the canonical YAML."""
    data = yaml.safe_load(CATEGORIES_YAML.read_text())
    return [f"solutions/{entry['name']}" for group in data.values() for entry in group]


def _ensure_dirs(root: Path) -> None:
    for d in ("sessions", *_load_categories(), "brainstorms", "specs"):
        (root / d).mkdir(parents=True, exist_ok=True)


def _ensure_gitignore(root: Path) -> None:
    """Ensure `.erpaval/sessions/` is gitignored at the project root."""
    project_root = root.parent  # root is .erpaval, its parent is project root
    gitignore = project_root / ".gitignore"
    line = ".erpaval/sessions/"
    existing = gitignore.read_text() if gitignore.exists() else ""
    if line in existing.splitlines():
        return
    prefix = "\n" if existing and not existing.endswith("\n") else ""
    gitignore.write_text(existing + prefix + line + "\n")


def _ensure_index(root: Path) -> None:
    index = root / "INDEX.md"
    if index.exists():
        return
    index.write_text(
        dedent(
            """\
            # ERPAVal lessons index

            Lessons learned from prior ERPAVal sessions. Claude reads this at
            session start and greps `.erpaval/solutions/**` for relevant
            lessons before starting work.

            ## By category

            _Populated by `erpaval-compound` as lessons are extracted._

            ## Recent additions

            _None yet._
            """
        )
    )


def _git_state(project_root: Path) -> dict:
    try:
        branch = subprocess.check_output(
            ["git", "-C", str(project_root), "symbolic-ref", "--short", "HEAD"],
            stderr=subprocess.DEVNULL,
        ).decode().strip()
    except subprocess.CalledProcessError:
        branch = None
    try:
        dirty = bool(
            subprocess.check_output(
                ["git", "-C", str(project_root), "status", "--porcelain"],
                stderr=subprocess.DEVNULL,
            ).decode().strip()
        )
    except subprocess.CalledProcessError:
        return {"is_repo": False}
    return {"is_repo": True, "branch": branch, "dirty": dirty}


@app.default
def new(request: str = "", project_root: Path | None = None) -> None:
    """Scaffold a new ERPAVal session directory and seed intake.yaml."""
    project = (project_root or Path.cwd()).resolve()
    root = project / ".erpaval"
    _ensure_dirs(root)
    _ensure_gitignore(root)
    _ensure_index(root)

    session_id = f"session-{secrets.token_hex(3)}"
    session_dir = root / "sessions" / session_id
    if session_dir.exists():
        print(f"error: session {session_id} already exists", file=sys.stderr)
        sys.exit(1)
    session_dir.mkdir(parents=True)
    (session_dir / "tasks").mkdir()

    git_state = _git_state(project)
    intake_yaml = dedent(
        f"""\
        session_id: {session_id}
        working_dir: {project}
        raw_request: |
          {request or '<fill in>'}
        inferred:
          scope: null
          complexity: null
          dir_state: null
          rigor_needed: null
        git:
          is_repo: {git_state.get('is_repo', False)}
          branch: {git_state.get('branch') or 'null'}
          dirty: {git_state.get('dirty', False)}
        upstream_artifacts:
          prd: null
          stack_decisions: null
        """
    )
    (session_dir / "intake.yaml").write_text(intake_yaml)

    print(f"created {session_dir}")
    print(f"  intake.yaml seeded — Claude will refine `inferred.*` via classifiers")
    print(f"  .erpaval/sessions/ gitignored, INDEX.md initialized")


if __name__ == "__main__":
    app()
