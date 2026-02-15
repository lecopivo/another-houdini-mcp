# FLIP Solver (SOP)

## Intent

`flipsolver` advances SOP FLIP fluid state from synchronized source/container/collision streams, with optional external boundary flow input.

## Core Behavior

- Required stream contract:
  - input 0: source particles
  - input 1: container fields
  - input 2: collisions
- Optional input 3: boundary flow (for example ocean/open-boundary workflows).
- Supports waterline initialization, boundary condition modes, collisions, substeps, reseeding, and advanced solve controls.
- Outputs updated 0/1/2 streams for downstream simulation/surfacing/compression.

## Key Parameters

- setup: `particlesep`, `gridscale`, substeps/time scale.
- waterline block: `dowaterline`, `waterline`, boundary source/pressure/velocity bands.
- boundary condition: `boundarytype` (pressure vs velocity driven).
- collision behavior: particle collision mode, stick settings, ground options.
- fluid behavior: velocity transfer mode, reseeding, narrowband, adaptivity.

## Typical Workflow

```text
flipcontainer -> [flipboundary] -> [flipcollide] -> flipsolver -> surface/cache chain
```

- Maintain 0/1/2 stream synchronization through every intermediate FLIP SOP.
- Use input 3 only for dedicated boundary-flow data (ocean/upres patterns).

## Production Usage

- Keep `particlesep` and `gridscale` coherent with container/collider scale.
- Use higher substeps for fast motion or stiff settings; tradeoff is runtime.
- Set boundary condition explicitly in waterline/open-boundary setups.

Measured outcomes (live FLIP test network):
- baseline waterline-enabled solve produced source stream counts around:
  - frame1: `14535` pts
  - frame12: `~17600-17670` pts depending on mode.
- boundary condition sweep:
  - boundarytype `0`: frame12 `17672`
  - boundarytype `1`: frame12 `17602`
- substep sweep (same setup):
  - substep `1`: frame12 `17602`
  - substep `3`: frame12 `17666`

## Canonical Build Orders

### Source-driven tank

```text
flipcontainer -> flipboundary -> flipsolver -> fluidcompress -> particlefluidsurface
```

### Collision-driven FLIP

```text
flipcontainer -> flipboundary -> flipcollide -> flipsolver
```

### Ocean/open-boundary FLIP

```text
flipcontainer (0/1/2) -> flipsolver (0/1/2)
oceanevaluate -> flipsolver (3)
```

## Gotchas

- Stream misalignment across 0/1/2 causes invalid or misleading results.
- `particlesep` mismatch with container is a high-frequency failure mode.
- Input-3 boundary flow should not replace main 0/1/2 stream chain.

## Companion Nodes

- `flipcontainer`
- `flipboundary`
- `flipcollide`
- `fluidcompress`
- `particlefluidsurface`
- ocean/whitewater nodes for specialized workflows

## Study Validation

- ✅ Read docs: `nodes/sop/flipsolver.txt`
- ✅ No official node example listing in current corpus
- ✅ Validated boundary/substep effects in controlled live FLIP chain
