# Ambiguity And Expansion

This document defines how the harness should behave when the user's request is real but incomplete.

## Core Principle

The prompt is often not the full specification.

Users frequently need to see a draft, workflow, or implemented slice before they can react with
useful criticism. Therefore the harness should not stop at the literal words of the request when a
reviewable delivery clearly requires missing horizontal or vertical details to be filled in.

The harness should complete the missing parts that are necessary to make the result reviewable.

## Horizontal And Vertical Completion

Horizontal completion means filling in the adjacent pieces required for the current slice to work
as an integrated delivery.

Vertical completion means driving one slice all the way through implementation, verification,
recording, and handoff.

The harness should avoid two distortions:

- horizontal distortion: many touched surfaces, but no complete reviewable slice
- vertical distortion: one deeply polished detail, but no meaningful integrated delivery

## Primary Control Fields

- `expansion_level_mode`
- `delivery_stop_rule`

Recommended default:

- `expansion_level_mode = explicit_only`
- `delivery_stop_rule = codex_default_unless_level_explicit`

If no level is explicitly selected by the user or project, the harness should ignore the level
system and continue with the normal Codex plus harness behavior.

## Expansion Levels

### Level 1

Scope:

- do only the explicitly requested work

Stop when:

- the explicitly requested artifact is complete and reviewable

### Level 2

Scope:

- add the direct prerequisites needed to finish the explicit request

Stop when:

- the requested artifact and its immediate dependencies are complete and reviewable

### Level 3

Scope:

- fill in enough missing work to create the minimum runnable or usable closed loop for the current task

Stop when:

- the current task is no longer a fragment and instead forms a working closed loop

### Level 4

Scope:

- extend to the minimum reviewable feature slice

Stop when:

- the user can review one coherent slice rather than isolated partial work

### Level 5

Scope:

- reach a common-practice complete slice for the current feature

Stop when:

- the current feature feels normally complete enough for serious review in common practice

### Level 6

Scope:

- extend into adjacent support work that is usually expected, such as basic error handling, handoff notes, or operational polish

Stop when:

- the feature slice works with the nearby support work that a reviewer would normally expect

### Level 7

Scope:

- connect adjacent workflow steps so the delivered slice feels operationally coherent

Stop when:

- the reviewer can follow the slice through the neighboring workflow without obvious gaps

### Level 8

Scope:

- deepen integration, edge handling, and handoff quality for the milestone slice

Stop when:

- the milestone slice is integrated, validated, and ready for sustained team review or handoff

### Level 9

Scope:

- proactively build a strong draft of the broader implied solution, not just the narrow requested slice

Stop when:

- the reviewer can assess a substantial and coherent draft of the intended direction

### Level 10

Scope:

- maximize useful extension and completion beyond the explicit request

Stop when:

- the strongest available reviewable delivery has been assembled within the configured hard budget

Level 10 is the only level that should use token or wall-clock budget as a hard outer boundary.

## Stop Rule

If no level is explicitly selected, normal Codex plus harness stop behavior applies.

If a level is explicitly selected, `delivery_stop_rule = match_level_reviewable_delivery` means:

- do not stop because a small intermediate task finished
- do not stop because the first acceptable local patch exists
- stop when the deliverable implied by the chosen expansion level is actually reviewable

This makes stopping a delivery decision, not a conversational pause.

## Level 10 Budget

Only explicit level 10 should use hard runtime budget controls such as:

- wall-clock limit
- token limit
- parallelism limit

If the budget ends before the expansion frontier is naturally exhausted, the harness should:

1. package the best integrated delivery reached so far
2. make the remaining obvious extensions explicit
3. preserve the state in recorder and memory artifacts

## Project Manager Guidance

The Project Manager should choose the smallest explicit expansion level that still creates a meaningful
reviewable delivery when the level system is being used.

Do not use any expansion level by default.
Do not use level 10 unless broader autonomy is explicitly wanted.

Prefer lower levels when:

- the requested scope is already clear
- the reviewable artifact is narrow
- the user wants strict obedience to the stated request

Prefer higher levels when:

- the user's intent is obvious but under-specified
- the user needs a draft in order to react
- common practice strongly suggests missing supporting work

## Recorder Guidance

Record these items when expansion matters:

- chosen explicit expansion level
- the level-matched `delivery_target`
- what missing requirements were inferred
- what common-practice additions were included
- what was intentionally deferred
