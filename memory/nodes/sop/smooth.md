# Smooth (SOP)

## Intent

`smooth` relaxes geometry (and selected attributes) without adding points, reducing local roughness while preserving broader shape trends.

## Core Behavior

- Operates on existing points/attributes; topology count remains unchanged.
- Supports scoped smoothing via primitive groups and constrained boundaries/points.
- Method/strength/filter quality control smoothing model and detail retention.
- Attribute list allows smoothing `P` and/or other float attributes.

## Key Parameters

- `group`: localize smoothing to a selection.
- `method`: smoothing model selection.
- `strength`: smoothing magnitude.
- `filterquality`: detail-retention/quality control.
- `attributes`: which attributes are smoothed.

## Typical Workflow

```text
noisy/deformed mesh -> group (optional scope) -> smooth -> downstream clip/merge/render
```

- Define spatial scope first (group/boundary), then tune strength/quality.

## Production Usage

- Good post-noise cleanup for terrain-like surfaces and curve reliefs.
- Useful as a non-topology-changing polish stage before clipping/booleans.

Measured outcomes (`Hills` example on `smooth1`):
- Baseline output: `5929 pts / 11552 prims` (topology unchanged across tested parameter sweeps).
- In this dataset, `strength`, `filterquality`, and `method` changes produced negligible bbox/count differences at default grouped scope.
- Scope was the dominant behavioral switch:
  - `group="Hills"`: bbox Y size `0.312524`.
  - `group=""` (all): bbox Y size reduced to `0.257076` (broader smoothing effect).

## Gotchas

- Count-based checks will miss most effects; evaluate shape metrics or displacement instead.
- Group scope can dominate outcomes more than strength tuning.
- If normals are required downstream, confirm normal-update policy after smoothing.

## Companion Nodes

- `group` for bounded smoothing regions.
- `fractal` as upstream roughness source in terrain-style setups.
- `clip` when trimming smoothed geometry into layered forms.

## Study Validation

- ✅ Read docs: `nodes/sop/smooth.txt`
- ✅ Reviewed example: `examples/nodes/sop/smooth/Hills.txt`
- ✅ Inspected stickies and full companion chain (`grid/fractal/group/smooth/clip/merge`)
- ✅ Ran live scope/method/strength/quality parameter sweeps and compared resulting geometry metrics
