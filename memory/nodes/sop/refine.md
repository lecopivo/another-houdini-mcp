# Refine (SOP)

## Intent

`refine` adds or removes CV/point detail on curves and surfaces, with support for localized domains and mode-specific behavior (refine, unrefine, subdivide).

## Core Behavior

- Works on curve/surface primitives to change control density while aiming to preserve overall shape in refine/subdivide modes.
- `unrefine` performs lossy simplification controlled by tolerances.
- Domain controls (`domainu*`, `domainv*` with first/second toggles) define where operations apply.
- Point/primitive counts can change dramatically while primitive count may remain stable for mesh-like inputs.

## Key Parameters

- `stdswitcher1`: operation mode (`refine`, `unrefine`, `subdivide`).
- `divsu`, `divsv`: density controls in refine/subdivide modes.
- `domainu1/2`, `domainv1/2`, `secondu`, `secondv`: local operation window.
- `tolu`, `tolv`: simplification tolerance in unrefine mode.

## Typical Workflow

```text
surface/curve -> refine (mode-specific) -> downstream modeling/deformation
```

- Start with refine/subdivide for non-lossy detail increase.
- Use unrefine only when controlled simplification is acceptable.

## Production Usage

- Good for controlled CV densification before deformation, trimming, or interpolation-sensitive operations.
- Useful as a quick reduction pass on heavy procedural surfaces when strict geometric fidelity is not required.

Measured outcomes (`BasicRefine`, polygon branch):
- Baseline `refine` output: `1016 pts / 196 prims / 1568 verts`.
- Refine density sweep (`stdswitcher1=refine`):
  - `divsu/v 2 -> 6 -> 10` gave `232 -> 1016 -> 1800` points.
- Unrefine tolerance sweep (`stdswitcher1=unrefine`):
  - `tol 0.01 -> 0.06 -> 0.12` gave `232 -> 139 -> 66` points,
  - higher tolerance reduced vertical detail (bbox Z `0.691791 -> 0.61174`).
- Subdivide mode mirrored refine-style density scaling on this dataset (`232 -> 1016 -> 1800` points for the same divisions).

## Gotchas

- Unrefine is intentionally lossy; increasing tolerance can melt/smooth features.
- Example setups often have mode-specific toggles preconfigured (`secondu/secondv`); missing these can make parameter edits appear ineffective.
- Primitive counts may stay fixed while point/vertex density changes significantly.

## Companion Nodes

- `convert` to establish target primitive type before refine behavior comparisons.
- `skin` for multi-curve surface generation before refinement.
- `resample` as an alternative density-control strategy for curve-centric workflows.

## Study Validation

- ✅ Read docs: `nodes/sop/refine.txt`
- ✅ Reviewed example: `examples/nodes/sop/refine/BasicRefine.txt`
- ✅ Inspected all primitive-type branches and sticky notes
- ✅ Ran live mode/division/tolerance sweeps with measured topology/extent outcomes
