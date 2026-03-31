# Light Eval

This document defines the first-pass evaluation layer for the harness.

## Purpose

A full benchmark program can come later.
The first step is a lightweight eval practice that checks whether milestone delivery is becoming
more reliable over time.

## Scope

This version should stay small and practical.

Good first evals include:

- a few representative milestone tasks
- one or two failure-heavy tasks
- one repair-heavy task
- one handoff-and-resume task

## Eval Questions

The light eval layer should answer:

- did the harness produce a reviewable deliverable?
- did the trace and log stay coherent?
- did inspection catch meaningful issues?
- was the result resumable after interruption?

## Core Artifact

- `evals/eval-suite.json`

## Recorder Requirements

When a milestone is reported:

- update the relevant eval case status when possible
- record why a case passed, failed, or is still unknown
- keep the eval suite small enough to remain useful

## Future Direction

Later versions can add:

- automated grading
- regression suites
- configuration comparisons
- benchmark dashboards
