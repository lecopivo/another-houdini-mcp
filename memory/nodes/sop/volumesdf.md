# Volume SDF (SOP)

## What This Node Is For

`volumesdf` rebuilds a signed-distance field from an iso-contour of a source volume.

## Session Status

- Status: studied
- Docs read: yes (`nodes/sop/volumesdf.txt`)
- Example set reviewed: yes (fallback: no local `examples/nodes/sop/volumesdf/` folder)
- Example OTL internals inspected: yes (fallback live repro)
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent: convert fog/volume fields to usable SDFs or renormalize existing SDFs.
- Observed: `/obj/academy_volumesdf_live` (`volume -> volumesdf`) cooks reliably; changing `iso` (`0 -> 0.5`) keeps valid output while altering target contour definition.
- Mismatches: none.

## Minimum Repro Setup

- Node graph: `/obj/academy_volumesdf_live/volume1 -> volumesdf1 -> OUT_VOLUMESDF`
- Key parms: `iso`, `invert`, `usemaxdist/maxdist`, `rebuildwithfim`.
- Verification: successful cook and stable probe output.

## Key Parameters and Interactions

- `iso` picks surface level used as rebuilt SDF zero-crossing.
- `invert` is commonly needed when converting fog-like semantics.
- Max distance controls are useful for narrow-band performance.

## Gotchas and Failure Modes

- Wrong iso choice yields offset or inverted surfaces.
- FIM mode is faster but approximate; verify quality where distance accuracy matters.

## Related Nodes

- `volume`
- `vdbfrompolygons`
- `isooffset`
