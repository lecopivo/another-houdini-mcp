# Quad Remesh (SOP)

## Intent

`quadremesh` retopologizes arbitrary polygon meshes into structured quad-dominant meshes with controllable resolution, symmetry, and edge-flow guidance.

## Core Behavior

- Builds a global parameterization and extracts quads from integer grid lines.
- Computes direction fields, singularities, and seams internally.
- Supports adaptive sizing and alignment guidance from curvature, boundaries, and custom guide vectors.
- Can output extracted quad mesh or intermediate global parameterization.

## Key Parameters

- Topology controls: decimation level, output mode, resolution mode/scale.
- Symmetry controls: axis planes, mirror output, plane alignment.
- Alignment/adaptivity: field weighting, curvature/boundary/guide channels and masks.
- Guide attribute integration for directional edge-flow influence.

## Typical Workflow

```text
input mesh -> optional remesh cleanup -> quadremesh -> downstream UV/rig/model ops
```

- Start with target resolution and decimation, then add alignment/symmetry constraints.
- Use field/seam/singularity visualization modes to debug edge-flow decisions.

## Production Usage

- Good for organic retopology and reduced quad meshes from dense scans/procedural surfaces.
- `QuadRemeshBasicExample` demonstrates core retopology workflow.
- `QuadRemeshGuidingExample` demonstrates guide-based edge-flow control (UV boundary driven).

Measured outcomes:
- Live Houdini remesh measurements are pending in this session.

## Gotchas

- Hard-surface sharp edges remain a known weak spot; node tends to round features.
- Input triangle quality strongly affects output quality; pre-remeshing can help.
- Additional constraints (symmetry/guides) can reduce solver flexibility and diminish individual control weight.

## Companion Nodes

- `remesh` for preconditioning triangle quality.
- `tangentfield` for explicit guide-field workflows.
- symmetry/mirror SOP tools for post-remesh cleanup.

## Study Validation

- ✅ Read docs: `help/nodes/sop/quadremesh.txt`
- ✅ Reviewed examples: `help/examples/nodes/sop/quadremesh/QuadRemeshBasicExample.txt`, `help/examples/nodes/sop/quadremesh/QuadRemeshGuidingExample.txt`
- ⏳ Live validation pending
