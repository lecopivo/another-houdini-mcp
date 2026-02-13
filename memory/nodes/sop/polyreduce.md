# PolyReduce (SOP)

## What This Node Is For

`polyreduce` lowers polygon/point counts while trying to preserve shape and important features (boundaries, creases, attributes, silhouettes).

## Session Status

- Status: studied
- Docs read: yes (`help/nodes/sop/polyreduce.txt`)
- Example set reviewed: yes (`help/examples/nodes/sop/polyreduce/PolyreduceBatwing.txt`)
- Example OTL internals inspected: yes (`PolyreduceBatwing.hda` + related `FeaturedEdges.otl` group-driven setup)
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent (docs/comments/stickies):
  - Reduce topology to a target count/percent with feature preservation controls.
  - Example demonstrates high-res to low-res conversion.
- Observed (live scene/params/geometry):
  - `/obj/academy_PolyreduceBatwing/polyreduce2` reduces batwing from `30720 prims` to `3072 prims` at `percentage=10`.
  - In `/obj/academy_FeaturedEdges/sphere_object1/polyreduce1`, edge-group preservation is used (`creases=group1`, `creaseweight=10`, `percentage=60`).
  - Changing `percentage` on `polyreduce1` from `60 -> 30` reduced output from `432` to `216` prims; restoring to `60` restored baseline.
- Mismatches:
  - None in behavior.
  - `polyreduce2` inside locked example asset is not editable directly in this session (permission error), so parameter variation testing was done on unlocked/regular example network `polyreduce1`.

## Minimum Repro Setup

- Node graph:
  - Batwing: `/obj/academy_PolyreduceBatwing/batwing -> polyreduce2`
  - Feature-preserve variant: `/obj/academy_FeaturedEdges/sphere_object1/sphere1 -> group1 -> polyreduce1`
- Key parameter names and values:
  - `polyreduce2.percentage=10`
  - `polyreduce1.percentage=60|30`
  - `polyreduce1.creases=group1`, `polyreduce1.creaseweight=10`
- Output verification method:
  - `probe_geometry` on source vs reduced nodes across percentage values.

## Key Parameters and Interactions

- `percentage` / `numpolys`: primary reduction target controls.
- `creases` + `creaseweight`: keep important edge features.
- `borderweight` / `lengthweight`: boundary and triangle-shape bias.
- `originalpoints`: constrains movement, often reducing reduction flexibility.

## Practical Use Cases

1. Create game-ready LOD meshes from high-res assets.
2. Reduce sim/collision proxy complexity while preserving silhouette-critical edges.

## Gotchas and Failure Modes

- Aggressive targets can create long skinny polys unless additional weights are tuned.
- Feature groups must be valid and in sync with topology revisions.
- Locked example HDAs can block live parm edits; use an unlocked/copy network for variation tests.

## Related Nodes

- `remesh`
- `fuse`
- `divide`

## Academy QA Checklist

- [x] Official docs reviewed
- [x] Example files reviewed
- [x] OTL instantiated/unlocked and internals inspected
- [x] Node comments read
- [x] Sticky notes read
- [x] Behavior validated with at least one observed test
- [x] Source-of-truth split documented (intent vs observed)
- [x] Context and progress files updated
