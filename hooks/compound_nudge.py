#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = ["pydantic>=2"]
# ///
"""Stop hook: one-shot nudge to run the ERPAVal Compound phase.

Stop hooks cannot inject additionalContext per the authoritative schema
(code.claude.com/docs/en/hooks.md) — the only Claude-facing channel is
`decision: "block"` + `reason`. This hook uses that channel exactly like
codeprobe's review-before-commit pattern: block the first turn-end that
matches the gates, feed Claude the instruction, then step out of the way.

Firing gates (ALL must hold):

  1. This Claude session actually wrote to .erpaval/ — marker file
     dropped by validate_packet.py. Prevents nudges in sessions that
     never touched ERPAVal.
  2. A .erpaval/sessions/session-<hex>/ dir in cwd has validation.yaml
     but no lessons.yaml (the original pending-Compound signal).
  3. validation.yaml mtime < 2h ago. Abandoned sessions stop nagging.
  4. Session dir name matches `session-<hex>` — filters hand-named dirs.
  5. Not nudged this Claude session (HookState).
  6. Session ID not in .erpaval/sessions/.nudged ledger — dismiss-once
     across Claude sessions.

On fire: returns `decision: "block"` with instructions to run Compound.
Claude either runs it (lessons.yaml lands, gate 2 fails next turn) or
skips it (HookState + ledger prevent re-fire). Either way: bounded.

Harness caveat: stop_hook_active caps consecutive Stop blocks at 2, so
even a buggy nudge cannot trap a session.
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
    StopInput,
    SyncHookOutput,
    block,
    run_hook,
)


SESSION_RE = re.compile(r"^session-[a-f0-9]{6,}$")
RECENCY_WINDOW_SECONDS = 2 * 60 * 60  # 2 hours

ERPAVAL_DOT_DIR = ".erpaval"
ERPAVAL_MARKER_PREFIX = "claude-erpaval-active-"


def _erpaval_active(session_id: str) -> bool:
    """Did this Claude session write to .erpaval/? Set by validate_packet.py."""
    return (Path("/tmp") / f"{ERPAVAL_MARKER_PREFIX}{session_id}").exists()


def _find_pending_compound(cwd: Path) -> Path | None:
    """Return the first session dir with pending Compound, or None.

    Applies: name-shape filter, recency gate, per-project dismiss ledger.
    """
    sessions = cwd / ERPAVAL_DOT_DIR / "sessions"
    if not sessions.is_dir():
        return None

    dismissed = _load_ledger(sessions)
    now = time.time()

    for session in sorted(sessions.iterdir()):
        if not session.is_dir():
            continue
        if not SESSION_RE.match(session.name):
            continue
        if session.name in dismissed:
            continue
        validation = session / "validation.yaml"
        lessons = session / "lessons.yaml"
        if not validation.exists() or lessons.exists():
            continue
        try:
            age = now - validation.stat().st_mtime
        except OSError:
            continue
        if age > RECENCY_WINDOW_SECONDS:
            continue
        return session

    return None


def _load_ledger(sessions_dir: Path) -> set[str]:
    ledger = sessions_dir / ".nudged"
    if not ledger.exists():
        return set()
    try:
        return {line.strip() for line in ledger.read_text().splitlines() if line.strip()}
    except OSError:
        return set()


def _append_ledger(sessions_dir: Path, session_name: str) -> None:
    ledger = sessions_dir / ".nudged"
    try:
        with ledger.open("a") as fh:
            fh.write(session_name + "\n")
    except OSError:
        pass


def handle(input: HookInput, state: HookState) -> SyncHookOutput | None:
    if not isinstance(input, StopInput):
        return None
    if state.has("compound_nudged"):
        return None
    if not _erpaval_active(input.session_id):
        return None

    session = _find_pending_compound(Path(input.cwd))
    if session is None:
        return None

    state.set("compound_nudged", True)
    _append_ledger(session.parent, session.name)

    reason = (
        f"ERPAVal Compound phase is pending for {session}. "
        "validation.yaml exists but lessons.yaml does not — the session "
        "has not written its dual-track lessons yet.\n\n"
        "Before ending: run CL-LESSONS against the session trace and, for "
        "each novel + reusable candidate, write .erpaval/solutions/<category>/"
        "<slug>.md, then update .erpaval/INDEX.md and write "
        f"{session}/lessons.yaml. See "
        "${CLAUDE_PLUGIN_ROOT}/skills/erpaval/references/compound.md "
        "for the full operating sequence.\n\n"
        "If the session was abandoned and no lessons should be persisted, "
        "write an empty {lessons_written: []} lessons.yaml so the gate "
        "clears. This nudge fires at most once per Claude session and is "
        "suppressed permanently for this session-id via "
        ".erpaval/sessions/.nudged."
    )
    return block(reason)


if __name__ == "__main__":
    run_hook(handle, name="erpaval_compound_nudge")
