# Grid (SOP)

## What This Node Is For

`grid` creates planar surfaces/lines/points with selectable primitive type, connectivity, and orientation.

## Session Status

- Status: deep-studied
- Docs read: yes (`nodes/sop/grid.txt`)
- Example set reviewed: yes (`examples/nodes/sop/grid/GridBasic.txt`)
- Example OTL internals inspected: yes
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent (docs + example):
  - Show how primitive type and connectivity alter topology while preserving planar parameterization.
- Observed (live play):
  - Baseline 10x10 grids:
    - quads: `100 pts / 81 prims`
    - triangles/alternating triangles: `100 pts / 162 prims`
    - rows-only: `100 pts / 10 prims`
    - columns-only: `100 pts / 10 prims`
    - mesh/NURBS/Bezier: `100 pts / 1 prim`
  - Density math check on polygon grid:
    - `rows=20`, `cols=5` -> `100 pts / 76 prims` (`(rows-1)*(cols-1)`).
  - Connectivity interaction:
    - switching `surftype` from quads to triangles doubled primitive count with same points (`76 -> 152 prims`).
  - Orientation interaction:
    - changing orientation from XY to XZ moved extent from Z=0 plane to Y=0 plane (bbox axis swap).
  - Primitive type interaction:
    - `type=Points` yielded `100 pts / 0 prims` (point-cloud mode).
- Mismatches: none.

## Minimum Repro Setup

- Use `GridBasic` example to compare multiple branches side-by-side.
- Probe representative nodes (`polygonal`, `triangles`, `rows`, `mesh`, etc.) and verify topology formulas against row/column settings.

## Key Parameter Interactions

- `rows`/`cols` set sample lattice count; primitive count depends on connectivity mode.
- `type` changes representation class (surface vs points-only), which changes downstream compatibility.
- `surftype` controls polygon connectivity behavior for polygon/mesh types.
- `orient` changes working plane, which affects any world-axis-dependent downstream ops.

## Gotchas and Failure Modes

- Counting rows/cols as primitive count is a common mistake; actual primitives are connectivity-derived.
- Mesh/NURBS/Bezier single-primitive behavior can surprise group/primitive-based downstream operations.
- Points-only mode intentionally outputs no primitives; downstream primitive ops will appear to "do nothing".
