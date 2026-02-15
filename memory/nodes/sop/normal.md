# Normal (SOP)

## Intent

`normal` computes or modifies normal attributes (`N`) on points, vertices, primitives, or detail with better stability/weighting controls than legacy quick-normal approaches.

## Core Behavior

- `type` selects normal class target (point/vertex/primitive/detail).
- `cuspangle` controls vertex-normal smoothing across incident faces.
- `method` controls weighting strategy when aggregating normals.
- `docompute=0` switches node into modify-only mode (`normalize`, `reverse`) for existing normals.

## Key Parameters

- `type`: where to write/modify `N`.
- `cuspangle`: vertex-normal split/average threshold.
- `method`: weighting mode (`By Vertex Angle`, `Each Vertex Equally`, `By Face Area`).
- `origifzero`: preserve input `N` when computed normal is zero (important for disconnected points/custom uses).
- `docompute`, `normalize`, `reverse`: compute vs post-process behavior.

## Typical Workflow

```text
geo -> normal (compute) -> optional normal (modify-only normalize/reverse) -> downstream shading/deform
```

- Compute normals at the class your downstream consumers expect.
- Use vertex normals with tuned cusp for hard/smooth edge control.
- Keep modify-only passes separate when normal post-processing should be explicit.

## Production Usage

- Prefer vertex normals for mixed hard/smooth hard-surface assets.
- Use point normals where per-point continuity is required.
- Keep `origifzero=1` when points may be isolated and carry intentional custom normal vectors.

Measured outcomes (`BoxNormals` example + live `/obj/academy_normal_live`):
- Type-contract verification:
  - vertex mode -> vertex `N` only (`vtxN=True`, `ptN=False`),
  - point mode -> point `N` only,
  - primitive mode -> primitive `N` only,
  - detail mode -> detail `N` only.
- Polygon soup support (example claim validated):
  - `normal` wrote vertex normals on polygon soup branch (`normal_polySoup`: `vtxN=True`) even with single soup primitive.
- Cusp-angle interaction (vertex mode, same point with 3 incident vertices):
  - `cusp=30` -> `3` unique incident normals (hard split behavior),
  - `cusp=120/180` -> `1` unique incident normal (smoothed averaging behavior).
- Weighting/triangulation comparison (point normals, quad vs triangulated box):
  - mean absolute normal alignment stayed high for all methods (`~0.993-1.0`),
  - signs were inverted in this test branch (triangulation winding orientation effect), so compare using absolute alignment when validating weighting robustness.
- `origifzero` on disconnected points with seeded custom `N={0,2,0}`:
  - `origifzero=0` -> computed zero normal (`{0,0,0}`),
  - `origifzero=1` -> preserved seeded normal (`{0,2,0}`).
- Modify-only mode on existing normals (`docompute=0`, `normalize=1`, `reverse=1`) produced unit-length flipped normals (mean `|N|=1.0`).

## Gotchas

- If `docompute=0` and upstream lacks `N`, this node will not create normals.
- Triangulation/winding changes can flip normal direction signs while preserving magnitude/alignment.
- Misaligned normal class (point vs vertex) is a frequent downstream shading/deformation mismatch.
- Very low cusp values can unintentionally harden edges broadly.

## Companion Nodes

- `divide` for triangulation tests affecting normal direction/winding behavior.
- `polysoup` for polygon soup pipelines requiring vertex normal support.
- `attribpromote` when converting point normals to vertex normals for merged-display/debug workflows.

## Study Validation

- ✅ Read docs: `nodes/sop/normal.txt`
- ✅ Reviewed example: `examples/nodes/sop/normal/BoxNormals.txt`
- ✅ Inspected stickies and companion branches (quads/tris/polysoup/tets)
- ✅ Ran live tests for type contracts, cusp/weighting behavior, polygon soup support, and modify/origifzero edge cases
