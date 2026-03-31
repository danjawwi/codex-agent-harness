# Control Plane

This document defines the first interactive governance surface for the harness.

## Purpose

The harness should not be visible only through chat and raw files.

It should also expose a human-readable and human-actionable control plane that shows:

- current task progress
- current slice and milestone progress
- recent execution trace
- checkpoints
- branch graph
- approvals when enabled

## Recommended Operating Model

Use a split-screen setup:

- Codex client on one screen for voice input, task instructions, and primary execution
- control plane web page on the other screen for live progress visibility and governance actions

This keeps the strongest input modality in Codex while giving humans a dedicated review surface.

## Page Responsibilities

The first version of the page should provide:

- milestone overview and progress bars
- active tasks and status counts
- recent trace timeline
- checkpoint list
- branch graph
- approval actions when enabled
- knowledge and light eval summaries

## Input Model

Primary task input should remain in the Codex client.

The web control plane is for:

- observation
- review
- optional approval actions
- branch and checkpoint understanding

It is not the primary conversational surface.

## Refresh Model

The first version should support automatic polling refresh.

This is simpler than a real-time streaming system and is enough for practical use.

## Future Direction

Later versions can add:

- websocket or server-sent event updates
- richer branch diffing
- inline checkpoint creation
- task drill-down views
- role-specific views
