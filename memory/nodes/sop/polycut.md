# PolyCut (SOP)

## Intent

`polycut` breaks curves/polylines by removing edges/points or inserting cuts when an attribute crosses or changes beyond thresholds.

## Core Behavior

- Operates on curves by point-mode or edge-mode (`type`).
- Uses `strategy` to either remove offending components or cut/split at detected transitions.
- Transition detection can be by attribute crossing (`cutvalue`) or attribute change magnitude (`cutthreshold`).
- Supports optional closed-fragment preservation via `keepclosed`.

## Key Parameters

- `type`: points vs edges operation mode.
- `strategy`: remove vs cut.
- `detectedgechanges`: crossing vs change-threshold detection.
- `cutattrib`, `cutvalue`, `cutthreshold`: transition criteria.
- `keepclosed`: preserve closed fragments when possible.
- `cutpoints`/`cutedges` groups: constrain editable elements.

## Typical Workflow

```text
curve/polyline with driving attribute -> polycut -> optional cleanup/rebuild
```

- Start with a clear cut-driving attribute (`P.x`, length proxy, custom scalar).
- Choose edge mode for precise split insertion; point mode for harder segmentation.
- Use threshold mode for adaptive segmentation based on attribute delta.

## Production Usage

- Useful for procedural segment extraction, contour splitting, and curve cleanup.
- Good pre-processing before resampling/sweep/path operations.
- Prefer explicit criteria and groups to avoid over-fragmentation.

Measured outcomes (`PolyCutBasic` + live `/obj/academy_polycut_live`):
- Example variants on base 10-point curve:
  - remove edges at crossing: `10 pts / 3 prims`.
  - cut long edges (attribute change threshold): `60 pts / 26 prims`.
  - cut at crossing (point mode): `14 pts / 5 prims`.
  - split at crossing (edge mode): `14 pts / 3 prims`.
- Live edge/point strategy sweep (`cutattrib=P.x`, `cutvalue=2.2`):
  - edges-remove: `10 pts / 3 prims`.
  - edges-cut: `14 pts / 3 prims`.
  - points-remove: `6 pts / 3 prims`.
  - points-cut: `14 pts / 5 prims`.
- Threshold mode detail growth (`detectedgechanges=change`, `cutattrib=P`):
  - `cutthreshold 2.0 -> 1.0 -> 0.5` produced `32 -> 60 -> 124` points and progressively smaller max segment lengths (`2.0 -> 1.0 -> 0.5`).
- `keepclosed` interaction validated on closed polygon circle cut at `P.x=0`:
  - `keepclosed=0`: `16 pts / 4 prims`, `0` closed fragments.
  - `keepclosed=1`: same counts but `2` fragments remained closed.

## Gotchas

- Low thresholds can explode point/primitive counts quickly.
- Choice of `type` and `strategy` changes topology class significantly for similar inputs.
- `keepclosed` may not affect open inputs; validate on truly closed curves.
- Missing/incorrect cut attribute silently changes behavior (for example all edges treated uniformly depending on mode).

## Companion Nodes

- `curve` to author base polylines with predictable point order.
- `dissolve`/`edgedivide` for alternative edge editing workflows.
- downstream resample/sweep nodes for rebuilt segments.

## Study Validation

- ✅ Read docs: `nodes/sop/polycut.txt`
- ✅ Reviewed example: `examples/nodes/sop/polycut/PolyCutBasic.txt`
- ✅ Inspected stickies and all four example strategy variants
- ✅ Ran live strategy/type/threshold/keepclosed behavior tests in `/obj/academy_polycut_live`
