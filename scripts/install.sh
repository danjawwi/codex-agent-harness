#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"

mkdir -p "$CODEX_HOME/skills"

cp "$REPO_ROOT/AGENTS.md" "$CODEX_HOME/AGENTS.md"
rm -rf "$CODEX_HOME/skills/agent-governance-harness"
cp -R "$REPO_ROOT/skills/agent-governance-harness" "$CODEX_HOME/skills/agent-governance-harness"

chmod +x "$CODEX_HOME/skills/agent-governance-harness/scripts/init_harness.py"

echo "Installed harness into $CODEX_HOME"
echo "Review $REPO_ROOT/config/harness-config.toml for optional config values."
