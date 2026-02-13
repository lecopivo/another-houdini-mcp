# Vellum Constraints (SOP)

## What This Node Is For

`vellumconstraints` builds and updates Vellum constraint geometry that pairs with simulation geometry for `vellumsolver`.

- output 0: simulation/display geometry
- output 1: constraint geometry

Most Vellum materials/workflows are assembled by chaining one or more `vellumconstraints` nodes (for example: Hair constraints, then Pin constraints).

## Session Status

- Status: studied
- Docs read: yes (`help/nodes/sop/vellumconstraints.txt`)
- Example set reviewed: fallback companion coverage via `sop/vellumsolver` examples and custom live setups (no local `help/examples/nodes/sop/vellumconstraints/` folder in this corpus)
- Node comments read: yes (from companion examples)
- Sticky notes read: yes (from companion examples)
- QA pass complete: yes (live debug + frame sampling)

## Source-of-Truth Split

- Intent (docs/comments/stickies):
  - One node can generate many constraint types (`cloth`, `hair`, `pin`, `attach`, `stitch`, `glue`, `tet*`, etc.).
  - Pinning and attachment behavior is group-driven and can be animated/matched over time.
  - Constraint setup is often layered in multiple stages for clarity/control.
- Observed (live scene/params/geometry):
  - In `/obj/academy_vellum_setup3_hair`, using `constrainttype=hair` and `constrainttype=pin` in separate nodes produced predictable behavior.
  - Empty or wrong-class groups can silently lead to "bad sim" symptoms (roots free-falling instead of pinned).
  - Frame sampling confirmed root drift disappears once valid pin constraints are actually created and wired.
- Mismatches:
  - No docs mismatch; the failures were setup-level (group creation and constraint staging), not solver bugs.

## Minimum Repro Setup

- Node graph:
  - `guides -> hair_constraints (hair) -> pin_constraints (pin) -> vellumsolver`
- Key parameter names and values:
  - `hair_constraints.constrainttype=hair`
  - `pin_constraints.constrainttype=pin`
  - `pin_constraints.group=pins`
  - `pin_constraints.matchanimation=1`
- Output verification method:
  - Validate group count before solve, then sample root point movement over frames.

## Key Parameters and Interactions

- `constrainttype`:
  - Defines what is actually built; wrong choice can produce valid but unintended behavior.
- `group` / `grouptype`:
  - Must match real geometry class and be non-empty.
- `pingroup` + `matchanimation` (Pin to Animation section):
  - Critical when using soft pin workflows and animated targets.
- `computeorient` (hair workflows):
  - Important for deforming/animated hair pipelines.

## Practical Use Cases

1. Multi-stage setup: `cloth/hair` base constraints followed by `pin/attach/stitch/glue` refinements.
2. Debugging unstable Vellum setups by isolating each constraint stage and verifying group membership.

## Gotchas and Failure Modes

- Empty groups often fail silently and look like solver instability.
- Group class mismatch (`primitive` vs `point`) causes downstream constraints to target nothing.
- Combining too many behaviors in one node makes failures harder to isolate; staged nodes are easier to debug.

## Related Nodes

- `vellumsolver`
- `vellumconstraints_grain`
- `vellumpostprocess`
- `vellumio`

## Academy QA Checklist

- [x] Official docs reviewed
- [x] Example files reviewed (fallback companion coverage)
- [x] Node comments read
- [x] Sticky notes read
- [x] Behavior validated with at least one observed test
- [x] Source-of-truth split documented (intent vs observed)
- [x] Context and progress files updated
