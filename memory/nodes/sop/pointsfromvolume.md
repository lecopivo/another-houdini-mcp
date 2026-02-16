# Points from Volume (SOP)

## Intent

`pointsfromvolume` fills geometry/volumes with regularly distributed points for particle/FLIP initialization and volumetric point seeding workflows.

## Core Behavior

- Supports geometry, fog volume, and SDF source interpretation.
- Generates points via dense-grid or sparse-volume construction methods.
- Controls lattice style (grid/tetrahedral), separation, jitter, and optional dithering near surfaces.
- Can output `pscale` and point groups for downstream fluid/particle pipelines.

## Key Parameters

- `sourcetype`: auto/geometry/fog/SDF interpretation.
- `pointmethod`: Dense Grid vs Sparse Volume strategy.
- `particlesep`, `inittype`: core spacing and packing pattern.
- `jitterscale`, `jitterseed`: positional randomness.
- `addscale`, `radscale`: `pscale` output contract.
- Surface-band controls: scatter density, oversampling, relax iterations.

## Typical Workflow

```text
closed surface or volume -> pointsfromvolume -> POP/FLIP/point-based simulation
```

- Start with point separation and construction method, then add jitter/dither for boundary quality.
- Enable output scale when downstream nodes expect particle radius metadata.

## Production Usage

- Useful for initializing particle fluid volumes and volumetric emission targets.
- `AlphaOmega` example demonstrates creating a target fill volume used as a goal region in FLIP-style simulation context.

Measured outcomes:
- Live Houdini parameter/geometry measurements are pending in this session.

## Gotchas

- Dense grid can become memory-heavy for sparse wide-bounds inputs.
- Invert mode often yields outer-box point fields unless border assumptions are managed.
- Inconsistent separation/pscale contracts can destabilize downstream surface reconstruction.

## Companion Nodes

- `scatter` for surface-only stochastic point generation.
- `particlefluidsurface` for reconstructing fluid surfaces from seeded particles.
- `vdbfrompolygons` when converting geometry to sparse volumetric intermediates.

## Study Validation

- ✅ Read docs: `help/nodes/sop/pointsfromvolume.txt`
- ✅ Reviewed example: `help/examples/nodes/sop/pointsfromvolume/AlphaOmega.txt`
- ⏳ Live validation pending
