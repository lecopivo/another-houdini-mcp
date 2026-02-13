# Volume (SOP)

## What This Node Is For

`volume` creates volume primitives (scalar/vector/matrix ranks) with configurable bounds, resolution, and metadata semantics.

## Session Status

- Status: studied
- Docs read: yes (`nodes/sop/volume.txt`)
- Example set reviewed: yes (fallback: no local `examples/nodes/sop/volume/` folder)
- Example OTL internals inspected: yes (fallback live repro)
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent: create base volume fields and initialize their size/resolution/type info.
- Observed: `/obj/academy_volume_live` produced valid volume primitive output; increasing `samplediv` (`10 -> 20`) changes internal resolution behavior while keeping one primitive representation.
- Mismatches: none.

## Minimum Repro Setup

- Node graph: `/obj/academy_volume_live/volume1 -> OUT_VOLUME`
- Key parms: `rank`, `name`, `initialval*`, `samplediv`/`divs*`, `volborder`, `voltypeinfo`.
- Verification: `probe_geometry` validity and successful parameter recook.

## Key Parameters and Interactions

- `rank` and `name` define simulation/shader binding semantics.
- Resolution controls (`samplediv` or explicit `divs*`) drive fidelity/perf.
- Border mode matters when sampling outside bounds.

## Gotchas and Failure Modes

- Default unnamed fields can create ambiguous downstream binding.
- Overly dense grids become memory-heavy quickly.

## Related Nodes

- `volumewrangle`
- `volumevop`
- `volumesdf`
