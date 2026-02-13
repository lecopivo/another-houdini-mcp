# Vellum Constraint Property (DOP)

## What This Node Is For

`vellumconstraintproperty` edits existing constraint attributes during solve (stiffness, damping, rest values, break thresholds, removal, etc.).

## Session Status

- Status: studied
- Docs read: yes (`help/nodes/dop/vellumconstraintproperty.txt`)
- Example set reviewed: fallback companion coverage (no local `help/examples/nodes/dop/vellumconstraintproperty/` folder)
- QA pass complete: yes (live DOP node + prior companion usage in vellumsolver examples)

## Key Takeaways

- Best used for modifying constraints already present in `ConstraintGeometry`.
- Use `vellumconstraints` DOP/SOP to create new constraints; use this node to animate/adjust existing ones.
- `Use VEXpression` gives precise per-constraint control and supports external geometry bindings.
