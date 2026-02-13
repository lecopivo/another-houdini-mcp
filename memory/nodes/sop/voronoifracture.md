# Voronoi Fracture (SOP)

## What This Node Is For

`voronoifracture::2.0` breaks polygonal geometry into Voronoi pieces using input seed points, with optional interior surfaces and piece metadata.

## Session Status

- Status: studied
- Docs read: yes (`help/nodes/sop/voronoifracture.txt`)
- Example set reviewed: yes (fallback via companion official example `help/examples/nodes/sop/assemble/PackedFragments.txt`)
- Example OTL internals inspected: yes (`PackedFragments.otl` companion workflow)
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes (fallback workflow used: docs + companion example + live repro)

## Source-of-Truth Split

- Intent (docs/comments/stickies):
  - Fracture geometry from cell points (often from `scatter`/`pointsfromvolume`).
  - Emit piece-identifying attributes (notably `name`) and optional constraint output.
- Observed (live scene/params/geometry):
  - Companion node `/obj/academy_PackedFragments/sphere/voronoifracture1` uses scatter seeds from `chunkcenters`.
  - At `chunkcenters.npts=20`, fracture output is `371 prims` and packed result downstream is `20` packed pieces.
  - At `chunkcenters.npts=40`, fracture output grows to `639 prims` and downstream packed output becomes `40` packed pieces.
  - Output carries primitive `name` (consumed by `assemble`).
- Mismatches:
  - No behavioral mismatch found in tested workflow.

## Minimum Repro Setup

- Node graph:
  - `/obj/academy_PackedFragments/sphere/sphere1 -> voronoifracture1 <- chunkcenters`
- Key parameter names and values:
  - companion control: `chunkcenters.npts=20|40`
  - observed piece metadata in output: primitive `name`
- Output verification method:
  - `probe_geometry` on `chunkcenters`, `voronoifracture1`, and downstream `setup_packed_prims`.

## Key Parameters and Interactions

- Seed-point distribution is the primary art-directable control on piece size/count.
- `Create Interior Surfaces` and name/piece settings determine fracture usefulness downstream.
- `Name Attribute` mode and prefix/namespace choices matter in multi-stage fracture chains.

## Practical Use Cases

1. RBD pre-fracture for destruction setups.
2. Procedural piece generation where piece ids/names drive shading/sim behavior.

## Gotchas and Failure Modes

- Poor seed coverage causes oversized/undesirable fragments.
- Fracturing very dense meshes is expensive; pre-reduce where possible.
- No local node-scoped examples means behavior should be validated in companion workflows.

## Related Nodes

- `scatter`
- `assemble`
- `rbdinteriordetail`

## Academy QA Checklist

- [x] Official docs reviewed
- [x] Example files reviewed
- [x] OTL instantiated/unlocked and internals inspected
- [x] Node comments read
- [x] Sticky notes read
- [x] Behavior validated with at least one observed test
- [x] Source-of-truth split documented (intent vs observed)
- [x] Context and progress files updated
