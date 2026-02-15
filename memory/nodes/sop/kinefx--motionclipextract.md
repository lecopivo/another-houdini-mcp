# MotionClip Extract (SOP, KineFX)

## Intent

`kinefx::motionclipextract` unpacks a range/pattern of poses from a MotionClip into pose geometry (or motion trails) for editing or analysis before optional repacking.

## Core Behavior

- Evaluates MotionClip over a frame range and outputs extracted skeleton poses.
- Supports frame-range sampling with step and optional existing-sample-only extraction.
- Supports joint-group filtering and COM-only extraction options.
- Leaves source clip metadata (`clipinfo`) available on output.

## Key Parameters

- `mode`: frames vs motion trails.
- `jointnames`: topology-joint group to extract.
- `cliprangemode` + `framerange` triple (start/end/inc).
- `unpackexisting`: key/sample-aware extraction behavior.
- `useendbehavior` / `endbehavior`.
- COM and unpack-attribute options.

## Typical Workflow

```text
motionclip -> motionclipextract -> pose edits -> motionclipupdate
```

- Extract targeted frames and joints.
- Modify extracted geometry.
- Repack changes with `motionclipupdate`.

## Production Usage

- Use frame increment to control edit density/performance.
- Use `@name=`-based joint groups for reliable filtering.
- Keep extraction sparse when only key poses need adjustment.

Measured outcomes (`SimpleMotionClipExtract`):
- Baseline (`10-40 step 1`) output: `806 pts / 775 prims`.
- Range/step scaling:
  - `10-20 step 1` -> `286 / 275`
  - `10-40 step 2` -> `416 / 400`
- Joint-group syntax behavior:
  - `jointnames='@name=Hips'` -> `31` pts (single joint trajectory)
  - plain `jointnames='Hips'` did **not** filter (full extraction remained)

## Gotchas

- Joint filtering expects proper group expressions (typically `@name=...`), not plain token strings.
- `clipinfo.range` can stay unchanged while extracted pose count varies; validate both count and metadata.

## Companion Nodes

- `kinefx::motionclipevaluate` for single-frame readback.
- `kinefx::motionclipupdate` for repacking edited extractions.

## Study Validation

- ✅ Read docs: `nodes/sop/kinefx--motionclipextract.txt`
- ✅ Reviewed example: `SimpleMotionClipExtract`
- ✅ Ran range/step/joint-group extraction tests with measured output scaling
