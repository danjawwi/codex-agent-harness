#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"

mkdir -p "$CODEX_HOME/skills"

cp "$REPO_ROOT/AGENTS.md" "$CODEX_HOME/AGENTS.md"
rm -rf "$CODEX_HOME/skills/agent-governance-harness"
cp -R "$REPO_ROOT/skills/agent-governance-harness" "$CODEX_HOME/skills/agent-governance-harness"
mkdir -p "$CODEX_HOME/skills/agent-governance-harness/references"
rm -rf "$CODEX_HOME/skills/agent-governance-harness/references/orchestration"
rm -rf "$CODEX_HOME/skills/agent-governance-harness/references/roles"
rm -rf "$CODEX_HOME/skills/agent-governance-harness/references/schemas"
rm -rf "$CODEX_HOME/skills/agent-governance-harness/references/templates"
cp -R "$REPO_ROOT/orchestration" "$CODEX_HOME/skills/agent-governance-harness/references/orchestration"
cp -R "$REPO_ROOT/roles" "$CODEX_HOME/skills/agent-governance-harness/references/roles"
cp -R "$REPO_ROOT/schemas" "$CODEX_HOME/skills/agent-governance-harness/references/schemas"
cp -R "$REPO_ROOT/templates" "$CODEX_HOME/skills/agent-governance-harness/references/templates"

chmod +x "$CODEX_HOME/skills/agent-governance-harness/scripts/init_harness.py"

echo "Installed harness into $CODEX_HOME"
echo "Installed governance references into $CODEX_HOME/skills/agent-governance-harness/references"
echo "Review $REPO_ROOT/config/harness-config.toml for optional config values."
