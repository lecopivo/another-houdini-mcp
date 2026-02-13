# Falloff (SOP)

## What This Node Is For

`falloff` writes smooth distance-based point attributes (and optional groups/lead-point links) for procedural masking.

## Session Status

- Status: deep-studied
- Docs read: yes (`nodes/sop/falloff.txt`)
- Example set reviewed: yes (`examples/nodes/sop/falloff/falloff_twisted_squab.txt`)
- Example HDA internals inspected: yes
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent (docs + stickies):
  - Measure distance from a source group and emit a smooth mask attribute for downstream deformation.
  - Example uses falloff from squab tail and blends undeformed/deformed geometry via wrangle.
- Observed (live play):
  - Baseline output includes `vis_falloff`; enabling `outputleadpt` and `outputgroup` adds `falloff_leadpt` and point group `insideRad`.
  - Radius strongly controls affected scope: `rad=3` -> `insideRad=2678` points; `rad=1` -> `insideRad=279` points.
  - `reverse` flips effective influence distribution (`vis_falloff` mean about `0.025` vs `0.975` in tested setup).
  - `outputtype=Unbounded Distance` produced values above 1 (`max ~5.32`), which caused strong extrapolation in downstream `lerp` blend (`blend_max_disp ~11.30`).
  - Renaming `distattr` from `vis_falloff` to `tailmask` broke downstream wrangle contract (`@vis_falloff` missing), resulting in zero deformation (`blend_avg_disp=0`).
- Mismatches: none.

## Minimum Repro Setup

- Example network: `/obj/academy_deep_falloff`.
- Core chain: `testgeometry_squab1 -> falloff -> (bend + attribwrangle blend)`.
- Key downstream contract in example wrangle:
  - `@P = lerp(@P, @opinput1_P, @vis_falloff);`
- Verification used point-attribute checks, group counts, and source-vs-output displacement metrics.

## Key Parameter Interactions

- `distattr` is an API contract for downstream nodes; renaming requires downstream updates.
- `outputtype` changes numeric range semantics; unbounded output is dangerous for direct blend weights.
- `reverse` and `ramp` shape where influence accumulates, even when topology is unchanged.
- `outputleadpt` and `outputgroup` are high-value debug/selection outputs for downstream control.

## Gotchas and Failure Modes

- Using unbounded distance directly as a blend weight can overdrive deformation.
- Falloff often changes only attributes/groups, so geometry counts can look "unchanged" while behavior changes drastically.
- If downstream behavior unexpectedly vanishes, first check attribute naming (`distattr`) and existence.
