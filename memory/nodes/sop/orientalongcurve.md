# Orientation along Curve (SOP)

## Intent

`orientalongcurve` computes stable frame attributes (tangent/up/out/quaternion/transform) along curves for downstream copy, sweep, and path-based deformation workflows.

## Core Behavior

- Treats polygons as curves (including closed loops), making closed-path orientation easier than generic frame tools.
- Computes tangents first, then resolves up vectors and optional roll/yaw/pitch rotations.
- Can optionally read point transform attributes (`N`, `up`, `orient`, `rot`, `transform`, etc.) to drive frame construction.
- Outputs frame data on points or vertices as vector/quaternion/matrix attributes.

## Key Parameters

- `tangenttype`, `continuousclosed`, `extrapolateendtangents`: tangent continuity and end behavior controls.
- `upvectortype`, `upvectoratstart`, `useendupvector`: up-vector targeting and twist resolution.
- `applyroll`, `rollper`, `fulltwists`, `incroll`: twist policy and accumulation behavior.
- `applyyaw`, `applypitch`: additional per-frame reorientation.
- `stretcharoundturns`, `maxstretcharoundturns`: cross-section stretch compensation in turns.
- Output attribute names (`xaxisname`, `yaxisname`, `zaxisname`, `quaternionname`, `transform3name`, `transform4name`).

## Typical Workflow

```text
curve -> orientalongcurve -> copytopoints/sweep/path consumer
```

- Establish tangent/up policy first for stability.
- Add controlled twist/yaw/pitch only after base frame continuity is correct.

## Production Usage

- Preferred for robust path frames on open and closed curves where frame flips must be minimized.
- Useful as a shared orientation contract for `sweep`, `copytopoints`, and curve-follow rigs.
- In tank tread-like setups (official `TankTread` example), this node provides the orientation backbone for repeated segment placement along curved tracks.

Measured outcomes:
- Live Houdini geometry measurements are pending in this session (tool-access checkpoint recorded in `short_term_memory.md`).

## Gotchas

- Mixing custom up targets with heavy twist can introduce unexpected roll unless start/end up policy is explicit.
- Closed curves can still show end discontinuity if continuity/twist options are not aligned.
- Output class (point vs vertex) can change averaging behavior on shared points.

## Companion Nodes

- `sweep` for frame-driven profile construction.
- `copytopoints` for orient-driven instancing.
- `polyframe` when lower-level explicit frame attributes are needed.

## Study Validation

- ✅ Read docs: `help/nodes/sop/orientalongcurve.txt`
- ✅ Reviewed example: `help/examples/nodes/sop/orientalongcurve/TankTread.txt`
- ⏳ Live parameter/geometry validation pending in this session
