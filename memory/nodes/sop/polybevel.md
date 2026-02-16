# PolyBevel (SOP)

## Intent

`polybevel` inserts fillet faces along selected polygon edges/points to create chamfers/rounds/creases while preserving modeling topology constraints.

## Core Behavior

- Replaces selected edges/points with new fillet topology.
- Supports multiple fillet shape modes (none/solid/crease/chamfer/round-style variants depending on build).
- `offset` controls bevel size; `divisions` controls fillet resolution.
- Can emit output groups for edge/corner fillet faces.

## Key Parameters

- Selection/scope:
  - `group`, `grouptype`, flat/inline ignore toggles.
- Offsetting:
  - `offset`, optional point-scale attribute usage.
- Fillet topology:
  - `filletshape`, `divisions`, profile controls (`profilesource`, convexity/ramp/curve variants).
- Output bookkeeping:
  - edge/corner fillet output groups.

## Typical Workflow

```text
poly mesh -> polybevel -> optional facet/subdivide cleanup -> downstream modeling/shading
```

- Start with explicit edge group selection for controlled bevel scope.
- Increase `offset` to target silhouette, then add `divisions` for smoothness.
- Use output groups to isolate bevel faces for materials/UV/tweaks.

## Production Usage

- Prefer moderate offsets first; large offsets can cause pinch/collision edge cases.
- Keep `divisions` low in modeling phase, raise later when needed for final smoothness.
- Use output groups to avoid brittle face re-selection downstream.

Measured outcomes (`PolybevelBox` example + live `/obj/academy_polybevel_live`):
- Example branch (legacy-style node in this asset):
  - `box`: `8 pts / 6 prims`
  - `polybevel`: `24 pts / 14 prims`
  - `facet(cusp=1)`: `72 pts / 14 prims` (hard-edge style point split).
- Live bevel on subdivided box with modern node (`polybevel::3.0`):
  - `offset=0`, `divisions=2`, round shape -> `488 pts / 486 prims`.
  - Offset changes moved geometry magnitude while keeping counts fixed:
    - `offset 0.05`: mean nearest-to-original distance `0.057773`
    - `offset 0.15`: `0.173318`
    - `offset 0.3`: `0.192366` (approaching local geometric limits).
- Division sweep (`offset=0.15`):
  - `divisions=1`: `216 pts / 218 prims`
  - `divisions=2`: `488 / 486`
  - `divisions=4`: `1352 / 1350`.
- Fillet shape sweep (same base settings):
  - shape modes produced materially different primitive counts (`54` up to `486` prims).
- Output group emission:
  - enabling edge+corner fillet groups created explicit primitive groups (`edgefillets`, `cornerfillets`, each `216` prims in test).
- Partial group bevel (`group="0-3"`) constrained operation (`98 pts / 96 prims`) and changed only targeted region.

## Gotchas

- Blank `group` means bevel all eligible edges; use explicit groups for predictable edits.
- Large offsets can hit collision/pinch constraints and stop behaving linearly.
- High `divisions` escalates topology rapidly.
- Different Houdini versions/assets may instantiate different PolyBevel definitions (legacy vs modern parameter sets).

## Companion Nodes

- `group` for robust edge/point scoping.
- `facet`/`normal` for post-bevel hard/smooth shading control.
- `subdivide` for secondary smoothing after bevel topology creation.

## Study Validation

- ✅ Read docs: `nodes/sop/polybevel.txt`
- ✅ Reviewed example: `examples/nodes/sop/polybevel/PolybevelBox.txt`
- ✅ Inspected sticky notes and companion chain (`box -> polybevel -> facet`)
- ✅ Ran live offset/division/shape/group/output-group behavior tests in `/obj/academy_polybevel_live`
