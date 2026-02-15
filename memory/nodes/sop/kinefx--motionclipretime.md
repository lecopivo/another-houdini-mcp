# MotionClip Retime (SOP, KineFX)

## Intent

`kinefx::motionclipretime` retimes a MotionClip by either shifting/cropping existing sample timing or resampling the clip with time/frame/speed-driven evaluation.

## Core Behavior

- Input: MotionClip.
- Output: retimed MotionClip with updated `time` samples and `clipinfo` timing metadata.
- `Range Shift` mode adjusts timing without resampling sample count.
- Resample modes (`by time`, `by frame`, `by speed`) rebuild sampled poses over an output range/sample rate policy.
- Optional left/right end behavior overrides control out-of-range evaluation semantics.

## Key Parameters

### Timing / Evaluation Mode

- `evalmode`: `Range Shift`, `Resample by Time`, `Resample by Frame`, `Resample by Speed`.

### By Shift (Range Shift mode)

- `trim`: remove samples outside animation start/end.
- `animstart`, `animend`: crop source animation window.
- `shift`: playback start frame offset.
- `speed`: constant playback speed factor.

### Resample (resample modes)

- `time`, `frame`, `speedanim`: driving function per mode.
- `outputrange`, `outputsamplerate`: output clip timing contract.
- `repackattribs`, `restattribs`, `animattribs`: attribute repack policy.

### End Behavior

- `leftendbehavior`, `rightendbehavior` with optional override toggles.

## Typical Workflow

```text
motionclip -> motionclipretime -> motionclipevaluate
```

- Use `Range Shift` for fast crop/offset/speed edits on existing samples.
- Switch to resample modes when explicit output timing/sample contracts are required.
- Validate with `motionclipevaluate` only after confirming `clipinfo` contract.

## Production Usage

- Prefer `Range Shift` for lightweight editorial timing adjustments.
- Use resample modes to conform clip duration/rate for downstream batching.
- Treat `clipinfo.range` and `clipinfo.rate` as authoritative QA outputs.

Measured outcomes (`SimpleMotionClipRetime` example):
- Upstream clip: `241` samples.
- Example default (`Range Shift` with trim and speed `0.7`) output: `22` samples, range `0..1.1905`, rate ~`16.8`.
- `Range Shift` speed interaction (sample count stable at `22`):
  - `speed=0.5` -> range `0..1.6667`, rate `12.0`
  - `speed=1.0` -> range `0..0.8333`, rate `24.0`
  - `speed=2.0` -> range `0..0.4167`, rate `48.0`

Observed nuance in this example setup:
- Resample mode parameter sweeps produced stable clip counts/ranges in tested settings, suggesting source/default expressions constrain visible change in this asset.

## Gotchas

- If pose differences seem absent, inspect `clipinfo` first; timing contract may have changed even when sampled pose checks at specific frames appear unchanged.
- Some official examples include constrained/default expressions that can mask expected resample behavior.

## Companion Nodes

- `kinefx::motionclip` (source generation)
- `kinefx::motionclipevaluate` (retime verification)
- `kinefx::motionclipblend`, `kinefx::dynamicwarp` (downstream timing/edit tools)

## Study Validation

- ✅ Read docs: `nodes/sop/kinefx--motionclipretime.txt`
- ✅ Reviewed example: `SimpleMotionClipRetime`
- ✅ Inspected official network (`motionclip -> Crop_and_slow -> evaluate`)
- ✅ Ran mode and speed-factor tests with measured `clipinfo` outcomes
