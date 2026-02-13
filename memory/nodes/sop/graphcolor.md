# Graph Color (SOP)

## What This Node Is For

`graphcolor` assigns integer IDs so directly connected elements never share the same value, enabling safe batching/worksets for parallel operations.

## Session Status

- Status: deep-studied
- Docs read: yes (`nodes/sop/graphcolor.txt`)
- Example set reviewed: yes (`examples/nodes/sop/graphcolor/FindNonInteractingAgents.txt`)
- Example HDA internals inspected: yes
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent (docs + example):
  - Partition crowd agents (or general graph elements) into non-interacting batches.
  - Support workset detail arrays for OpenCL multi-pass processing.
- Observed (live play):
  - Example network confirmed crowd use-case and `batch` point attribute concept.
  - Controlled live repro (`grid -> graphcolor`) showed mode-dependent coloring:
    - connectivity=Point -> point `color` attribute with 4 colors on 20x20 quad grid.
    - connectivity=Primitive -> primitive `color` attribute with 4 colors.
    - connectivity=Polygon Edge -> primitive `color` attribute with 2 colors (map-coloring-like checkerboard on quad grid).
  - `sortoutput=1` changed color layout to contiguous runs (run count dropped from 400 to 4 in point mode).
  - `createworksets=1` emitted detail arrays:
    - example point mode: `ws_begin=(0,100,200,300)`, `ws_len=(100,100,100,100)`.
  - Workset arrays updated by connectivity mode and resulting color frequencies.
- Mismatches: none.

## Minimum Repro Setup

- Reliable test setup: `/obj/academy_graphcolor_live` with a medium-resolution quad grid.
- Test each connectivity mode and inspect:
  - class of output attribute (point vs primitive),
  - number of unique colors,
  - workset detail arrays.

## Key Parameter Interactions

- `type` changes both connectivity rule and attribute class.
- `sortoutput` is important for contiguous memory/workset-friendly layout.
- `createworksets` + custom names (`worksets_begin`, `worksets_length`) define downstream OpenCL batching contract.

## Gotchas and Failure Modes

- Color count is heuristic/greedy, not globally minimal; do not hardcode expected exact counts across arbitrary meshes.
- Downstream nodes must read the right class (point vs primitive) based on connectivity mode.
- Workset arrays are only meaningful when output is sorted/grouped as intended.
