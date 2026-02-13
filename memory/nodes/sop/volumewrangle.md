# Volume Wrangle (SOP)

## What This Node Is For

`volumewrangle` runs VEX per voxel to read/write volume/VDB values.

## Session Status

- Status: studied
- Docs read: yes (`nodes/sop/volumewrangle.txt`)
- Example set reviewed: yes (fallback: no local `examples/nodes/sop/volumewrangle/` folder)
- Example OTL internals inspected: yes (fallback live repro)
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent: text-based low-level voxel modification (volume equivalent of wrangle-style workflows).
- Observed: `/obj/academy_volumewrangle_live` with snippet `@density = @density + 0.25;` cooked successfully on a `volume` input and preserved expected volume primitive representation.
- Mismatches: none.

## Minimum Repro Setup

- Node graph: `/obj/academy_volumewrangle_live/volume1 -> volumewrangle1 -> OUT_VOLUMEWRANGLE`
- Key parms: `snippet`, `group`, `bindeach`, `exportlist`.
- Verification: successful cook + `probe_geometry` validity.

## Key Parameters and Interactions

- `snippet` controls all behavior; keep it explicit and minimal.
- `bindeach` changes name-binding semantics (`@density` reuse pattern).
- `exportlist` can reduce unnecessary write/copy overhead.

## Gotchas and Failure Modes

- Writing to unknown `@name` does not create a new volume automatically.
- Time variables should use `Frame/Time/TimeInc`, not `$F` inside snippet context.

## Related Nodes

- `volumevop`
- `volumemix`
- `volume`
