# Pyro Solver (SOP)

## Intent

`pyrosolver` runs Pyro simulations through a SOP-level wrapper over DOP pyro networks, streamlining sourcing, collisions, shaping, caching, and look-dev bindings.

## Core Behavior

- Consumes source volumes (input 0) and optional collision inputs (input 1).
- Supports sparse, dense, and minimal OpenCL simulation modes.
- Manages simulation domain sizing/resizing, collision conversion, and source range controls.
- Exposes solver fields, shaping forces, and output/export controls in one SOP interface.

## Key Parameters

- Setup/simulation: voxel size, simulation type, OpenCL usage, substeps/CFL.
- Bounds: max domain, resize padding/reference fields/active region behavior.
- Sourcing/collision ranges: static frame vs frame-range looping.
- Field shaping: dissipation, temperature/flame/density couplings, turbulence/disturbance/shredding.
- Output: field export list, post-process conversion and visualization bindings.

## Typical Workflow

```text
pyro source volumes + collision SDF/vel -> pyrosolver -> pyrobakevolume/render cache
```

- Initialize source mappings first, then tune voxel size and simulation type.
- Use sparse active-region guides to understand and optimize solve cost.

## Production Usage

- Effective for smoke/fire/explosion prototyping and production solves without manual DOP assembly.
- Example set highlights upres workflow (`PyroSimpleUpres`) and packed-RBD interaction (`PyroPackedRBD`).

Measured outcomes:
- Live Houdini simulation measurements are pending in this session.

## Gotchas

- Halving voxel size increases memory/time by roughly 8x; resolution tuning is first-order cost control.
- Minimal OpenCL mode has important feature restrictions (dense-only, limited sourcing/collider behavior, no timeline cache).
- Collision/source frame-range cycling can silently loop inputs if not checked.

## Companion Nodes

- `pyrosource`, `volumerasterizeattributes` for source generation.
- `collisionsource`, `vdbfrompolygons` for collision inputs.
- `pyrobakevolume` for look refinement and render bindings.

## Study Validation

- ✅ Read docs: `help/nodes/sop/pyrosolver.txt`
- ✅ Reviewed examples: `help/examples/nodes/sop/pyrosolver/PyroSimpleUpres.txt`, `help/examples/nodes/sop/pyrosolver/PyroPackedRBD.txt`
- ⏳ Live validation pending
