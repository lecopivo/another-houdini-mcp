# Spray Paint (SOP)

## Intent

`spraypaint` interactively sprays random points onto surfaces with controllable radius/orientation distributions, intended for copy/instance placement workflows.

## Core Behavior

- Brush-driven point creation on target primitives.
- Generates randomized point radii and optional orientation attributes (quaternion or axis vectors).
- Supports relaxation to reduce overlap and emergency limits for safety.
- Can visualize as spheres or copy geometry from input 2 for direct placement preview.

## Key Parameters

- Painting controls: `rate`, stroke radius/color/opacity, target group.
- Relaxation/safety: `relaxiterations`, `emergencylimit`.
- Radius distribution controls: distribution type, seeds, min/max/median/spread.
- Orientation controls: quaternion/axis generation and cone/bias controls.
- Surface transfer controls: prim/uvw attrs and attribute import patterns.

## Typical Workflow

```text
surface (+optional copy geo) -> spraypaint -> copy/instance/render
```

- Use sphere visualization for fast interactive density/scale tuning.
- Then feed real copy geometry once distribution looks correct.

## Production Usage

- Useful for manual art-directed scattering (crowds, foliage clusters, debris splats).
- `Splurgegun` example demonstrates feeding a metaball-based setup into spray paint for stylized spray behavior.

Measured outcomes:
- Live Houdini parameter/geometry measurements are pending in this session.

## Gotchas

- Requires valid first-input surface for generated points; otherwise no points are produced.
- Reusing identical seeds across position/radius/orientation channels can unintentionally correlate randomness.
- Distribution tails (e.g., Cauchy/log-normal) need radius limits to avoid problematic outliers.

## Companion Nodes

- `copytopoints` / `copy` for instancing sprayed points.
- `scatter` for fully procedural non-interactive point generation.
- `attribinterpolate` with prim/uvw attrs for deforming-surface sticking.

## Study Validation

- ✅ Read docs: `help/nodes/sop/spraypaint.txt`
- ✅ Reviewed example: `help/examples/nodes/sop/spraypaint/Splurgegun.txt`
- ⏳ Live validation pending
