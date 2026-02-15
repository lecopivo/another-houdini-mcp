# MotionClip Blend (SOP, KineFX)

## Intent

`kinefx::motionclipblend` overlays a layer MotionClip onto a base MotionClip with controllable blend windows, joint scope, and locomotion-aware behavior.

## Core Behavior

- Input 0 is base clip, input 1 is layer clip.
- Produces a blended output clip whose length covers base plus layered segment.
- Blend envelope is controlled by fade-in/out region params.
- Supports per-joint, per-group, or attribute-driven blend weighting.
- Optional locomotion-aware velocity blending for more natural path continuity.

## Key Parameters

### Region
- `fadein`, `start`, `peak` for ramp-in.
- `fadeout`, `release`, `end` for ramp-out.
- `inc` sample increment for blend section.

### Blend
- `effect`: maximum layer contribution.
- `blend_shape`, `bias`: blend curve and biasing.
- `blendmode`: all joints / joint groups / by attribute.
- `jointnames`: restrict to joint subset.

### Locomotion
- locomotion method and source options (existing, computed, joint/COM based).
- orientation and shift-axis controls for path blending quality.

## Typical Workflow

```text
base motionclip + layer motionclip -> motionclipblend -> motionclipevaluate
```

- Define the temporal blend region first.
- Tune effect/bias while inspecting key joints.
- Add locomotion blending when trajectory continuity is required.

## Production Usage

- Use fade windows to avoid hard snaps at overlay boundaries.
- Keep `effect` animatable for art-directed punch-in/punch-out overlays.
- Use joint-group blend mode for upper/lower body layering.

Measured outcomes (`SimpleMotionClipBlend` example):
- Blend output contract: `240 packed prims` with `clipinfo` detail.
- Evaluated skeleton output: `26 pts / 25 prims`.
- Changing blend-region controls affected pose result (frame 10 max point displacement ~`0.2493` between `fadein=1` and `fadein=0`).
- `effect` strongly affected result when fade-in was disabled (frame 10 max displacement ~`0.2493` for `effect 0` vs `1`).

## Gotchas

- If `effect` seems inert, check fade windows and evaluation frame; outside blend region differences can vanish.
- Distinguish clip-domain output changes from evaluated-pose changes; many differences show up only after `motionclipevaluate`.
- Locomotion mode mismatches can produce visually odd trajectory blends even when limb blending looks correct.

## Companion Nodes

- `kinefx::motionclip`, `kinefx::motionclipevaluate`.
- `kinefx::motionclipretime`, `kinefx::motionclipsequence`.

## Study Validation

- ✅ Read docs: `nodes/sop/kinefx--motionclipblend.txt`
- ✅ Reviewed example: `SimpleMotionClipBlend`
- ✅ Inspected full base/layer/import/evaluate chain
- ✅ Ran blend envelope/effect sweeps and measured evaluated-pose differences
