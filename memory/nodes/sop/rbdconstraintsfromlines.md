# RBD Constraints From Lines (SOP)

## Intent

`rbdconstraintsfromlines` creates rigid-body constraint geometry from artist-drawn viewport lines between pieces, enabling direct manual constraint authoring.

## Core Behavior

- Interactive line drawing/editing drives constraint creation.
- Supports multiple connection types (surface points, hinges, center of mass).
- Can merge with existing constraints and use proxy geometry for build context.
- Hinge editing tools allow explicit hinge placement and adjustment.

## Key Parameters

- `Connection Type`: determines anchor/line construction strategy.
- `Hinge Length`: hinge constraint extent control.
- Group/tag naming inherited from rule-based constraint systems.
- Utilities: clear lines/hinge edits, object-link and constraint-link guides.

## Typical Workflow

```text
packed pieces (+existing constraints/proxy) -> rbdconstraintsfromlines -> rbdconstraintproperties -> rbdbulletsolver
```

- Draw coarse interactive links first, then refine hinge placement and properties downstream.

## Production Usage

- Useful for fast art-directed structural constraints where procedural rules are insufficient.
- `RBDConstraints` example demonstrates combined usage with constraints-from-curves and constraints-from-rules approaches.

Measured outcomes:
- Live Houdini interactive/geometry measurements are pending in this session.

## Gotchas

- Viewport-authored constraints are inherently manual and can drift from regenerated fracture topology.
- Wrong connection type can produce unintuitive anchor placement (especially hinges vs COM links).

## Companion Nodes

- `rbdconstraintsfromcurves`, `rbdconstraintsfromrules` for alternate constraint authoring.
- `rbdconstraintproperties` for physical behavior setup.
- `rbdbulletsolver` for simulation.

## Study Validation

- ✅ Read docs: `help/nodes/sop/rbdconstraintsfromlines.txt`
- ✅ Reviewed example: `help/examples/nodes/sop/rbdconstraintsfromlines/RBDConstraints.txt`
- ⏳ Live validation pending
