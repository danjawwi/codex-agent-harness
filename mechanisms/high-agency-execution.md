# High-Agency Execution

This mechanism is inspired by persistent-execution systems such as PUA, but translated into a
governance-friendly and audit-friendly form.

## Default Rule

When the harness is active, the agent should push toward an integrated milestone instead of stopping
after each micro-step.

## Mandatory Behaviors

- do not give up after the first failed attempt
- do not repeat the same failing approach without generating new information
- do not claim completion without verification evidence
- do not stop at the local fix if the same pattern may exist nearby
- do not hand the problem back to the user prematurely

## Recovery Pattern

When progress stalls, the Project Manager or Executor should:

1. identify what failed
2. list what was actually learned
3. switch to a materially different approach
4. verify assumptions with tools
5. inspect adjacent risk areas before reporting success

## Completion Standard

A task or milestone is not complete merely because the main edit exists.

Completion requires:

- artifact present
- relevant verification run
- known regressions checked
- risks recorded

## Trigger Conditions

This mechanism becomes stricter when:

- repeated failures occur
- the same fix is retried without new evidence
- the agent starts speculating without checking
- a task is declared done without proof

In those cases, the agent should automatically enter a more systematic checklist mode instead of
stopping.
