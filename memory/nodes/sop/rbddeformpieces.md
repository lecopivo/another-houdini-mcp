# RBD Deform Pieces (SOP)

## Intent

`rbddeformpieces` deforms high-resolution render geometry using animated proxy/sim pieces, preserving coarse simulation speed with detailed output deformation.

## Core Behavior

- Matches render pieces to proxy pieces (default via `name`, optional custom attr).
- Computes capture weights from proxy point cloud around each render point.
- Supports boundary influence restriction via cluster attributes or constraint-derived clusters.
- Deforms `P` always, plus optional attribute transforms by pattern/type-info.

## Key Parameters

- Matching: custom match-attribute toggle and name attribute.
- Boundary connection mode: cluster attribute vs constraints clustering.
- Capture controls: rest frame, radius, min/max points.
- Deform controls: attributes to transform (point/vertex with type-aware transforms).

## Typical Workflow

```text
hi-res render geo + simulated proxy geo (+constraints) -> rbddeformpieces -> shading/render
```

- Capture at a stable rest frame before large simulation divergence.
- Tune radius/min/max points to balance continuity vs speed/memory.

## Production Usage

- Standard post-sim reconstruction stage for destruction workflows.
- `RBDDeformPieces` example demonstrates direct usage of proxy-driven deformation.

Measured outcomes:
- Live Houdini capture/deform measurements are pending in this session.

## Gotchas

- Name mismatches between render and proxy pieces cause deformation mapping failures.
- Too-low max points or too-small radius can create discontinuities/orphan influences.
- Constraint-cluster mode depends on valid/up-to-date constraint connectivity.

## Companion Nodes

- `rbdbulletsolver` for proxy simulation generation.
- `xformpieces` for rigid transform transfer alternatives.
- constraint SOP family for cluster-constrained influence domains.

## Study Validation

- ✅ Read docs: `help/nodes/sop/rbddeformpieces.txt`
- ✅ Reviewed example: `help/examples/nodes/sop/rbddeformpieces/RBDDeformPieces.txt`
- ⏳ Live validation pending
