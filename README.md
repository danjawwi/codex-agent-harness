# Codex Agent Harness

This repository stores a reusable governance harness for Codex.

It is designed for long-running project work where the agent should:

- initialize a project once
- break work into 5-10 features
- execute one feature at a time
- persist progress to disk
- resume from artifacts instead of chat memory

## Repository Layout

- `AGENTS.md`: global governance guidance
- `config/harness-config.toml`: optional Codex config defaults for long-context work
- `skills/agent-governance-harness/`: reusable skill and initializer script
- `scripts/install.sh`: syncs the harness into `~/.codex`

## Install

```bash
bash scripts/install.sh
```

## What Gets Installed

- `~/.codex/AGENTS.md`
- `~/.codex/skills/agent-governance-harness/`

The config file is not merged automatically because many Codex installs already have personal
model and MCP settings. Review `config/harness-config.toml` before copying values into
`~/.codex/config.toml`.

## Typical Usage

Inside a project:

```bash
python3 ~/.codex/skills/agent-governance-harness/scripts/init_harness.py --root "$PWD" --goal "Your project goal"
```

Then ask Codex to use the harness and work one feature at a time.
