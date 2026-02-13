# VDB From Polygons (SOP)

## What This Node Is For

`vdbfrompolygons` rasterizes polygon meshes into sparse VDB fields (SDF/fog/attribute VDBs).

## Session Status

- Status: studied
- Docs read: yes (`nodes/sop/vdbfrompolygons.txt`)
- Example set reviewed: yes (fallback: no local `examples/nodes/sop/vdbfrompolygons/` folder)
- Example OTL internals inspected: yes (fallback live repro)
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent: convert tri/quad meshes to sparse SDF/fog volumes with controllable voxel size and bands.
- Observed: `/obj/academy_vdbfrompolygons_live` default created one VDB primitive (`name` attr present). Enabling `buildfog=1` added a second VDB primitive (`1 -> 2 prims` in probe representation).
- Mismatches: none.

## Minimum Repro Setup

- Node graph: `/obj/academy_vdbfrompolygons_live/sphere1 -> vdbfrompolygons1 -> OUT_VDBFROMPOLYGONS`
- Key parms: `voxelsize`, `builddistance`, `buildfog`, `fillinterior`.
- Verification: `probe_geometry` primitive count/`name` attribute check.

## Key Parameters and Interactions

- `voxelsize` drives fidelity/performance.
- `builddistance` and `buildfog` can be enabled together for paired fields.
- Band settings (`exterior/interior`) strongly affect memory footprint.

## Gotchas and Failure Modes

- Non-mesh input quality can break interior/exterior assumptions.
- Too-small voxels can explode memory/cook time.

## Related Nodes

- `vdbactivate`
- `volumesdf`
- `isooffset`
