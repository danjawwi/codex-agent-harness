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
- If the user or project explicitly sets a delivery expansion level, use it to decide how far to extend the work beyond the explicitly stated request.
- If no delivery expansion level is explicitly set, ignore the level system and use Codex plus the normal harness rules.
- Apply level-matched reviewable-delivery stopping only when a delivery expansion level was explicitly selected.
- Treat token or wall-clock budget as a hard stop only for explicit level 10 expansion.
- Advance work until a meaningful milestone is complete or a real blocker requires escalation.
- Do not stop after every micro-step to ask what to do next.
- Prefer milestone-level reporting with integrated status, completed work, validation outcomes, and remaining risks.
- When the user asks for harness, governance, long-running agent execution, delivery orchestration, or multi-agent coordination, use the `agent-governance-harness` skill.
