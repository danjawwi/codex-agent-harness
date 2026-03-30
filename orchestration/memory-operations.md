# Memory Operations

This document defines how memory should be captured, read, and synchronized.

## Session Start

At the beginning of a harness-controlled session, read:

- `project.md`
- `backlog.json`
- `current.md`
- `log.md`
- `memory/memory-index.json`
- `memory/active-context.md`
- `memory/handoff.md`

Only then resume execution.

## During Execution

Update memory when any of the following occur:

- a milestone starts or completes
- a major decision is made
- an inspection fails
- a repair changes the execution path
- work is handed off between agents or people

## Session End

Before stopping a meaningful work cycle:

- update `active-context.md`
- append key facts to `observations.ndjson`
- update `handoff.md`
- update `project-summary.md` when milestone state changed

## Git Sync Practice

Recommended practice:

- commit memory changes with milestone work
- or use dedicated memory commits for handoff points
- pull or rebase before writing large memory updates

## Team Collaboration

For multiple collaborators:

- do not overwrite handoff information casually
- prefer append-only observation records
- keep decision logs readable to both humans and agents
- use milestone reports as synchronization anchors
