# Attach Joint Geometry (SOP, KineFX)

## Intent

`kinefx::attachjointgeo` attaches control/capture shapes to skeleton joints and writes the metadata needed for KineFX tools to treat those shapes as joint selectors or capture-influence geometry.

## Core Behavior

- Input 0 is the skeleton (typically points with `name`, `transform`, and optional `rest_transform`).
- Input 1 is the shape library (packed/unpacked primitives with usable `name` values).
- Optional input 2 transfers existing shape assignments/tweaks as a template.
- Output keeps skeleton hierarchy intact and appends shape primitives with `jointgeo` metadata.
- `role` is encoded in `jointgeo` (for example `control` vs `capture`) and drives downstream behavior.

## Key Parameters

### Add Shapes

- `role`: sets semantic use of attached geometry (`control` or `capture`).
- `userestposeattrib`: stabilizes assignment behavior on animated skeletons by using rest-pose matrices.
- `group#` + `shapename#`: assignment mapping from joints to library shape primitive names.
- `shape_worldtrans#`: preserves world-space shape transform instead of inheriting local-joint placement.

### Tweak

- `tweak_group#` with translate/rotate/scale offsets: per-joint local offset authoring for assigned shapes.
- `useoffsetattr` / `tweakoffsetattr`: consume joint offset attributes as shape offset source.
- `usecolorattr` / `tweakcolorattr`: drive shape color from joint attributes.

### Shape Template

- `target_group`, `template_group`: choose destination/template joints.
- `referencetype` + match fields: define mapping strategy (attribute/point number/mapping dict).
- `transfertweak`, `template_worldtrans`: retain template offsets/world transforms.

## Typical Workflow

```text
skeleton -> attachjointgeo (shape library input connected) -> rig/capture tools
```

Capture-focused pattern from official example:

```text
character skeleton + world-space capture shapes
  -> attachjointgeo(role=capture)
  -> (optional mirror/template transfer)
  -> jointcapturebiharmonic (uses capture geo)
```

## Production Usage

- Ensure shape-library primitives have reliable names before assignment; name collisions/missing names cause assignment confusion.
- Use `shape_worldtrans` for complex world-authored controls/capture volumes.
- Prefer rest-pose-based assignment when source skeleton is animated to avoid time-dependent ambiguity.
- Mirror-and-transfer via template input is effective for bilateral rigs.

Measured outcomes:
- Official example `/obj/academy_capturegeoexample/capture_geometry_example`:
  - `add_capture_geometry`: `45` prims, with `4` `jointgeo`-tagged packed capture shapes.
  - `transfer_mirrored_capturegeo`: `47` prims (mirrored assignments added), `jointgeo` and `name` prim attrs present.
- Live validation `/obj/academy_attachjointgeo_live/attach1`:
  - After one assignment, prim count increased `41 -> 42`.
  - `role=0` produced `jointgeo.role='control'`.
  - `role=1` produced `jointgeo.role='capture'`.
  - `shape_worldtrans1=1` stored explicit `jointgeo.offset` matrix translation.
  - `shape_worldtrans1=0` removed explicit world offset (local-joint placement behavior).

## Gotchas

- Library names after `mergepacked` may differ from upstream node names; verify actual output `name` values before setting `shapename#`.
- If attach appears to do nothing, confirm input 0 is a skeleton stream (not captured/deformed mesh geometry).
- Tiny/missing viewport controls can be caused by skeleton joint scale.
- For mixed local/world libraries, define world-shape grouping to keep assignment state clear.

## Companion Nodes

- `kinefx::jointcapturebiharmonic` to consume capture-role geometry for weight influence.
- `kinefx::skeletonmirror` plus second `attachjointgeo` (template mode) for left/right transfer.
- `mergepacked`, `name`, and primitive-modeling SOPs for building shape libraries.

## Study Validation

- ✅ Read docs: `nodes/sop/kinefx--attachjointgeo.txt`
- ✅ Reviewed example: `examples/nodes/sop/kinefx--attachjointgeo/capturegeoexample.txt`
- ✅ Inspected official network and sticky notes
- ✅ Ran live tests for `role` and `shape_worldtrans` behavior with measured `jointgeo` metadata changes
