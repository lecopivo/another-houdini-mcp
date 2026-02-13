# Extrude Volume (SOP)

## What This Node Is For

`extrudevolume` turns surface geometry into closed extrusion volume-like shell geometry with controllable base direction/depth and optional top/base/side grouping.

## Session Status

- Status: studied
- Docs read: yes (`nodes/sop/extrudevolume.txt`)
- Example set reviewed: yes (fallback: no local `examples/nodes/sop/extrudevolume/` folder)
- Example OTL internals inspected: yes (fallback live repro)
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent: extrude input surface along a base normal and provide usable top/base/side boundaries/groups.
- Observed: `/obj/academy_extrudevolume_live` (`grid -> extrudevolume`) outputs closed extruded mesh (`200 pts / 198 prims`), and changing `depth -1.0 -> 0.5` preserves topology while changing extrusion direction/placement.
- Mismatches: none.

## Minimum Repro Setup

- Node graph: `/obj/academy_extrudevolume_live/grid1 -> extrudevolume1 -> OUT_EXTRUDEVOLUME`
- Key parms: `depth`, `basenormal*`, optional `output*grp` toggles.
- Verification: `probe_geometry` on `OUT_EXTRUDEVOLUME`.

## Key Parameters and Interactions

- `depth` controls signed extrusion distance.
- `basenormal*` defines extrusion direction.
- Group outputs (`topgrp/basegrp/sidegrp`) are useful handoff masks for sims/shading.

## Gotchas and Failure Modes

- Non-planar/messy inputs can produce unexpected side topology.
- If you need only a solid field, convert result to VDB/SDF downstream.

## Related Nodes

- `extrude`
- `polyextrude`
- `vdbfrompolygons`
