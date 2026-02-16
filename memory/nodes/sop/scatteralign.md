# Scatter and Align (SOP)

## Intent

`scatteralign` scatters points and builds instancing-ready attributes (`pscale`, `orient`, tagging, transferred attrs) for copy/instance pipelines.

## Core Behavior

- Combines scatter generation with orientation/scale/randomization logic in one node.
- Supports three operational regimes: scatter on surface, scatter around constraint points, or add attrs to existing points.
- Produces tag-based organizational attributes and optional hit/transfer attributes.
- Relaxation and overlap/avoid constraints shape final point distribution quality.

## Key Parameters

- `mode`: generation vs attribute-only behavior.
- Point count strategies: by size/density/spacing/explicit count.
- `coverage`: instance-coverage target (not exact count control).
- Orientation stack: normal/forward mapping, random cone, normal-axis rotation.
- Relaxation controls: `relaxiterations`, overlap removal, constraint-point avoidance.
- Output attributes: `radiusattrib` (`pscale`), `orientattrib`, prim/uvw hit attrs, transferred attrs.

## Typical Workflow

```text
surface (+optional constraint points) -> scatteralign -> copytopoints/instancer
```

- Tune point generation and spacing first, then orientation variation.
- Validate against actual instanced geometry, not points alone.

## Production Usage

- High-level vegetation/rocks/debris scattering with controllable variation.
- `ScatterAlignBasic` example shows primary scatter and secondary scatter around existing points.

Measured outcomes:
- Live Houdini parameter/geometry measurements are pending in this session.

## Gotchas

- Coverage/spacing interactions can spike point counts; emergency limit safeguards are important.
- Orientation settings assume modeled-instance axis conventions (default up=+Y, forward=+Z).
- Constraint-point workflows can still overlap geometry unless avoid/remove-overlap settings are balanced.

## Companion Nodes

- `copytopoints` for instance realization.
- `attribfrompieces` for variation assignment.
- `attribpaint` for painted density/scale/orientation drivers.

## Study Validation

- ✅ Read docs: `help/nodes/sop/scatteralign.txt`
- ✅ Reviewed example: `help/examples/nodes/sop/scatteralign/ScatterAlignBasic.txt`
- ⏳ Live validation pending
