# Vellum Configure Grain (SOP)

## What This Node Is For

`vellumconstraints_grain` configures geometry as Vellum grain/fluid particles.

- It can generate particles from closed volume input (`createpoints=1`), or
- tag existing points for grain-like behavior (`createpoints=0`).

## Session Status

- Status: studied
- Docs read: yes (`help/nodes/sop/vellumconstraints_grain.txt`)
- Example set reviewed: fallback companion coverage (no local `help/examples/nodes/sop/vellumconstraints_grain/` folder)
- Node comments read: yes (from companion Vellum example networks)
- Sticky notes read: yes (from companion Vellum example networks)
- QA pass complete: yes (live setup + frame sampling)

## Source-of-Truth Split

- Intent (docs/comments/stickies):
  - Build grain/fluid particles from volume or existing points.
  - Set key per-point attrs (`isgrain`, `pscale`, `mass`, and optional fluid attrs like `viscosity`, `surfacetension`, phase).
  - Grain/fluid workflows typically need more solver substeps (docs recommend >= 5).
- Observed (live scene/params/geometry):
  - In `/obj/academy_vellumconstraints_grain/grain_cfg` with `createpoints=1`, `grainsize=0.06`, `scatter=4000`, node produced `1757` particles with attrs: `P`, `v`, `mass`, `pscale`, `isgrain`.
  - With solver `substeps=5` and ground enabled, particles settle near the ground plane over time.
  - Frame sampling (OUT node) showed settling behavior: by frame 72, `ymin` stabilizes around `-0.12`.
- Mismatches:
  - No docs mismatch found. Main practical pitfall remains collider setup/quality and solver substeps.

## Minimum Repro Setup

- Node graph:
  - `sphere -> xform -> vellumconstraints_grain -> vellumsolver -> OUT`
  - plus collision support into solver input 2 (or solver ground plane)
- Key parameter names and values:
  - `grain_cfg.createpoints=1`
  - `grain_cfg.grainsize=0.06`
  - `grain_cfg.scatter=4000`
  - `solver.substeps=5`
  - `solver.useground=1`, `solver.groundposy=-0.15`
- Output verification method:
  - `probe_geometry` for attrs/counts, then frame-sampled Y distribution to verify settling.

## Key Parameters and Interactions

- `createpoints`:
  - Big mode switch between volume-fill and existing-point tagging workflows.
- `type` (grain vs fluid):
  - Controls intended material behavior and related physical attrs (phase/viscosity/surface tension for fluids).
- `grainsize` + `packingdensity` + `scatter`:
  - Strongly affect count/distribution/stability.
- `substeps` in solver:
  - Critical for stable grain/fluid collision behavior (>=5 is a good baseline).

## Practical Use Cases

1. Turn emitters/volumes into grain piles or fluid-like particles quickly.
2. Build multi-phase fluid setups by combining multiple configured sources.

## Gotchas and Failure Modes

- Too few substeps often causes unstable/tunneling behavior.
- Input must represent a proper closed volume when using `createpoints=1`.
- Collider setup quality still matters; verify collision strategy and frame-sample early.

## Related Nodes

- `vellumconstraints`
- `vellumsolver`
- `vellumio`
- `grainsource`

## Academy QA Checklist

- [x] Official docs reviewed
- [x] Example files reviewed (fallback companion coverage)
- [x] Node comments read
- [x] Sticky notes read
- [x] Behavior validated with at least one observed test
- [x] Source-of-truth split documented (intent vs observed)
- [x] Context and progress files updated
