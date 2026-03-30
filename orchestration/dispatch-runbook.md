# Dispatch Runbook

This is the operational runbook for the Project Manager.

## Default Loop

1. Re-read `project.md`, `backlog.json`, `current.md`, and `log.md`.
2. Identify the active milestone.
3. Find all `ready` tasks that belong to that milestone.
4. Split those tasks into:
   - safe to run in parallel
   - must run in sequence
5. Check for conflicts:
   - shared write surfaces
   - unresolved dependencies
   - inspection gates
   - missing acceptance checks
6. Dispatch one clear task per Executor.
7. Request Recorder updates for every task transition.
8. Trigger inspection as soon as a task reports completion.
9. Route any failed inspection to repair without stopping unrelated safe work.
10. Reassess milestone status after each completed inspection.
11. Continue until the milestone is complete or a real blocker requires escalation.

## Parallel Dispatch Rules

Parallel fanout is allowed when all of the following are true:

- each task is independently understandable
- each task has its own acceptance checks
- write scope overlap is low or manageable
- inspection can be run per task or per bounded slice
- failure in one task does not invalidate all sibling tasks

Avoid parallel fanout when:

- multiple tasks edit the same fragile module
- one task's output determines another task's implementation
- integration cost is likely to exceed the speed benefit

## Sequential Dispatch Rules

Use strict sequencing when:

- a task depends on generated outputs from another task
- inspection must pass before downstream work is safe
- migration or release operations are stateful
- the architecture is still changing rapidly

## Re-dispatch Rules

After an inspection failure:

- keep the task attached to the same Executor when that is fastest and safe
- create a new repair task if the fix is substantial or should be tracked separately
- update the Recorder before any repair begins

After a pass:

- mark the task as done
- reassess downstream tasks that were waiting on it
- dispatch newly unblocked work without waiting for a chat checkpoint

## Escalation Rules

Escalate to the user only when:

- a decision has non-obvious product or technical tradeoffs
- a blocker prevents safe advancement
- inspection reveals a high-risk contradiction in the original request
- credentials, access, or external dependencies cannot be resolved internally

Otherwise, keep moving.

## Milestone Closure Rules

Do not close a milestone until:

- all required tasks are done or explicitly deferred
- milestone-level checks are satisfied
- critical inspection findings are resolved or clearly documented
- the Recorder has enough history to support replay and reporting
