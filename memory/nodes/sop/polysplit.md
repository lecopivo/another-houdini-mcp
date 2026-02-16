# PolySplit (SOP)

## Intent

`polysplit` inserts new edges/edge loops into polygonal surfaces to refine topology while preserving primitive/vertex attributes and group memberships.

## Core Behavior

- Supports two main path modes: shortest-path cuts and edge-loop insertion.
- Uses encoded `splitloc` tokens to define exact cut locations.
- Can optionally close cut paths and emit edge groups for newly created split edges.
- Includes loop controls (`numloops`, profile options) for repetitive loop insertion.

## Key Parameters

- `splitloc`: cut-point chain specification.
- `pathtype`: shortest-path vs edge-loop mode.
- `close`: close path from last to first split point.
- `numloops`: number of loops in edge-loop mode.
- `grouptoggle`, `groupname`, `groupappend`: output edge-group controls.
- `tolerance`: precision safeguard for tiny-scale or near-corner cuts.

## Typical Workflow

```text
base polygon surface -> polysplit (targeted cuts/loops) -> optional smoothing/subdivide
```

- Start with sparse strategic cuts, then add loops where deformation or shading needs density.
- Prefer explicit split locations for reproducible procedural edits.
- Emit edge groups when downstream operations depend on newly inserted loops.

## Production Usage

- Core for control-loop placement in subdivision-ready topology.
- Effective for refining panel seams and flow lines in hard-surface modeling.
- Combine with fuse/cleanup before splitting when source curves are dependency-driven.

Measured outcomes (`PolySplitHood` + live `/obj/academy_polysplit_live`):
- Example progression:
  - pre-fuse merged curves: `40 pts / 3 prims`.
  - post-fuse: `29 pts / 3 prims`.
  - after long polysplit chain (`polysplit21`): `56 pts / 40 prims`.
- Live shortest-path split tests on polygon box:
  - baseline (no splitloc): `56 pts / 54 prims`.
  - `splitloc "0e0:0.5 0e2:0.5"`: `58 pts / 55 prims`.
  - multi-point path `"0e0:0.2 0e1:0.8 0e2:0.2"`: `59 pts / 56 prims`.
- `close` interaction on multi-point path:
  - `close=0`: `56` prims,
  - `close=1`: `57` prims (extra closure cut).
- Edge-loop mode density (`pathtype=edge loop`, `splitloc="0e0:0.5"`):
  - `numloops 1 -> 2 -> 3` produced `66 -> 78 -> 90` prims.
- Output edge-group emission:
  - enabling `grouptoggle` created edge group `splitPath` for generated split edges.

## Gotchas

- `splitloc` syntax errors or invalid references can silently produce no meaningful cut.
- Very dense split chains quickly multiply topology.
- `groupappend` does not accumulate across independent cooks the way history-based modeling might suggest; groups reflect current operation output.
- Precision-sensitive models may require smaller `tolerance` to avoid malformed near-corner cuts.

## Companion Nodes

- `curve` for initial panel/guide curve authoring.
- `fuse` for consolidating dependency-generated curve intersections before splitting.
- `subdivide` for smoothing after loop insertion.

## Study Validation

- ✅ Read docs: `nodes/sop/polysplit.txt`
- ✅ Reviewed example: `examples/nodes/sop/polysplit/PolySplitHood.txt`
- ✅ Inspected sticky notes and full panel/fuse/split chain
- ✅ Ran live shortest-path/close/edge-loop/group-output tests in `/obj/academy_polysplit_live`
