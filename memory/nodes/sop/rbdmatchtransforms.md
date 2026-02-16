# RBD Match Transforms (SOP)

## Intent

`rbdmatchtransforms` extracts per-piece transforms from simulated geometry/proxy and reapplies them to matching reference geometry and optional constraints.

## Core Behavior

- Uses an untransformed reference (input 4) to derive per-name transform deltas.
- Can extract transforms from geometry input or proxy input.
- Applies matched transforms to geometry pieces by `name`.
- Optionally transforms constraint points and recomputes `restlength`.

## Key Parameters

- `Reference`: choose source (geometry vs proxy geometry) for transform extraction.
- `Transform Constraints`: include constraint points in transform application.
- `Update Rest Length`: recompute constraint primitive rest lengths after transform.

## Typical Workflow

```text
sim/proxy result + constraints + original rest geo -> rbdmatchtransforms -> downstream render/constraint stages
```

- Use when piece transforms need to be reconstructed onto alternate-resolution or rest-state geometry.

## Production Usage

- Helpful in RBD workflows where render/proxy representations diverge and transforms must be reconciled by name.
- `RBDMatchTransforms` example demonstrates SOP usage in this transform-reapplication role.

Measured outcomes:
- Live Houdini parameter/geometry measurements are pending in this session.

## Gotchas

- Requires consistent naming between transformed and reference pieces.
- If constraints are transformed, stale rest lengths can produce incorrect solver behavior unless updated.

## Companion Nodes

- `rbdmaterialfracture` for source piece generation.
- `rbdxform` and `rbddeformpieces` for adjacent transform/deform workflows.

## Study Validation

- ✅ Read docs: `help/nodes/sop/rbdmatchtransforms.txt`
- ✅ Reviewed example: `help/examples/nodes/sop/rbdmatchtransforms/RBDMatchTransforms.txt`
- ⏳ Live validation pending
