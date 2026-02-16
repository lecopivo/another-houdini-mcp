# PolyHinge (SOP)

## Intent

`polyhinge` extrudes polygon faces or edge-defined pieces around a hinge pivot line, producing front/back/side regions with controllable division and inset behavior.

## Core Behavior

- Operates on primitive or edge groups, with piece detection by connectivity.
- Supports pivot definition by selected hinge edge, explicit position+direction, or per-piece attributes.
- Builds hinged side topology with angle/division/inset controls.
- Can output grouped front/back/side/inset/boundary regions for downstream processing.

## Key Parameters

- Group selection: `group`, `grouptype`.
- Pivot controls: `pivotmode`, `hingeedge`, explicit pivot pos/dir, pivot attrs.
- Angle/divisions: `hingeangle`, division mode (`max angle` vs `count`), equal spacing.
- Inset/fuse controls: `inset`, common inset limit, fuse hinge/collided points, tolerance.
- Output controls: front/back/side toggles and named output groups.

## Typical Workflow

```text
polygon region or edge strip -> polyhinge -> optional convertline/fuse/bevel cleanup
```

- Define hinge pivot contract first, then tune angle/division density.
- Use output groups to isolate front/back/side for material or secondary modeling stages.

## Production Usage

- Useful for panel flaps, mechanical foldouts, and edge-based hinged shell construction.
- `PolyHingeBasic` demonstrates face-group hinge around pivot edge.
- `PolyHingeEdge` demonstrates open-curve extrusion around freely positioned pivot line.

Measured outcomes:
- Live Houdini parameter/geometry measurements are pending in this session.

## Gotchas

- Edge-centric mode requires valid hinge edge selection; missing edges yields warnings.
- Group type controls attribute class expectation (primitive vs point); mismatches break attribute-driven pivots/scales.
- Deprecated isolating advice: use `convertline` for edge-group extraction (not split/blast), as noted in docs.

## Companion Nodes

- `polybridge`, `polybevel`, `polyextrude` for related panel/extrusion workflows.
- `convertline` for clean edge extraction from output edge groups.

## Study Validation

- ✅ Read docs: `help/nodes/sop/polyhinge.txt`
- ✅ Reviewed examples: `help/examples/nodes/sop/polyhinge/PolyHingeBasic.txt`, `help/examples/nodes/sop/polyhinge/PolyHingeEdge.txt`
- ⏳ Live validation pending
