# Ray (SOP)

## Intent

`ray` projects source points/primitives onto collision geometry using ray intersection or minimum-distance methods, commonly for wrap/shrink conform workflows.

## Core Behavior

- Input 0 is projected geometry; input 1 is collision target.
- Projection behavior depends on direction source, direction type, and nearest/farthest intersection policy.
- `dotrans` controls whether points are moved to hit locations or only hit information is evaluated.
- Optional sampling/jitter and combiner modes control multi-ray aggregation.

## Key Parameters

- `method`: ray projection vs minimum-distance placement.
- `dirmethod`, `reverserays`, `lookfar`: ray direction and hit-side policy.
- `dotrans`, `scale`, `lift`: transform and post-hit offset controls.
- `sample`, `jitter`, `combinetype`: stochastic multi-ray behavior.

## Typical Workflow

```text
source geometry (+normals) + collision geometry -> ray -> facet/normal cleanup -> downstream shading/modeling
```

- Ensure source normals/directions are valid before projection.
- Add a normal-recompute pass after deformation for correct shading.

## Production Usage

- Useful for shrink-wrap projection, cloth-to-body drape approximation, and surface-conforming overlays.
- `lookfar` is useful for selecting opposite-side intersections on closed targets.

Measured outcomes (`RayWrap` + live tests on `ray1`):
- Baseline wrapped grid: `100 pts / 81 prims`, bbox Z size `1.729584`, mean displacement vs source grid `0.172942`.
- `lookfar` switch:
  - `0` (closest): bbox Z size `1.729584`.
  - `1` (farthest): bbox Z size `4.513329`, mean displacement vs source `0.47069`.
- `lift` shifted wrap offset along projection path:
  - `lift -0.05 -> 0.05` increased mean displacement vs source `0.169702 -> 0.181702`.
- `dotrans` contract:
  - `dotrans=0` kept geometry near source state (mean displacement `0.006`),
  - `dotrans=1` performed full projection displacement.
- Multi-sample combiner variation (`sample=4`, `jitter=0.15`) changed resulting wrap extents and displacement (`combine shortest` lower than `longest/median` in this setup).

## Gotchas

- If source normals are badly oriented or embedded in collision geometry, projection can appear inert or unstable.
- Topology usually remains unchanged; validate movement via extents/displacement, not counts.
- After wrapping, normals may need explicit recompute for correct lighting.

## Companion Nodes

- `point` for source normal/direction authoring.
- `facet` for post-ray normal correction.
- `attribinterpolate` when using hit prim/uvw attributes for deforming-target stickiness.

## Study Validation

- ✅ Read docs: `nodes/sop/ray.txt`
- ✅ Reviewed example: `examples/nodes/sop/ray/RayWrap.txt`
- ✅ Inspected stickies and internal network (`grid/point/ray/facet/merge`)
- ✅ Ran live far-hit/lift/transform/sample-combiner tests with measured outcomes
