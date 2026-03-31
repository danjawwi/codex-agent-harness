#!/usr/bin/env bash
set -euo pipefail

REPO_URL="${1:-https://github.com/danjawwi/codex-agent-harness.git}"
INSTALL_ROOT="${2:-$HOME/.codex/repos/codex-agent-harness}"

mkdir -p "$(dirname "$INSTALL_ROOT")"

if [ -d "$INSTALL_ROOT/.git" ]; then
  git -C "$INSTALL_ROOT" pull --ff-only
else
  git clone "$REPO_URL" "$INSTALL_ROOT"
fi

bash "$INSTALL_ROOT/scripts/install.sh"

echo "Harness repo ready at $INSTALL_ROOT"
