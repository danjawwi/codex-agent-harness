---
name: agent-governance-harness
description: Use when the user wants long-running agent governance, role-based multi-agent orchestration, milestone-driven execution, external state artifacts, execution inspection, repair loops, backlog-driven work, or Codex delivery harness behavior.
---

# Agent Governance Harness

Use this skill when the user asks for a harness, governance, long-horizon work, multi-agent
delivery, external state, project decomposition, inspection loops, or milestone-based execution.

## Goal

Run project work as a sustained, role-based delivery process backed by disk artifacts instead of
relying on conversation memory alone.

## Governance Model

Default functional roles:

- `Project Manager`: owns orchestration, dependency order, milestone boundaries, and overall flow
- `Requirements Manager`: turns the user goal into work packages, acceptance checks, and constraints
- `Executors`: implement bounded tasks and produce concrete artifacts
- `Inspectors`: validate work continuously and return defects for repair
- `Recorder`: records decisions, state changes, progress, blockers, repairs, and outcomes

The Project Manager and Requirements Manager may be combined in smaller projects.

## References

Open these only when needed:

- `references/orchestration/`: lifecycle, dispatch, and state-transition runbooks
- `references/roles/`: role contracts for Project Manager, Requirements Manager, Executor, Inspector, and Recorder
- `references/schemas/backlog.schema.json`: backlog and milestone structure
- `references/schemas/task.schema.json`: task contract for bounded executor work
- `references/schemas/log-entry.schema.json`: structured logging contract
- `references/templates/`: starter artifacts for `project.md`, `current.md`, `log.md`, `backlog.json`, and milestone reports

## Default Artifact Layout

Use `.codex-harness/` in the project root. If it does not exist, initialize it with:

```bash
python3 ~/.codex/skills/agent-governance-harness/scripts/init_harness.py --root "$PWD"
```

Default files:

- `project.md`: goal, constraints, governance model, repo facts, and definition of done
- `backlog.json`: workstreams, tasks, states, dependencies, acceptance checks, and notes
- `current.md`: active milestone, active tasks, planned verification, and integration notes
- `log.md`: append-only record of execution, inspection, repairs, blockers, and milestone outcomes

## Initializer

Run once per project, or again only if the scope changed enough that the old plan is no longer
reliable.

- Read the repo and user request before planning.
- Define the project goal, constraints, and done definition in `project.md`.
- Split the request into 5-10 major workstreams, features, or delivery slices.
- For each slice, define acceptance checks and key dependencies.
- Mark which work can run in parallel and which must run in order.
- Establish the first milestone rather than only the first tiny task.

## Execution Model

The harness should not stop after every small action.

Default cycle:

1. Re-read `.codex-harness/` artifacts.
2. Select the current milestone or delivery slice.
3. Dispatch ready tasks across one or more Executors.
4. Keep each Executor on one clear task at a time.
5. Run Inspectors continuously as work completes.
6. Repair failures immediately when practical.
7. Record all task transitions and validation outcomes in `log.md`.
8. Continue until the milestone is complete or a real blocker requires escalation.
9. Report back with an integrated milestone update.

## Parallel And Sequential Work

- Use parallel execution when tasks are bounded, independent enough, and safe to validate separately.
- Use sequential execution when downstream work depends on upstream outputs or inspections.
- Let the Project Manager choose the dependency strategy; Executors should not decide global flow on their own.

## Inspector Rules

- Do not accept "implemented" as "done" without validation.
- Check that artifacts exist, behavior matches the requirement, and relevant verification has been run.
- When a failure is found, route it back for repair and keep the overall project moving if possible.
- Inspect planning quality too when decomposition or acceptance criteria look weak.

## Recorder Rules

- Important state belongs in artifacts, not only in chat replies.
- Record progress, defects, repairs, and milestone outcomes as they happen.
- Keep the project resumable after compaction, interruption, or thread changes.
- Preserve enough detail for audit and replay, but keep logs concise and structured.

## Reporting Cadence

- Prefer milestone-level feedback over micro-step feedback.
- Escalate early only for real blockers, unsafe assumptions, or decisions with non-obvious consequences.
- Otherwise continue executing, inspecting, and integrating until a meaningful stage is complete.

## Small-Task Shortcut

If the task is a single tiny edit, the full harness is optional. For anything that feels like a
project, use the harness.
