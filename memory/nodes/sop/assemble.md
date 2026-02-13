# Assemble (SOP)

## What This Node Is For

`assemble` finalizes fractured pieces by creating piece ids/groups/name attrs and optionally converting pieces to packed primitives for simulation.

## Session Status

- Status: studied
- Docs read: yes (`help/nodes/sop/assemble.txt`)
- Example set reviewed: yes (`help/examples/nodes/sop/assemble/PackedFragments.txt`)
- Example OTL internals inspected: yes (`PackedFragments.otl`)
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent (docs/comments/stickies):
  - Clean fracture output and create per-piece metadata.
  - Pack pieces for memory-efficient RBD workflows.
- Observed (live scene/params/geometry):
  - `/obj/academy_PackedFragments/sphere/voronoifracture1` outputs fractured geo with primitive `name`.
  - `/obj/academy_PackedFragments/sphere/setup_packed_prims` (assemble) outputs `20` packed pieces (`20 pts, 20 prims`) with point `name` and primitive `path`.
  - Key overrides confirm packing workflow (`pack_geo=1`, `createpath=1`, `connect=0`).
  - Companion nodes (`scatter` -> 20 seeds, `voronoifracture`) define piece count and boundaries consumed by assemble.
- Mismatches:
  - None found.

## Minimum Repro Setup

- Node graph:
  - `/obj/academy_PackedFragments/sphere/sphere1 -> voronoifracture1 -> setup_packed_prims`
  - companion: `sphere1 -> isooffset -> scatter(chunkcenters) -> voronoifracture1 input 1`
- Key parameter names and values:
  - `setup_packed_prims.pack_geo=1`
  - `setup_packed_prims.createpath=1`
  - `setup_packed_prims.connect=0`
- Output verification method:
  - `probe_geometry` before/after assemble and inspect output attrs.

## Key Parameters and Interactions

- `pack_geo`: toggles packed output creation.
- `createpath` / `path`: metadata for packed piece references.
- `newname` / prefix controls piece naming conventions.
- Upstream fracture quality and `name` consistency determine assemble usefulness.

## Practical Use Cases

1. Prepare Voronoi-fractured assets for RBD sims with low memory footprint.
2. Standardize piece naming/group metadata before caching/export.

## Gotchas and Failure Modes

- Packing hides raw topology; debug on pre-pack branch when diagnosing geometry issues.
- Inconsistent upstream naming can produce unexpected packed grouping.
- `connect` and cusp choices affect seam appearance and perceived fracture lines.

## Related Nodes

- `voronoifracture`
- `connectivity`
- `partition`

## Academy QA Checklist

- [x] Official docs reviewed
- [x] Example files reviewed
- [x] OTL instantiated/unlocked and internals inspected
- [x] Node comments read
- [x] Sticky notes read
- [x] Behavior validated with at least one observed test
- [x] Source-of-truth split documented (intent vs observed)
- [x] Context and progress files updated
