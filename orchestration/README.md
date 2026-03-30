# Orchestration Layer

This directory defines how the harness should actually run.

The role files explain ownership. The orchestration files explain sequence, dispatch logic,
handoffs, inspection loops, repair routing, and milestone reporting.

Start here when you need to answer questions such as:

- how the Project Manager should decide what to dispatch next
- when to use parallel execution versus sequential execution
- when Inspectors should block advancement
- how Recorder updates should map to execution events
- when the harness should stop and report versus continue working
