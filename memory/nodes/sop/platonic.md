# Platonic (SOP)

## Intent

`platonic` generates canonical polyhedral primitives (plus soccer ball and Utah teapot variants) with simple controls for type, orientation, size, and transform.

## Core Behavior

- `type` selects one of seven built-in solid presets.
- Produces polygonal surface geometry (not volumetric solids).
- `radius` scales the generated asset.
- `orient`, `t`, and `r` control initial alignment and placement.

## Key Parameters

- `type`: tetrahedron, cube, octahedron, icosahedron, dodecahedron, soccer ball, Utah teapot.
- `orient`: predefined up/orientation variants.
- `radius`: uniform size control.
- `t`, `r`: translation and rotation transforms.

## Typical Workflow

```text
platonic -> optional primitive/material/label merge -> downstream modeling/lookdev
```

- Start with `type` for topology class, then size with `radius`.
- Apply orientation before downstream symmetry/boolean operations.
- Use as clean procedural seed geometry for tests, demos, and rig/model blockouts.

## Production Usage

- Good for deterministic benchmark/test meshes with known face distributions.
- Useful as quick topology seeds for tool validation pipelines.
- Keep in mind the Utah teapot option is a historical demo mesh and structurally different from strict Platonic solids.

Measured outcomes (`PlatonicSolidsTypes` + live `/obj/academy_platonic_live`):
- Type sweep contracts (points/prims/face sides):
  - `type=0` tetrahedron: `4 pts / 4 prims`, triangular faces.
  - `type=1` cube: `8 / 6`, quad faces.
  - `type=2` octahedron: `6 / 8`, triangular faces.
  - `type=3` icosahedron: `12 / 20`, triangular faces.
  - `type=4` dodecahedron: `20 / 12`, pentagonal faces.
  - `type=5` soccer ball: `60 / 32`, mixed pentagon+hexagon faces.
  - `type=6` Utah teapot: `330 / 33`, high-sided polygon patches in this build.
- Radius scaling (cube): `radius 0.5 -> 1.0 -> 2.0` produced proportional bbox sizes `0.5 -> 1.0 -> 2.0`.
- Orientation interaction (tetrahedron): changing `orient` altered bbox axis distribution/center offsets while keeping topology fixed.
- Transform contract: setting `t` and `r` shifted center/oriented bbox without changing point/primitive counts.

## Gotchas

- Only first five modes are true Platonic solids; soccer ball and teapot are convenience/demo additions.
- Some types (for example tetrahedron) are not centered identically across orientation presets; verify center assumptions before symmetry operations.
- Generated meshes are surfaces, not watertight “solid modeler” volumes by definition.

## Companion Nodes

- `primitive` for quick primitive-level color/material properties in demo setups.
- `font` + `merge` for labeled visualization variants.
- `transform`/`xform` for staged placement.

## Study Validation

- ✅ Read docs: `nodes/sop/platonic.txt`
- ✅ Reviewed example: `examples/nodes/sop/platonic/PlatonicSolidsTypes.txt`
- ✅ Inspected stickies and repeated per-type companion branch pattern
- ✅ Ran live type/radius/orientation/transform contract tests in `/obj/academy_platonic_live`
