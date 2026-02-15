# MotionClip Cycle (SOP, KineFX)

## Intent

`kinefx::motionclipcycle` repeats a selected MotionClip range and blends boundaries for seamless looping while optionally preserving locomotion continuity.

## Core Behavior

- Consumes a MotionClip and emits a longer cycled MotionClip.
- Cycle length is controlled by source frame range plus cycles-before/after.
- Supports locomotion-aware sequencing (existing or computed locomotion).
- Blend methods determine seam handling between repeated segments.

## Key Parameters

- `framerange` (start/end/inc): source segment to loop.
- `cyclesbefore`, `cyclesafter`: repetition count (fractional values allowed).
- locomotion block: `locomotion`, source/joint/translation/orientation controls.
- `method` + `region`: seam blend strategy and blend-frame length.
- blend style parameters (`shape`, `bias`, group/attribute blend modes).

## Typical Workflow

```text
motionclip -> motionclipcycle -> motionclipevaluate
```

- Start with clean base cycle range.
- Add cycles after/before.
- Enable locomotion handling for forward path continuity.
- Tune seam blend region/shape.

## Production Usage

- Use fractional `cyclesafter` for partial extension during clip transitions.
- Validate seam quality in evaluated pose space, not only clip-level counts.
- Prefer explicit locomotion joint for predictable trajectory behavior.

Measured outcomes (`SimpleMotionClipCycle`):
- Baseline cycle output: `132` packed prims, `clipinfo.range = 0..5.4375`.
- `cyclesafter` scaling:
  - `0.0` -> `56` prims, range `0..2.25`
  - `1.5` -> `132` prims, range `0..5.4375`
  - `3.0` -> `209` prims, range `0..8.6667`
- Evaluated output contract remained skeleton-sized (`26 pts / 25 prims`) while clip duration changed.

## Gotchas

- Clip topology may stay stable while timing changes significantly; always inspect `clipinfo.range`.
- Locomotion settings can dominate visual quality of loop joins even when blend region is tuned.

## Companion Nodes

- `kinefx::motionclip`, `kinefx::motionclipevaluate`.
- `kinefx::extractlocomotion` for existing-locomotion workflows.

## Study Validation

- ✅ Read docs: `nodes/sop/kinefx--motionclipcycle.txt`
- ✅ Reviewed example: `SimpleMotionClipCycle`
- ✅ Probed cycle output and evaluated skeleton
- ✅ Swept `cyclesafter` and measured range/primitive-count scaling
