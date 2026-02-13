# Fur (SOP)

## What This Node Is For

`fur` generates hair-like curves from skin geometry or explicit root points, with optional guides/clumps/parting and CVEX-based styling.

## Session Status

- Status: deep-studied
- Docs read: yes (`nodes/sop/fur.txt`)
- Example sets reviewed: yes (`examples/nodes/sop/fur/FurBall.txt`, `examples/nodes/sop/fur/PointFur.txt`)
- Example OTL internals inspected: yes
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent (docs + stickies):
  - Use skin area+density for stochastic hair generation, or use point-cloud roots for explicit placement.
  - Guides/clumps influence shape and distribution; shaders can add attributes like `width`.
- Observed (live play):
  - **FurBall (surface+guide mode)**:
    - baseline: `1230` hair prims, `12300` points.
    - lowering `density 100 -> 20`, `length 0.5 -> 0.2`, and raising `segs 4 -> 8` gave `259` hair prims, `2590` points.
    - `display` affects cooked output count in this mode: `display=0.1` reduced to `27` prims / `270` points.
  - **PointFur (explicit roots mode)**:
    - input roots are points-only geometry with `P` + `N` (`4800` points).
    - output produced exactly `4800` hair prims (one per root point).
    - changing `density` and `display` did not change hair count in this mode (root-count driven), but `segs` changed points per hair (`segs=10` -> `52800` points total).
    - output primitive attrs included `N`, `whitehair`, `guardhair`, `furdensity` from shader/attribute pipeline.
- Mismatches: none.

## Minimum Repro Setup

- Use both examples because they represent different generation contracts:
  - `FurBall` for area-density stochastic generation.
  - `PointFur` for explicit root-point generation.
- Probe both input root geometry and fur output after each parameter change.

## Key Parameter Interactions

- `density` and `display` are meaningful for area-based generation from skin surfaces.
- In explicit point-root mode, root count dominates; density/display may not reduce hair count.
- `segs` directly controls vertices per hair and thus geometry size.
- Guide/clump radii only matter when corresponding inputs/attributes are present.

## Gotchas and Failure Modes

- Misinterpreting generation mode leads to wrong expectations ("density not working" when roots are explicit points).
- Fur output cost scales quickly with `segs * hair_count`; tune segments with performance budget in mind.
- Stable distribution on animated skins depends on proper rest-space attributes (`rest`, direction attrs for point-cloud workflows).
