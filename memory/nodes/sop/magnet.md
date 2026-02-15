# Magnet (SOP)

## Intent

`magnet` deforms or attribute-modifies source geometry using a metaball-driven falloff field. It is useful for localized dents/bulges, animated distortion effects, and selective perturbation of point attributes (position, color, normals, velocity).

## Core Behavior

- Input 0 is the geometry to affect; input 1 is magnet geometry (typically metaballs) defining influence falloff.
- Transform parameters on the Magnet SOP (`tx/ty/tz`, `rx/ry/rz`, `sx/sy/sz`) define the applied change.
- Attribute toggles gate what receives the change:
  - `position`, `color`, `nml`, `velocity`.
- Metaball weighting/radius controls influence strength and region; unaffected points pass through unchanged.

## Key Parameters

- Scope:
  - `deformGrp`, `magnetGrp`, `grouptype` for limiting target and magnet subsets.
- Deform transform:
  - `tx/ty/tz`, `rx/ry/rz`, `sx/sy/sz`, `px/py/pz`.
- Attribute gates:
  - `position` (geometry displacement),
  - `color` + `clampcolor` (point color remap/clamp),
  - `nml` (normal reorientation),
  - `velocity` (point velocity modification).
- Magnet influence source:
  - upstream metaball `rad*` and `metaweight` strongly control how many points are affected and by how much.

## Typical Workflow

```text
source_geo -> magnet(input0)
metaball(s) -> magnet(input1)
magnet -> downstream shading/sim/deform
```

- Build clean source attributes first (`Cd`, `N`, `v`) if you plan to use non-position magnet modes.
- Position magnets so their field intersects target points (shell surfaces only react where field overlaps).
- Enable exactly the attribute gates you intend; keep others off to avoid accidental side effects.

## Production Usage

- Use multiple metaballs (merged/copied) to sculpt richer influence shapes.
- Start with position mode for lookdev, then branch specialized attribute-only magnets for color/normal/velocity passes.
- Keep `clampcolor` on when using strong negative/positive color scaling in pipelines expecting `[0,1]` color ranges.

Measured outcomes (official examples + live `/obj/academy_magnet_live`):
- Example coverage (`MagnetDistortion`):
  - `Affect_Position` uses `tx=1` with position mode.
  - `Affect_Point_Colour` uses `color=1`, `position=0`, `sy=-1`.
  - `Affect_Point_Normals` uses `nml=1`, `position=0`, `ty=-69`.
  - `Affect_Position_Fancy` demonstrates multi-metaball influence composition.
- Live attribute-gated tests on NURBS sphere (`312 pts`) with intersecting metaball:
  - baseline (position on, zero transform): `moved 0/312`, `max_disp=0.0`.
  - position deformation (`tx=1.0`): `moved 96/312`, `max_disp=2.0000`, `mean_disp=0.4037`.
  - color-only (`position=0`, `color=1`, `sy=-1`): no position displacement; `Cd` range expanded to `(-0.002, 1.0)`.
  - with `clampcolor=1`: `Cd` range clamped back to `(0.0, 1.0)`.
  - normal-only (`position=0`, `nml=1`, `ty=-69`): no position displacement; mean normal delta `~0.5976`.
  - velocity-only (`position=0`, `velocity=1`, `tz=1.5`): no position displacement; mean `v` changed from `(0.0, 1.0, 0.0)` to `(0.0, 0.8536, 0.2371)`.
- Metaball weight interaction (`tx=1.0`, position mode):
  - `metaweight 0.5 -> max_disp 0.5`,
  - `metaweight 2.0 -> max_disp 2.0`,
  - `metaweight 4.0 -> max_disp 4.0`.

## Gotchas

- If metaball field does not intersect target points (for example shell surface outside influence), output can appear unchanged even with large transform values.
- Attribute-only modes can look like "no effect" unless you inspect the affected attribute (`Cd`, `N`, `v`).
- Negative scale in color mode can push values outside legal display ranges without `clampcolor`.
- Dense deformation surfaces often require additional tessellation/subdivision to avoid faceted-looking bumps (as shown in `MagnetBubbles`).

## Companion Nodes

- `metaball` and `copy`/`merge` for influence-field authoring.
- `divide`/subdivision utilities for smoother deformation response.
- `point`/`attribwrangle` for seeding and validating `Cd`, `N`, `v` attributes.

## Study Validation

- ✅ Read docs: `nodes/sop/magnet.txt`
- ✅ Reviewed examples: `examples/nodes/sop/magnet/MagnetBubbles.txt`, `examples/nodes/sop/magnet/MagnetDistortion.txt`
- ✅ Inspected sticky notes and companion networks (position/color/normal/velocity variants)
- ✅ Ran live parameter and interaction tests in `/obj/academy_magnet_live`
