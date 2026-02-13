# Sphere (SOP)

## What This Node Is For

`sphere` generates sphere/ellipsoid geometry in multiple primitive representations.

## Session Status

- Status: studied
- Docs read: yes (`nodes/sop/sphere.txt`)
- Example set reviewed: yes (`examples/nodes/sop/sphere/SphereTypes.txt`)
- Example OTL internals inspected: yes (`SphereTypes.otl`)
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent: choose geometry type based on fidelity, editability, and performance.
- Observed:
  - Live repro `/obj/academy_sphere_live`: default primitive type is analytic (`1 pt / 1 prim`); switching to polygon type with `freq=3` gives explicit mesh (`92 pts / 180 prims`).
  - Example `/obj/academy_SphereTypes` validates practical type comparison across primitive/polygon/mesh/NURBS/Bezier (perfect + imperfect).
- Mismatches: none.

## Minimum Repro Setup

- Node graph: `/obj/academy_sphere_live/sphere1 -> OUT_SPHERE`
- Key parms: `type`, `freq`, `rows/cols`, `rad*`, `imperfect`, `triangularpoles`.
- Verification: `probe_geometry` before/after type/frequency changes.

## Key Parameters and Interactions

- `type` has the largest downstream impact (analytic vs explicit topology).
- `freq` is polygon-only density control.
- NURBS/Bezier imperfect toggles alter CV distribution and edit behavior.

## Practical Collision Reminder (from prior Vellum tests)

- For Vellum collision inputs, prefer polygonal sphere output over primitive sphere output.
- Always probe topology before wiring into solver collision inputs.

## Gotchas and Failure Modes

- Primitive sphere output can be too abstract for SOP-level topology operations.
- Overly high polygon frequency increases cost quickly.

## Related Nodes

- `box`
- `tube`
- `bound`
