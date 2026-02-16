# Path Deform (SOP)

## Intent

`pathdeform` reshapes existing geometry along one or more curves, with controls for mapping position/length, capture region, twist/scale, and rigidity.

## Core Behavior

- Deforms point positions without changing topology.
- Maps geometry length and offset to curve domain using fraction or distance units.
- Supports piece-based mapping (geometry pieces matched to curve pieces via attribute).
- Supports rigid-region constraints and transition softening to keep selected parts from bending.

## Key Parameters

- Mapping: `curve_endunit`, `curve_posend`, `curve_posoffsetunit`, `curve_posoffset`.
- Boundary handling: `startbehavior`, `endbehavior` (extend/clamp/clip).
- Secondary deformation: `taper_*` (scale), `rotate_*` (twist/rotation).
- Capture/alignment: `geo_controlaxis`, `geo_controlup`, `geo_capturestart`, `geo_captureend`, `geo_centeroncurve`.
- Rigidity: `rigid_enable`, `rigid_method`, `rigid_group`, `soften_*`, rigidity mask controls.
- Piece workflows: `usepiece`, `pieceattrib`.

## Typical Workflow

```text
straight modeled asset + spine curve -> pathdeform -> shading/sim/export
```

- Align model forward/up axes to intended deformation direction.
- Tune capture range before adding scale/twist and rigidity constraints.
- Use per-curve attributes for piece-driven variation in multi-curve setups.

## Production Usage

- Strong for hoses, belts, creatures, and path-following rigid+flex hybrids.
- Useful for per-curve instancing/deformation control in piece pipelines.
- Official examples indicate two high-value patterns:
  - rigid subparts on a deforming character (`PathDeformBasic`),
  - per-piece/per-curve assignment and per-curve parameter overrides (`PathDeformPiece`).

Measured outcomes:
- Live Houdini geometry measurements are pending in this session (tool-access checkpoint recorded in `short_term_memory.md`).

## Gotchas

- Misaligned forward/up axes are the most common cause of incorrect bend orientation.
- Clip start/end behavior is functionally convenient but can be significantly more expensive than extend/clamp.
- Base rotation of `0` disables visible ramp/attribute-driven twist effects.

## Companion Nodes

- `sweep` for geometry generation along curves (complementary, not equivalent).
- `wiredeform` / `pointdeform` for alternate deformation models.
- `attribwrangle`/`attribute` for per-curve overrides used by mapping/scale/rotation capture controls.

## Study Validation

- ✅ Read docs: `help/nodes/sop/pathdeform.txt`
- ✅ Reviewed examples: `help/examples/nodes/sop/pathdeform/PathDeformBasic.txt`, `help/examples/nodes/sop/pathdeform/PathDeformPiece.txt`
- ⏳ Live parameter/geometry validation pending in this session
