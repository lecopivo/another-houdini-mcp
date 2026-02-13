# Whitewater Post-Process (SOP)

## What This Node Is For

`whitewaterpostprocess` prepares simulated whitewater for rendering as particles, fog volume, or mesh.

## Session Status

- Status: studied
- Docs read: yes (`help/nodes/sop/whitewaterpostprocess.txt`)
- Example set reviewed: fallback companion coverage (`/obj/geo1` branch 4)

## Key Notes

- Can remap `density` and `pscale` from age/depth/domain proximity.
- Supports output conversion to fog/mesh for render workflows.
- Includes flattening/clip controls to blend with domain boundaries.
- Input contract matches whitewater solver outputs (particles+container+collisions).
