#!/usr/bin/env python3

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path


def read_json(path: Path, fallback):
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return fallback


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def parse_log_bullets(text: str) -> list[str]:
    lines = []
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("- "):
            lines.append(line[2:])
    return lines[-12:]


def parse_trace_events(path: Path) -> list[dict]:
    if not path.exists():
        return []
    events: list[dict] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            continue
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(data, dict):
            events.append(data)
    return events[-20:]


def count_task_statuses(features: list[dict]) -> dict[str, int]:
    counts = {"pending": 0, "ready": 0, "in_progress": 0, "blocked": 0, "done": 0}
    for feature in features:
        status = feature.get("status", "pending")
        counts[status] = counts.get(status, 0) + 1
    return counts


def badge(text: str, cls: str = "") -> str:
    class_attr = f' class="badge {cls}"' if cls else ' class="badge"'
    return f"<span{class_attr}>{html.escape(text)}</span>"


def render_list(items: list[str], empty: str) -> str:
    if not items:
        return f"<p class='empty'>{html.escape(empty)}</p>"
    lis = "".join(f"<li>{html.escape(item)}</li>" for item in items)
    return f"<ul>{lis}</ul>"


def render_table(headers: list[str], rows: list[list[str]], empty: str) -> str:
    if not rows:
        return f"<p class='empty'>{html.escape(empty)}</p>"
    head = "".join(f"<th>{html.escape(header)}</th>" for header in headers)
    body = []
    for row in rows:
        cols = "".join(f"<td>{html.escape(col)}</td>" for col in row)
        body.append(f"<tr>{cols}</tr>")
    return f"<table><thead><tr>{head}</tr></thead><tbody>{''.join(body)}</tbody></table>"


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a static HTML dashboard for Codex harness progress.")
    parser.add_argument("--root", default=".", help="Project root containing .codex-harness.")
    parser.add_argument("--output", default="", help="Optional output HTML path.")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    harness = root / ".codex-harness"
    dashboard_dir = harness / "dashboard"
    dashboard_dir.mkdir(parents=True, exist_ok=True)
    output = Path(args.output).expanduser().resolve() if args.output else dashboard_dir / "index.html"

    project_md = read_text(harness / "project.md")
    backlog = read_json(harness / "backlog.json", {"milestones": [], "features": []})
    current_md = read_text(harness / "current.md")
    log_md = read_text(harness / "log.md")
    checkpoints = read_json(harness / "checkpoints" / "checkpoints.json", {"checkpoints": []})
    approvals = read_json(harness / "approvals" / "approvals.json", {"enabled": False, "gates": []})
    knowledge = read_json(harness / "knowledge" / "knowledge-index.json", {"items": []})
    evals = read_json(harness / "evals" / "eval-suite.json", {"cases": []})
    trace_events = parse_trace_events(harness / "observability" / "trace.ndjson")

    milestones = backlog.get("milestones", [])
    features = backlog.get("features", [])
    task_counts = count_task_statuses(features)
    latest_log = parse_log_bullets(log_md)

    milestone_rows = [
        [
            str(m.get("id", "")),
            str(m.get("title", "")),
            str(m.get("status", "")),
            str(m.get("delivery_target", ""))
        ]
        for m in milestones
    ]
    checkpoint_rows = [
        [
            str(c.get("id", "")),
            str(c.get("created_at", "")),
            str(c.get("trigger", "")),
            str(c.get("summary", ""))
        ]
        for c in checkpoints.get("checkpoints", [])[-10:]
    ]
    approval_rows = [
        [
            str(g.get("id", "")),
            str(g.get("status", "")),
            str(g.get("action_type", "")),
            str(g.get("summary", ""))
        ]
        for g in approvals.get("gates", [])[-10:]
    ]
    knowledge_rows = [
        [
            str(item.get("id", "")),
            str(item.get("kind", "")),
            str(item.get("title", "")),
            str(item.get("summary", ""))
        ]
        for item in knowledge.get("items", [])[-10:]
    ]
    eval_rows = [
        [
            str(case.get("id", "")),
            str(case.get("status", "")),
            str(case.get("title", "")),
            str(case.get("goal", ""))
        ]
        for case in evals.get("cases", [])[-10:]
    ]
    trace_rows = [
        [
            str(event.get("timestamp", "")),
            str(event.get("phase", "")),
            str(event.get("event_type", "")),
            str(event.get("summary", ""))
        ]
        for event in trace_events
    ]

    html_output = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Harness Progress Dashboard</title>
  <style>
    :root {{
      --bg: #f3efe7;
      --panel: #fffaf2;
      --ink: #1d1c19;
      --muted: #6d675d;
      --line: #d7cdbd;
      --accent: #0f766e;
      --warn: #a16207;
      --danger: #b91c1c;
      --shadow: 0 12px 36px rgba(45, 38, 26, 0.08);
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: Georgia, "Iowan Old Style", "Palatino Linotype", serif;
      background:
        radial-gradient(circle at top right, rgba(15,118,110,0.08), transparent 28%),
        linear-gradient(180deg, #f8f4ec 0%, var(--bg) 100%);
      color: var(--ink);
    }}
    .wrap {{
      max-width: 1240px;
      margin: 0 auto;
      padding: 32px 20px 56px;
    }}
    .hero {{
      background: linear-gradient(135deg, rgba(15,118,110,0.14), rgba(255,250,242,0.95));
      border: 1px solid var(--line);
      border-radius: 24px;
      padding: 28px;
      box-shadow: var(--shadow);
      margin-bottom: 22px;
    }}
    h1, h2 {{ margin: 0 0 12px; }}
    h1 {{ font-size: 34px; line-height: 1.1; }}
    h2 {{ font-size: 20px; }}
    p {{ margin: 0 0 12px; color: var(--muted); }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 18px;
      margin-bottom: 18px;
    }}
    .panel {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 18px;
      padding: 18px;
      box-shadow: var(--shadow);
    }}
    .stats {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
      gap: 12px;
      margin-top: 14px;
    }}
    .stat {{
      padding: 14px;
      border-radius: 16px;
      background: rgba(255,255,255,0.72);
      border: 1px solid rgba(15,118,110,0.15);
    }}
    .stat strong {{
      display: block;
      font-size: 28px;
      color: var(--ink);
    }}
    table {{
      width: 100%;
      border-collapse: collapse;
      font-size: 14px;
    }}
    th, td {{
      text-align: left;
      padding: 10px 8px;
      border-bottom: 1px solid var(--line);
      vertical-align: top;
    }}
    th {{ color: var(--muted); font-weight: 700; }}
    ul {{ margin: 0; padding-left: 18px; color: var(--ink); }}
    li {{ margin-bottom: 8px; }}
    .empty {{ color: var(--muted); font-style: italic; }}
    .badge {{
      display: inline-block;
      padding: 4px 10px;
      border-radius: 999px;
      background: rgba(15,118,110,0.12);
      color: var(--accent);
      font-size: 12px;
      font-weight: 700;
      margin-right: 6px;
    }}
    .footer {{ margin-top: 18px; font-size: 13px; color: var(--muted); }}
    code {{
      background: rgba(29,28,25,0.06);
      padding: 2px 6px;
      border-radius: 6px;
      font-family: ui-monospace, "SFMono-Regular", Menlo, monospace;
    }}
  </style>
</head>
<body>
  <div class="wrap">
    <section class="hero">
      <h1>Harness Progress Dashboard</h1>
      <p>{html.escape(root.name)} is being tracked through file-backed governance artifacts.</p>
      <div>{badge('trace')} {badge('checkpoints')} {badge('knowledge')} {badge('light evals')} {badge('optional approvals')}</div>
      <div class="stats">
        <div class="stat"><span>Milestones</span><strong>{len(milestones)}</strong></div>
        <div class="stat"><span>Pending</span><strong>{task_counts.get('pending', 0)}</strong></div>
        <div class="stat"><span>In Progress</span><strong>{task_counts.get('in_progress', 0)}</strong></div>
        <div class="stat"><span>Blocked</span><strong>{task_counts.get('blocked', 0)}</strong></div>
        <div class="stat"><span>Done</span><strong>{task_counts.get('done', 0)}</strong></div>
      </div>
    </section>

    <div class="grid">
      <section class="panel">
        <h2>Project Snapshot</h2>
        <p>{html.escape(project_md[:420] if project_md else 'No project summary available yet.')}</p>
      </section>
      <section class="panel">
        <h2>Current Focus</h2>
        <p>{html.escape(current_md[:420] if current_md else 'No current milestone notes available yet.')}</p>
      </section>
    </div>

    <div class="grid">
      <section class="panel">
        <h2>Milestones</h2>
        {render_table(["ID", "Title", "Status", "Delivery Target"], milestone_rows, "No milestones defined yet.")}
      </section>
      <section class="panel">
        <h2>Recent Log</h2>
        {render_list(latest_log, "No log entries available yet.")}
      </section>
    </div>

    <div class="grid">
      <section class="panel">
        <h2>Trace Events</h2>
        {render_table(["Time", "Phase", "Event", "Summary"], trace_rows, "No trace events recorded yet.")}
      </section>
      <section class="panel">
        <h2>Checkpoints</h2>
        {render_table(["ID", "Created", "Trigger", "Summary"], checkpoint_rows, "No checkpoints recorded yet.")}
      </section>
    </div>

    <div class="grid">
      <section class="panel">
        <h2>Approvals</h2>
        <p>{html.escape('Approvals enabled.' if approvals.get('enabled') else 'Approvals disabled by default.')}</p>
        {render_table(["ID", "Status", "Action", "Summary"], approval_rows, "No approval records yet.")}
      </section>
      <section class="panel">
        <h2>Knowledge</h2>
        {render_table(["ID", "Kind", "Title", "Summary"], knowledge_rows, "No reusable knowledge items captured yet.")}
      </section>
    </div>

    <div class="grid">
      <section class="panel">
        <h2>Light Evals</h2>
        {render_table(["ID", "Status", "Title", "Goal"], eval_rows, "No eval cases defined yet.")}
      </section>
    </div>

    <p class="footer">Generated from <code>.codex-harness</code> artifacts. Regenerate after milestone changes to refresh this dashboard.</p>
  </div>
</body>
</html>
"""

    output.write_text(html_output, encoding="utf-8")
    print(f"Rendered dashboard to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
