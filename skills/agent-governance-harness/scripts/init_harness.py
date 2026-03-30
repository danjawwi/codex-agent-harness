#!/usr/bin/env python3

from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def write_if_missing(path: Path, content: str, force: bool) -> None:
    if path.exists() and not force:
        return
    path.write_text(content, encoding="utf-8")


def render_template(path: Path, replacements: dict[str, str]) -> str:
    content = path.read_text(encoding="utf-8")
    for key, value in replacements.items():
        content = content.replace(f"{{{{{key}}}}}", value)
    return content


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize a file-backed Codex governance harness.")
    parser.add_argument("--root", default=".", help="Project root where .codex-harness will be created.")
    parser.add_argument("--goal", default="", help="Optional initial project goal.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing harness files.")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    harness_dir = root / ".codex-harness"
    harness_dir.mkdir(parents=True, exist_ok=True)
    references_dir = Path(__file__).resolve().parents[1] / "references" / "templates"

    created_at = utc_now()
    goal = args.goal.strip()
    replacements = {
        "CREATED_AT": created_at,
        "GOAL": goal or "Fill in the concrete user goal here."
    }

    project_md = render_template(references_dir / "project.md", replacements)
    backlog_json = render_template(references_dir / "backlog.json", replacements)
    current_md = render_template(references_dir / "current.md", replacements)
    log_md = render_template(references_dir / "log.md", replacements)

    write_if_missing(harness_dir / "project.md", project_md, args.force)
    write_if_missing(harness_dir / "backlog.json", backlog_json, args.force)
    write_if_missing(harness_dir / "current.md", current_md, args.force)
    write_if_missing(harness_dir / "log.md", log_md, args.force)

    print(f"Initialized harness at {harness_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
