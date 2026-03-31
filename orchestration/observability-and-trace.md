# Observability And Trace

This document defines how execution progress should become visible to both humans and agents.

## Purpose

The harness should not force collaborators to reconstruct progress from scattered chat turns.

Instead, it should maintain:

- a structured trace stream
- milestone-level summaries
- a static HTML dashboard that a human can open and review quickly

## Core Artifacts

- `observability/trace.ndjson`
- `dashboard/index.html`
- `log.md`
- `current.md`

## Trace Model

Each meaningful execution event should be written as a structured trace event.

Good candidates include:

- milestone started
- task dispatched
- task completed
- inspection passed
- inspection failed
- repair requested
- repair completed
- checkpoint created
- approval requested
- approval granted
- eval executed
- dashboard refreshed

## Display Goals

The HTML dashboard should answer these questions quickly:

- what is the project trying to achieve?
- what milestone is active?
- how many tasks are pending, in progress, blocked, and done?
- what happened recently?
- are approvals pending?
- what checkpoints exist?
- what eval status do we have?
- what knowledge has been captured?

## Recorder Requirements

The Recorder should keep the trace stream current enough that the dashboard can be regenerated
without guessing.

At a minimum:

- log milestone transitions
- log task transitions
- log inspection and repair outcomes
- log checkpoint creation
- log approval events when approvals are enabled

## Dashboard Refresh Rules

Refresh the dashboard when:

- a milestone starts or ends
- task distribution changes materially
- a new checkpoint is created
- an approval becomes pending, approved, or rejected
- a light eval result changes

## Scope For This Version

This first version is intentionally simple:

- static HTML
- file-backed inputs
- no server required
- no live streaming required

It is meant to be practical immediately, not perfect.
