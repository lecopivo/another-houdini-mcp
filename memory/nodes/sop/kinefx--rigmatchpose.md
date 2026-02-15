# Rig Match Pose (SOP, KineFX)

## Intent

`kinefx::rigmatchpose` authors corresponding match poses on two skeletons for retarget preparation, storing those poses in a configurable matrix attribute (typically `rest_transform`).

## Core Behavior

- Input 0: target skeleton, input 1: source skeleton.
- Can write pose directly to each output (`Matched Pose`) or keep current transform stream while storing pose as attribute (`Pass Through`).
- Supports global size/space matching (bbox and scene transforms) and stores applied global delta in detail attribute.
- Maintains two-output contract (target and source branches).

## Key Parameters

### Pose Destination
- `poseattrib` (attribute name for stored pose, default `rest_transform`).
- `firstoutput`, `secondoutput`: `Matched Pose` vs `Pass Through` behavior per output.

### Match Size
- `bboxmatch` + group/frame controls for initial bounds alignment.
- scene transforms (`scene_t/r/p/scale`) for manual global alignment.
- `stashattrib` detail attribute for applied global delta (default `scene_transform`).

### Interaction / Tweak Pose
- enable per-side editing (`enabletarget`, `enablesource`).
- destination and reference transformation multiparms for pose authoring.

## Typical Workflow

```text
target skeleton + source skeleton -> rigmatchpose -> computerigpose/retarget chain
```

- Align global size/space first.
- Author corresponding match poses on both rigs.
- Feed stored pose attrs into downstream retarget offset computation.

## Production Usage

- Use `Pass Through` outputs when you need to preserve incoming animation while attaching pose metadata.
- Keep `scene_transform` (or custom delta attr) for reversible global alignment operations.
- Explicitly verify which output is writing live transforms vs metadata-only.

Measured outcomes (live validation; no official node example listing for this node):
- Output contracts:
  - target output carried `rest_transform` and optional `transform` based on `firstoutput` mode.
  - source output carried `rest_transform` and optional `transform` based on `secondoutput` mode.
- `firstoutput` mode behavior (live test):
  - mode `0` (`Pass Through`): target output had no `transform` attr and stayed at original target bbox (`0..1` in Y).
  - mode `1` (`Matched Pose`): target output had `transform` and matched source-space bbox (`1.2..4.2` in Y).
- `scene_scale=1.5` changed target output extent (`Y max 4.2 -> 5.7`) and retained detail `scene_transform`.

## Gotchas

- Misreading output-mode semantics can make it seem like match pose is "not applied"; check whether output is pass-through.
- Even with similar topology, global scene transforms can silently shift rig space; track via detail delta attribute.
- No official example for this node in current example corpus; validate with a synthetic two-rig setup.

## Companion Nodes

- `kinefx::computerigpose`, `kinefx::mappoints`, `kinefx::fktransfer`, `kinefx::fullbodyik`.
- `xformbyattrib` for reversing stored global delta transforms.

## Study Validation

- ✅ Read docs: `nodes/sop/kinefx--rigmatchpose.txt`
- ✅ Confirmed no official node example listing from `list_example_nodes`
- ✅ Built and tested two-rig live setup with both outputs and mode switches
