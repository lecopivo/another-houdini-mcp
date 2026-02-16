# Spiral (SOP)

## Intent

`spiral` procedurally generates spiral/helix curves with control over radial growth, height, turns, sampling, and output frame attributes.

## Core Behavior

- Generates one or more spiral curves as polygon/NURBS/Bezier primitives.
- Supports Archimedean (constant turn spacing) and logarithmic (multiplicative expansion) families.
- Height can be driven by pitch/height or explicit turns mode.
- Can emit orientation/tangent/angle/distance attributes for downstream curve consumers.

## Key Parameters

- `family`: Archimedean vs logarithmic radial growth model.
- `mode`, `height`, `pitch`, `turns`: vertical/turn-count contract.
- `radiusmode`, `startradius`, `endradius`, `radiusincreaseperturn`, `radiusscaleperturn`.
- `divsmode`, `divspercurve`, `divsperturn`, `uniformdivs`: sampling density and spacing.
- Output attribute toggles (`outputangle`, `outputorient`, `outputdistance`, axis outputs).

## Typical Workflow

```text
spiral -> sweep/polywire/copytopoints -> detail modeling
```

- Establish geometric family and turn/height contract first.
- Then tune divisions for downstream deformation/sweep smoothness.

## Production Usage

- Useful for threads, springs, coils, cable wraps, and decorative procedural motifs.
- `BoltSpiral` example indicates a practical bolt-thread generation workflow using spiral as the guide profile.

Measured outcomes:
- Live Houdini parameter/geometry measurements are pending in this session.

## Gotchas

- Logarithmic growth can explode extents quickly at higher turn counts.
- Low division counts can make downstream sweep/copy normals/orientation unstable.
- Multi-spiral count changes angular distribution and can break assumptions in one-curve downstream networks.

## Companion Nodes

- `sweep` / `polywire` for turning curves into threaded solids.
- `copytopoints` for repeated details along spiral paths.
- `orientalongcurve` when explicit frame control is needed.

## Study Validation

- ✅ Read docs: `help/nodes/sop/spiral.txt`
- ✅ Reviewed example: `help/examples/nodes/sop/spiral/BoltSpiral.txt`
- ⏳ Live validation pending
