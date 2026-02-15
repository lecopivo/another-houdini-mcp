# MotionClip Update (SOP, KineFX)

## Intent

`kinefx::motionclipupdate` writes edited point-time joint data back into a MotionClip, enabling extract-edit-update workflows.

## Core Behavior

- Input 0: source MotionClip.
- Input 1: list of points with `name` + `time` (typically from MotionClip Extract).
- Updates matching joints/samples according to overlap/new-point policies.
- Can blend overridden/new joints by group or attribute-based weights.

## Key Parameters

- `overlapmode`: Override / Remove / Keep Existing / Override Range.
- `newmode`: Insert New Sample or Skip for non-overlapping points.
- `uselocals`: prefer local transforms when local/world disagree.
- attribute repack controls (`repackattribs`, `restattribs`, `animattribs`).
- blend-joint controls (`blendjoints`, `ptblend`, weight method/group/attrib).

## Typical Workflow

```text
motionclip -> motionclipextract -> edit points -> motionclipupdate -> motionclipevaluate
```

- Extract target joints/frames.
- Apply geometric/VEX edits to extracted points.
- Update clip and validate in evaluator.

## Production Usage

- Use `Override Range` when edited points do not exactly align to existing sample times.
- Use `Keep Existing` for non-destructive patch passes.
- Use joint-group weighting for partial influence updates.

Measured outcomes (`SimpleMotionClipUpdate`):
- Update output stayed MotionClip-form (`54` samples).
- Extracted update set: `106` points for two shoulder joints across clip range.
- Editing `shift_the_joints.ty` directly changed shoulder heights after update:
  - `ty=0.0` -> baseline shoulder Y
  - `ty=0.2` -> +`0.2` shoulder Y offset on both targeted joints at frame 30
- `overlapmode=Keep Existing` ignored edited values (returned baseline shoulders).

## Gotchas

- If updates seem ignored, check `overlapmode` first.
- Ensure input-2 points carry valid `name` and `time`; otherwise matching fails silently or acts like no-op.
- Pose count may remain unchanged even when joint transforms changed substantially.

## Companion Nodes

- `kinefx::motionclipextract` (authoring source)
- `kinefx::motionclipevaluate` (verification)
- `kinefx::motionclipposeinsert` for explicit frame insertion workflows

## Study Validation

- ✅ Read docs: `nodes/sop/kinefx--motionclipupdate.txt`
- ✅ Reviewed example: `SimpleMotionClipUpdate`
- ✅ Tested overlap-mode behavior and measured joint-transform deltas
