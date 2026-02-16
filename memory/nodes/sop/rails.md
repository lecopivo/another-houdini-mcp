# Rails (SOP)

## Intent

`rails` generates guide cross-section curves stretched/oriented between two rail curves, giving more placement control than basic sweep-style operations.

## Core Behavior

- Input 0 is cross-section geometry; input 1 is rail geometry.
- Produces replicated cross sections following rail pairs; commonly followed by `skin` to create final surfaces.
- Placement can be default, vertex-constrained, or rail-stretched.
- Topology counts may remain constant while shape/orientation changes significantly.

## Key Parameters

- `usevtx`, `vertex1`, `vertex2`: anchor cross-section vertices to rail points.
- `stretch`: preserve/stretch cross-section vertical scale relative to rails.
- `scale`, `roll`: global section size/orientation controls.
- `noflip`, `usedir`, `dir`: orientation stability controls.

## Typical Workflow

```text
cross section + rail pair -> rails -> point/attrib shaping -> skin
```

- Build clean open rail curves first.
- Use vertex anchoring only when specific profile points must lock to rail sides.

## Production Usage

- Useful for ribbon/loft pre-surfaces, track-like forms, and bridge sections where two rail boundaries define width/profile.
- Keep `skin` downstream as the explicit surface-building stage.

Measured outcomes (`BasicRail` example):
- Baseline rails outputs (`rails_default`, `rails_vertex`, `rails_stretch`) all kept `162 pts / 9 prims` but changed placement.
- Deformation distance vs default:
  - vertex mode (`rails_vertex`) mean point displacement `0.070899`.
  - stretch mode (`rails_stretch`) mean displacement `0.092457`.
- Shape controls on `rails_default`:
  - `scale 0.5 -> 1.0 -> 1.5` scaled Y extent `0.149149 -> 0.298297 -> 0.447446`.
  - `roll 0 -> 45 -> 90` rotated section orientation (Y extent decreased to `0`, Z extent increased to `2.470044`).
- Vertex anchoring sensitivity (`usevtx=1`):
  - `(0,1)` produced extreme spread (`bbox X 8.699169`),
  - `(9,16)` matched example’s stable placement,
  - alternate pairs changed scale/offset materially.
- Downstream `skin1/2/3` built final surfaces with `198 pts / 1 prim` from corresponding rails variants.

## Gotchas

- Rails output is typically a frame/section network, not the final shaded surface; evaluate downstream `skin` too.
- `usevtx` pair choices can massively distort section placement.
- Equal topology counts across modes can hide large positional/orientation differences.

## Companion Nodes

- `copy` for mirrored rail generation (example uses negative-scale duplicate rail source).
- `skin` for final lofted surface construction.
- `point` for per-point color/attribute treatment before skin.

## Study Validation

- ✅ Read docs: `nodes/sop/rails.txt`
- ✅ Reviewed example: `examples/nodes/sop/rails/BasicRail.txt`
- ✅ Inspected stickies and all three mode branches (`default`, `vertex`, `stretch`)
- ✅ Ran live scale/roll/vertex/stretch sweeps with measured rail and skin outputs
