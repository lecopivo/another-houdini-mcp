# RBD Cone Twist Constraint Properties (SOP)

## Intent

`rbdconetwistconstraintproperties` authors and edits Bullet cone-twist constraint attributes, globally and per-constraint, including interactive viewport editing.

## Core Behavior

- Writes cone-twist relationship attributes onto constraint primitives.
- Supports global param-driven editing and per-constraint overrides (individual edits).
- Provides tooling to import/update/clear edits and interactive axis/limit manipulation.
- Supports filtering constraints by constrained piece groups.

## Key Parameters

- Selection/filtering: constraint group, piece-group filtering modes.
- Edit controls: edit parms mode, lock axis, guide scale, clear/import/update edits.
- Constraint setup: constraint name, soft constraint enable.
- Rotation/translation limits, CFM/ERP, stiffness/damping, motor target and impulse controls.

## Typical Workflow

```text
constraint geometry -> rbdconetwistconstraintproperties -> rbdbulletsolver
```

- Establish global limits/motor behavior first.
- Apply per-constraint overrides only where needed; keep edit state manageable.

## Production Usage

- Used for articulated/mechanical hinge-like Bullet rigs with controlled angular cones and twist limits.
- `ConeTwist` example demonstrates mechanical cone-twist setup workflow.

Measured outcomes:
- Live Houdini constraint-behavior measurements are pending in this session.

## Gotchas

- Individual edits supersede node-level parameters; forgotten overrides can hide global changes.
- Axis locking/edit mode choices alter whether edits reorient constraints or only alter limits.
- Motor settings interact strongly with mass/impulse limits and can destabilize if overtuned.

## Companion Nodes

- `rbdbulletsolver` for simulation.
- `rbdconstraintproperties` for other constraint families.
- fracture/constraint-creation SOPs (`rbdmaterialfracture`, constraints-from-*).

## Study Validation

- ✅ Read docs: `help/nodes/sop/rbdconetwistconstraintproperties.txt`
- ✅ Reviewed example: `help/examples/nodes/sop/rbdconetwistconstraintproperties/ConeTwist.txt`
- ⏳ Live validation pending
