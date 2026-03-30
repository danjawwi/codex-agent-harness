# Codex Agent Harness

This repository is the shared home for how we design, operate, govern, deliver, and evolve
agent-based work in Codex.

It is not only a config dump. It is the place where we align on how agents should work, how
multiple agents should collaborate, how work should be verified, how execution should be recorded,
and how a long-running delivery process should reach a meaningful milestone before reporting back.

The first version is a general-purpose harness. Later versions can branch into specialized harnesses
for different kinds of agents, projects, teams, and delivery environments.

## Why This Repository Exists

We want one place to maintain the governance needed for real agent execution, including:

- how a request is received and understood
- how a project is decomposed into manageable work
- how subagents are assigned and coordinated
- how execution is verified instead of merely claimed
- how errors are repaired without stopping the whole process
- how progress, decisions, and outcomes are recorded for replay and audit
- how finished work is packaged, delivered, and eventually published

This repository is meant to become that long-term coordination layer.

## Core Belief

The harness should not behave like a chat assistant that takes one step, stops, asks again, and
repeats that loop forever.

The harness should behave like a delivery organization:

- receive a goal
- understand the goal deeply enough to break it apart
- execute multiple related streams of work
- verify each stream as it completes
- repair problems immediately
- continue moving until a meaningful long-cycle outcome is complete
- report back after an integrated stage of work is actually done

In other words, feedback should happen at milestone boundaries, not after every tiny action.

## First-Principles Execution Model

The initial harness architecture is built around five functional roles.

### 1. Project Manager

The Project Manager owns the overall delivery rhythm.

Responsibilities:

- convert a user goal into a project-level execution objective
- determine what should run in parallel and what must run in sequence
- maintain the overall dependency graph
- decide milestone boundaries and integration checkpoints
- keep the system moving forward until a meaningful delivery stage is complete

The Project Manager is not the main implementer. It is the orchestrator of execution.

### 2. Requirements Manager

The Requirements Manager turns a broad request into clear, testable work units.

Responsibilities:

- clarify the intent of the request
- split the request into subprojects, workstreams, and tasks
- define success conditions and acceptance checks
- identify hidden constraints, assumptions, and risks
- keep the scope coherent as the project evolves

In some projects, the Project Manager and Requirements Manager can be combined. In more complex
projects, they should be treated as separate roles.

### 3. Executors

Executors are the worker agents that actually perform the implementation work.

Responsibilities:

- take on a concrete task or work package
- perform implementation, setup, migration, integration, release prep, or operational work
- report concrete artifacts, not vague status language
- hand completed work to inspection

There can be many Executors running at the same time. Some tasks are parallel, some have strict
ordering constraints, and the harness must support both.

### 4. Inspectors

Inspectors do not own execution. They own validation.

Responsibilities:

- check whether a task was actually completed
- test whether the result matches the requirement
- identify defects, missing pieces, regressions, or weak assumptions
- return issues quickly so Executors can repair them
- inspect not only Executor work, but also planning and decomposition quality when needed

There can be multiple Inspectors. Inspection should be continuous, not delayed until the very end.

### 5. Recorder

The Recorder maintains the full execution trail.

Responsibilities:

- record tasks, state changes, decisions, blockers, repairs, and outcomes
- keep the work replayable and auditable
- preserve context across long-running sessions
- make it possible to resume after compaction, interruption, or thread changes
- produce a final history of what happened, why it happened, and what remains

The Recorder runs throughout the project, not only at the end.

## How Work Should Flow

The default work cycle for this harness is:

1. A user provides a goal.
2. The Project Manager and Requirements Manager translate that goal into a structured project.
3. The work is split into tasks, grouped by dependency and parallelism.
4. Executors are dispatched across the work graph.
5. Inspectors validate completed work continuously.
6. If a problem is found, repair happens immediately and execution continues.
7. The Recorder updates the project trail in real time.
8. The harness keeps moving until an integrated milestone is complete.
9. Only then does the harness provide a consolidated status back to the user.

This is intentionally not a one-step-at-a-time human approval loop.

## Parallel And Sequential Work

The harness must support mixed execution patterns.

### Parallel work

Use parallel execution when:

- tasks do not share a write surface
- tasks are independent enough to validate separately
- speed matters and the dependency graph allows fanout

Typical examples:

- frontend and backend scaffolding
- implementation and documentation
- multiple bounded feature workers
- validation workers that can inspect completed slices independently

### Sequential work

Use sequential execution when:

- one task depends on the output of another
- inspection must pass before downstream work is safe
- integration order affects correctness
- migration or release steps have stateful dependencies

The Project Manager should decide which path is appropriate, not the Executor acting alone.

## Verification Before Advancement

The harness should not treat "implemented" as equivalent to "done".

A task only advances when:

- the expected artifact exists
- the expected behavior is present
- the relevant checks have been run
- obvious regressions have been examined
- any discovered issue has either been fixed or explicitly recorded

If inspection fails, the work returns to execution immediately. The system should not stop just to
announce that failure unless a real blocker requires escalation.

## Long-Cycle Delivery Instead Of Tiny-Step Reporting

One of the key design choices in this harness is reporting cadence.

We do not want:

- execute one small action
- stop
- ask the user what to do next
- repeat indefinitely

We do want:

- receive a meaningful goal
- execute across related workstreams
- verify and repair while moving
- integrate the outputs
- report after a substantial delivery slice is complete

This means the harness should optimize for sustained momentum, not conversational checkpointing.

## Artifact-Backed Governance

This repository starts from a file-backed operating model because chat memory is not enough for
long-running execution.

The default project runtime artifacts are:

- `.codex-harness/project.md`
- `.codex-harness/backlog.json`
- `.codex-harness/current.md`
- `.codex-harness/log.md`

These files make the project resumable and reviewable across compaction, session changes, and long
delivery timelines.

## Repository Scope

Over time, this repository should hold the shared governance assets for:

- general Codex harness behavior
- role definitions for multi-agent collaboration
- planning and decomposition rules
- execution and inspection loops
- recorder formats and project logs
- release and delivery governance
- templates for project initialization
- specialized harness variants for different agent types

This repository is the base layer, not the final layer.

## General Harness First, Specialized Harness Later

Different agents need different harnesses.

That is expected.

The current strategy is:

- first, define a strong general-purpose harness
- second, prove that it works across real projects
- third, split out specialized harnesses for different domains and execution styles

Possible future variants include:

- product-build harness
- coding-delivery harness
- research-and-synthesis harness
- release-and-operations harness
- QA-heavy verification harness
- design-to-code harness

The general harness should establish the common governance contract that all specialized harnesses
inherit from.

## Current Repository Layout

- `AGENTS.md`: high-level governance defaults for Codex
- `config/harness-config.toml`: optional Codex config values for long-context work
- `skills/agent-governance-harness/`: the reusable skill and runtime initializer
- `scripts/install.sh`: syncs the harness assets into `~/.codex`

## Installation

```bash
bash scripts/install.sh
```

This installs:

- `~/.codex/AGENTS.md`
- `~/.codex/skills/agent-governance-harness/`

The config file is stored separately on purpose because personal Codex installs often already have
their own model, MCP, and environment settings.

## Typical Usage

Inside a project:

```bash
python3 ~/.codex/skills/agent-governance-harness/scripts/init_harness.py --root "$PWD" --goal "Your project goal"
```

Then instruct Codex to use the harness and drive the project toward a milestone, not just a single
micro-step.

## Near-Term Evolution

The next iterations of this repository should define:

- concrete role interfaces for Project Manager, Requirements Manager, Executor, Inspector, and Recorder
- task schemas and dependency graph formats
- inspection schemas and repair loops
- milestone definitions and handoff criteria
- release and publish governance for completed agent work
- specialized harness packages that extend the shared base model

This repository begins as a governance home. It should evolve into a full operating system for
serious multi-agent delivery.
