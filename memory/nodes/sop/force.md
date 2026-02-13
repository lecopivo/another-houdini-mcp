# Force (SOP)

## What This Node Is For

`force` writes metaball force-field attributes used by particle-style solvers (radial attraction/repulsion and directional components).

## Session Status

- Status: deep-studied
- Docs read: yes (`nodes/sop/force.txt`)
- Example set reviewed: yes (`examples/nodes/sop/force/ForceBasic.txt`)
- Example OTL internals inspected: yes
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent (docs + examples):
  - Combine metaball influence with radial and/or directional force attributes.
  - Positive radial attracts, negative radial repels.
  - Directional force components are in metaball-local orientation.
- Observed (live play):
  - In example networks, radial branch outputs only `fradial`; directional branch outputs `dir`, `fedge` (axial), `fvortex`, `fspiral`, and `fradial`.
  - In clean live setup (`metaball -> force`):
    - with both toggles off (`doradial=0`, `doaxis=0`), force primitive attrs are empty.
    - enabling only radial creates only `fradial`.
    - enabling axis creates directional attrs and maps parameters as:
      - `axial -> fedge`
      - `vortex -> fvortex`
      - `spiral -> fspiral`
      - `dir* -> dir`
  - Non-metaball input behavior:
    - connecting a `sphere` to `force` passed geometry through with no force attrs added (matches docs: non-metaball has no force effect).
- Mismatches: none.

## Minimum Repro Setup

- Example: `/obj/academy_deep_force` (`radial_force` + `directional_force` branches).
- Verification setup: `/obj/academy_force_live/metaball1 -> force1 -> OUT_FORCE`.
- Validate by inspecting primitive attributes on `force1` output.

## Key Parameter Interactions

- `doradial` gates `fradial` creation entirely.
- `doaxis` gates all directional attrs (`dir`, `fedge`, `fvortex`, `fspiral`).
- Directional values are interpreted in metaball-local orientation; upstream metaball transforms alter effective world-space force direction.

## Gotchas and Failure Modes

- If no force attrs appear, first check toggle gates (`doradial`, `doaxis`).
- Do not assume force node modifies arbitrary geometry; it is metaball-force authoring, not a general geometry deformer.
- In old particle workflows, force-field strength can become unstable quickly; keep scales conservative and tune incrementally.
