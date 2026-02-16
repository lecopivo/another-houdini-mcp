# Fuse (SOP)

## What This Node Is For

`fuse::2.0` snaps nearby points and optionally consolidates them into shared points, which is core for cleaning seams and stitching modeled parts.

## Session Status

- Status: studied
- Docs read: yes (`help/nodes/sop/fuse.txt`)
- Example set reviewed: yes (`help/examples/nodes/sop/fuse/FuseHood.txt`)
- Example OTL internals inspected: yes (`FuseHood.hda`)
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent (docs/comments/stickies):
  - Snap points by distance/grid/specified targets.
  - Optionally fuse snapped points to reduce point count and weld topology.
  - Example focuses on curve-panel consolidation for a car hood.
- Observed (live scene/params/geometry):
  - `/obj/academy_FuseHood/Hood/merge_all` has `40 pts, 3 prims` before fuse.
  - `/obj/academy_FuseHood/Hood/fuse1` outputs `29 pts, 3 prims` with defaults.
  - Turning off `consolidatesnappedpoints` changes fused output to `40 pts, 3 prims`; turning it back on returns to `29 pts, 3 prims`.
- Mismatches:
  - None found.

## Minimum Repro Setup

- Node graph:
  - `/obj/academy_FuseHood/Hood/hood + side_panel + front_panel -> merge_all -> fuse1`
- Key parameter names and values:
  - `fuse1.snaptype=0` (Near Points)
  - `fuse1.tol3d=0.001`
  - `fuse1.consolidatesnappedpoints=1|0`
- Output verification method:
  - `probe_geometry` on `merge_all` and `fuse1`.

## Key Parameters and Interactions

- `tol3d`: controls near-point snap threshold.
- `consolidatesnappedpoints`: decides whether snapped points are welded into one point.
- `deldegen` and `delunusedpoints`: cleanup options after rewiring.
- `querygroup` / `targetgroup`: constrain what snaps and what receives snaps.

## Practical Use Cases

1. Weld mirrored/modelled halves before subdivision or booleans.
2. Stitch imported CAD or curve-panel seams with controlled tolerance.

## Gotchas and Failure Modes

- Too-large tolerance can collapse intended detail.
- Snapping without consolidation only moves points; it does not weld topology.
- For line cleanup, fuse may still leave separate primitives; append `join` when needed.

## Companion Finding (from PolyWire study)

- For curve-skeleton tube workflows, fusing before `polywire` reduces duplicate branch points and improves junction consistency.
- In `PolywireModel`, fusing reduced backbone points (`30 -> 24`) before tube generation, yielding cleaner input for attribute-driven width modulation.

## Related Nodes

- `pointweld`
- `facet`
- `uvfuse`

## Academy QA Checklist

- [x] Official docs reviewed
- [x] Example files reviewed
- [x] OTL instantiated/unlocked and internals inspected
- [x] Node comments read
- [x] Sticky notes read
- [x] Behavior validated with at least one observed test
- [x] Source-of-truth split documented (intent vs observed)
- [x] Context and progress files updated
