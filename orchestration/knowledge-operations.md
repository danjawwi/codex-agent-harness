# Knowledge Operations

This document defines how the harness should separate project memory from reusable knowledge.

## Memory Versus Knowledge

Project memory answers:

- what is happening in this project right now?

Reusable knowledge answers:

- what did we learn that should help future projects too?

## Knowledge Candidates

Promote an item into reusable knowledge when it is:

- likely to recur across projects
- validated rather than speculative
- short enough to retrieve quickly
- useful as a pattern, warning, workaround, or checklist

Examples:

- a reliable deployment workaround
- a repeated failure pattern and its fix
- a useful review checklist
- a design pattern that proved effective

## Core Artifact

- `knowledge/knowledge-index.json`

## Capture Rules

Do not dump raw project memory into the knowledge index.

Instead, capture compact reusable items with:

- title
- kind
- short summary
- source artifact
- applicability tags
- validation date when known

## Retrieval Goals

The first version is file-backed and manual.

The goal is to make future retrieval possible through:

- tags
- source references
- structured summaries

Later versions can add search and ranking.
