# Duplicate (SOP)

## What This Node Is For

`duplicate` node behavior validated with docs + official example + live parameter play.

## Session Status

- Status: studied
- Docs read: yes (`nodes/sop/duplicate.txt`)
- Example set reviewed: yes (`examples/nodes/sop/duplicate/DuplicateBox.txt`)
- Example OTL/HDA internals inspected: yes
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent: from docs and example notes.
- Observed: baseline duplicate output 48 pts / 36 prims.
- Live tweak: increased `ncy` 5 -> 6; output became 56 pts / 42 prims.
- Mismatches: none observed.

## Minimum Repro Setup

- Example was instantiated one-by-one under `/obj`, tested, then deleted before moving to next node.
- Verification used geometry probes and attribute-list checks after parameter changes.

## Gotchas and Failure Modes

- duplicate appends copies to source, so growth is additive and can escalate quickly.
