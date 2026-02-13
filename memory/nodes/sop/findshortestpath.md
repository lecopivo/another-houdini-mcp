# Find Shortest Path (SOP)

## What This Node Is For

`findshortestpath` computes lowest-cost routes across surface edges, with optional direction constraints and customizable cost models.

## Session Status

- Status: deep-studied
- Docs read: yes (`nodes/sop/findshortestpath.txt`)
- Example sets reviewed: yes (`examples/nodes/sop/findshortestpath/DirectedEdgesPath.txt`, `examples/nodes/sop/findshortestpath/PathAnalysis.txt`)
- Example OTL internals inspected: yes
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent (docs + stickies):
  - Build shortest routes while respecting directed edges, avoided edges, and weighted path costs.
  - Output can be explicit path curves and/or point-level cost maps for analysis workflows.
- Observed (live play):
  - **Directed example** (`/obj/academy_deep_findshortestpath_dir/findshortestpath1`):
    - Baseline (`start=8`, `end=2`, directed enabled): `paths_prims=1`.
    - Unreachable target (`end=0` with directed constraints): `paths_prims=0` while surface remains.
    - Disabling directed constraints (`enabledirectedprims=0`) restored reachable path (`paths_prims=1`).
    - `outputpaths=0` removed path-curve output and returned surface-only result.
    - Enabling `startpt/endpt/pathcost` outputs created corresponding primitive attrs; non-path prims carry sentinel values (`-1`).
  - **Path analysis example** (`/obj/academy_deep_findshortestpath_analysis/findshortestpath_modified_Cost`):
    - With point cost attribute enabled (`cost=weight`), per-point average route costs were much higher than no-cost branch (mean ~`30.53` vs ~`3.44`).
    - Disabling `enablecost` made modified-cost branch numerically match no-cost branch.
    - Interaction test:
      - `omitdistance=1` + `enablecost=0` produced zero cost everywhere.
      - `omitdistance=1` + `enablecost=1` produced nonzero costs driven purely by point weights.
- Mismatches: none.

## Minimum Repro Setup

- Use both official examples:
  - `DirectedEdgesPath` for reachability and directed-edge behavior.
  - `PathAnalysis` for weighted-cost behavior and diagnostics.
- Probe:
  - primitive count in `paths` group,
  - point `cost` attribute distributions,
  - output path metadata attributes when enabled.

## Key Parameter Interactions

- `enabledirectedprims` + `directedprims` can convert "reachable" endpoints into unreachable ones.
- `outputpaths` and `keep` define whether output is path-only, surface-only, or combined.
- `enablecost` and `omitdistance` together define cost semantics:
  - distance-only,
  - weight-only,
  - distance+weight,
  - or degenerate zero-cost if both disabled/omitted.
- Output metadata toggles (`outputstartpt`, `outputendpt`, `outputpathcost`, `pathsgroup`) are crucial for downstream debugging and filtering.

## Gotchas and Failure Modes

- "No path" often means constraints are working (directed or avoided edges), not necessarily node failure.
- With many start points and certain output modes, `cost` can be tuple-valued; downstream wrangles must handle tuple/array semantics.
- If `omitdistance=1` without alternative costs, routing loses geometric meaning and can collapse to uniform zero-cost behavior.
