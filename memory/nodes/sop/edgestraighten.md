# Edge Straighten (SOP)

## What This Node Is For

`edgestraighten` deep-play validated with official examples and targeted parameter changes.

## Session Status

- Status: studied
- Docs read: yes (`nodes/sop/edgestraighten.txt`)
- Example set reviewed: yes (`examples/nodes/sop/edgestraighten/EdgeStraightenBasic.txt`)
- Example OTL/HDA internals inspected: yes
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent: from docs and official example guidance.
- Observed: edgestraighten output 92 pts / 180 prims.
- Live tweak: cleared `group` selection; topology stable while edge-line constraint scope changed.
- Mismatches: none observed.

## Minimum Repro Setup

- Example instantiated one-by-one under `/obj`, probed before/after tweak, then deleted before next node.

## Gotchas and Failure Modes

- straighten/equalize ops are best validated with visual edge metrics or downstream fit quality.
