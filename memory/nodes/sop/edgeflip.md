# Edge Flip (SOP)

## What This Node Is For

`edgeflip` deep-play validated with official examples and targeted parameter changes.

## Session Status

- Status: studied
- Docs read: yes (`nodes/sop/edgeflip.txt`)
- Example set reviewed: yes (`examples/nodes/sop/edgeflip/EdgeFlipBasic.txt`)
- Example OTL/HDA internals inspected: yes
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent: from docs and official example guidance.
- Observed: edgeflip output 10 pts / 2 prims.
- Live tweak: increased `cycles` 1 -> 2; topology unchanged.
- Mismatches: none observed.

## Minimum Repro Setup

- Example instantiated one-by-one under `/obj`, probed before/after tweak, then deleted before next node.

## Gotchas and Failure Modes

- flipping changes diagonal/vertex ordering semantics rather than size.
