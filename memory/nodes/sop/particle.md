# Particle (SOP)

## Intent

`particle` provides lightweight SOP-level particle simulation behavior (birth, forces, collisions, split/limits) without building a full POP network.

## Core Behavior

- Uses input points as particle sources or treats input points as moving particles based on behavior settings.
- Supports external force, wind, turbulence, collisions, and limit-plane hit behaviors.
- Carries particle-centric attributes (velocity, life, age, optional id/mass/drag).
- Can split particles on collision/death and optionally cull unused source points.

## Key Parameters

- State controls: behavior mode, point reuse, start/preroll/time increment.
- Forces: `external*`, `wind*`, `turb*`, period/seed.
- Particle lifecycle: birth rate, life expectancy/variance, mass/drag toggles.
- Limits/collision: plane bounds, hit behavior, gain tangent/normal, split controls.

## Typical Workflow

```text
source points -> particle -> optional collide/force inputs -> render/sim handoff
```

- Use for quick emissions and deformation-like particle motion prototypes.
- Promote to POP networks when behavior complexity exceeds SOP particle controls.

## Production Usage

- Practical for simple fountains, sparks, snowfall, and fast motion studies.
- Official examples (`ParticleExamples`, `ParticleFountain`) cover creep/grouped births, bounce/split/collision behavior, moving-source births, and force-field influence.

Measured outcomes:
- Live Houdini simulation measurements are pending in this session.

## Gotchas

- First input is required; node does not operate without a source.
- Collision with deforming objects can leak points depending on timestep/motion.
- `Die on Contact` needs unused-particle cleanup for expected deletion behavior.

## Companion Nodes

- `force` SOP input for metaball-driven influences.
- `popnet` when simulation complexity grows.
- `trail`/attribute prep for velocity-aware downstream processing.

## Study Validation

- ✅ Read docs: `help/nodes/sop/particle.txt`
- ✅ Reviewed examples: `help/examples/nodes/sop/particle/ParticleExamples.txt`, `help/examples/nodes/sop/particle/ParticleFountain.txt`
- ⏳ Live validation pending
