# Attribute Wrangle (SOP)

## What This Node Is For

`attribwrangle` runs a VEX snippet over geometry elements (detail/point/primitive/vertex) to read, create, and modify attributes and even create new geometry.

## Session Status

- Status: studied
- Docs read: yes (`help/nodes/sop/attribwrangle.txt`)
- Example set reviewed: yes (`help/examples/nodes/sop/attribwrangle/AddPoint.txt`, `help/examples/nodes/sop/attribwrangle/CentroidPoints.txt`)
- Example OTL internals inspected: yes (`AddPoint.otl`, `CentroidPoints.otl`)
- Node comments read: yes (no comments present on studied wrangle nodes)
- Sticky notes read: yes
- QA pass complete: yes

## Source-of-Truth Split

- Intent (docs/comments/stickies):
  - Execute custom VEX over selected class and optional group.
  - Support geometry creation (`addpoint`) and attribute logic.
  - Example files focus on detail-mode point creation and centroid derivation.
- Observed (live scene/params/geometry):
  - AddPoint example uses detail mode (`class=0`) and `addpoint(geoself(), {0,1,0});` to create one point from empty input.
  - CentroidPoints example uses detail mode and loops over primitive vertices from input 1 to create one centroid point per primitive.
  - Geometry probes match expected outcomes (see snapshot below).
- Mismatches:
  - None found.

## Minimum Repro Setup

- Node graph:
  - Add-point repro: `/obj/academy_AddPoint/vex_add_point/null1 -> attribwrangle1`
  - Centroid repro: `/obj/academy_CentroidPoints/geo1/torus1 -> (input 1) attribwrangle1`
- Key parameter names and values:
  - `attribwrangle*.class=0` (Detail / only once)
  - Add-point snippet: `addpoint(geoself(), {0,1,0});`
  - Centroid snippet: `primintrinsic("vertexcount") + vertexindex() + vertexpoint() + addpoint()` loop
- Output verification method:
  - HOM geometry probe (point/prim/vertex counts).

## Key Parameters and Interactions

- `class`: controls run-over domain; detail mode is common for topology creation.
- `snippet`: VEX source of truth; behavior is entirely code-driven.
- `group` and `grouptype`: limit execution scope when not running globally.
- `attributes to create`: can restrict which `@` bindings are allowed to auto-create.
- `attribute to match`: affects `opinput#_` bindings when pulling from secondary inputs.

## Observed Behavior Snapshot

- AddPoint network:
  - `/obj/academy_AddPoint/vex_add_point/null1`: `points=0`, `prims=0`
  - `/obj/academy_AddPoint/vex_add_point/attribwrangle1`: `points=1`, `prims=0`
- CentroidPoints network:
  - `/obj/academy_CentroidPoints/geo1/torus1`: `points=288`, `prims=288`, `vertices=1152`
  - `/obj/academy_CentroidPoints/geo1/attribwrangle1`: `points=288`, `prims=0`

Interpretation:
- `addpoint()` in detail mode can generate geometry from empty input.
- centroid loop creates one output point per source primitive in this example.

## Example OTL Inspection Notes

- `AddPoint.otl`:
  - Contains `vex_add_point` geo with two wrangles demonstrating equivalent point-add patterns.
  - `attribwrangle1` is display/render active and shows minimal form: `addpoint(geoself(), {0,1,0});`.
- `CentroidPoints.otl`:
  - Uses a torus as secondary input and computes per-primitive centroid via explicit vertex traversal.
  - Wrangle writes only points (no primitives) in final output.

## Sticky Notes Read (Post-its)

- AddPoint notes emphasize detail mode and `addpoint()` usage with `geoself()`.
- CentroidPoints notes explain `primintrinsic("vertexcount")` and primitive-vertex to point lookup flow.

## Practical Use Cases

1. Fast procedural attribute and topology tweaks without building full VOP graphs.
2. One-off geometry generation or analysis passes (centers, markers, helper points).

## Gotchas and Failure Modes

- Wrong run-over class can duplicate operations unexpectedly (e.g., one `addpoint()` per point).
- Reading from additional inputs requires careful index usage (`point(1, ...)`, `vertexindex(1, ...)`).
- VEX errors often surface via node MMB info, not obvious viewport feedback.
- **Using input-index references without wiring the corresponding input**: Functions like `nearpoint(1, @P)` or `point(1, "P", pt)` require input 1 to be wired. Using these without the input connected causes errors or incorrect behavior.
- **Hardcoded geometry paths are fragile**: Using `nearpoint("op:/obj/geo/target", @P)` breaks when networks are moved or copied. Prefer relative input references like `nearpoint(1, @P, 10.0)` over hardcoded paths.
- **No need to unlock native nodes**: Native Houdini nodes like attribwrangle can have their parameters set directly without unlocking. Only HDAs require unlocking before parameter edits.
- **Working example**: `/obj/nearpoint_example` demonstrates correct usage of `nearpoint(1, @P)` with input 1 wired to target geometry.

## Related Nodes

- `attribvop`
- `attribexpression`
- `volumewrangle`

## Academy QA Checklist

- [x] Official docs reviewed
- [x] Example files reviewed
- [x] OTL instantiated/unlocked and internals inspected
- [x] Node comments read
- [x] Sticky notes read
- [x] Behavior validated with at least one observed test
- [x] Source-of-truth split documented (intent vs observed)
- [x] Context and progress files updated
