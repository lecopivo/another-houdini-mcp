# Edge Equalize (SOP)

## What This Node Is For

`edgeequalize` deep-play validated with official examples and targeted parameter changes.

## Session Status

- Status: studied
- Docs read: yes (`nodes/sop/edgeequalize.txt`)
- Example set reviewed: yes (`examples/nodes/sop/edgeequalize/EdgeEqualizeBasic.txt`)
- Example OTL/HDA internals inspected: yes
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent: from docs and official example guidance.
- Observed: edgeequalize output 132 pts / 122 prims.
- Live tweak: changed `method` 2 -> 0; topology stable, edge lengths redistributed.
- Mismatches: none observed.

## Minimum Repro Setup

- Example instantiated one-by-one under `/obj`, probed before/after tweak, then deleted before next node.

## Gotchas and Failure Modes

- equalize is geometric reshaping; verify edge-length quality, not counts.
