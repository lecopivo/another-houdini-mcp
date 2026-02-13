# Fractal (SOP)

## What This Node Is For

`fractal` subdivides and displaces geometry to create jagged/noisy forms, commonly used for terrain, rocks, and debris-style breakup.

## Session Status

- Status: deep-studied
- Docs read: yes (`nodes/sop/fractal.txt`)
- Example set reviewed: yes (`examples/nodes/sop/fractal/FractalGeoTypes.txt`)
- Example OTL internals inspected: yes
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent (docs + stickies):
  - Increase detail via subdivisions (`divs`) and apply randomized displacement controlled by `smooth`, `scale`, `seed`.
  - Displacement can follow explicit direction vector or point normals (`vtxnms`).
- Observed (live play):
  - Geometry-type baseline differs strongly:
    - polygon sphere branch baseline: `642 pts / 1280 prims`.
    - NURBS sphere branch baseline: `1480 pts / 1 prim`.
  - Increasing `divs` from `2 -> 3` increased density significantly:
    - polygon branch: `642 -> 2562 pts`.
    - NURBS branch: `1480 -> 5840 pts`.
  - On polygon branch, `scale` and `smooth` interaction:
    - `scale 1 -> 2` increased radial roughness variance (higher radius std dev).
    - `smooth 8` dramatically reduced roughness variance versus `smooth 3`.
  - Direction mode interaction:
    - `vtxnms=0` with `dir=(0,1,0)` constrained displacement mostly in Y (X/Z bounds stayed near sphere limits).
    - `vtxnms=1` produced fuller isotropic displacement around local normals (expanded X/Y/Z bounds).
  - Changing `seed` altered pattern while preserving overall roughness class (similar aggregate stats, different sample positions).
- Mismatches: none.

## Minimum Repro Setup

- Example object: `/obj/academy_deep_fractal`.
- Use `Fractal_Polygons/fractal1` for fast parameter iteration and `Fractal_NURBS/fractal1` for type-contrast checks.
- Validate with topology counts plus simple shape metrics (bbox and roughness statistics), not counts alone.

## Key Parameter Interactions

- `divs` is the primary topology growth control.
- `scale` controls displacement amplitude; `smooth` counterbalances jaggedness per division.
- `vtxnms` toggles normal-driven displacement versus explicit global direction vector.
- `seed` changes noise realization without fundamentally changing control ranges.

## Gotchas and Failure Modes

- Fractal can increase topology very quickly; budget subdivision levels early.
- Direction-vector mode can unintentionally bias deformation to one axis if `vtxnms` is off.
- Different primitive types respond differently in topology representation; compare like-for-like before judging output quality.
