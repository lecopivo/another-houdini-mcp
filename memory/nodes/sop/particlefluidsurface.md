# Particle Fluid Surface (SOP)

## What This Node Is For

`particlefluidsurface` builds renderable liquid surfaces from FLIP/Vellum-fluid particles (and optional compressed fluid fields).

## Session Status

- Status: studied
- Docs read: yes (`help/nodes/sop/particlefluidsurface.txt`)
- Example set reviewed: fallback companion coverage (`/obj/geo1` all branches)

## Key Notes

- Input 0: particles (often from `filecache`), inputs 1/2: compressed fields/collisions.
- Supports multiple output modes: preview, VDB, polygons, polygon soup.
- `method` and filtering stack (`dilate/smooth/erode`) control shape quality.
- Handles compressed FLIP seamlessly when fed matching `surface/vel` data.
