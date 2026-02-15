# Point (SOP)

## Intent

`point` is a broad point-attribute editor for manually/expression-driving point position and many standard attributes (`Cd`, `N`, `uv`, `Pw`, velocity-related fields, etc.), including optional cross-input matching behavior.

## Core Behavior

- Evaluates parameter expressions per point.
- Attribute sections are gated by per-attribute mode toggles (`Keep/New/Add/No` semantics).
- Can use a second input and optionally match corresponding points by an attribute instead of raw point number.
- Supports legacy local-variable workflows (`$PT`, `$TX`, `$MAPU`, `$TX2`, etc.).

## Key Parameters

- Matching:
  - `matchbyattribute`, `attributetomatch` (for two-input correspondence).
- Standard attribute edits:
  - position `tx/ty/tz`, color `diffr/diffg/diffb`, normal `nx/ny/nz`, texture `mapu/mapv/mapw`, weight `weight`.
- Section toggles:
  - `doclr`, `donml`, `douvw`, `doweight`, and related particle/force toggles.

## Typical Workflow

```text
source points (+ optional reference input) -> point -> downstream shading/deform/sim
```

- Enable only the sections you intend to modify.
- Keep expressions simple and test on small geometry first.
- For two-input transfer workflows, decide early whether matching is by point number or stable id attribute.

## Production Usage

- Strong for quick procedural prototyping and legacy expression-driven effects.
- Prefer `attribwrangle` for larger maintainable logic, but `point` remains useful for compact artist-facing controls.
- Use `matchbyattribute` for particle-like streams where point numbers drift.

Measured outcomes (`PointExamples` + live `/obj/academy_point_live`):
- Example branches validated common usage patterns:
  - weight animation (`Pw`), color animation (`Cd`), normal animation (`N`), UV animation (`uv`), and normal-to-color remapping.
- Live attribute-toggle tests on polygon sphere (`162 pts / 320 prims`):
  - baseline: attrs `id,P`.
  - `doclr=1`: adds `Cd`.
  - `donml=1`: adds `N`.
  - `douvw=1`: adds `uv`.
  - `doweight=1`: adds `Pw`.
- Match-by-attribute test (second input point order scrambled, transfer via `$TX2`):
  - `matchbyattribute=0` -> mean abs X error vs id-matched target `0.717613`.
  - `matchbyattribute=1` with `attributetomatch=id` -> error `0.0`.
  - Confirms attribute matching resolves correspondence when point numbers are unstable.

## Gotchas

- Section toggles must be enabled; setting values alone may do nothing.
- Local-variable workflows are legacy-friendly but brittle for complex logic.
- Two-input edits without `matchbyattribute` can silently mis-map when point order changes.
- Expression-heavy setups are easy to inherit with hidden keyframes/expressions from templates.

## Companion Nodes

- `primitive` for primitive-class edits.
- `attribwrangle` for larger/custom logic.
- `normal` for dedicated normal computation quality.

## Study Validation

- ✅ Read docs: `nodes/sop/point.txt`
- ✅ Reviewed example: `examples/nodes/sop/point/PointExamples.txt`
- ✅ Inspected stickies and multiple branch patterns (weight/color/normal/uv/normal->color)
- ✅ Ran live toggle and two-input matching tests in `/obj/academy_point_live`
