# FLIP Container (SOP)

## What This Node Is For

`flipcontainer` initializes SOP FLIP simulation streams (sources/container/collisions) and core fluid properties.

## Session Status

- Status: studied
- Docs read: yes (`help/nodes/sop/flipcontainer.txt`)
- Example set reviewed: fallback companion coverage (`/obj/geo1`)

## Key Notes

- `particlesep` is the primary resolution dial and must match `flipsolver` setup.
- `gridscale` affects voxel resolution and memory pressure.
- Input can be closed geometry/volume for custom domain shape.
- Provides three synchronized streams consumed by downstream FLIP SOP nodes.
