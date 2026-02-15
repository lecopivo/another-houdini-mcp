# MotionClip Sequence (SOP, KineFX)

## Intent

`kinefx::motionclipsequence` concatenates two MotionClips and blends the transition to create a continuous combined clip.

## Core Behavior

- Input 0 is first clip, input 1 is second clip.
- Output is a single MotionClip with transition blending.
- Blend method (`preserve`, `overlap`, `insert`) changes seam region size and sample count.
- Optional locomotion handling shifts/sequences second clip for trajectory continuity.

## Key Parameters

- `joints`: limit sequencing to joint subset.
- locomotion block: `locomotion`, `sequencetype`, `locomotionjoint`, translation/orientation matching.
- blend block: `method`, `region`, sample increment, blend mode/shape/bias.

## Typical Workflow

```text
motionclip A + motionclip B -> motionclipsequence -> motionclipevaluate
```

- Choose sequencing strategy first (locomotion-aware vs simple concatenation).
- Tune blend method and blend-frame region.
- Validate transition around seam in evaluated pose.

## Production Usage

- Use overlap mode for compact transitions.
- Use insert mode when explicit transition window is needed.
- Keep locomotion joint explicit for consistent pathing across clips.

Measured outcomes (`SimpleMotionClipSequence`):
- Baseline output: `84` clip samples, `clipinfo.range 0..3.4583`.
- Blend method impact:
  - `method=0` preserve: `84` samples
  - `method=1` overlap: `83` samples
  - `method=2` insert: `85` samples
- Overlap blend-region impact (`method=1`):
  - `region=0.0` -> `85` samples, range `0..3.4583`
  - `region=0.56` -> `83` samples, range `0..3.435`
  - `region=5.0` -> `80` samples, range `0..3.25`

## Gotchas

- Transition quality changes can appear mainly in sample distribution/range before obvious pose differences.
- Some example clips produce subtle locomotion toggles in evaluated output; confirm with clip metadata and seam-frame checks.

## Companion Nodes

- `kinefx::motionclip`, `kinefx::motionclipevaluate`.
- `kinefx::motionclipblend`, `kinefx::motionclipcycle`, `kinefx::dynamicwarp`.

## Study Validation

- ✅ Read docs: `nodes/sop/kinefx--motionclipsequence.txt`
- ✅ Reviewed example: `SimpleMotionClipSequence`
- ✅ Tested blend methods and blend region with measured sample/range changes
