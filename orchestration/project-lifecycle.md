# Project Lifecycle

This document defines the default lifecycle for a milestone-driven Codex harness.

## Phase 1: Intake

Owned by:

- Project Manager
- Requirements Manager

Objectives:

- understand the user's actual goal
- identify scope boundaries, constraints, and risk areas
- define the first delivery milestone

Exit conditions:

- project goal is written down
- the first milestone is meaningful to the user
- the backlog has initial tasks or workstreams

## Phase 2: Structuring

Owned by:

- Requirements Manager
- Recorder

Objectives:

- break work into bounded tasks
- attach acceptance checks
- mark dependencies and potential parallel groups
- record assumptions explicitly

Exit conditions:

- tasks are actionable
- tasks are small enough for one Executor to own at a time
- dependencies are clear enough for dispatch

## Phase 3: Dispatch

Owned by:

- Project Manager

Objectives:

- choose the next ready tasks
- decide which tasks can run concurrently
- assign one clear task per Executor

Exit conditions:

- all dispatched tasks are ready
- no dispatched pair creates an unsafe write conflict
- the current milestone remains coherent

## Phase 4: Execution

Owned by:

- Executors

Objectives:

- produce the assigned artifacts
- stay inside task boundaries
- surface follow-up work without silently expanding scope

Exit conditions:

- artifact is produced
- implementation notes are available
- work is ready for inspection

## Phase 5: Inspection

Owned by:

- Inspectors

Objectives:

- verify the output against acceptance checks
- identify regressions or gaps
- decide whether the task passes, fails, or partially passes with a recorded risk

Exit conditions:

- pass, fail, or risk status is explicit
- defects are routed immediately if found

## Phase 6: Repair

Owned by:

- Executors
- Inspectors

Objectives:

- fix concrete defects found during inspection
- re-run the relevant checks
- avoid opening unrelated work unless the defect requires it

Exit conditions:

- the defect is resolved, or
- the unresolved issue is explicitly recorded as a risk or blocker

## Phase 7: Integration

Owned by:

- Project Manager
- Inspectors
- Recorder

Objectives:

- combine completed task outputs into the milestone slice
- confirm cross-task compatibility
- make sure milestone acceptance is still true after integration

Exit conditions:

- completed tasks work together
- integration defects are either fixed or recorded

## Phase 8: Milestone Report

Owned by:

- Project Manager
- Recorder

Objectives:

- summarize completed work
- summarize validation outcomes
- summarize repairs and remaining risks
- recommend the next milestone

Exit conditions:

- report is accurate
- milestone status is explicit
- next step is clear
