#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["pydantic>=2"]
# ///
"""SessionStart hook: emit category counts + INDEX pointer when this repo
has recent ERPAVal activity.

SessionStart genuinely supports additionalContext per the authoritative
schema (code.claude.com/docs/en/hooks.md), so injection is legal here.

Firing gates (ALL must hold):

  1. .erpaval/solutions/ exists with at least one lesson.
  2. A session-<hex>/ dir under .erpaval/sessions/ was modified in the
     last 24h — proxy for active-build rhythm or recent resume.
     Without this, cold repos with old lessons emit on every unrelated
     session just because the directory exists on disk.
  3. Fires at most once per Claude session (HookState `bootstrapped`).

Skip conditions:
  - No .erpaval/ at all → return None (usual no-op).
  - Lessons exist but no recent session activity → silent. User hasn't
    opted into an ERPAVal run this week.
"""

import os
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from framework import (
    HookInput,
    HookState,
    SessionStartInput,
    SyncHookOutput,
    add_context,
    run_hook,
)


SESSION_RE = re.compile(r"^session-[a-f0-9]{6,}$")
ACTIVITY_WINDOW_SECONDS = 24 * 60 * 60  # 24 hours

ERPAVAL_DOT_DIR = ".erpaval"


def _recent_session_activity(erpaval: Path) -> bool:
    """True iff any session-<hex>/ dir has been touched in the last 24h."""
    sessions = erpaval / "sessions"
    if not sessions.is_dir():
        return False
    cutoff = time.time() - ACTIVITY_WINDOW_SECONDS
    for session in sessions.iterdir():
        if not session.is_dir() or not SESSION_RE.match(session.name):
            continue
        try:
            if session.stat().st_mtime >= cutoff:
                return True
        except OSError:
            continue
    return False


def _bootstrap_summary(solutions: Path) -> str | None:
    counts: dict[str, int] = {}
    for md in solutions.rglob("*.md"):
        counts[md.parent.name] = counts.get(md.parent.name, 0) + 1
    total = sum(counts.values())
    if total == 0:
        return None
    lines = [f"prior ERPAVal lessons: {total} across {len(counts)} categories"]
    for cat in sorted(counts):
        lines.append(f"  {cat}: {counts[cat]}")
    index = solutions.parent / "INDEX.md"
    if index.exists():
        lines.append(f"index: {index}")
    return "\n".join(lines)


def handle(input: HookInput, state: HookState) -> SyncHookOutput | None:
    if not isinstance(input, SessionStartInput):
        return None
    if state.has("bootstrapped"):
        return None
    erpaval = Path(input.cwd) / ERPAVAL_DOT_DIR
    solutions = erpaval / "solutions"
    if not solutions.is_dir():
        return None
    if not _recent_session_activity(erpaval):
        return None
    summary = _bootstrap_summary(solutions)
    if summary is None:
        return None
    state.set("bootstrapped", True)
    return add_context(summary, event_name="SessionStart")


if __name__ == "__main__":
    run_hook(handle, name="erpaval_session_start_bootstrap")
