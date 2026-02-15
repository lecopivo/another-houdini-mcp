# Character Blend Shapes (SOP, KineFX)

## Intent

`kinefx::characterblendshapes` applies blend shape deformation to character geometry using blend-weight channels on a KineFX skeleton/pose stream.

## Core Behavior

- Input 0 expects rest geometry with base and target shapes.
- Input 1 expects rest pose skeleton.
- Input 2 expects animated pose channels/attributes that drive blend weights.
- Node is a KineFX-oriented wrapper over `blendshapes`, with channel mapping conventions (`blendshape_channel`, `clipchannels`).
- Output topology can change from source when hidden/aux blend-shape inputs are consumed into deformation output.

## Key Parameters

- `group`, `grouptype`: scope blend application to subset geometry.
- `attribs`: attributes to blend (commonly `P`, optionally `N` etc).
- OpenCL options: performance path selection (`Use OpenCL`, mode).

Companion authoring attributes on input geometry:
- `blendshape_channel`: channel name used as weight driver.
- `blendshape_name`, `blendshape_inbetween_name`, `blendshape_inbetween_weight`.
- `name`: associates base and target shapes.

## Typical Workflow

```text
scenecharacterimport -> (optional channel edits) -> characterblendshapes -> bonedeform
```

- Import character with blend shape targets.
- Edit/author channel values on animated pose stream.
- Apply `characterblendshapes`.
- Skin/deform downstream.

## Production Usage

- Keep channel naming contract consistent between `blendshape_channel` and animated pose channels.
- Use in-between targets for non-linear facial/body transitions rather than single linear target interpolation.
- Keep blendshape targets in packed/hidden groups to reduce viewport clutter.

Measured outcomes:
- `SimpleCharacterBlendShapes` example:
  - `scenecharacterimport`: `582 pts / 560 prims` with `blendshape_channel` and `blendshape_name` attrs.
  - `apply_blendshapes`: `580 pts / 558 prims`; blendshape helper prim attrs removed after deformation.
- `InbetweenShapes` example:
  - `characterblendshapes10` output remained `98 pts / 96 prims` while shape changed with channel value.
  - Changing `characterblendshapechannels7.blend0` from `0.0 -> 0.5 -> 1.0` changed output bbox significantly:
    - `0.0`: `(-0.5..0.5)`
    - `0.5`: expanded to roughly `(-0.8536..0.8536)`
    - `1.0`: contracted to roughly `(-0.609..0.609)` on Z

## Gotchas

- Channel-name mismatch can silently result in no deformation (or compile/cook errors if invalid attribute naming is used in expression nodes).
- In-between workflows depend on correct `weight` and in-between metadata; missing metadata gives linear-looking results.
- Many official examples are locked HDAs; unlock instances before parameter sweeps.

## Companion Nodes

- `kinefx::characterblendshapechannels` for driving blend channels.
- `kinefx::characterblendshapesadd` for assembling base/target/in-between sets.
- `bonedeform` for final skinning after blend-shape deformation.

## Study Validation

- ✅ Read docs: `nodes/sop/kinefx--characterblendshapes.txt`
- ✅ Reviewed examples: `SimpleCharacterBlendShapes`, `InbetweenShapes`
- ✅ Inspected official networks and input/output contracts
- ✅ Ran live channel-value sweeps and measured geometry-change outcomes
