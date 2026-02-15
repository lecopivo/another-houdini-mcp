# Line (SOP)

## Intent

`line` creates a straight 1D primitive (or point-only chain) from origin, direction, length, and sample count. It is a lightweight source node for guide curves, sweep rails, path tests, and procedural reference axes.

## Core Behavior

- Generates one linear primitive by default (`Polygon`) with evenly spaced points along `origin + dir * t`.
- `type` switches output contract between polygon/NURBS/Bezier curve classes and point-only mode.
- `points` controls sampling density; for curve modes this is the control-point count.
- `order` affects spline basis behavior for NURBS/Bezier and can change emitted point count in some settings.

## Key Parameters

- Geometry mode:
  - `type`: primitive contract switch (`Polygon`, `NURBS`, `Bezier`, `Points`).
- Placement:
  - `origin`: start position.
  - `dir`: line direction vector.
  - `dist`: line length.
- Resolution:
  - `points`: sample/control-point count.
  - `order`: spline order for NURBS/Bezier modes.

## Typical Workflow

```text
line -> (resample/sweep/copy/guide ops) -> OUT
```

- Set orientation with `dir` and size with `dist` first.
- Set `points` to match downstream deformation/sweep density needs.
- If centered behavior is needed, drive one origin axis from `-ch("dist")/2` while aligning `dir` to that axis.

## Production Usage

- Use `type=Polygon` for most modeling/guide tasks where explicit vertices are expected.
- Use `type=Points` when only sampled positions are needed (no primitive topology).
- Keep `points` as low as practical; increase only when downstream operations need denser samples.

Measured outcomes (`LineDirection` example + live `/obj/academy_line_live`):
- Baseline polygon: `points=2`, `dist=1` -> `2 pts / 1 prim / 2 verts`, endpoints `(0,0,0)` to `(0,1,0)`.
- Density increase: polygon `points=10`, `dist=3` -> `10 pts / 1 prim / 10 verts`, endpoints `(0,0,0)` to `(0,3,0)`.
- Primitive-type sweep with `points=10`, `dist=3`:
  - `type=0`: `Polygon` (`1 prim`)
  - `type=1`: `NURBSCurve` (`1 prim`)
  - `type=2`: `BezierCurve` (`1 prim`)
  - `type=3`: point-only (`10 pts / 0 prims`)
- Bezier interaction test (`type=2`): changing `order 2 -> 6` increased emitted points from `10 -> 11` in this build.
- Centering expression pattern (from example): with `dir=(1,0,0)` and `originx=-ch("dist")/2`, changing `dist 4.0 -> 7.5` moved endpoints from `(-2,0,0)/(2,0,0)` to `(-3.75,0,0)/(3.75,0,0)` while staying centered.

## Gotchas

- `type=Points` is valid but emits no primitive; downstream primitive-only nodes may appear to "lose" geometry.
- Large `order` values can alter effective point output in spline modes; verify counts before using as strict topology contracts.
- If using expression-driven centering, manual edits to `originx` will be overridden until the expression is removed.

## Companion Nodes

- `resample` for arc-length re-sampling.
- `sweep` / `polywire` for turning guide lines into renderable geometry.
- `copytopoints` for instancing along sampled line points.

## Study Validation

- ✅ Read docs: `nodes/sop/line.txt`
- ✅ Reviewed example: `examples/nodes/sop/line/LineDirection.txt`
- ✅ Inspected node comments/sticky guidance in `/obj/academy_LineDirection/Line_SOP_Example`
- ✅ Ran live parameter and interaction tests in `/obj/academy_line_live`
