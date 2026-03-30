# State Transitions

This document defines the first-pass transition rules for tasks and milestones.

## Task States

Allowed task states:

- `pending`
- `ready`
- `in_progress`
- `blocked`
- `done`

## Task Transition Rules

### `pending -> ready`

Allowed when:

- the task has a clear title
- the task has acceptance checks
- dependencies are either empty or already satisfied

### `ready -> in_progress`

Allowed when:

- an Executor has been assigned
- the active milestone still requires this task
- the write scope is safe relative to other active tasks

### `in_progress -> blocked`

Allowed when:

- an unresolved dependency stops safe progress
- required access, data, or external state is missing
- inspection reveals a prerequisite issue outside the task's current control

### `blocked -> ready`

Allowed when:

- the blocking condition is resolved
- the task can resume without redefining scope

### `in_progress -> done`

Allowed when:

- the artifact exists
- acceptance checks are satisfied or explicitly passed by inspection
- relevant verification is complete

### `done -> ready`

Allowed only when:

- inspection or integration later reveals a real defect
- the reopened work is explicitly recorded

Avoid reopening tasks casually. Reopen only with evidence.

## Milestone States

Allowed milestone states:

- `pending`
- `ready`
- `in_progress`
- `blocked`
- `done`

## Milestone Transition Rules

### `pending -> ready`

Allowed when:

- the milestone goal is clear
- the milestone is meaningful to the user
- there is at least one actionable task or workstream

### `ready -> in_progress`

Allowed when:

- at least one task under the milestone enters active dispatch
- the Project Manager commits to this milestone as the current integration target

### `in_progress -> blocked`

Allowed when:

- a critical blocker prevents reliable completion
- unresolved risks make continued execution unsafe

### `blocked -> in_progress`

Allowed when:

- the blocker is resolved
- the milestone plan is still valid enough to continue

### `in_progress -> done`

Allowed when:

- required tasks are completed or intentionally deferred
- milestone acceptance is satisfied
- milestone report is recorded

## Recorder Requirements

Every state transition should be mirrored in `log.md` or a structured log stream with:

- timestamp
- role
- object type
- object id
- old state
- new state
- short reason
