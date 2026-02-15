# Rig Mirror Pose (SOP, KineFX)

## Intent

`kinefx::rigmirrorpose` mirrors SOP skeleton poses across a defined symmetry plane, using precomputed or on-the-fly mirrored-joint correspondence.

## Core Behavior

- Can run in two operations:
  - `Mirror Pose`: modifies transforms.
  - `Compute Mirroring`: computes correspondence metadata only.
- Uses `mirrorpt` point dict attribute to store mirror mapping and flip-axis behavior.
- Supports name/position search strategies for correspondence generation.
- Mirrors selected point group only (`group` parameter).

## Key Parameters

- `operation`: mirror transforms vs compute correspondences only.
- `mirrorptattrib`: correspondence attribute name (default `mirrorpt`).
- `computemirroring`: recompute correspondences while mirroring.
- matching method:
  - position+name similarity (`maxnamedist`, `maxposdist`)
  - token-based name matching (`tokenpos`, `matchtokens`, `mirroredtokens`)
- symmetry setup: `symmetryaxis`, mirror-plane direction/origin options.
- rest-pose source controls (`restposesrc`, frame/attribute).

## Typical Workflow

```text
posed skeleton -> rigmirrorpose -> mirrored pose output
```

- Ensure skeleton has stable naming and transform attrs.
- Compute/check mirror correspondences.
- Apply mirror operation to desired group.

## Production Usage

- Prefer compute-only pass first to validate `mirrorpt` mappings.
- Keep mirror token strategy aligned with naming convention (`prefix`, `suffix`, separators).
- Use position+name method as fallback when token parsing is ambiguous.

Measured outcomes (live validation; no official node example listing for this node):
- Output included `mirrorpt` dict attribute with per-point mapping (`value`) and flip metadata.
- `operation` behavior:
  - `Mirror Pose` changed transforms according to mirror rules.
  - `Compute Mirroring` preserved source transforms while outputting correspondence metadata.
- Method sensitivity:
  - `Position & Name Similarity` successfully paired left/right joints in synthetic rig (`shoulder_L <-> shoulder_R`, `hand_L <-> hand_R`).
  - `From Names` with token setup `_L/_R` in this test produced `-1` (no match) for all non-root points, demonstrating token-configuration fragility.

## Gotchas

- Token-based matching fails silently into unmatched mappings (`value=-1`) when token settings are slightly off (token content or token position).
- If transforms don't change as expected, verify operation mode is not compute-only.
- Mirroring quality depends on reliable rest pose and transform attribute integrity.

## Companion Nodes

- `kinefx::skeletonmirror` (structure mirroring)
- `kinefx::orientjoints`, `kinefx::rigpose`
- `kinefx::rigdoctor` (pre-cleanup before mirror operations)

## Study Validation

- ✅ Read docs: `nodes/sop/kinefx--rigmirrorpose.txt`
- ✅ Confirmed no official node example listing from `list_example_nodes`
- ✅ Built synthetic bilateral rig and validated operation/method correspondence behavior
