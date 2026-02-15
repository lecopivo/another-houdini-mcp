# Join (SOP)

## Intent

Join multiple compatible curves/surfaces into a single primitive, with optional blending, wrapping, and retention of source primitives.

## Core Behavior

- Consumes a sequence of primitives and emits a joined primitive that inherits attributes.
- Can operate on mixed complexity inputs by promoting simpler types when needed.
- Blending can reshape connection neighborhoods; non-blend mode keeps a sharper connection character.
- Can close first-to-last for looped forms.

## Key Parameters

- `blend`: smooth/blended transition behavior vs sharper connection behavior.
- `tolerance`: controls how strongly ends are modified during connection.
- `bias`: side weighting for blend influence.
- `knotmult`: multiplicity behavior around join seams.
- `loop`: wrap last primitive to first.
- `prim`: keep original primitives in output in addition to joined result.

## Typical Workflow

```
surface pieces -> join -> OUT
```

- Author pieces as NURBS/Bezier/mesh (or validate conversion if using polygons).
- Tune `blend` + `tolerance` together first.
- Enable `loop` when building closed ribbons/rings.
- Turn on `prim` during lookdev/debug, then disable if single-output primitive is required.

## Production Usage

- Use `prim=1` as a temporary QA mode to compare source vs joined result in one stream.
- Keep output primitive-class checks in validation (NURBS vs mesh conversion can affect downstream tools).
- Treat sticky-note guidance as contextual; verify against docs/build behavior.

Measured outcomes:
- Example no-wrap branch: `copy1 (3 prims / 300 pts)` -> `join_U (1 prim / 340 pts)` with `Cd` inherited.
- Wrap branch: `copy1 (3 prims / 300 pts)` -> `join_U (1 prim / 270 pts)` with `loop=1`.
- Live sweeps:
  - default: `1` NURBS surface (`280 pts`)
  - `blend=0`: `340 pts` (sharper/denser transition)
  - `loop=1`: `270 pts` (closed topology)
  - `prim=1`: `4 prims` (originals + joined)
- Input-class test: polygon input joined successfully and output `Mesh` in this build.

## Gotchas

- Unexpected primitive count inflation is usually `prim=1`.
- Blend tuning without checking `tolerance` often gives misleading conclusions.
- Example notes may lag version behavior; trust docs + live probe when conflicting.

## Companion Nodes

- `copy`, `xform` for patterned source-piece generation.
- `fillet` and `stitch` as adjacent but semantically different connection strategies.

## Study Validation

- ✅ Read docs: `nodes/sop/join.txt`
- ✅ Reviewed example: `examples/nodes/sop/join/BasicJoin.txt`
- ✅ Inspected both official branches (`NoWrap_Attribute`, `Wrap_Blend`)
- ✅ Performed live parameter sweeps for `blend`, `tolerance`, `loop`, `prim`, `knotmult`
