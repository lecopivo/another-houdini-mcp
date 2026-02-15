# FLIP Container (SOP)

## Intent

`flipcontainer` defines the SOP FLIP domain and initializes the three synchronized FLIP streams (sources, container fields, collisions) plus baseline physical attributes.

## Core Behavior

- Creates three output contracts consumed by downstream FLIP nodes:
  - output 0: particle source stream
  - output 1: container volume/field stream
  - output 2: collision volume stream scaffold
- Accepts optional closed geometry/volume for custom domain shape.
- Embeds fluid settings and scale metadata in container detail attributes.
- `particlesep` and `gridscale` control both particle and voxel-side resolution behavior.

## Key Parameters

- `particlesep`: master resolution control (must match solver).
- `gridscale`: voxel sizing factor relative to particle separation.
- domain controls (`implicit`, `size`, `center`).
- physical property blocks (`density`, viscosity, surface tension, custom attrs).

## Typical Workflow

```text
domain geometry -> flipcontainer -> [flipboundary/flipcollide] -> flipsolver
```

- Build domain first (box or custom closed geometry).
- Keep streams 0/1/2 together through the FLIP chain.
- Tune `particlesep` and `gridscale` before downstream quality tweaks.

## Production Usage

- Keep container and solver `particlesep` synchronized.
- Use lower `particlesep` for detail/collision fidelity; expect higher particle counts and cost.
- Adjust `gridscale` carefully; lower values increase field fidelity and memory pressure.

Measured outcomes (live FLIP test network):
- `particlesep` impact (with matched solver setting):
  - `0.12`: frame1 `12153` pts, frame8 `13963` pts
  - `0.08`: frame1 `21792` pts, frame8 `25132` pts
- `gridscale` metadata and sim influence:
  - container detail `gridscale` tracked parameter changes (`2.0` -> `1.5`)
  - frame8 particle counts shifted (`25132` at `2.0`, `21065` at `1.5`) in this setup.
- container stream detail attrs included `particlesep`, `gridscale`, and `fluid_settings` dictionary keys.

## Gotchas

- Mismatched `particlesep` between container and solver is a frequent source of unstable/coarse behavior.
- Treat output streams as a synchronized tuple; rewiring only one stream is error-prone.
- Narrow-band/waterline behavior in solver can mask domain-scale issues if container sizing is wrong.

## Companion Nodes

- `flipsolver`
- `flipboundary`
- `flipcollide`
- `particlefluidsurface`

## Study Validation

- ✅ Read docs: `nodes/sop/flipcontainer.txt`
- ✅ No official node example listing in current corpus
- ✅ Built live SOP FLIP network and measured parameter/stream effects
