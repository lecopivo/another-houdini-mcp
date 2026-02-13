# FLIP Boundary (SOP)

## What This Node Is For

`flipboundary` adds/removes fluid and applies boundary-driven velocity/pressure behavior using source/sink geometry or volumes.

## Session Status

- Status: studied
- Docs read: yes (`help/nodes/sop/flipboundary.txt`)
- Example set reviewed: fallback companion coverage (`/obj/geo1` branches 1/2)

## Key Notes

- Modes: `source` and `sink`.
- Boundary methods: `none`, `velocity`, `pressure`.
- Pressure and waterline controls are useful for fill-to-level behavior.
- Deformation velocity transfer (`computevel`) matters for animated emitters/sinks.
