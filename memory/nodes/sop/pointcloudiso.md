# PointCloudIso (SOP)

## Intent

`pointcloudiso` reconstructs an iso-surface mesh from a point cloud (typically scanned/sampled points with outward normals).

## Core Behavior

- Consumes point positions and point normals to infer a surface field.
- Polygonization density is controlled by `stepsize*`.
- `buildpolysoup` toggles polygon vs polysoup output representation.
- `radscale` adjusts per-point influence radius used during reconstruction.

## Key Parameters

- `stepsize1/2/3`: polygonization step size (resolution/perf tradeoff).
- `radscale`: influence radius scale for surfacing.
- `buildpolysoup`: output as a single polysoup primitive when enabled.

## Typical Workflow

```text
point cloud (+ N) -> pointcloudiso -> optional smoothing/cleanup -> downstream mesh ops
```

- Ensure point normals exist and are oriented consistently outward.
- Tune step size first for target detail/performance.
- Toggle polysoup for heavy output pipelines where primitive count matters.

## Production Usage

- Useful for scanner-style point sets and intermediate particle-to-surface reconstruction.
- Validate output density early; overly fine steps can explode counts.
- Keep a points-only pre-pass (`add` keep points) when extracting cloud input from polygonal sources.

Measured outcomes (`TwistyCube` example + live `/obj/academy_pointcloudiso_live`):
- Example chain (`box -> twist -> point(add normals) -> add(remove prims) -> pointcloudiso`) validated required point-cloud preparation pattern.
- Example high-density reconstruction (`stepsize=0.02`) output: `36390 pts / 36446 prims / 145668 verts` (polygon mode).
- Step size interaction on live sphere cloud:
  - `stepsize=1.5` -> empty mesh (`0/0`),
  - `stepsize=1.0` -> `16 pts / 18 prims`,
  - `stepsize=0.5` -> `80 pts / 82 prims`.
- Normals requirement check:
  - with point normals present -> valid reconstructed mesh,
  - without point normals -> no cooked geometry (`None`/empty output behavior).
- Polysoup toggle (`stepsize=1.0`):
  - `buildpolysoup=0` -> polygon output (`18` prims),
  - `buildpolysoup=1` -> polysoup output (`1` prim).

## Gotchas

- Missing point normals can produce empty/no output even when point positions exist.
- Large step sizes can fully erase small/medium features.
- Very small step sizes quickly increase point/primitive counts and cook cost.
- `radscale` may have subtle or minimal visible effect depending on source density/step settings; test in context.

## Companion Nodes

- `point` / `normal` for preparing reliable point normals.
- `add` for stripping primitives and keeping pure point cloud inputs.
- `polysoup` for output compaction if not using internal polysoup toggle.

## Study Validation

- ✅ Read docs: `nodes/sop/pointcloudiso.txt`
- ✅ Reviewed example: `examples/nodes/sop/pointcloudiso/TwistyCube.txt`
- ✅ Inspected stickies and companion prep chain (`twist`, `point`, `add`)
- ✅ Ran live step-size/normals/polysoup behavior tests in `/obj/academy_pointcloudiso_live`
