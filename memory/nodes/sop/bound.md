# Bound (SOP)

## What This Node Is For

`bound` builds proxy bounding shapes (box/sphere/rectangle) around geometry and can emit transform/radii metadata for downstream procedural use.

## Session Status

- Status: studied
- Docs read: yes (`nodes/sop/bound.txt`)
- Example set reviewed: yes (`examples/nodes/sop/bound/BoundingBox.txt`)
- Example OTL internals inspected: yes (`BoundingBox.otl`)
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent (docs/comments/stickies):
  - Create a bounding box or sphere around incoming geometry.
  - Example uses `switch` to compare sources and feed one `bound` node.
  - Node can output detail attributes (`radii`, `xform`) for transform-aware workflows.
- Observed (live scene/params/geometry):
  - In `/obj/academy_bound_live`, `boundtype=0` (box) outputs `8 pts / 6 prims`.
  - Switching to `boundtype=1` (sphere) outputs a primitive sphere representation (`1 pt / 1 prim`) in this build.
  - Enabling `addradiiattrib=1` and `addxformattrib=1` adds detail attrs `radii` and `xform` on output.
  - Example `/obj/academy_BoundingBox/TeapotTetrahedron` confirms practical switch-driven source testing before bound generation.
- Mismatches:
  - None observed.

## Minimum Repro Setup

- Node graph:
  - `/obj/academy_bound_live/platonic1 -> bound1 -> OUT_BOUND`
- Key parameter names and values:
  - `bound1.boundtype = 0` (box), `1` (sphere)
  - `bound1.maxpadx=0.5`, `maxpady=0.25`, `maxpadz=0.1`
  - `bound1.addradiiattrib=1`, `addxformattrib=1`
- Output verification method:
  - `probe_geometry` counts + detail-attribute presence checks.

## Key Parameters and Interactions

- `boundtype` determines both shape semantics and output topology class.
- `minpad/maxpad` expand bounds for safety margins around animated/deforming data.
- `keepOriginal` + `boundsgroup` is useful when wanting both source and proxy in one stream.
- `orientedbbox` can improve fit, but only works correctly on compatible point-based primitive hulls.

## Practical Use Cases

1. Build deformation cages/proxy collision shells around source meshes.
2. Emit `xform`/`radii` attributes to drive downstream placement, scaling, or instancing logic.

## Gotchas and Failure Modes

- Oriented box mode can fail or mislead on packed/primitives without polygonal hull points.
- Sphere bounds with non-uniform padding can violate strict containment assumptions.
- If source selection is group-driven, wrong group class silently yields oversized/empty bounds.

## Related Nodes

- `box`
- `sphere`
- `lattice`
- `xformbyattrib`

## Academy QA Checklist

- [x] Official docs reviewed
- [x] Example files reviewed
- [x] OTL instantiated/unlocked and internals inspected
- [x] Node comments read
- [x] Sticky notes read
- [x] Behavior validated with at least one observed test
- [x] Source-of-truth split documented (intent vs observed)
- [x] Context and progress files updated
