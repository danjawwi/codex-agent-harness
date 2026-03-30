# Harness Roles

These role definitions are the first concrete interface layer for the Codex Agent Harness.

They describe who owns planning, decomposition, execution, inspection, and recording in a
long-running multi-agent delivery system.

The baseline roles are:

- `project-manager.md`
- `requirements-manager.md`
- `executor.md`
- `inspector.md`
- `recorder.md`

Future harness variants may refine or split these further, but specialized variants should inherit
from this shared base model instead of replacing it ad hoc.
