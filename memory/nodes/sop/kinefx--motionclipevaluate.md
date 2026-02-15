# MotionClip Evaluate (SOP, KineFX)

## Intent

`kinefx::motionclipevaluate` samples a MotionClip at a single frame and outputs an evaluated skeleton pose for playback, inspection, or downstream SOP operations.

## Core Behavior

- Input is MotionClip packed data; output is unpacked skeleton pose.
- Supports current-frame or custom-frame evaluation.
- Supports linear/constant interpolation and configurable end behavior.
- Can emit center-of-mass helper point and additional unpacked attrs.

## Key Parameters

- `mode`: current frame vs custom frame.
- `frame`: explicit sample frame in custom mode.
- `interp`: linear vs constant.
- `useendbehavior` + `endbehavior`: clamp/loop/mirrored loop outside range.
- COM options: `outputcom`, `isolatecom`, `configattrib`.
- attribute unpack controls: `restattribs`, `attribs`.

## Typical Workflow

```text
motionclip -> motionclipevaluate -> deform/visualize/debug
```

- Keep clip edits in MotionClip domain.
- Evaluate only where geometric pose output is required.

## Production Usage

- Use custom-frame mode for deterministic debugging/validation.
- Keep extra-attribute unpacking minimal for performance.
- Enable COM output only when explicitly needed.

Measured outcomes (`SimpleMotionClipEvaluate`):
- Evaluated output: `26 pts / 25 prims`, attrs include `time`, `transform`, `localtransform`, `name`.
- In this official setup, frame/interp/end-behavior changes produced identical sampled pose (max displacement `0.0` between tested frames), indicating the source clip behaves as effectively static in this example configuration.

## Gotchas

- If frame changes appear to do nothing, verify source clip actually contains meaningful pose variation in the tested range.
- Distinguish node behavior from example data quality; static source clips can mask interpolation/end-mode effects.

## Companion Nodes

- `kinefx::motionclip` (producer)
- `kinefx::motionclipextract` (range extraction)
- `kinefx::motionclipupdate` (write-back after edits)

## Study Validation

- ✅ Read docs: `nodes/sop/kinefx--motionclipevaluate.txt`
- ✅ Reviewed example: `SimpleMotionClipEvaluate`
- ✅ Validated output contract and parameter controls
- ✅ Recorded static-source behavior observed in this build/example
