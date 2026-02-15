# Dynamic Warp (SOP, KineFX)

## Intent

`kinefx::dynamicwarp` time-warps a source animation/MotionClip against a reference animation/MotionClip to synchronize timing or produce similar motion pacing.

## Core Behavior

- Input 0: source animation.
- Input 1: reference animation.
- Supports two algorithms:
  - synchronize entire clip (DTW-style),
  - create similar motions (guided warp).
- Can operate directly on MotionClips while preserving repacked attributes.
- Output remains animation/MotionClip contract with updated timing in `clipinfo`.

## Key Parameters

- `warpmethod`: algorithm selection (synchronize vs similar motions).
- `maxstep`, `maxstall`: speed-up/slow-down constraints.
- mapping controls (`mappingmethod`, mapping attrib / match attrib).
- source/reference range and sample rate controls.
- output length controls (`outputlengthtype`, `frames/seconds/scale`).
- MotionClip repack controls (`repackattribs`, `restattribs`, `animattribs`).

## Typical Workflow

```text
source motionclip + reference motionclip
  -> mappoints (or attribute matching)
  -> dynamicwarp
  -> motionclipevaluate / downstream clip tools
```

- Pre-map important joints.
- Select warp method per task (global sync vs motif similarity).
- Constrain speed with `maxstep`/`maxstall`.
- Set output-length policy for production clip targets.

## Production Usage

- Use synchronize mode for stride/phase alignment.
- Use similar-motions mode for phrase-level timing cleanup and stall removal.
- Keep locomotion-node assignment explicit when root motion quality matters.

Measured outcomes (`DynamicWarpRemoveStalls` example):
- `warp_the_animation` output contract: `26 pts / 25 prims`, detail `clipinfo` present.
- Changing `warpmethod` altered output clip range materially:
  - `warpmethod=1` (example default): range `0..6.875`
  - `warpmethod=0`: range `0..10.4583`
- In similar-motions mode with output-length-by-frame:
  - `frames=120` -> range `0..4.95833`
  - `frames=240` -> range `0..7.125`

## Gotchas

- Mapping quality dominates result quality; poor joint mapping gives unstable or unnatural warps.
- Output timing can change significantly by method/output-length settings even when topology is unchanged.
- When operating on MotionClips, verify `clipinfo` after each parameter change instead of relying on viewport feel alone.

## Companion Nodes

- `kinefx::mappoints` for robust joint correspondence.
- `kinefx::motionclip`, `kinefx::motionclipevaluate`, `kinefx::motionclipcycle`.

## Study Validation

- ✅ Read docs: `nodes/sop/kinefx--dynamicwarp.txt`
- ✅ Reviewed example: `DynamicWarpRemoveStalls`
- ✅ Inspected mapping + cycle + warp chain
- ✅ Performed mode/output-length sweeps and measured `clipinfo.range` changes
