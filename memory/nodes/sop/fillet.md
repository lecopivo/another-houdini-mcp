# Spline Fillet (SOP)

## What This Node Is For

`fillet` builds a bridging surface between compatible input spline surfaces/curves while preserving originals.

## Session Status

- Status: deep-studied
- Docs read: yes (`nodes/sop/fillet.txt`)
- Example set reviewed: yes (`examples/nodes/sop/fillet/GridFillet.txt`)
- Example OTL internals inspected: yes
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent (docs + stickies):
  - Bridge two NURBS surfaces; keep source geometry intact.
  - Main controls are direction, fillet type, UV anchors, width/scale/offset, order, and optional cut/match behavior.
- Observed (live play on `/obj/academy_deep_fillet/grid_fillet/fillet1`):
  - Baseline (`dir=U`, `order=4`, freeform): `240 pts / 3 prims` from input merge (`200 pts / 2 prims`).
  - Switching direction to `V` (`dir=1`) changed bridge complexity: `330 pts / 3 prims`.
  - Increasing order `4 -> 6` (with `dir=V`) increased density: `330 -> 350 pts`.
  - Width/scale tuning (`lrwidth=0.4`, `lrscale=+/-0.6`) changed bridge extents and density (`316 pts / 3 prims`).
  - Fillet type interaction in this setup:
    - freeform/convex produced similar bounds,
    - circular expanded bridge extent (bbox max-x grew in tested configuration).
  - Parameter interaction test:
    - with `dir=V`, `cut=1` reduced output to `140 pts / 2 prims`,
    - reverting `cut=0` restored `330 pts / 3 prims`.
- Mismatches: none.

## Minimum Repro Setup

- Example network: `/obj/academy_deep_fillet/grid_fillet`.
- Core chain: `grid1 + transformed grid2 -> merge1 -> fillet1`.
- Probe both `merge1` and `fillet1` while changing one parameter at a time.

## Key Parameter Interactions

- `dir` (U/V) is high-impact; often changes bridge sampling and topology counts.
- `order` increases smoothness/control but also raises point density.
- `fillettype` mostly changes shape quality/curvature, not always topology count.
- `lrwidth*` and `lrscale*` strongly affect bridge footprint; tune together.
- `cut` can remove/trim source participation and drastically reduce output complexity in some direction/mode combinations.

## Gotchas and Failure Modes

- Input type compatibility matters (stickies call this out explicitly); mixed incompatible primitive types can invalidate expected fillet behavior.
- Topology count alone can hide meaningful curvature differences; compare bounds/shape when testing fillet type and width/scale.
- Direction and cut settings interact; test them together before concluding a setup is broken.
