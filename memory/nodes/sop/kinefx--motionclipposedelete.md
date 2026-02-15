# MotionClip Pose Delete (SOP, KineFX)

## Intent

`kinefx::motionclipposedelete` removes selected poses from a MotionClip (or removes joint subsets within those poses) using frame/pose selection patterns.

## Core Behavior

- Operates on pose samples (excluding rest pose).
- Selection can be by frame range/pattern, pose range/group, with invert options.
- Can target whole poses or joint subsets.
- Output stays MotionClip-form with reduced/altered sample set.

## Key Parameters

- `selectionmode`: frame range / frame pattern / pose group / pose range.
- frame-range section (`framerange*`, step/pattern controls, include edges).
- invert controls (mode-specific `negate*` parms).
- `jointgroup` + delete non-selected-joints for partial-pose cleanup.

## Typical Workflow

```text
motionclip -> motionclipposedelete -> (optional pose insert/update) -> evaluate
```

- Delete noisy or unwanted sample spans.
- Optionally keep only selected span (invert selection) for clip trimming.

## Production Usage

- Use mode-specific negate toggles carefully; invert parameter names differ by selection mode.
- Preserve boundary poses intentionally when trimming to avoid hard motion truncation.
- For selective body cleanup, use joint-group deletion instead of full pose deletion.

Measured outcomes (`SimpleMotionClipPoseDelete`):
- Example baseline (`frame 10-20` deletion) output: `45` prims.
- Wider deletion (`10-40`) reduced to `25` prims.
- In frame-range mode, invert uses `negate2`:
  - `negate2=0` (delete selection) -> `45` prims
  - `negate2=1` (keep selection) -> `12` prims

## Gotchas

- Different selection modes use different negate parms (`negate2` vs `negate`), easy to mis-set.
- Pose counts can change while clip range metadata appears stable; validate both.

## Companion Nodes

- `kinefx::motionclipposeinsert` for filling/replacing removed frames.
- `kinefx::motionclipupdate` for repacking edited pose geometry workflows.

## Study Validation

- ✅ Read docs: `nodes/sop/kinefx--motionclipposedelete.txt`
- ✅ Reviewed example: `SimpleMotionClipPoseDelete`
- ✅ Tested frame-range and invert-mode behavior with measured pose-count changes
