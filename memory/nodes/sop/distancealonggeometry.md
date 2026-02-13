# Distance Along Geometry (SOP)

## What This Node Is For

`distancealonggeometry` node behavior validated with docs + official example + live parameter play.

## Session Status

- Status: studied
- Docs read: yes (`nodes/sop/distancealonggeometry.txt`)
- Example set reviewed: yes (`examples/nodes/sop/distancealonggeometry/DistanceDriver.txt`)
- Example OTL/HDA internals inspected: yes
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent: from docs and example notes.
- Observed: `single_point` output had point attrs `dist` + `mask` over 3029 pts / 31 prims.
- Live tweak: disabled `enableoutmask` and changed `rad` 10 -> 2; `mask` attr removed while `dist` remained.
- Mismatches: none observed.

## Minimum Repro Setup

- Example was instantiated one-by-one under `/obj`, tested, then deleted before moving to next node.
- Verification used geometry probes and attribute-list checks after parameter changes.

## Gotchas and Failure Modes

- these nodes are attribute writers; topology usually unchanged, so validate attr contracts explicitly.
