# Curve (SOP)

## Intent

`curve` creates editable polygon/NURBS/Bezier curve primitives and supports coordinate-driven, snapping, and freehand fitting workflows.

## Core Behavior

- Supports primitive classes: polygon, NURBS, Bezier, and points.
- Input geometry can be referenced/snapped via coordinate tokens (`pN`, breakpoint references).
- Freehand mode fits sampled strokes using parameterization/tolerance/smoothing controls.
- Curve properties include close/reverse/order and optional preservation of input geometry.

## Key Parameters

- `type`, `method`: primitive and drawing interpretation.
- `coords`: explicit coordinate/reference scripting for deterministic curve authoring.
- `close`, `reverse`, `order`: topology/order and direction control.
- Freehand fitting: `param`, `tolerance`, `smooth`, `keepshape`.
- `keep`: include input geometry in output for templated construction networks.

## Typical Workflow

```text
curve -> (edit/convert/resample) -> sweep/skin/loft workflows
```

- Use explicit coordinate tokens for dependency-driven modeling rigs.
- Convert and resample early when downstream tools require polygonal regularity.

## Production Usage

- Foundational curve authoring node for manual and procedural hybrid shape setup.
- `CurveHood` example demonstrates dependency-linked curves where downstream curves follow upstream point edits.

Measured outcomes:
- Live Houdini parameter/geometry measurements are pending in this session.

## Gotchas

- Polygon `CVs` and `Breakpoints` modes behave similarly, unlike NURBS/Bezier behavior.
- Curve direction can silently affect downstream skin/sweep/orient operations.
- Freehand fitting tolerance/smoothness can over-simplify intended control features.

## Companion Nodes

- `resample` for spacing regularization.
- `convert` for primitive-type normalization.
- `skin`/`sweep` for surface generation from authored curves.

## Study Validation

- ✅ Read docs: `help/nodes/sop/curve-.txt`
- ✅ Reviewed example: `help/examples/nodes/sop/curve-/CurveHood.txt`
- ⏳ Live validation pending
