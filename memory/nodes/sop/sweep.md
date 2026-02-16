# Sweep (SOP)

## Intent

`sweep` builds surfaces by copying/orienting cross sections along a backbone curve and skinning the result into ribbons/tubes/frames.

## Core Behavior

- Input 0 is the backbone/path; input 1 is cross-section geometry.
- Orientation is computed along the path; optional attribute-driven transforms can modify section orientation/scale.
- Output topology can remain constant while shape/placement changes significantly.
- Commonly paired with `skin`/`cap` to produce final closed surfaces.

## Key Parameters

- `scale`, `twist`, `roll`: primary section transform controls along the path.
- `xformbyattribs`, `ptattribs`: attribute-driven transform behavior from path data.
- `polyout`, `skin`: output construction mode controls.
- `cycle` and grouping parameters for multi-curve / multi-section sequencing.

## Typical Workflow

```text
backbone curve -> convert/resample (if needed) -> sweep -> skin/cap -> downstream modeling
```

- Keep backbone sampling predictable before sweeping.
- Decide whether transforms come from parameters or path attributes early.

## Production Usage

- Fast procedural tube/ribbon generation for cables, tendrils, stylized stems, and frame scaffolds.
- Expression-driven `scale` is effective for gradient thickness along the path.
- Pair with `cap` when open ends must be closed for render/sim handoff.

Measured outcomes (`SweepBasic` example):
- Baseline `sweep1` output: `648 pts / 36 prims / 648 verts`.
- Baseline downstream `cap1` output: `792 pts / 1 prim` (rounded end caps enabled).
- Constant-scale sweep (temporarily removing expression keyframes) changed extents while topology stayed fixed:
  - `scale 0.03 -> 0.1 -> 0.3` kept `648/36`, bbox scaled from `(0.006,1.686227,0.900201)` to `(0.06,1.738706,0.928844)`.
- `xformbyattribs` was a major shape contract switch in this example:
  - `0`: bbox `(0.059089,1.739606,0.929335)`
  - `1`: bbox `(0.2,1.874764,1.003103)`
  - topology remained `648/36` in both states.
- `roll` adjustments produced subtle orientation/extents changes; `twist` changed orientation while keeping counts constant in this setup.

## Gotchas

- Topology-only checks can miss substantial orientation/placement differences.
- Expression-keyed `scale` can hide manual edits unless keyframes are inspected/disabled.
- Attribute-driven transforms (`xformbyattribs`) can drastically change shape with unchanged primitive counts.

## Companion Nodes

- `convert` to regularize backbone sampling before sweep.
- `skin` to turn swept frames into surfaces.
- `cap` to close open swept ends.

## Study Validation

- ✅ Read docs: `nodes/sop/sweep.txt`
- ✅ Reviewed example: `examples/nodes/sop/sweep/SweepBasic.txt`
- ✅ Inspected stickies and full companion chain (`curve/convert/sweep/skin/cap/xform`)
- ✅ Ran live scale/twist/roll/attribute-transform sweeps with measured geometry outputs
