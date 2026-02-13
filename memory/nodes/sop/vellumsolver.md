# Vellum Solver (SOP)

## What This Node Is For

`vellumsolver` runs Vellum dynamics from SOPs with a simplified 3-input interface:

- input 0: sim geometry
- input 1: matching constraints/constraint geometry
- input 2: collision geometry

It wraps an internal DOP network and is the main production entry point for cloth, grains, softbodies, weld/attach workflows, and Vellum fluids.

## Session Status

- Status: studied
- Docs read: yes (`help/nodes/sop/vellumsolver.txt`)
- Example set reviewed: yes (`help/examples/nodes/sop/vellumsolver/*.txt`)
- Example OTL internals inspected: yes (all 18 local vellumsolver examples; loaded one-at-a-time and deleted before loading the next)
- Node comments read: yes
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent (docs/comments/stickies):
  - Solver quality is mainly controlled by `substeps`, `niter`, collision pass controls, and targeted options like `layershock`.
  - Dynamic constraint creation/updates are expected inside the internal DOP network (`forces` subnet).
  - Collision behavior can be controlled globally and per-point (`collisionignore`, `collisiongroup`, `disableexternal`, friction attrs).
  - Fluid use cases can emit via Vellum Source DOPs inside the solver.
- Observed (live scene/params/geometry):
  - `AnimatedConstraints` and related examples wire live constraint updates inside `vellumsolver1/dopnet1/forces` via Vellum Constraint Property and Vellum Constraints DOPs.
  - `CollisionIgnore` demonstrates three parallel variants in one network (full interaction, group-limited, and ignore-based) using per-point string attrs.
  - `StiffnessDropoff` confirms soft-release pins by combining dropoff + break threshold at matching distances.
  - `ResolutionTarget` demonstrates low-res->high-res targeting using soft pins and a painted `targetweight` mask.
  - `VellumFluidPhasesReference` runs fluid sources from DOP-side Vellum Source nodes; direct `vellumsolver1` SOP output is empty at start frame while `merge_show_all` contains collider/display geometry.
- Mismatches:
  - No major behavior mismatch found; examples mainly reinforce docs and expose practical setup patterns.

## Minimum Repro Setup

- Node graph:
  - `grid -> vellumconstraints (cloth) -> vellumsolver` with collider plugged to input 2.
- Key parameter names and values:
  - `vellumsolver1.substeps`
  - `vellumsolver1.niter`
  - `vellumsolver1.useground`
  - `vellumsolver1.collisionsiter` and `vellumsolver1.postcollisioniter`
- Output verification method:
  - `probe_geometry` on solver/post-process output and inspect stress/guide visualizations.

## Key Parameters and Interactions

- `solvermode`:
  - `Minimal` can be faster for grains/fluids, but has explicit feature limits (no animated pins/attach constraints, restricted collision setup, etc.).
- `substeps` + `niter`:
  - Primary stability controls for stretch/collision quality.
- `collisionsiter` + `postcollisioniter` + `resolveallmax`:
  - Interleaving and cleanup controls for collision quality vs cost.
- `layershock` with integer point attr `layer`:
  - Effective for stacked cloth ordering (`ArmLayer`).
- Friction controls (`static_threshold`, `dynamic_scale`, `friction`, `selffriction`) + point attrs (`dynamicfriction`, `friction`):
  - Used in `VaryingFriction` to spatially vary slip behavior.
- Secondary pass (`dosecondary`, `secondarygroup`, `secondaryfrequency`):
  - Useful when expensive/unstable constraints should be solved at different frequency.

## Observed Behavior Snapshot

- `/obj/academy_vellumsolver_animatedconstraints/cloth/vellumpostprocess1`:
  - `points=900`, `prims=841` with expected sim attrs (`v`, `P`, `pscale`, etc.).
- `/obj/academy_vellumsolver_vellumfluidphasesreference/fluid/vellumsolver1` (start frame):
  - `points=0`, `prims=0` (sources injected in DOP over time).
- `/obj/academy_vellumsolver_vellumfluidphasesreference/fluid/merge_show_all`:
  - `points=6408`, `prims=6306` including bowl/blender + display state.

## Practical Use Cases

1. Cloth and softbody production sims with targeted controls (pinning, welds, dynamic attach/stitch/glue).
2. Multi-material or multi-phase fluid/grain setups where phase properties and emission timing differ by source.

## Gotchas and Failure Modes

- Heavy examples can be expensive; load and inspect one-at-a-time to avoid unnecessary memory/cook pressure.
- Internal sticky notes under `integrate_forces`/`integrate_torques` are shared solver internals and often not example-specific.
- For fluid-source workflows, empty early-frame solver output can be expected if source activation is delayed.
- `Minimal` solver mode is not a drop-in replacement for all setups; check feature limitations before switching.

## Related Nodes

- `vellumconstraints`
- `vellumconstraints_grain`
- `vellumpostprocess`
- `vellumio`

## Academy QA Checklist

- [x] Official docs reviewed
- [x] Example files reviewed
- [x] OTL instantiated/unlocked and internals inspected
- [x] Node comments read
- [x] Sticky notes read
- [x] Behavior validated with at least one observed test
- [x] Source-of-truth split documented (intent vs observed)
- [x] Context and progress files updated
