# Agent Animation Unpack (SOP, KineFX)

## Intent

Extract agent animation into SOP-side representations: skeleton poses for rig workflows, or MotionClip data (single or packed multi-clip) for clip editing pipelines.

## Core Behavior

- Converts agent primitives into one of several output contracts selected by `output`.
- Pose modes emit skeleton geometry.
- MotionClip modes emit packed clip geometry suitable for KineFX clip nodes.
- Clip selection (`agentclipname` / `agentclippattern`) strictly controls what is emitted.

## Key Parameters

- `output`:
  - `Current Pose`, `Agent Clip Pose`, `Rest Pose`
  - `MotionClip`
  - `Packed MotionClips`
- `agentclipname`: clip selector for single-clip modes.
- `agentclippattern`: clip pattern/list selector for packed multi-clip mode.
- Timing controls (`frame`, `time`, start/end ranges): define sampling moment/range semantics.

## Typical Workflow

```
agent -> agentanimationunpack -> motionclip tools -> agentclip (write-back)
```

- Extract desired clip(s) from agent.
- Edit with clip tools (`motionclipretime`, blend/sequence tools, etc.).
- Push modified clip(s) back into agent definition using `agentclip`.

## Production Usage

- Use `output=MotionClip` for focused single-clip edits.
- Use `output=Packed MotionClips` + `agentclippattern` for bulk clip processing in foreach pipelines.
- Validate clip extraction with metadata (`clipinfo`) and per-primitive timing attrs.

Measured outcomes (`/obj/academy_AgentClipToMotionClip/crowd`):
- `output=3` (MotionClip): `27` packed prims for `walk`, with detail `clipinfo` and prim `time`.
- `output=4` (Packed MotionClips):
  - `agentclippattern='*'` -> `2` packed prims
  - `'walk'` -> `1`
  - `'run'` -> `1`
- `agentclipname` strictness in MotionClip mode:
  - `walk` -> `27` packed prims
  - `run` -> `18` packed prims
  - invalid name -> empty output (`0 prims`)
- Pose modes (`output=0/1/2`) emitted skeleton polygon geometry rather than packed clip form.

## Gotchas

- Empty outputs are frequently selector mismatches (`agentclipname`/`agentclippattern`), not broken input agents.
- Packed outputs can hide complexity; primitive count alone is insufficient for QA.
- Check clip metadata (`clipinfo`) before downstream retime/blend assumptions.

## Companion Nodes

- `agentclip` for importing/updating clip data on agent definitions.
- `kinefx::motionclipretime` and other motionclip SOPs for edit passes.
- `block_begin`/`block_end`, `unpack`/`pack` for multi-clip batch operations.

## Study Validation

- ✅ Read docs: `nodes/sop/kinefx--agentanimationunpack.txt`
- ✅ Reviewed example: `examples/nodes/sop/kinefx--agentanimationunpack/AgentClipToMotionClip.txt`
- ✅ Inspected official crowd branch and companion clip-update chain
- ✅ Swept output modes and clip selectors with measured geometry/metadata checks
