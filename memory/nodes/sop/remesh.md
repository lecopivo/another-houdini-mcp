# Remesh (SOP)

## What This Node Is For

`remesh::2.0` rebuilds polygon surfaces into high-quality triangles (uniform or adaptive sizing), useful for simulation prep, cleanup, and topology regularization.

## Session Status

- Status: studied
- Docs read: yes (`help/nodes/sop/remesh.txt`)
- Example set reviewed: yes (`help/examples/nodes/sop/remesh/Squidremesh.txt`)
- Example OTL internals inspected: yes (`Squidremesh.hda`)
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent (docs/comments/stickies):
  - Support adaptive and uniform edge sizing.
  - Preserve boundaries/hard edges, optionally driven by explicit edge groups.
  - Example focuses on preserving hard edges while remeshing a squid/crab model.
- Observed (live scene/params/geometry):
  - `/obj/academy_Squidremesh/remesh2` runs adaptive sizing (`sizing=1`) with hard edge group `hard_edges_group` and outputs dense triangulation: `36417 pts, 72724 prims`.
  - Switching to uniform sizing (`sizing=0`) reduced topology: `9177 pts, 18262 prims`.
  - Increasing `targetsize` in uniform mode (`0.2 -> 0.4`) reduced topology further: `5952 pts, 11812 prims`.
  - Sticky notes in the example explicitly call out hard-edge group creation and optional mesh-size attributes.
- Mismatches:
  - None found.

## Minimum Repro Setup

- Node graph:
  - `/obj/academy_Squidremesh/Input_Geometry -> hard_edges_group -> attribcreate* -> remesh2`
- Key parameter names and values:
  - Baseline: `remesh2.sizing=1`, `remesh2.iterations=4`, `remesh2.hard_edges="hard_edges_group"`
  - Uniform test: `remesh2.sizing=0`, `remesh2.targetsize=0.2`
  - Coarser uniform test: `remesh2.targetsize=0.4`
- Output verification method:
  - `probe_geometry` on `remesh2` across parameter variants.

## Key Parameters and Interactions

- `sizing`: adaptive vs uniform mode switch.
- `targetsize` / `minsize` / `maxsize`: output density controls.
- `hard_edges` / `hard_points`: feature preservation constraints.
- `iterations` + `smoothing`: quality/runtime/shape-preservation balance.

## Practical Use Cases

1. Convert uneven scan/kitbash meshes into simulation-friendly triangles.
2. Normalize topology before deformation and attribute transfer workflows.

## Gotchas and Failure Modes

- Adaptive mode can generate far denser meshes than expected on detailed curvature.
- Missing hard-edge constraints can soften important silhouette/crease features.
- Very high iterations may over-smooth or over-cook with diminishing returns.

## Related Nodes

- `polyreduce`
- `triangulate2d`
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
