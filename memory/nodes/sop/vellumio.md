# Vellum I/O (SOP)

## What This Node Is For

`vellumio` streamlines caching Vellum geometry/constraints and loading from disk.

## Session Status

- Status: studied
- Docs read: yes (`help/nodes/sop/vellumio.txt`, legacy `help/nodes/sop/vellumio-.txt`)
- Example set reviewed: fallback companion coverage (no local `help/examples/nodes/sop/vellumio/` folder)
- QA pass complete: yes

## Source-of-Truth Split

- Intent: choose storage mode (`Geometry Only` vs packed geometry+constraints), then switch live vs cached reads.
- Observed: `/obj/academy_vellumconstraints_grain/io` output keeps Vellum stream compatible with downstream SOPs; node carries file-cache style expressions by default.
- Mismatches: none.

## Practical Notes

- Use packed geometry+constraints when you need restarts or constraint visualization from cache.
- Use geometry-only when storage size is priority and restart is not required.
