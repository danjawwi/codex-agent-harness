# Search Before Ask

This mechanism makes the harness prefer internal investigation before interrupting the user.

## Default Rule

Before asking the user for clarification or blaming the environment, the agent should first:

- inspect relevant local files
- inspect logs and error output
- search the codebase for related patterns
- search official docs or authoritative sources when needed
- verify assumptions about paths, permissions, configuration, versions, and dependencies

## Escalate Only After Search

Escalation is allowed only when:

- a real ambiguity remains after investigation
- the decision has meaningful product or risk tradeoffs
- credentials, accounts, or hidden external context cannot be discovered safely

## Why It Exists

This mechanism captures the strongest practical effect of high-agency systems:

- fewer passive questions
- fewer guessed explanations
- more grounded execution
