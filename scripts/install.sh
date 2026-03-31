#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"

mkdir -p "$CODEX_HOME/skills"

cp "$REPO_ROOT/AGENTS.md" "$CODEX_HOME/AGENTS.md"
rm -rf "$CODEX_HOME/skills/agent-governance-harness"
cp -R "$REPO_ROOT/skills/agent-governance-harness" "$CODEX_HOME/skills/agent-governance-harness"
cp "$REPO_ROOT/scripts/sync-harness-memory.sh" "$CODEX_HOME/skills/agent-governance-harness/scripts/sync_harness_memory.sh"
cp "$REPO_ROOT/skills/agent-governance-harness/scripts/render_progress_dashboard.py" "$CODEX_HOME/skills/agent-governance-harness/scripts/render_progress_dashboard.py"
cp "$REPO_ROOT/skills/agent-governance-harness/scripts/serve_control_plane.py" "$CODEX_HOME/skills/agent-governance-harness/scripts/serve_control_plane.py"
mkdir -p "$CODEX_HOME/skills/agent-governance-harness/references"
rm -rf "$CODEX_HOME/skills/agent-governance-harness/references/mechanisms"
rm -rf "$CODEX_HOME/skills/agent-governance-harness/references/orchestration"
rm -rf "$CODEX_HOME/skills/agent-governance-harness/references/roles"
rm -rf "$CODEX_HOME/skills/agent-governance-harness/references/schemas"
rm -rf "$CODEX_HOME/skills/agent-governance-harness/references/templates"
cp -R "$REPO_ROOT/mechanisms" "$CODEX_HOME/skills/agent-governance-harness/references/mechanisms"
cp -R "$REPO_ROOT/orchestration" "$CODEX_HOME/skills/agent-governance-harness/references/orchestration"
cp -R "$REPO_ROOT/roles" "$CODEX_HOME/skills/agent-governance-harness/references/roles"
cp -R "$REPO_ROOT/schemas" "$CODEX_HOME/skills/agent-governance-harness/references/schemas"
cp -R "$REPO_ROOT/templates" "$CODEX_HOME/skills/agent-governance-harness/references/templates"

chmod +x "$CODEX_HOME/skills/agent-governance-harness/scripts/init_harness.py"
chmod +x "$CODEX_HOME/skills/agent-governance-harness/scripts/sync_harness_memory.sh"
chmod +x "$CODEX_HOME/skills/agent-governance-harness/scripts/render_progress_dashboard.py"
chmod +x "$CODEX_HOME/skills/agent-governance-harness/scripts/serve_control_plane.py"
chmod +x "$REPO_ROOT/scripts/sync-harness-memory.sh"
chmod +x "$REPO_ROOT/scripts/bootstrap-from-github.sh"
chmod +x "$REPO_ROOT/skills/agent-governance-harness/scripts/sync_harness_memory.sh"
chmod +x "$REPO_ROOT/skills/agent-governance-harness/scripts/render_progress_dashboard.py"
chmod +x "$REPO_ROOT/skills/agent-governance-harness/scripts/serve_control_plane.py"

echo "Installed harness into $CODEX_HOME"
echo "Installed governance references into $CODEX_HOME/skills/agent-governance-harness/references"
echo "Review $REPO_ROOT/config/harness-config.toml for optional config values."
