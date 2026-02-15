# Rig Attribute VOP (SOP, KineFX)

## Intent

`kinefx::rigattribvop` runs CVEX/VOP logic on KineFX rig attributes, with rig-specific transform recomputation controls for input/output skeleton streams.

## Core Behavior

- Functionally parallels `attribvop` but with KineFX rig-oriented state/parameters.
- Executes CVEX network (internal/shop/script) on selected group/class.
- Can auto/explicit-bind attributes and groups.
- `Rig` tab compute toggles can recompute transforms on inputs/output to keep KineFX transform attrs coherent.

## Key Parameters

- VEX source controls: `vexsrc`, `shoppath`, `script`, compile/reload.
- binding controls: autobind, explicit bindings, group bindings.
- `vex_matchattrib`: cross-input correspondence key.
- `compute`, `compute1..4`: recompute transforms for output/inputs.
- precision/threading/perf controls (`vex_precision`, multithreading, in-place).

## Typical Workflow

```text
rest rig + control rig -> rigattribvop (solve network inside) -> animated rig
```

- Build/author KineFX VOP network inside node (CVEX context).
- Bind required rig attrs/groups.
- Enable compute toggles where transform consistency is required downstream.

## Production Usage

- Prefer explicit transform recompute toggles when writing transform-related attrs.
- Keep `vex_matchattrib` aligned with stable IDs/names for multi-input rig correspondence.
- Use CVEX-compatible VOPs only (SOP-specific VOP ops are unavailable).

Measured outcomes (`IkSolverVop` example):
- `solveik_vop` output: `3` points (`root/middle/tip`) with transform attrs.
- Editing controls (`Edit_Controls` tip Y +/-0.5) produced expected IK pose changes in `ANIM` output:
  - middle/tip points moved accordingly.
- `compute` toggle behavior:
  - `compute=1` output point attrs included `localtransform` and `__effectivelocaltransform`.
  - `compute=0` removed those recomputed attrs, leaving `P`, `name`, `transform`.

Observed mismatch:
- Root sticky note text references CurveSolver in this IK example asset; treat this as stale/mismatched annotation.

## Gotchas

- Forgetting compute toggles can leave downstream nodes with missing/unsynced local transform attrs.
- Because this is CVEX context, SOP-only VOP assumptions can silently break intended logic.
- Example annotations may be stale across asset revisions.

## Companion Nodes

- `kinefx::rigattribwrangle` (VEX text equivalent)
- `kinefx::computetransform` (explicit transform recompute)
- internal KineFX VOP ops such as `solveik`, `solvecurve`, `setpointtransforms`

## Study Validation

- ✅ Read docs: `nodes/sop/kinefx--rigattribvop.txt`
- ✅ Reviewed example docs: `IkSolverVop`, `CurveSolverVop`, `CameraOnPath`
- ✅ Inspected internal VOP network and tested control-driven IK changes
- ✅ Validated `compute` toggle effect on output transform attribute contract
