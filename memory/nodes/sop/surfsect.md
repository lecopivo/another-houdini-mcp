# Spline Surfsect (SOP)

## Intent

`surfsect` computes intersections between NURBS/Bezier surface sets and can either generate intersection profiles or perform spline-surface boolean trims.

## Core Behavior

- Intersects all surfaces in set A with set B.
- Can output boolean-trimmed surfaces (union/intersect/subtract variants) or only profile curves.
- Works with open or closed topologies; solid results depend on input sets forming solids.
- Normal orientation determines inside/outside semantics for trimming.

## Key Parameters

- Group filters: `groupa`, `groupb`.
- Precision controls: `tol3d`, `tol2d`, `step` (marching steps).
- Boolean controls: operation presets and keep-inside/outside toggles.
- Profile generation controls: target set (A/B/both), profile groups, trim-aware profile truncation, profile joining.

## Typical Workflow

```text
surface set A + surface set B -> surfsect (boolean or profiles) -> trim/bridge/model cleanup
```

- Validate surface normal direction before boolean classification.
- Use profile-only mode when extracting intersection rails for downstream trims.

## Production Usage

- Useful for spline-based CSG where polygon booleans are not appropriate.
- `SurfsectBasic` example demonstrates reciprocal subtraction: box-from-sphere and sphere-from-box outcomes.

Measured outcomes:
- Live Houdini parameter/geometry measurements are pending in this session.

## Gotchas

- Incorrect surface normal direction flips inside/outside logic and inverts boolean expectations.
- Loose tolerances can miss intersections; overly tight tolerances can increase cost/instability.
- Open input topology produces open results even when one side is solid.

## Companion Nodes

- `trim` for downstream manual spline trims.
- `carve`/`curvesect` for profile handling.
- `boolean` for polygonal CSG alternatives.

## Study Validation

- ✅ Read docs: `help/nodes/sop/surfsect.txt`
- ✅ Reviewed example: `help/examples/nodes/sop/surfsect/SurfsectBasic.txt`
- ⏳ Live validation pending
