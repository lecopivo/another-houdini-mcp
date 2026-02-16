# Revolve (SOP)

## Intent

`revolve` generates surfaces by spinning input curves/surfaces around a defined axis, supporting closed/full revolution and arc variants with multiple topology outputs.

## Core Behavior

- Uses input curve/face as source profile and sweeps it around `origin` + `dir` axis.
- `type` selects closed revolution or arc variants.
- `divs` controls circumferential tessellation density.
- End caps can close open results; polygon-mesh parameterization can be converted to explicit polygons when needed.

## Key Parameters

- `divs`: primary tessellation-density control.
- `type`: Closed / Open Arc / Closed Arc.
- `cap`: generate end-cap primitives.
- `surftype`: rows/cols/quads/triangles output organization.
- `polys`: mesh-style vs explicit polygon output parameterization.
- `imperfect` (NURBS/Bezier contexts): even-CV approximation vs exact-follow behavior.

## Typical Workflow

```text
profile curve -> revolve -> (optional facet/convert/cap handling) -> downstream modeling/render
```

- Lock axis and revolution type first.
- Then tune `divs` and polygonization strategy for downstream needs.

## Production Usage

- Useful for rotational forms: vases, torus-like forms, lathed parts.
- Keep `divs` as first-order perf/quality dial.
- For face-normal workflows, explicit polygon conversion can be important before facet/cusp operations.

Measured outcomes (`BasicRevolve` example):
- Polygon branch baselines:
  - `revolve`: `100 pts / 1 prim`.
  - `revolve_open_arc`: `70 pts / 1 prim`.
  - `revolve_end_caps`: `120 pts / 3 prims`.
  - `revolve_convert`: `100 pts / 90 prims` (explicit polygonized parameterization).
- NURBS branch contrast:
  - `revolve_imperfect`: `100 pts / 1 prim`.
  - `revolve_perfect` (`imperfect=0`): `120 pts / 1 prim`, with fuller X/Z extent.
- Division scaling (`revolve`):
  - `divs 8 -> 24 -> 48` yielded `80 -> 240 -> 480` points.
- Type and capping behavior (at high `divs` test state):
  - `type closed -> open arc -> closed arc`: `480 -> 490 -> 500` points.
  - `cap 0 -> 1`: `1 -> 3` primitives.
- Polygonization switch:
  - `polys 0`: `600 pts / 3 prims`,
  - `polys 1`: `600 pts / 452 prims / 1900 verts`.

## Gotchas

- Mesh-style outputs can hide per-face normal differences until explicitly polygonized.
- `imperfect` has no practical effect on pure polygon source workflows but is meaningful for NURBS/Bezier shape fidelity.
- End-cap behavior depends on source openness and revolve type; validate cap results directly.

## Companion Nodes

- `facet` for cusp/per-face normal behavior after polygonization.
- `convert` for explicit primitive-type control in legacy/interop workflows.
- `font` + `merge` for annotated multi-variant comparison setups.

## Study Validation

- ✅ Read docs: `nodes/sop/revolve.txt`
- ✅ Reviewed example: `examples/nodes/sop/revolve/BasicRevolve.txt`
- ✅ Inspected extensive companion branches and sticky annotations across primitive types
- ✅ Ran live division/type/cap/polys/imperfect comparisons with measured geometry outcomes
