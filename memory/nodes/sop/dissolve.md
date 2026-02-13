# Dissolve (SOP)

## What This Node Is For

`dissolve` node behavior validated with docs + official example + live parameter play.

## Session Status

- Status: studied
- Docs read: yes (`nodes/sop/dissolve.txt`)
- Example set reviewed: yes (`examples/nodes/sop/dissolve/DissolveBox.txt`)
- Example OTL/HDA internals inspected: yes
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent: from docs and example notes.
- Observed: `dissolve_edge` baseline: 8 pts / 5 prims.
- Live tweak: set `invertsel` 0 -> 1; output collapsed to 2 pts / 1 prim.
- Mismatches: none observed.

## Minimum Repro Setup

- Example was instantiated one-by-one under `/obj`, tested, then deleted before moving to next node.
- Verification used geometry probes and attribute-list checks after parameter changes.

## Gotchas and Failure Modes

- invert mode can radically change scope and quickly over-dissolve topology.
