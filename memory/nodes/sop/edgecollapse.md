# Edge Collapse (SOP)

## What This Node Is For

`edgecollapse` deep-play validated with official examples and targeted parameter changes.

## Session Status

- Status: studied
- Docs read: yes (`nodes/sop/edgecollapse.txt`)
- Example set reviewed: yes (`examples/nodes/sop/edgecollapse/EdgeCollapseBasic.txt`)
- Example OTL/HDA internals inspected: yes
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent: from docs and official example guidance.
- Observed: edgecollapse2 baseline 5 pts / 3 prims.
- Live tweak: toggled `removedegen` 1 -> 0; prim count changed 3 -> 4.
- Mismatches: none observed.

## Minimum Repro Setup

- Example instantiated one-by-one under `/obj`, probed before/after tweak, then deleted before next node.

## Gotchas and Failure Modes

- degenerate cleanup materially changes final primitive count after collapse.
