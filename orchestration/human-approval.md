# Human Approval

This document defines optional approval gates for actions that should not always proceed
autonomously.

## Important Default

Approval is optional and disabled by default.

Do not require approval just because the user described the request imperfectly.
Incomplete requirements should normally be handled through exploration, drafting, and reviewable
delivery, not automatic escalation to approval.

## When Approval Helps

Approval is useful when the action has higher external consequence, such as:

- production release
- destructive delete or irreversible migration
- expensive paid external action
- security-sensitive permission change
- large-scale repo rewrite

## Approval States

- `pending`
- `approved`
- `rejected`
- `changes_requested`

## Recorder Requirements

If approvals are enabled:

- record approval requests in `approvals/approvals.json`
- write a trace event for request and resolution
- keep the dashboard current so pending approvals are visible

## Decision Rule

Do not expand the approval system into normal day-to-day implementation work.
Use it narrowly where human signoff is genuinely protective.
