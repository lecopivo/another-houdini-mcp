# DeltaMush (SOP)

## What This Node Is For

`deltamush` node behavior validated with docs + official example + live parameter play.

## Session Status

- Status: studied
- Docs read: yes (`nodes/sop/deltamush.txt`)
- Example set reviewed: yes (`examples/nodes/sop/deltamush/DeltaMushDemo.txt`)
- Example OTL/HDA internals inspected: yes
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent: from docs and example notes.
- Observed: example output 336 pts / 312 prims after mush stage.
- Live tweak: increased `iterations` 20 -> 21 on first deltamush node; topology unchanged as expected for relaxation op.
- Mismatches: none observed.

## Minimum Repro Setup

- Example was instantiated one-by-one under `/obj`, tested, then deleted before moving to next node.
- Verification used geometry probes and attribute-list checks after parameter changes.

## Gotchas and Failure Modes

- visual deformation quality changes without topology change; always verify shape not counts.
