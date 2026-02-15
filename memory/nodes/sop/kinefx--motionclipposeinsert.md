# MotionClip Pose Insert (SOP, KineFX)

## Intent

`kinefx::motionclipposeinsert` inserts a new pose sample into a MotionClip at a specified frame, with configurable behavior when that frame already exists.

## Core Behavior

- Input 0: MotionClip to modify.
- Input 1: pose geometry to insert.
- Inserts sample at `frame` and resolves overlap via `overlapmode`.
- Supports full replacement, keep existing, update existing, or explicit error on overlap.

## Key Parameters

- `frame`: target sample frame.
- `overlapmode`:
  - Replace
  - Keep Existing
  - Update
  - Error

## Typical Workflow

```text
motionclip -> (optional pose delete/extract) -> motionclipposeinsert -> motionclipevaluate
```

- Remove or target frame region first when needed.
- Insert edited pose from rig pose/extracted skeleton.
- Evaluate and verify continuity.

## Production Usage

- Use `Replace` when authoritative authored pose should fully override sample.
- Use `Update` when only subset joints are provided and existing joints must be preserved.
- Use `Error` mode in procedural pipelines to enforce no accidental overwrites.

Measured outcomes (`SimpleMotionClipPoseInsert`):
- Upstream delete node (`12-18`) produced `49` clip poses.
- Inserting at missing frame `15` increased output to `50` poses.
- Inserting at existing frame `10`:
  - overlap `Replace/Keep/Update` all preserved pose count (`49`)
  - overlap `Error` produced cook failure as expected.

## Gotchas

- Pose count alone cannot distinguish Replace vs Update vs Keep on existing-frame inserts; inspect joint transforms when this distinction matters.
- Inserting at interpolable frames may appear unchanged visually if inserted pose matches interpolation result.

## Companion Nodes

- `kinefx::motionclipposedelete` for clearing insertion windows.
- `kinefx::motionclipevaluate` for visual QA of inserted frame.
- `kinefx::rigpose` or extracted pose edits as insertion source.

## Study Validation

- ✅ Read docs: `nodes/sop/kinefx--motionclipposeinsert.txt`
- ✅ Reviewed example: `SimpleMotionClipPoseInsert`
- ✅ Tested insert-at-missing and insert-at-existing frame behavior across overlap modes
