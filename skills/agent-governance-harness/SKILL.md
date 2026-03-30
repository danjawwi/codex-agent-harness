---
name: agent-governance-harness
description: Use when the user wants long-running agent governance, Anthropic-style harness behavior, feature-by-feature execution, external state artifacts, project initialization, backlog-driven work, or single-feature constraints in Codex.
---

# Agent Governance Harness

Use this skill when the user asks for a harness, governance, long-horizon work, external state, initializer-worker-artifact patterns, or single-feature execution.

## Goal

Run project work from disk-backed artifacts instead of relying on conversation memory.

## Default Artifact Layout

Use `.codex-harness/` in the project root. If it does not exist, initialize it with:

```bash
python3 ~/.codex/skills/agent-governance-harness/scripts/init_harness.py --root "$PWD"
```

Default files:

- `project.md`: goal, constraints, repo facts, definition of done
- `backlog.json`: 5-10 concrete features with status and acceptance checks
- `current.md`: the one feature currently being executed
- `log.md`: append-only record of verification, blockers, touched files, and next step

## Initializer

Run once per project, or again only if scope changed enough that the old backlog is no longer valid.

- Read the repo and user request before planning.
- Write the project goal, constraints, and done definition to `project.md`.
- Break the work into 5-10 concrete features in `backlog.json`.
- Make features commit-sized: one worker cycle should usually finish one feature.
- Promote only features with clear acceptance checks to `ready`.

## Worker Loop

For each execution cycle:

1. Re-read `.codex-harness/` artifacts.
2. Pick exactly one `ready` feature.
3. Copy its title, acceptance checks, and planned verification into `current.md`.
4. Implement only that feature.
5. Run best-effort verification for that feature.
6. Update `backlog.json`, `current.md`, and `log.md`.
7. Stop after that feature unless the user explicitly asks to continue.

## Single-Feature Constraint

- Do not work on two backlog items in the same cycle.
- If you notice follow-up work, record it and leave it for the next cycle.
- Prefer small, reviewable diffs over large end-to-end rewrites.

## Artifact Rules

- Disk artifacts are the source of truth after compaction, resume, or a new thread.
- Chat summaries stay short; important state goes into the harness files.
- Record blockers and assumptions in `log.md`, not only in the assistant message.
- If verification is skipped or partial, write that down explicitly.

## Suggested Status Values

Keep feature status to:

- `pending`
- `ready`
- `in_progress`
- `blocked`
- `done`

## Small-Task Shortcut

If the task is a single small edit, the full harness is optional. For anything that feels like a project, use the harness.
