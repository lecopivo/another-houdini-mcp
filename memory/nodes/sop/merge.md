# Merge (SOP)

## What This Node Is For

`merge` combines multiple geometry streams into one output stream. It is a structural node used everywhere in SOP graphs.

## Session Status

- Status: studied
- Docs read: yes (`help/nodes/sop/merge.txt`)
- Example set reviewed: yes (`help/examples/nodes/sop/merge/MergeAttributes.txt`)
- Example OTL internals inspected: yes (`MergeAttributes.otl`)
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent (docs/comments/stickies):
  - Merge geometry and carry attributes across all merged outputs.
  - Example comments claim attributes missing on some branches may be filled with zero values.
- Observed (live scene/params/geometry):
  - Example `/obj/academy_MergeAttributes/merge/merge_combines_attributes` outputs merged geometry with unioned point attrs `P, N, Cd` (`126 pts, 240 prims`).
  - Custom repro `/obj/academy_merge_live` confirms merge behavior: one colored point stream + one uncolored box stream outputs merged `Cd` attribute on all points.
  - Custom repro attribute sample: merged `Cd` values were `{(1.0,1.0,1.0): 8, (1.0,0.2,0.2): 1}`.
- Mismatches:
  - Example sticky text says missing values become zero/black; in this tested build/repro, default-filled `Cd` on non-colored branch was white `(1,1,1)`.

## Minimum Repro Setup

- Node graph:
  - `/obj/academy_merge_live/sphere1 -> color1 -> merge1 <- xform1 <- box1 -> output1`
- Key parameter names and values:
  - `xform1.tx=2`
  - `color1.colorr=1`, `color1.colorg=0.2`, `color1.colorb=0.2`
- Output verification method:
  - `probe_geometry` on branch nodes and `output1`, plus HOM point-attribute sampling.

## Key Parameters and Interactions

- Merge itself has no tunable parms in this variant; behavior is driven by connected inputs.
- Upstream attribute creation determines which attributes get unioned onto final points/prims.
- Input order affects point/prim ordering and can matter for downstream assumptions.

## Practical Use Cases

1. Combine parallel modeling branches before shared finishing operations.
2. Aggregate variant streams while preserving per-branch attributes for later masking/styling.

## Gotchas and Failure Modes

- Do not rely on implicit attribute fill values without checking in your Houdini build.
- Bypassing merge passes only first input, which can hide missing-branch bugs.
- If downstream tools depend on stable ordering, lock input order and document it.

## Related Nodes

- `object_merge`
- `switch`
- `group`

## Academy QA Checklist

- [x] Official docs reviewed
- [x] Example files reviewed
- [x] OTL instantiated/unlocked and internals inspected
- [x] Node comments read
- [x] Sticky notes read
- [x] Behavior validated with at least one observed test
- [x] Source-of-truth split documented (intent vs observed)
- [x] Context and progress files updated
