# Fluid Compress (SOP)

## What This Node Is For

`fluidcompress` reduces FLIP cache size by culling/packing particles and limiting fluid volume bandwidth.

## Session Status

- Status: studied
- Docs read: yes (`help/nodes/sop/fluidcompress.txt`)
- Example set reviewed: fallback companion coverage (`/obj/geo1` all branches)

## Key Notes

- Compression is intentionally lossy; tuned for downstream compatibility.
- `particleband` and volume bandwidth controls are core size/quality dials.
- Supports sparse VDB conversion and optional 16-bit write hints.
- Designed to feed `particlefluidsurface` and `whitewatersource` correctly.
