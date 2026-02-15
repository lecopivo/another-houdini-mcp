# FLIP Collide (SOP)

## Intent

`flipcollide` converts connected collider geometry/volumes into FLIP collision representations and merges them into the simulation collision stream.

## Core Behavior

- Consumes FLIP streams on inputs 0/1/2 and new collider geometry on input 3.
- Emits updated collision stream on output 2 while forwarding source/container streams.
- Supports volume and/or surface collision generation.
- Can compute collider velocity from deformation/motion for more accurate interactions.

## Key Parameters

- `dovolume`: solid/closed collider mode.
- `dosurface`: open/sheet/surface collider mode.
- `computevel`, `computevelsubstep`, `velscale`: motion-derived collision velocity controls.
- `activate`: temporal enable.
- `objname`: collision object stream naming.

## Typical Workflow

```text
flip streams + collider geometry -> flipcollide -> flipsolver
```

- Feed colliders into input 3 (merge if multiple).
- Choose volume/surface mode based on collider topology.
- Forward output streams 0/1/2 to solver 0/1/2.

## Production Usage

- Closed solids usually need volume collisions.
- Open/2D colliders require surface collisions and compatible solver collision mode.
- Increase velocity quality for fast/deforming colliders to avoid weak splashes or leaks.

Measured outcomes (live FLIP test network):
- Collision stream output-type changes:
  - volume only (`1/0`): `2` VDB prims
  - surface only (`0/1`): `2` VDB + `1` PackedGeometry prim
  - both (`1/1`): `2` VDB + `1` PackedGeometry prim
- Fluid particle count at frame8 shifted with collision mode in same setup:
  - volume only: `17571`
  - surface only: `16715`
  - both: `17662`

## Gotchas

- Using only surface mode for solid watertight colliders can produce unintended behavior.
- Collision resolution depends heavily on upstream FLIP scale settings (`particlesep`, `gridscale`).
- Collider topology consistency matters for time-sampled velocity computation.

## Companion Nodes

- `flipcontainer`
- `flipboundary`
- `flipsolver`

## Study Validation

- ✅ Read docs: `nodes/sop/flipcollide.txt`
- ✅ No official node example listing in current corpus
- ✅ Validated volume/surface mode output contracts and sim-impact deltas
