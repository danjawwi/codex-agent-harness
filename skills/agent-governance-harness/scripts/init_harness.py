#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write_if_missing(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        return
    path.write_text(content, encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize a file-backed Codex governance harness.")
    parser.add_argument("--root", default=".", help="Project root where .codex-harness will be created.")
    parser.add_argument("--goal", default="", help="Optional initial project goal.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing harness files.")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    harness_dir = root / ".codex-harness"
    harness_dir.mkdir(parents=True, exist_ok=True)

    created_at = utc_now()
    goal = args.goal.strip()

    project_md = f"""# Project

Created: {created_at}

## Goal

{goal or "Fill in the concrete user goal here."}

## Constraints

- Fill in product, technical, or timeline constraints.

## Repo Facts

- Fill in important facts discovered from the codebase.

## Definition Of Done

- Fill in what must be true before the project is considered complete.
"""

    backlog = {
        "version": 1,
        "created_at": created_at,
        "project_goal": goal,
        "status_values": ["pending", "ready", "in_progress", "blocked", "done"],
        "features": [],
    }

    current_md = f"""# Current Feature

Updated: {created_at}

## Feature

None selected yet.

## Acceptance Checks

- Add checks for the single active feature here.

## Planned Verification

- Add the exact verification steps for the active feature here.

## Notes

- Add implementation notes for the active feature here.
"""

    log_md = f"""# Harness Log

## {created_at}

- Harness initialized.
- Next step: run the initializer and break the project into 5-10 concrete features.
"""

    write_if_missing(harness_dir / "project.md", project_md, args.force)
    write_if_missing(harness_dir / "backlog.json", json.dumps(backlog, indent=2) + "\n", args.force)
    write_if_missing(harness_dir / "current.md", current_md, args.force)
    write_if_missing(harness_dir / "log.md", log_md, args.force)

    print(f"Initialized harness at {harness_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
