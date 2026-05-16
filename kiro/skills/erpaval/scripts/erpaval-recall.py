# /// script
# requires-python = ">=3.12"
# dependencies = ["pyyaml", "cyclopts"]
# ///
"""erpaval-recall — grep `.erpaval/solutions/**.md` for relevant prior lessons.

Ranks by (3 × module match) + (tag overlap count) + (0.5 × recency).
Intended for invocation by the main erpaval skill at session start
(SessionStart hook) and per-task when writing Act context packets.

Usage:
  uv run erpaval-recall.py search --module src/auth --tags oauth,pkce
  uv run erpaval-recall.py bootstrap  # summary for SessionStart
"""
from __future__ import annotations

import json
import sys
from dataclasses import dataclass, asdict
from pathlib import Path

import yaml
from cyclopts import App

app = App()


def _parse_frontmatter(text: str) -> tuple[dict, str]:
    """Split --- frontmatter YAML from markdown body."""
    if not text.startswith("---\n"):
        return {}, text
    try:
        end = text.index("\n---", 4)
    except ValueError:
        return {}, text
    fm = yaml.safe_load(text[4:end]) or {}
    body = text[end + 4 :].lstrip("\n")
    return fm, body


def _solutions_dir(start: Path | None = None) -> Path | None:
    """Walk up from start looking for .erpaval/solutions/. Return None if not found."""
    cwd = (start or Path.cwd()).resolve()
    for candidate in [cwd, *cwd.parents]:
        solutions = candidate / ".erpaval" / "solutions"
        if solutions.is_dir():
            return solutions
    return None


@dataclass
class LessonHit:
    path: str
    title: str
    track: str
    category: str
    score: float
    matched_on: list[str]


def _module_match(query: str, lesson: str) -> bool:
    """Path-boundary match: equal, prefix-with-separator, or parent-with-separator.

    Prevents `src/a` from matching `src/auth`.
    """
    if not (query and lesson):
        return False
    q = query.rstrip("/")
    l = lesson.rstrip("/")
    return q == l or l.startswith(q + "/") or q.startswith(l + "/")


def _score_lesson(fm: dict, module: str, tags: list[str]) -> tuple[float, list[str]]:
    score = 0.0
    matched: list[str] = []

    lesson_module = fm.get("module", "") or ""
    if _module_match(module, lesson_module):
        score += 3
        matched.append(f"module:{lesson_module}")

    lesson_tags = set(fm.get("tags", []) or [])
    overlap = lesson_tags & set(tags)
    if overlap:
        score += len(overlap)
        matched.append(f"tags:{','.join(sorted(overlap))}")

    return score, matched


def _collect_hits(solutions: Path, module: str, tags: list[str]) -> list[LessonHit]:
    """Score each lesson, then add a normalized recency bonus as tiebreaker.

    Formula: 3·module + tags + 0.5·recency_rank, where recency_rank is the
    lesson's mtime rank within the result set normalized to [0, 1].
    """
    raw: list[tuple[LessonHit, float]] = []  # (hit, mtime)
    for md in solutions.rglob("*.md"):
        try:
            fm, _ = _parse_frontmatter(md.read_text())
        except Exception:
            continue
        if not fm:
            continue
        score, matched = _score_lesson(fm, module, tags)
        if score <= 0:
            continue
        try:
            mtime = md.stat().st_mtime
        except OSError:
            mtime = 0.0
        raw.append(
            (
                LessonHit(
                    path=str(md),
                    title=fm.get("title", md.stem),
                    track=fm.get("track", "unknown"),
                    category=fm.get("category", md.parent.name),
                    score=score,
                    matched_on=matched,
                ),
                mtime,
            )
        )

    if not raw:
        return []

    # Rank by mtime descending — newest gets rank 1.0, oldest gets 0.0.
    sorted_by_mtime = sorted(raw, key=lambda pair: pair[1], reverse=True)
    n = len(sorted_by_mtime)
    mtime_rank: dict[str, float] = {}
    for i, (hit, _) in enumerate(sorted_by_mtime):
        mtime_rank[hit.path] = 1.0 - (i / max(n - 1, 1)) if n > 1 else 1.0

    hits: list[LessonHit] = []
    for hit, _ in raw:
        hit.score += 0.5 * mtime_rank[hit.path]
        hits.append(hit)
    hits.sort(key=lambda h: h.score, reverse=True)
    return hits


@app.command
def search(
    module: str = "",
    tags: str = "",
    limit: int = 5,
    cwd: Path | None = None,
    json_output: bool = True,
) -> None:
    """Search `.erpaval/solutions/` for lessons matching module and tags."""
    solutions = _solutions_dir(cwd)
    if solutions is None:
        if json_output:
            print(json.dumps({"status": "no_solutions_dir", "hits": []}))
        else:
            print("no prior lessons — no .erpaval/solutions/ found")
        return

    tag_list = [t.strip() for t in tags.split(",") if t.strip()]
    hits = _collect_hits(solutions, module, tag_list)[:limit]

    if json_output:
        print(json.dumps({"status": "ok", "hits": [asdict(h) for h in hits]}, indent=2))
    else:
        if not hits:
            print("no matching lessons")
            return
        for h in hits:
            print(f"{h.score:>4.1f}  {h.track:10}  {h.path}")
            print(f"       {h.title}")


@app.command
def bootstrap(cwd: Path | None = None) -> None:
    """Session-start summary: category counts + note if INDEX.md exists."""
    solutions = _solutions_dir(cwd)
    if solutions is None:
        print("no prior lessons — this project has no .erpaval/solutions/ yet")
        return

    counts: dict[str, int] = {}
    for md in solutions.rglob("*.md"):
        category = md.parent.name
        counts[category] = counts.get(category, 0) + 1

    total = sum(counts.values())
    if total == 0:
        print("no prior lessons — .erpaval/solutions/ is empty")
        return

    print(f"prior lessons available: {total} across {len(counts)} categories")
    for cat in sorted(counts):
        print(f"  {cat}: {counts[cat]}")

    index = solutions.parent / "INDEX.md"
    if index.exists():
        print(f"index: {index}")


if __name__ == "__main__":
    app()
