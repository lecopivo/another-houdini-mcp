# Sequence Blend (SOP)

## Intent

`sblend` morphs across an ordered sequence of geometry inputs while interpolating positions and selected attributes over a continuous blend parameter.

## Core Behavior

- Inputs are indexed from 0; fractional `blend` values interpolate between adjacent inputs.
- Extra points/prims on mismatched inputs remain stationary until whole-index transition.
- Non-polygonal inputs switch at integer boundaries instead of true geometric interpolation.
- Attribute interpolation is pattern-controlled; unmatched attributes switch discretely.

## Key Parameters

- `blend`: continuous driver for sequence traversal.
- `attribs`: attribute pattern to interpolate.
- `ptidattr`, `primidattr`: ID-based matching across reordered topology.
- `doslerp`: spherical interpolation for rotations/normals/transforms.
- `interp`: linear/cubic/subdivision interpolation modes.
- `usevforpinterp`, `timestep`: velocity-aware position interpolation.

## Typical Workflow

```text
shape0 + shape1 + shape2 + ... -> sblend -> animation/render output
```

- Ensure stable IDs when topology/order can change.
- Animate `blend` and constrain interpolated attribute set explicitly.

## Production Usage

- Useful for procedural morph timelines and staged shape transitions.
- Example variants show point vs vertex attribute blending behavior (`BlendPointAttributes`, `BlendVertexAttributes`).

Measured outcomes:
- Live Houdini parameter/geometry measurements are pending in this session.

## Gotchas

- Without ID attributes, reordering points/prims can cause apparent popping.
- Un-interpolated attributes switching at integer boundaries can produce abrupt shading/behavior jumps.
- Velocity interpolation needs correct timestep and meaningful `v` attributes.

## Companion Nodes

- `blendshapes` for dedicated shape blending workflows.
- `timeblend` for temporal interpolation.
- `trail` to compute velocity attributes for velocity-assisted interpolation.

## Study Validation

- ✅ Read docs: `help/nodes/sop/sblend.txt`
- ✅ Reviewed examples: `help/examples/nodes/sop/sblend/BlendPointAttributes.txt`, `help/examples/nodes/sop/sblend/BlendVertexAttributes.txt`
- ⏳ Live validation pending
