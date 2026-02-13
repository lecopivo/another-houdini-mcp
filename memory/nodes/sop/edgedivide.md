# Edge Divide (SOP)

## What This Node Is For

`edgedivide` deep-play validated with official examples and targeted parameter changes.

## Session Status

- Status: studied
- Docs read: yes (`nodes/sop/edgedivide.txt`)
- Example set reviewed: yes (`examples/nodes/sop/edgedivide/EdgeDivideBasic.txt`)
- Example OTL/HDA internals inspected: yes
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent: from docs and official example guidance.
- Observed: active branch showed 28 pts / 9 prims.
- Live tweak: increased `numdivs` 4 -> 5; points increased 28 -> 32.
- Mismatches: none observed.

## Minimum Repro Setup

- Example instantiated one-by-one under `/obj`, probed before/after tweak, then deleted before next node.

## Gotchas and Failure Modes

- division count directly increases inserted points on selected edges.
