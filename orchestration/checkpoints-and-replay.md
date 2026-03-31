# Checkpoints And Replay

This document defines how the harness should create recovery points during long-running execution.

## Purpose

Resumable memory is necessary but not sufficient.

The harness also needs explicit checkpoints so that a team can:

- recover from a bad execution branch
- hand work to another agent or person
- compare before-and-after state around risky changes

## Checkpoint Triggers

Create a checkpoint when:

- a milestone begins
- a milestone is ready to report
- a risky repair is about to start
- a major integration step is about to start
- ownership is being handed off

## Checkpoint Contents

Each checkpoint should record:

- checkpoint id
- creation time
- milestone id
- optional task id
- trigger reason
- summary of current state
- restore hint
- important artifact references

## Replay Practice

This harness does not yet implement automated state replay.

The first version supports replay by giving humans and agents enough explicit state to restart from
the checkpoint safely.

## Recorder Requirements

When a checkpoint is created:

- write it to `checkpoints/checkpoints.json`
- write a short note to `log.md`
- add a trace event

## Future Direction

Later versions can support:

- branching replay
- diffing two execution paths
- checkpoint comparison views
