# Inspection And Repair Loop

This document defines the standard loop between Executors and Inspectors.

## Purpose

Inspection should produce a concrete validation record.
Repair should produce a concrete remediation record.

The harness should avoid informal "looks good" or "please fix this" exchanges that cannot be
replayed later.

## Inspection Flow

1. Executor declares the task ready for inspection.
2. Inspector reads the task definition, acceptance checks, and relevant artifacts.
3. Inspector produces an inspection record.
4. The record result must be one of:
   - `pass`
   - `fail`
   - `pass_with_risk`
5. Recorder logs the inspection outcome immediately.

## When Inspection Passes

- mark the task as `done`
- release downstream tasks that were waiting on the pass
- include evidence in the milestone record if the pass is important to integration

## When Inspection Fails

- do not treat the task as complete
- create or update a repair record
- route the repair back to the owning Executor when practical
- record whether the failed task blocks the wider milestone or only that local slice

## When Inspection Passes With Risk

Use `pass_with_risk` only when:

- the task is good enough for milestone advancement
- the remaining issue is understood
- the risk is explicitly recorded

Avoid overusing this state. It should not become a shortcut for skipping real fixes.

## Repair Flow

1. Start from a failed inspection record.
2. Create a repair record with requested fixes.
3. Executor performs the repair.
4. Run the stated post-repair verification.
5. Return the task to inspection if the repair changes acceptance-critical behavior.
6. Recorder logs the repair outcome.

## Repair Routing Rules

- small defects can stay on the same task
- large defects can become explicit child repair tasks
- if the repair changes scope materially, Requirements Manager should update the backlog

## Blocking Rules

An inspection failure blocks the whole milestone only when:

- the failed task is on the critical path
- the defect invalidates sibling work
- the risk is too high to continue safely

Otherwise, unrelated safe work may continue.
