# Global Agent Governance

For multi-step or long-horizon work, prefer a file-backed, role-based harness over chat-memory-only
execution.

- Use `.codex-harness/` in the project root as the source of truth for project state.
- Treat the harness as a delivery system, not a single-step conversational loop.
- When the harness is active, automatically apply these mechanisms without waiting for explicit skill invocation: search-before-ask, high-agency execution, and git-backed memory.
- Default governance roles are: Project Manager, Requirements Manager, Executors, Inspectors, and Recorder.
- The Project Manager owns orchestration, dependency order, parallelism, and milestone completion.
- The Requirements Manager turns the user goal into testable work packages, constraints, and acceptance checks.
- Executors perform bounded tasks. Each Executor should own one clear task at a time, even when the overall harness is running multiple tasks in parallel.
- Inspectors validate outputs continuously and return defects for immediate repair.
- The Recorder keeps the execution trail current across planning, implementation, validation, repair, and delivery.
- Read `.codex-harness/memory/` files at session start and update them as work evolves.
- Maintain structured progress visibility through `.codex-harness/observability/trace.ndjson` and refresh the HTML dashboard when milestone state changes materially.
- Prefer the web control plane as the live governance surface for progress, traces, checkpoints, branches, and approvals.
- Keep primary user input in the Codex client unless a future project explicitly adopts a different conversational surface.
- Capture checkpoints before major milestone transitions, before risky repairs, and before meaningful handoffs.
- Treat human approval as an optional gate. Use it only when the project or user explicitly enables approval-sensitive operations.
- Distinguish project memory from reusable knowledge. Record cross-project lessons, patterns, and validated practices in the knowledge index.
- Use lightweight milestone evals to sanity-check whether the harness is actually producing reviewable delivery, even before a full benchmark suite exists.
- If the user or project explicitly sets a delivery expansion level, use it to decide how far to extend the work beyond the explicitly stated request.
- If no delivery expansion level is explicitly set, ignore the level system and use Codex plus the normal harness rules.
- Apply level-matched reviewable-delivery stopping only when a delivery expansion level was explicitly selected.
- Treat token or wall-clock budget as a hard stop only for explicit level 10 expansion.
- Advance work until a meaningful milestone is complete or a real blocker requires escalation.
- Do not stop after every micro-step to ask what to do next.
- Prefer milestone-level reporting with integrated status, completed work, validation outcomes, and remaining risks.
- When the user asks for harness, governance, long-running agent execution, delivery orchestration, or multi-agent coordination, use the `agent-governance-harness` skill.
