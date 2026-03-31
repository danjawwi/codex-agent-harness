#!/usr/bin/env python3

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_text(path: Path) -> str:
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")


def read_json(path: Path, fallback):
    if not path.exists():
        return fallback
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return fallback


def write_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")


def parse_log_bullets(text: str) -> list[str]:
    bullets = []
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("- "):
            bullets.append(line[2:])
    return bullets[-20:]


def parse_ndjson(path: Path) -> list[dict]:
    if not path.exists():
        return []
    events = []
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
    return events[-100:]


def slugify(value: str) -> str:
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return cleaned or "item"


def find_active_milestone(backlog: dict) -> dict | None:
    milestones = backlog.get("milestones", [])
    for status in ("in_progress", "ready", "pending", "blocked", "done"):
        for milestone in milestones:
            if milestone.get("status") == status:
                return milestone
    return milestones[0] if milestones else None


def task_counts(features: list[dict]) -> dict[str, int]:
    counts = {"pending": 0, "ready": 0, "in_progress": 0, "blocked": 0, "done": 0}
    for feature in features:
        status = str(feature.get("status", "pending"))
        counts[status] = counts.get(status, 0) + 1
    return counts


def slice_progress(features: list[dict]) -> list[dict]:
    slices: dict[str, dict] = {}
    for feature in features:
        slice_id = str(feature.get("slice_id", "")).strip() or "unsliced"
        item = slices.setdefault(slice_id, {
            "id": slice_id,
            "title": slice_id.replace("-", " ").title() if slice_id != "unsliced" else "Unassigned Slice",
            "total_tasks": 0,
            "done_tasks": 0,
            "in_progress_tasks": 0,
            "blocked_tasks": 0,
            "milestone_ids": set()
        })
        item["total_tasks"] += 1
        status = feature.get("status")
        if status == "done":
            item["done_tasks"] += 1
        if status == "in_progress":
            item["in_progress_tasks"] += 1
        if status == "blocked":
            item["blocked_tasks"] += 1
        if feature.get("milestone_id"):
            item["milestone_ids"].add(str(feature.get("milestone_id")))

    results = []
    for item in slices.values():
        total = item["total_tasks"]
        item["percent"] = int((item["done_tasks"] / total) * 100) if total else 0
        item["milestone_ids"] = sorted(item["milestone_ids"])
        results.append(item)
    return sorted(results, key=lambda entry: (entry["id"] != "unsliced", entry["id"]))


def milestone_progress(milestone: dict, features: list[dict]) -> dict:
    milestone_id = milestone.get("id", "")
    scoped = [feature for feature in features if feature.get("milestone_id") == milestone_id]
    total = len(scoped)
    done = len([feature for feature in scoped if feature.get("status") == "done"])
    in_progress = len([feature for feature in scoped if feature.get("status") == "in_progress"])
    blocked = len([feature for feature in scoped if feature.get("status") == "blocked"])
    percent = 100 if total == 0 and milestone.get("status") == "done" else (int((done / total) * 100) if total else 0)
    return {
        "id": milestone_id,
        "title": milestone.get("title", ""),
        "status": milestone.get("status", ""),
        "goal": milestone.get("goal", ""),
        "delivery_target": milestone.get("delivery_target", ""),
        "review_artifact": milestone.get("review_artifact", ""),
        "total_tasks": total,
        "done_tasks": done,
        "in_progress_tasks": in_progress,
        "blocked_tasks": blocked,
        "percent": percent
    }


def active_tasks(features: list[dict]) -> list[dict]:
    scoped = [feature for feature in features if feature.get("status") in {"in_progress", "blocked", "ready"}]
    return scoped[:20]


def load_state(root: Path) -> dict:
    harness = root / ".codex-harness"
    backlog = read_json(harness / "backlog.json", {"milestones": [], "features": []})
    features = backlog.get("features", [])
    milestones = backlog.get("milestones", [])
    active_milestone = find_active_milestone(backlog)
    progress = [milestone_progress(milestone, features) for milestone in milestones]
    branches = read_json(harness / "branches" / "branches.json", {"branches": []})
    approvals = read_json(harness / "approvals" / "approvals.json", {"enabled": False, "gates": []})
    checkpoints = read_json(harness / "checkpoints" / "checkpoints.json", {"checkpoints": []})
    evals = read_json(harness / "evals" / "eval-suite.json", {"cases": []})
    knowledge = read_json(harness / "knowledge" / "knowledge-index.json", {"items": []})
    risks = read_json(harness / "risks" / "risk-register.json", {"items": []})
    trace = parse_ndjson(harness / "observability" / "trace.ndjson")
    memory_index = read_json(harness / "memory" / "memory-index.json", {})

    active_branch = None
    for branch in branches.get("branches", []):
        if branch.get("status") == "active":
            active_branch = branch
            break
    if active_branch is None and branches.get("branches"):
        active_branch = branches["branches"][0]

    return {
        "project_name": root.name,
        "project_md": read_text(harness / "project.md"),
        "current_md": read_text(harness / "current.md"),
        "log_bullets": parse_log_bullets(read_text(harness / "log.md")),
        "memory_index": memory_index,
        "active_milestone": active_milestone,
        "milestones": progress,
        "slices": slice_progress(features),
        "task_counts": task_counts(features),
        "active_tasks": active_tasks(features),
        "trace_events": trace,
        "checkpoints": checkpoints.get("checkpoints", [])[-20:],
        "approvals": approvals,
        "branches": branches.get("branches", []),
        "active_branch": active_branch,
        "knowledge_items": knowledge.get("items", [])[-20:],
        "risk_items": risks.get("items", [])[-20:],
        "eval_cases": evals.get("cases", [])[-20:]
    }


def update_approval(root: Path, payload: dict) -> dict:
    harness = root / ".codex-harness"
    approvals_path = harness / "approvals" / "approvals.json"
    approvals = read_json(approvals_path, {"version": 1, "project": root.name, "enabled": False, "gates": []})
    gate_id = str(payload.get("id", ""))
    status = str(payload.get("status", ""))
    decision_summary = str(payload.get("decision_summary", "")).strip()
    decision_by = str(payload.get("decision_by", "human")).strip() or "human"

    if status not in {"approved", "rejected", "changes_requested"}:
        raise ValueError("Invalid approval status.")

    for gate in approvals.get("gates", []):
        if gate.get("id") == gate_id:
            gate["status"] = status
            gate["decision_summary"] = decision_summary
            gate["decision_by"] = decision_by
            gate["decided_at"] = utc_now()
            write_json(approvals_path, approvals)
            return gate

    raise ValueError(f"Approval gate not found: {gate_id}")


def activate_branch(root: Path, payload: dict) -> dict:
    harness = root / ".codex-harness"
    branches_path = harness / "branches" / "branches.json"
    data = read_json(branches_path, {"version": 1, "project": root.name, "branches": []})
    branch_id = str(payload.get("id", ""))
    selected = None
    for branch in data.get("branches", []):
        if branch.get("id") == branch_id:
            selected = branch
        elif branch.get("status") == "active":
            branch["status"] = "paused"
    if selected is None:
        raise ValueError(f"Branch not found: {branch_id}")
    selected["status"] = "active"
    write_json(branches_path, data)
    return selected


def create_checkpoint(root: Path, payload: dict) -> dict:
    harness = root / ".codex-harness"
    checkpoints_path = harness / "checkpoints" / "checkpoints.json"
    data = read_json(checkpoints_path, {"version": 1, "project": root.name, "checkpoints": []})
    summary = str(payload.get("summary", "")).strip()
    if not summary:
        raise ValueError("Checkpoint summary is required.")
    trigger = str(payload.get("trigger", "manual_control_plane")).strip() or "manual_control_plane"
    restore_hint = str(payload.get("restore_hint", "")).strip() or "Resume from current milestone state."
    milestone_id = str(payload.get("milestone_id", "")).strip()
    task_id = str(payload.get("task_id", "")).strip()
    branch_id = str(payload.get("branch_id", "")).strip()
    checkpoint_id = payload.get("id")
    if not checkpoint_id:
        base = slugify(summary)[:24]
        checkpoint_id = f"cp-{base}-{len(data.get('checkpoints', [])) + 1}"

    checkpoint = {
        "id": checkpoint_id,
        "created_at": utc_now(),
        "trigger": trigger,
        "summary": summary,
        "restore_hint": restore_hint
    }
    if milestone_id:
        checkpoint["milestone_id"] = milestone_id
    if task_id:
        checkpoint["task_id"] = task_id
    if branch_id:
        checkpoint["branch_id"] = branch_id

    data.setdefault("checkpoints", []).append(checkpoint)
    write_json(checkpoints_path, data)
    return checkpoint


def create_approval(root: Path, payload: dict) -> dict:
    harness = root / ".codex-harness"
    approvals_path = harness / "approvals" / "approvals.json"
    data = read_json(approvals_path, {"version": 1, "project": root.name, "enabled": False, "gates": []})
    summary = str(payload.get("summary", "")).strip()
    action_type = str(payload.get("action_type", "")).strip()
    if not summary or not action_type:
        raise ValueError("Approval action_type and summary are required.")
    gate_id = payload.get("id")
    if not gate_id:
        base = slugify(action_type)[:24]
        gate_id = f"ap-{base}-{len(data.get('gates', [])) + 1}"
    data["enabled"] = True
    gate = {
        "id": gate_id,
        "requested_at": utc_now(),
        "status": "pending",
        "action_type": action_type,
        "summary": summary
    }
    milestone_id = str(payload.get("milestone_id", "")).strip()
    task_id = str(payload.get("task_id", "")).strip()
    if milestone_id:
        gate["milestone_id"] = milestone_id
    if task_id:
        gate["task_id"] = task_id
    data.setdefault("gates", []).append(gate)
    write_json(approvals_path, data)
    return gate


class ControlPlaneHandler(BaseHTTPRequestHandler):
    root: Path
    html_path: Path
    refresh_interval_ms: int

    def log_message(self, format: str, *args) -> None:
        return

    def _send_json(self, payload, status: int = 200) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, text: str) -> None:
        body = text.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_payload(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(length) if length else b"{}"
        if not raw:
            return {}
        return json.loads(raw.decode("utf-8"))

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path == "/":
            html_text = self.html_path.read_text(encoding="utf-8").replace("__REFRESH_INTERVAL_MS__", str(self.refresh_interval_ms))
            self._send_html(html_text)
            return
        if parsed.path == "/api/state":
            self._send_json(load_state(self.root))
            return
        self.send_error(HTTPStatus.NOT_FOUND, "Not found")

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        try:
            payload = self._read_payload()
            if parsed.path == "/api/approval":
                result = update_approval(self.root, payload)
                self._send_json({"ok": True, "result": result})
                return
            if parsed.path == "/api/approval/create":
                result = create_approval(self.root, payload)
                self._send_json({"ok": True, "result": result})
                return
            if parsed.path == "/api/branch/activate":
                result = activate_branch(self.root, payload)
                self._send_json({"ok": True, "result": result})
                return
            if parsed.path == "/api/checkpoint/create":
                result = create_checkpoint(self.root, payload)
                self._send_json({"ok": True, "result": result})
                return
            self.send_error(HTTPStatus.NOT_FOUND, "Not found")
        except Exception as exc:
            self._send_json({"ok": False, "error": str(exc)}, status=400)


def main() -> int:
    parser = argparse.ArgumentParser(description="Serve the Codex harness control plane.")
    parser.add_argument("--root", default=".", help="Project root containing .codex-harness.")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind.")
    parser.add_argument("--port", type=int, default=8765, help="Port to bind.")
    parser.add_argument("--refresh-ms", type=int, default=2000, help="Client polling interval in milliseconds.")
    args = parser.parse_args()

    root = Path(args.root).expanduser().resolve()
    html_path = Path(__file__).resolve().parents[1] / "web" / "control-plane" / "index.html"
    handler = type(
        "ConfiguredControlPlaneHandler",
        (ControlPlaneHandler,),
        {"root": root, "html_path": html_path, "refresh_interval_ms": args.refresh_ms}
    )
    server = ThreadingHTTPServer((args.host, args.port), handler)
    print(f"Control plane serving {root} at http://{args.host}:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nControl plane stopped.")
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
