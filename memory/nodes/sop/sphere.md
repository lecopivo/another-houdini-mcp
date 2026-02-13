# Sphere (SOP)

## Practical Note (Vellum)

- For Vellum collision input, prefer polygonal sphere output (`type=poly` or `type=polymesh`) rather than primitive sphere output.
- Primitive analytic sphere output is not a reliable collider source for these SOP-level Vellum setups.

## Verification Snapshot

- Node checked: `/obj/academy_vellum_setup1_cloth/collider_sphere`
- Collider mode set to polygon: `type=poly`
- Geometry probe confirms mesh output (non-zero points/primitives) suitable for collision input.

## Workflow Reminder

- After choosing a collider source, always run a quick geometry probe and confirm the node emits polygonal geometry before wiring it into `vellumsolver` input 2.
