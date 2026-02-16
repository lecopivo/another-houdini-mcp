# PolyWire (SOP)

## Intent

`polywire` builds renderable polygonal tubes around polygon-curve backbones, with controllable branch smoothing/intersections and per-point overrides for radius/divisions/segments.

## Core Behavior

- Sweeps tube geometry along input polygon curves.
- Radius can be uniform or multiplied by a point attribute (`scaleattrib`).
- `div` controls radial roundness; `segs` controls along-curve tessellation.
- Supports branch/joint handling controls for smoother intersections than basic wireframe-style output.

## Key Parameters

- `radius`: base wire radius.
- `usescaleattrib` + `scaleattrib`: per-point radius modulation.
- `div` / `divattrib`: circle divisions around tube.
- `segs` / `segsattrib`: segment count along edges.
- `smooth`, `usesmoothattrib`, `maxvalence`, `maxscale`: branch/joint quality/stability controls.
- `build texture` controls (`dotexture`, `textu/v`, `up*`) for UV/twist behavior.

## Typical Workflow

```text
curve network -> (optional point attrs: width/div/segs/smooth) -> fuse/cleanup -> polywire -> optional subdivide/smooth
```

- Build/merge/fuse curve skeleton first.
- Author per-point controls (`width`/custom attrs) upstream.
- Tune `div` then `segs` to hit quality/perf budget.

## Production Usage

- Strong for branch-like structures, stylized tubes, and curve-driven sculptural forms.
- Keep backbone point valence reasonable; cap problematic high-valence joints.
- Use attribute-driven scaling for branch tapering instead of many node duplicates.

Measured outcomes (`PolywireModel` + live parameter tests):
- Example backbone compaction:
  - pre-fuse `scene`: `30 pts / 7 prims`
  - post-fuse `fuse1`: `24 pts / 7 prims`
  - `width` point attribute present after rename step (`Alpha -> width`).
- Baseline polywire output (`radius=0.03, div=4, segs=1`): `116 pts / 154 prims / 536 verts`.
- Radius sweep (topology unchanged, thickness changes):
  - `radius 0.01 -> 0.03 -> 0.08` kept counts constant, increased tube extent/bbox thickness.
- Division sweep (`div`):
  - `div=3`: `82 pts / 112 prims`
  - `div=4`: `116 / 154`
  - `div=8`: `224 / 278`.
- Segment sweep (`segs`):
  - `segs=1`: `116 / 154`
  - `segs=2`: `208 / 276`
  - `segs=4`: `392 / 460`.
- Attribute-scale modulation:
  - enabling `usescaleattrib=1, scaleattrib=width` on the same `radius` reduced effective tube thickness versus uniform radius,
  - upstream `width` stats in example: min `0.01`, max `0.21`, mean `0.0952`.

## Gotchas

- Missing/incorrect scale attribute name silently falls back to unexpected thickness behavior.
- High `div` and `segs` multiply topology quickly; tune with perf budget in mind.
- Unfused branch skeletons can produce duplicated joints/overlapping tubes.
- Extreme branch valence can destabilize joints; use `maxvalence` and pre-clean topology.

## Companion Nodes

- `fuse` for backbone welding before tube generation.
- `attribute`/`point` for authoring width/smooth/div/segs driver attributes.
- `subdivide` for post-polywire smoothing.

## Study Validation

- ✅ Read docs: `nodes/sop/polywire.txt`
- ✅ Reviewed example: `examples/nodes/sop/polywire/PolywireModel.txt`
- ✅ Inspected stickies and full companion chain (curve/merge/group/point/attribute/fuse/subdivide)
- ✅ Ran live radius/div/segs/scale-attribute interaction tests on example network
