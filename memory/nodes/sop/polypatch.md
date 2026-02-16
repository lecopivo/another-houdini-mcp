# PolyPatch (SOP)

## Intent

`polypatch` constructs smooth patch surfaces from ordered polygon/curve inputs, with configurable connectivity, wrapping, basis, and output representation (mesh vs polygons).

## Core Behavior

- Builds a patch from input point-number ordering (not necessarily primitive-vertex ordering).
- Connectivity mode controls whether output is rows, columns, rows+cols, triangles, alternating triangles, quads, or inherited.
- Divisions (`divisionsx/y`) control output resolution.
- Can output either polygon mesh primitive or explicit polygons (`polys`).

## Key Parameters

- `divisionsx`, `divisionsy`: surface refinement controls.
- `connecttype`: output topology pattern.
- `closeu`, `closev`: wrap behavior in U/V.
- `basis`: cardinal vs B-spline interpolation basis.
- `polys`: force polygon output instead of mesh primitive.
- `group`: subset selection of source elements.

## Typical Workflow

```text
ordered curves/mesh -> polypatch -> optional convert/wire/detailing -> downstream modeling/rendering
```

- Ensure source point ordering is meaningful; use sort-by-vertex prep if needed.
- Tune divisions first, then choose connectivity to fit intended topology style.
- Use mesh output during shaping; convert to polygons when downstream ops require explicit polys.

## Production Usage

- Useful for procedural skins connecting repeated curve scaffolds (ribs/spirals/strands).
- Connectivity mode is a major topology decision; choose early for downstream compatibility.
- Wrap controls are powerful for periodic surfaces (tube-like/spiral forms).

Measured outcomes (`PolyPatchDNA` + live parameter tests on `polypatch1`):
- Example base chain:
  - `copy1` produced scaffold (`60 pts / 30 prims`),
  - `polypatch1` generated surface (`60 pts / 29 prims / 116 verts` at low divisions),
  - downstream `wire` + `copy` + `merge` built stylized DNA form.
- Division sweep:
  - `1x1`: `60 pts / 29 prims`
  - `2x1`: `90 / 58`
  - `4x2`: `295 / 232`.
- Connectivity sweep at fixed divisions showed major topology differences:
  - rows/cols variants: as low as `5` or `59` prims,
  - quads/tri variants: up to `464` prims.
- Mesh vs polygon output:
  - `polys=0` -> single `Mesh` primitive (`1` prim),
  - `polys=1` -> explicit polygons (`464` prims in test setting).
- Wrap controls affected point/primitive counts significantly:
  - e.g. `closeu=1` roughly doubled topology vs open setting in tested configuration.

## Gotchas

- Point-order sensitivity is critical; wrong ordering gives twisted/unexpected surfaces.
- High divisions + dense connectivity (triangles/alternating) can escalate counts quickly.
- Mesh output may not be accepted by polygon-only downstream nodes without conversion.
- Wrap settings can radically alter topology; verify seam expectations early.

## Companion Nodes

- `sort` (by vertex) to fix point-order contracts before patching.
- `convert` to switch mesh output to polygons for downstream modeling.
- `wire` / `copy` for stylized post-patch detailing patterns.

## Study Validation

- ✅ Read docs: `nodes/sop/polypatch.txt`
- ✅ Reviewed example: `examples/nodes/sop/polypatch/PolyPatchDNA.txt`
- ✅ Inspected sticky notes and full companion chain (`line/copy/polypatch/convert/wire/copy/merge/point`)
- ✅ Ran live division/connectivity/wrap/output-mode sweeps with measured topology changes
