# Whitewater Source (SOP)

## What This Node Is For

`whitewatersource` generates whitewater emission fields (and optional preview particles) from liquid simulation fields.

## Session Status

- Status: studied
- Docs read: yes (`help/nodes/sop/whitewatersource.txt`)
- Example set reviewed: fallback companion coverage (`/obj/geo1` branch 4)

## Key Notes

- Expects liquid `surface` and `vel`; some criteria also require particles/pressure.
- Major emission criteria: curvature, acceleration, vorticity, splash, pressure, deformation.
- Outputs `emit` plus optional pass-through fluid fields for solver handoff.
- Designed as first stage in SOP whitewater chain (`source -> solver -> postprocess`).
