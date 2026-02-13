# Edge Cusp (SOP)

## What This Node Is For

`edgecusp` deep-play validated with official examples and targeted parameter changes.

## Session Status

- Status: studied
- Docs read: yes (`nodes/sop/edgecusp.txt`)
- Example set reviewed: yes (`examples/nodes/sop/edgecusp/EdgeCuspStairs.txt`)
- Example OTL/HDA internals inspected: yes
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent: from docs and official example guidance.
- Observed: edgecusp example output 36 pts / 9 prims.
- Live tweak: toggled `updatenorms` 1 -> 0; topology unchanged.
- Mismatches: none observed.

## Minimum Repro Setup

- Example instantiated one-by-one under `/obj`, probed before/after tweak, then deleted before next node.

## Gotchas and Failure Modes

- this node is often shading-affecting more than topology-changing.
