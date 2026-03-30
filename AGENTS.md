# Global Agent Governance

For multi-step or long-horizon work, prefer a file-backed harness over chat-memory-only execution.

- If the task is larger than one meaningful feature, use `.codex-harness/` in the project root.
- Keep these files as the source of truth: `project.md`, `backlog.json`, `current.md`, `log.md`.
- Run an initializer once: restate the goal, constraints, and 5-10 concrete features with acceptance checks.
- Run workers in a single-feature loop: pick exactly one ready feature, implement it, verify it, then update artifacts.
- Do not batch multiple backlog items in one cycle unless the user explicitly asks for that tradeoff.
- After each cycle, record touched files, verification, blockers, and the recommended next feature in `log.md`.
- When a thread resumes or context is compacted, reload the harness files first and trust them over chat history.
- Prefer commit-sized diffs and best-effort verification after each completed feature.
- When the user asks for harness/governance/long-running-agent behavior, use the `agent-governance-harness` skill.
