# Divide (SOP)

## What This Node Is For

`divide` node behavior validated with docs + official example + live parameter play.

## Session Status

- Status: studied
- Docs read: yes (`nodes/sop/divide.txt`)
- Example set reviewed: yes (`examples/nodes/sop/divide/RemoveSharedEdges.txt`)
- Example OTL/HDA internals inspected: yes
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent: from docs and example notes.
- Observed: example node output 36 pts / 1 prim in showcased remove-shared-edges setup.
- Live tweak: changed `divs` 1 -> 2 on tested node; example topology remained same in this particular mode.
- Mismatches: none observed.

## Minimum Repro Setup

- Example was instantiated one-by-one under `/obj`, tested, then deleted before moving to next node.
- Verification used geometry probes and attribute-list checks after parameter changes.

## Gotchas and Failure Modes

- different divide modes (convex, triangulate, smooth, remove shared edges) can dominate over `divs`.
