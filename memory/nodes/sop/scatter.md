# Scatter (SOP)

## What This Node Is For

`scatter::2.0` generates points on surfaces/volumes for instancing, fracture seeding, and stable sampling workflows.

## Session Status

- Status: studied
- Docs read: yes (`help/nodes/sop/scatter.txt`)
- Example set reviewed: yes (`help/examples/nodes/sop/scatter/SpikyDeformingTorus.txt`, `help/examples/nodes/sop/scatter/DoorWithPolkaDots.txt`)
- Example OTL internals inspected: yes (`SpikyDeformingTorus.otl`, `DoorWithPolkaDots.otl`)
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent (docs/comments/stickies):
  - Scatter by density/count/texture space with optional relaxation and stable-id attributes.
  - Keep points stable under deformation using `primnum` + `primuvw` with `attribinterpolate`.
  - Keep points stable across topology remodelling by scattering in texture space.
- Observed (live scene/params/geometry):
  - `SpikyDeformingTorus/scatter_points` outputs `1972` points with transferred attrs `N`, `Cd`, `primnum`, `primuvw`, `pscale`.
  - Companion `attribinterpolate` consumes `primnum`/`primuvw` (`numberattrib`, `weightsattrib`) to move copied spikes on deforming geometry.
  - `DoorWithPolkaDots/scatter_points_on_door_faces` uses texture-space mode (`generateby=2`) and outputs stable points with `uv` and transferred `N`.
  - In `PackedFragments`, companion scatter `chunkcenters` directly controls fracture granularity (`npts=20` -> 20 packed pieces, `npts=40` -> 40 packed pieces downstream).
- Mismatches:
  - No behavioral mismatch found.
  - Direct parameter variation inside some example assets is permission-locked, so variation was validated on editable companion scatter (`chunkcenters`).

## Minimum Repro Setup

- Node graphs:
  - Deform-stable pattern: `/obj/academy_SpikyDeformingTorus/add_point_normals -> scatter_points -> copy_spikes_to_points -> attribinterpolate`
  - Topology-change pattern: `/obj/academy_DoorWithPolkaDots/select_door -> scatter_points_on_door_faces`
- Key parameter names and values:
  - `scatter_points.primnumattrib=primnum`, `scatter_points.primuvwattrib=primuvw`, `relaxiterations=100`
  - `scatter_points_on_door_faces.generateby=2` (In Texture Space), `vertattribs=N`
- Output verification method:
  - `probe_geometry` on scatter outputs and companion downstream nodes.

## Key Parameters and Interactions

- `generateby`: density/count/texture-space strategy selector.
- `primnumattrib` + `primuvwattrib`: must be emitted for robust `attribinterpolate` workflows.
- `relaxiterations` + `maxradius`: clump control and blue-noise quality.
- `vertattribs`/`pointattribs`: orientation and metadata transfer to scattered points.

## Practical Use Cases

1. Scatter-driven instancing (spikes/foliage/props) with orientation attrs.
2. Fracture seeding for Voronoi pipelines with controllable piece count and density.

## Gotchas and Failure Modes

- Without stable prim attributes, points may flicker/reindex across topology or frame changes.
- Texture-space scatter stability depends on consistent UVs across model variants.
- Very low-density regions can destabilize relaxation unless radius limits are tuned.

## Related Nodes

- `attribinterpolate`
- `voronoifracture`
- `copytopoints`

## Academy QA Checklist

- [x] Official docs reviewed
- [x] Example files reviewed
- [x] OTL instantiated/unlocked and internals inspected
- [x] Node comments read
- [x] Sticky notes read
- [x] Behavior validated with at least one observed test
- [x] Source-of-truth split documented (intent vs observed)
- [x] Context and progress files updated
