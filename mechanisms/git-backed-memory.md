# Git-Backed Memory

This mechanism is inspired by persistent-memory systems such as claude-mem, but adapted for Codex
using tools available today.

## Why This Exists

Codex contains signs of an internal memories system, but in the current local installation the
feature is not active enough to trust as the primary operational memory layer.

Therefore the harness uses a repository-backed memory model as the default durable memory system.

## Default Memory Location

Project memory lives inside:

- `.codex-harness/memory/`

Recommended files:

- `memory-index.json`
- `active-context.md`
- `observations.ndjson`
- `decision-log.md`
- `handoff.md`
- `project-summary.md`

## Local Storage Model

Local disk is the working memory source of truth during execution.

The agent should:

- read memory files at session start
- update memory files during milestone progress
- write repair, inspection, and handoff information immediately
- avoid storing important state only in chat history

## GitHub Synchronization Model

Git is the sync transport.

The intended workflow is:

1. memory files are updated locally in the project repo
2. memory changes are committed with normal work or dedicated memory commits
3. GitHub becomes the remote durable store
4. other collaborators pull and continue from the same memory state

This keeps the memory system inspectable, diffable, reviewable, and compatible with normal team
workflows.

## Multi-Person Collaboration Rules

For teams, treat `.codex-harness/memory/` like structured project metadata:

- pull before starting major work
- rebase or merge memory changes promptly
- avoid rewriting history for memory files
- prefer append-only logs for observations and handoffs
- use explicit handoff records when switching owners

## What This Does Better Than Hidden Memory

- visible to humans
- versioned in Git
- syncable through GitHub
- reviewable in pull requests
- resumable across tools and sessions

## What This Does Not Automatically Provide

- semantic retrieval by itself
- vector search by itself
- automatic cross-project ranking

Those can be added later, but the baseline system should first be durable and simple.
