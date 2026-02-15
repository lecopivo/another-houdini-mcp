# MotionClip (SOP, KineFX)

## Intent

`kinefx::motionclip` caches skeleton animation into packed MotionClip form for efficient evaluation, retiming, blending, sequencing, and downstream clip processing.

## Core Behavior

- Produces packed-primitive clip structure with `clipinfo` detail metadata and per-pose `time` data.
- Supports single-input or packed multi-input clip creation (`packinputs`).
- Stores chosen attributes as animated payload.
- Can isolate key poses into sparse clip representations.

## Key Parameters

- `packinputs`: one packed clip per input.
- `restframe`: rest/topology frame selection.
- `usesamplerate` + `samplerate`: explicit sampling policy.
- `useframerange` + range fields: explicit clip extraction window.
- `reloadmethod` / `reload`: cache update behavior.
- `attribs`: animated attribute payload.
- key-pose controls (`isolatekeyposes`, key source/channel options).

## Typical Workflow

```text
skeleton animation -> motionclip -> (retime/blend/sequence) -> motionclipevaluate
```

- Convert imported animation to MotionClip early.
- Apply clip-domain operations.
- Evaluate only where geometry display/deform is needed.

## Production Usage

- Keep attribute payload minimal for performance.
- Use manual reload mode when iterating heavy clips to avoid accidental recooks.
- Prefer MotionClip domain for timing edits before expensive deformation stages.

Measured outcomes (`SimpleMotionClip` example):
- MotionClip output: `54 pts / 54 packed prims`, detail `clipinfo` present.
- Example appears to be fed from a source already in clip-friendly form; changing `samplerate` / frame-range controls did not materially alter output in this setup (contract remained stable).
- With `usesamplerate` and `useframerange` enabled, output still stayed stable in this specific network, indicating upstream source contract dominates.

## Gotchas

- Sampling/range parms only affect output when node is actually responsible for clip extraction; upstream pre-cached/clip-constrained inputs may make these controls appear inert.
- Forgetting reload policy can make debugging confusing (stale clips vs recooked clips).

## Companion Nodes

- `kinefx::motionclipevaluate` for display/evaluation.
- `kinefx::motionclipblend`, `kinefx::motionclipretime`, `kinefx::motionclipsequence` for clip edits.

## Study Validation

- ✅ Read docs: `nodes/sop/kinefx--motionclip.txt`
- ✅ Reviewed example: `SimpleMotionClip`
- ✅ Inspected source-import -> motionclip network
- ✅ Tested samplerate/range/reload controls and recorded observed stability in this setup
