# Spline Fit (SOP)

## What This Node Is For

`fit` rebuilds curves/surfaces from point samples using either interpolation (through data) or approximation (reduced/smoothed data).

## Session Status

- Status: deep-studied
- Docs read: yes (`nodes/sop/fit.txt`)
- Example sets reviewed: yes (`examples/nodes/sop/fit/FitCurves.txt`, `examples/nodes/sop/fit/FitSurfaces.txt`)
- Example OTL internals inspected: yes
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent (docs + stickies):
  - `Interpolation` is stable and data-following; `Approximation` is leaner but may vary CV layout during animation.
  - Scope and primitive type strongly affect CV counts and resulting shape behavior.
- Observed (live play):
  - **Curve example** (`/obj/academy_deep_fit_curves/FitCurves`):
    - Input blend curve: `8 pts`.
    - `fit_interpolate` baseline (NURBS, breakpoints): `10 pts`.
    - Interpolate scope impact:
      - `scope=global` -> `8 pts`
      - `scope=local` -> `16 pts`
      - `scope=breakpoints` -> `10 pts`
    - Interpolate type impact:
      - NURBS -> `10 pts`
      - Bezier -> `22 pts`
  - **Surface example** (`/obj/academy_deep_fit_surfaces/fit_poly_surface`):
    - Input noisy mesh: `64 pts`.
    - `fit_interpolate` baseline: `100 pts`; `fit_approximate` baseline: `16 pts`.
    - Approximate order impact:
      - `orderu/v 4->6` increased density `16 -> 36 pts`.
    - Interpolate scope/type interaction:
      - NURBS + `scope=global/local` -> `64 pts`
      - NURBS + `scope=breakpoints` -> `100 pts`
      - Bezier + `scope=breakpoints` -> `484 pts`
      - Bezier + `scope=global` -> `256 pts`
- Mismatches: none.

## Minimum Repro Setup

- Study both official examples (curves + surfaces) because each exposes different parameter behavior.
- Probe input node and both fit variants before/after each parameter change.

## Key Parameter Interactions

- `method` (approximation vs interpolation) is the biggest behavioral split.
- `scope` changes CV construction strategy in interpolation and can significantly alter output density.
- `type` (NURBS/Bezier) can multiply CV count for the same source and scope.
- `orderu/orderv` is a strong density/shape control in surface fits, especially approximation workflows.

## Gotchas and Failure Modes

- Do not assume approximation always has fixed topology over animation; stickies warn CV layout can vary as shape changes.
- For animated downstream dependencies, interpolation with stable input CV count is usually safer.
- Bezier + high-detail scope can explode point count quickly; check performance before adopting it in heavy networks.
