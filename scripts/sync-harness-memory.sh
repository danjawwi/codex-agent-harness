#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="${1:-$(pwd)}"

if [ ! -d "$REPO_ROOT/.git" ]; then
  echo "Not a git repository: $REPO_ROOT" >&2
  exit 1
fi

if [ ! -d "$REPO_ROOT/.codex-harness" ]; then
  echo "Missing .codex-harness in $REPO_ROOT" >&2
  exit 1
fi

git -C "$REPO_ROOT" add .codex-harness

if git -C "$REPO_ROOT" diff --cached --quiet; then
  echo "No harness memory changes to sync."
  exit 0
fi

git -C "$REPO_ROOT" commit -m "Sync harness memory"

if git -C "$REPO_ROOT" rev-parse --abbrev-ref "@{upstream}" >/dev/null 2>&1; then
  git -C "$REPO_ROOT" pull --rebase --autostash
  git -C "$REPO_ROOT" push
  exit 0
fi

current_branch="$(git -C "$REPO_ROOT" branch --show-current)"

if git -C "$REPO_ROOT" remote get-url origin >/dev/null 2>&1; then
  git -C "$REPO_ROOT" push -u origin "$current_branch"
  exit 0
fi

echo "Committed harness memory locally. No remote is configured, so remote sync was skipped."
