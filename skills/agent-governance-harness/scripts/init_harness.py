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


def resolve_templates_dir() -> Path:
    installed_dir = Path(__file__).resolve().parents[1] / "references" / "templates"
    if installed_dir.exists():
        return installed_dir

    repo_dir = Path(__file__).resolve().parents[3] / "templates"
    if repo_dir.exists():
        return repo_dir

    raise FileNotFoundError("Could not locate harness templates directory.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize a file-backed Codex governance harness.")
    parser.add_argument("--root", default=".", help="Project root where .codex-harness will be created.")
    parser.add_argument("--goal", default="", help="Optional initial project goal.")
    parser.add_argument("--force", action="store_true", help="Overwrite existing harness files.")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    harness_dir = root / ".codex-harness"
    harness_dir.mkdir(parents=True, exist_ok=True)
    memory_dir = harness_dir / "memory"
    memory_dir.mkdir(parents=True, exist_ok=True)
    observability_dir = harness_dir / "observability"
    observability_dir.mkdir(parents=True, exist_ok=True)
    checkpoints_dir = harness_dir / "checkpoints"
    checkpoints_dir.mkdir(parents=True, exist_ok=True)
    approvals_dir = harness_dir / "approvals"
    approvals_dir.mkdir(parents=True, exist_ok=True)
    branches_dir = harness_dir / "branches"
    branches_dir.mkdir(parents=True, exist_ok=True)
    knowledge_dir = harness_dir / "knowledge"
    knowledge_dir.mkdir(parents=True, exist_ok=True)
    risks_dir = harness_dir / "risks"
    risks_dir.mkdir(parents=True, exist_ok=True)
    evals_dir = harness_dir / "evals"
    evals_dir.mkdir(parents=True, exist_ok=True)
    dashboard_dir = harness_dir / "dashboard"
    dashboard_dir.mkdir(parents=True, exist_ok=True)
    references_dir = resolve_templates_dir()

    created_at = utc_now()
    goal = args.goal.strip()
    project_name = root.name
    replacements = {
        "CREATED_AT": created_at,
        "GOAL": goal or "Fill in the concrete user goal here.",
        "PROJECT_NAME": project_name
    }

    project_md = render_template(references_dir / "project.md", replacements)
    backlog_json = render_template(references_dir / "backlog.json", replacements)
    current_md = render_template(references_dir / "current.md", replacements)
    log_md = render_template(references_dir / "log.md", replacements)
    memory_index = render_template(references_dir / "memory-index.json", replacements)
    active_context = render_template(references_dir / "active-context.md", replacements)
    decision_log = render_template(references_dir / "decision-log.md", replacements)
    handoff = render_template(references_dir / "handoff.md", replacements)
    project_summary = render_template(references_dir / "project-summary.md", replacements)
    observations = render_template(references_dir / "observations.ndjson", replacements)
    trace = render_template(references_dir / "trace.ndjson", replacements)
    checkpoints = render_template(references_dir / "checkpoints.json", replacements)
    approvals = render_template(references_dir / "approvals.json", replacements)
    branches = render_template(references_dir / "branches.json", replacements)
    knowledge_index = render_template(references_dir / "knowledge-index.json", replacements)
    risk_register = render_template(references_dir / "risk-register.json", replacements)
    eval_suite = render_template(references_dir / "eval-suite.json", replacements)

    write_if_missing(harness_dir / "project.md", project_md, args.force)
    write_if_missing(harness_dir / "backlog.json", backlog_json, args.force)
    write_if_missing(harness_dir / "current.md", current_md, args.force)
    write_if_missing(harness_dir / "log.md", log_md, args.force)
    write_if_missing(memory_dir / "memory-index.json", memory_index, args.force)
    write_if_missing(memory_dir / "active-context.md", active_context, args.force)
    write_if_missing(memory_dir / "decision-log.md", decision_log, args.force)
    write_if_missing(memory_dir / "handoff.md", handoff, args.force)
    write_if_missing(memory_dir / "project-summary.md", project_summary, args.force)
    write_if_missing(memory_dir / "observations.ndjson", observations, args.force)
    write_if_missing(observability_dir / "trace.ndjson", trace, args.force)
    write_if_missing(checkpoints_dir / "checkpoints.json", checkpoints, args.force)
    write_if_missing(approvals_dir / "approvals.json", approvals, args.force)
    write_if_missing(branches_dir / "branches.json", branches, args.force)
    write_if_missing(knowledge_dir / "knowledge-index.json", knowledge_index, args.force)
    write_if_missing(risks_dir / "risk-register.json", risk_register, args.force)
    write_if_missing(evals_dir / "eval-suite.json", eval_suite, args.force)

    print(f"Initialized harness at {harness_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
