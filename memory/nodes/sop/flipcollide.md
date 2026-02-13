# FLIP Collide (SOP)

## What This Node Is For

`flipcollide` converts geometry/volumes into collision data for SOP FLIP and merges with incoming collision streams.

## Session Status

- Status: studied
- Docs read: yes (`help/nodes/sop/flipcollide.txt`)
- Example set reviewed: fallback companion coverage (`/obj/geo1` branch 4)

## Key Notes

- Input 3 is new collider geometry/volume.
- `dovolume` for solid closed colliders; `dosurface` for open/sheet colliders.
- Collision velocity quality is critical for splash realism and leak prevention.
- Collision resolution follows `flipcontainer.particlesep` + `gridscale`.
