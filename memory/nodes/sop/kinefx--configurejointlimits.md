# Configure Joint Limits (SOP, KineFX)

## Intent

`kinefx::configurejointlimits` creates/edits per-joint limit configuration dictionaries used by KineFX tools such as ragdoll, IK, and rig posing.

## Core Behavior

- Writes a dictionary point attribute (default `fbik_jointconfig`) containing rest pose and limit data.
- Can initialize/compute limits from MotionClip input.
- Supports guide visualization and out-of-limit highlighting.
- Output skeleton topology remains unchanged; configuration metadata is updated.

## Key Parameters

- `group`: joints to configure.
- `outputconfigurationattrib`: destination dict attribute name.
- `restposeattrib`: rest pose source.
- `computelimits`: compute limits from MotionClip input.
- `rOrd`: rotation order used for Euler cracking.
- `cliprangemode` / frame range params: sample window for limit derivation.
- guide toggles (`displayrotationlimits`, `displaytranslationlimits`, `displayjointsoutsidelimits`).

## Typical Workflow

```text
skeleton (+ optional motionclip) -> configurejointlimits -> ragdoll/ik/rigpose
```


- Start from stashed rest skeleton.
- Optionally feed representative MotionClip to derive baseline limits.
- Refine interactively in state and pass config downstream.

## Production Usage

- Treat the output config attribute as a reusable rig contract across downstream nodes.
- Compute from representative motion first, then tighten manually per joint class.
- Preserve `rest_transform` consistency between configuration and consumer nodes.

Measured outcomes (`ConfigureLimitsFromMotionClip` example):
- `configurejointlimits` output: `53 pts / 52 prims`, includes point dict attribute `fbik_jointconfig`.
- Attribute key sets observed:
  - root joint: `('rest_transform',)`
  - other joints: `('rest_transform', 'rotation_lower_limits', 'rotation_order', 'rotation_upper_limits')`
- `displayjointsoutsidelimits=1` enabled in example for quick violation diagnostics.

Observed nuance:
- Example sticky note indicates provided motionclip may be invalid in some branches; this can produce degenerate (near-zero) computed ranges despite valid config keys.

## Gotchas

- Presence of limit keys does not guarantee meaningful limit ranges; validate values, not keys only.
- Invalid/unrepresentative motionclips can generate trivial limits.
- Rotation order mismatches between setup and consumers can yield incorrect clamping behavior.

## Companion Nodes

- `kinefx::ragdollcollisionshapes`, `kinefx::ragdollsolver`.
- `kinefx::rigpose`, `kinefx::fullbodyik`.
- `kinefx::motionclip` as limit-source generator.

## Study Validation

- ✅ Read docs: `nodes/sop/kinefx--configurejointlimits.txt`
- ✅ Reviewed example: `ConfigureLimitsFromMotionClip`
- ✅ Inspected both `provided_motionclip` and `pose_your_own` branches
- ✅ Verified output config dictionary structure and key sets on points
