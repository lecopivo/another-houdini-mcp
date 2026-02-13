# VDB Activate (SOP)

## What This Node Is For

`vdbactivate` edits the active voxel region of VDB grids for downstream sparse processing.

## Session Status

- Status: studied
- Docs read: yes (`nodes/sop/vdbactivate.txt`)
- Example set reviewed: yes (fallback: no local `examples/nodes/sop/vdbactivate/` folder)
- Example OTL internals inspected: yes (fallback live repro)
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent: union/intersect/subtract/copy activation domains, optionally fill values and prune/deactivate background.
- Observed: `/obj/academy_vdbactivate_live` (`sphere -> vdbfrompolygons -> vdbactivate`) kept valid VDB output; changing `expand` increased activation band logically while retaining one VDB primitive in probe representation.
- Mismatches: none.

## Minimum Repro Setup

- Node graph: `/obj/academy_vdbactivate_live/sphere1 -> vdbfrompolygons1 -> vdbactivate1 -> OUT_VDBACTIVATE`
- Key parms: `operation`, `expand`, `setvalue/value`, region selectors.
- Verification: `probe_geometry` validity + stable VDB primitive output.

## Key Parameters and Interactions

- `operation` defines activation boolean behavior.
- `expand` is a fast way to create room before volume operations.
- `prune`/deactivate controls are important cleanup steps.

## Gotchas and Failure Modes

- Activation changes are not always obvious in basic probe stats; inspect visually with VDB visualize tools when needed.
- Over-expanding active regions can reduce sparse-performance benefits.

## Related Nodes

- `vdbfrompolygons`
- `volumevop`
- `volumewrangle`
