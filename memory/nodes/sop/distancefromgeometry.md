# Distance From Geometry (SOP)

## What This Node Is For

`distancefromgeometry` node behavior validated with docs + official example + live parameter play.

## Session Status

- Status: studied
- Docs read: yes (`nodes/sop/distancefromgeometry.txt`)
- Example set reviewed: yes (`examples/nodes/sop/distancefromgeometry/SurfaceDistance.txt`)
- Example OTL/HDA internals inspected: yes
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent: from docs and example notes.
- Observed: `from_points_mask` output carried `dist` + `mask` on dense mesh (205684 pts / 205664 prims).
- Live tweak: disabled `enableoutmask` and set `rad` 1.0 -> 0.25; `mask` attribute removed, `dist` preserved.
- Mismatches: none observed.

## Minimum Repro Setup

- Example was instantiated one-by-one under `/obj`, tested, then deleted before moving to next node.
- Verification used geometry probes and attribute-list checks after parameter changes.

## Gotchas and Failure Modes

- on heavy meshes, attr-only changes are easy to miss in viewport without attribute inspection.
