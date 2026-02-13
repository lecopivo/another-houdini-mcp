# Edit (SOP)

## What This Node Is For

`edit` deep-play validated with official examples and targeted parameter changes.

## Session Status

- Status: studied
- Docs read: yes (`nodes/sop/edit.txt`)
- Example set reviewed: yes (`examples/nodes/sop/edit/ReferenceGeometry.txt`)
- Example OTL/HDA internals inspected: yes
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent: from docs and official example guidance.
- Observed: with-reference edit branch output 2401 pts / 2304 prims.
- Live tweak: set transform `tx` 0 -> 0.3 on `with_reference_geometry`; topology unchanged.
- Mismatches: none observed.

## Minimum Repro Setup

- Example instantiated one-by-one under `/obj`, probed before/after tweak, then deleted before next node.

## Gotchas and Failure Modes

- Edit SOP is cumulative and transform-driven; use it for shape change, not topology operations.
