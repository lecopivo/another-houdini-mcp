# SOP Context Basics

This tutorial covers the core concepts for building geometry in Houdini SOP context and how to work with it reliably through MCP tools.

## 1. What SOP Context Is

SOPs (Surface Operators) are geometry-processing nodes.  
Each node takes geometry input, modifies or generates geometry, and passes result downstream.

Common places you see SOP networks:
- Inside a Geometry OBJ node (for example `/obj/geo1`)
- Inside an HDA of SOP type

## 2. Core Mental Model

Think in node chains:
1. Start with generator nodes (`box`, `sphere`, `tube`, etc.)
2. Modify with transform/attribute/edit nodes (`xform`, `attribwrangle`, etc.)
3. Combine with utility nodes (`merge`, `switch`)
4. End with an `output` node for predictable handoff

Recommended tools:
- `get_folder_info`
- `create_node`
- `connect_nodes`
- `set_parameter`

## 3. Primitive Space and Defaults

Understanding local primitive space prevents most placement mistakes.

- Box:
  - Centered at origin by default.
  - Extent is `[-sizex/2, +sizex/2]`, `[-sizey/2, +sizey/2]`, `[-sizez/2, +sizez/2]`.
- Tube:
  - Centered at origin by default along its height axis.
  - For Y-up defaults, top is `+height/2`, bottom is `-height/2`.
  - Radius parameters are ordered as node-defined (`rad1`, `rad2`), so verify orientation visually or by probing.

Practical implication:
- If you want geometry to “sit on ground” at `Y=0`, move center to `height/2` (or `sizey/2`) where appropriate.

## 4. Building Shape Variants

For multi-shape generators, use one branch per shape and a `switch`.

Pattern:
1. Build each branch (`dog_merge`, `cat_merge`, etc.).
2. Connect branches to `switch1` inputs.
3. Drive `switch1.input` using a menu parameter token/index.
4. Put shared operations after the switch (for example global scale in `xform`).

This keeps branch logic isolated and shared controls centralized.

## 5. Inspecting and Validating Geometry

Always validate runtime output, not just node wiring.

Recommended checks:
- Geometry cooks without errors.
- Non-zero points/primitives for each mode.
- `P` point attribute exists.
- Parameter edits actually change output where expected.

Recommended tools:
- `probe_geometry`
- `validate_hda`
- `validate_hda_behavior`

## 6. SOP Workflow with MCP (Quick Sequence)

1. Explore target network:
- `get_folder_info("/obj")`
- `get_folder_info("/obj/your_geo")`

2. Build graph:
- `create_node`
- `connect_nodes`
- `set_parameter`

3. Verify:
- `get_folder_info`
- `probe_geometry`

4. Package as HDA (if needed):
- `create_digital_asset`
- `set_hda_parm_templates`
- `set_hda_internal_binding`
- `save_hda_from_instance`

## 7. Common Gotchas

- Assuming primitives are based at `Y=0` instead of centered.
- Mixing up menu labels and menu tokens in conditionals.
- Using wrong tuple component names (`sizex` vs `size`, `rad1`/`rad2` vs guessed names).
- Forgetting an explicit `output` node.
- Validating internals only and skipping final HDA output checks.

## 8. Subnets and Output Index Safety

When you build inside subnets (or SOP-type HDAs), output-node indexing matters.

Important rule:
- Your primary output should almost always be an `output` node with `outputidx = 0`.

Why this breaks often:
- Creating/deleting/recreating `output` nodes can leave a single output node at index `1`.
- Houdini may still show geometry in places, but downstream consumers expecting primary output `0` can read nothing or the wrong stream.

Recommended checks:
1. Ensure there is a clear final `output` node in the subnet.
2. Verify `outputidx` is `0`.
3. If there are multiple outputs, make sure each index is intentional and documented.

Recommended tools:
- `get_folder_info` (confirm output node presence and wiring)
- `get_node_parameters` (read `outputidx`)
- `set_parameter` or `set_output_node_index` (fix index to `0`)
- `validate_hda` with `expected_output_indices`

Quick fix pattern:
- If the only output node has `outputidx = 1`, set it to `0` immediately.
- Re-run geometry probe/validation to confirm final output path is correct.

## 9. Lattice Patterns from Example OTLs

From the `sop/lattice` official examples (`DeformLattice`, `BallBounce`, `LatticePerChunk`), two reusable patterns stand out:

- Single-object lattice control:
  - Build one rest cage (`box` or `bound`) and a deformed-cage branch (`group` + `xform` or simulation node).
  - Feed `lattice` inputs as: target geo (0), rest cage (1), deformed cage (2).
  - Keep lattice divisions aligned with cage divisions.

- Per-piece lattice control:
  - Partition geometry into piece groups (`connectivity` + `partition`).
  - In a first foreach, generate per-piece cages (`bound` with divisions).
  - In a second foreach, isolate matching piece/cage groups (`blast`/group naming) and apply `lattice` per piece.
  - This scales better for fractured assets where each chunk needs local deformation.

## 10. PolyExtrude Patterns from Example OTLs

From `sop/polyextrude` (`PolyextrudeTube`), a practical split is:

- Global-style extrusion:
  - Keep front transform off (`xformfront=0`).
  - Drive shape mainly with `dist`, `inset`, and `divs`.
  - Good for consistent shell/thickness changes.

- Local/front-transform extrusion:
  - Enable front transform (`xformfront=1`).
  - Add non-uniform front scaling/rotation to shape profile.
  - Good for stylized per-front shaping.

Observed reminders:
- Parameter sets differ across legacy/new variants; inspect live parms before writing values.
- `outputfront/outputback/outputside` are fast topology controls for capping and open-shell workflows.

## 11. Copy-to-Points Patterns

From live `copytopoints` testing (`/obj/academy_copytopoints`) and related copy-template examples:

- Topology scaling rule of thumb:
  - `pack=0`: output topology scales roughly as source topology x number of target points.
  - `pack=1`: output tracks one packed primitive per target point (far lighter for large scatters).

- Practical workflow:
  - Build/clean source geometry first.
  - Build destination points (grid/scatter/particles) and validate count.
  - Apply `copytopoints`; then tune transform and attribute transfer fields.

## 12. For-Each Loop Patterns

From `foreach` examples (especially `AttributeShuffle`):

- Prefer explicit block pairing:
  - `block_begin.blockpath -> block_end`
  - `block_end.templatepath -> block_begin` (for piece mode)

- Piece-loop baseline:
  - `block_begin.method = Extract Piece or Point`
  - `block_end.itermethod = By Pieces`
  - `block_end.method = Merge Each Iteration`
  - `block_end.attrib = piece` (or `name`)

- Stability reminder:
  - Merge loops may reorder primitive numbering; preserve IDs if downstream steps depend on stable prim order.

## 13. Boolean Patterns

From `/obj/academy_boolean` tests with overlapping boxes:

- Fast sanity triad:
  - Test `booleanop` values for union/intersect/subtract early.
  - Verify both topology and bbox-size changes (counts alone can be ambiguous).

- Input hygiene:
  - Treat normals/manifold quality as first-class checks before debugging parameter tweaks.
  - Keep `collapsetinyedges` enabled unless you need very specific seam geometry behavior.

## 14. Blast Patterns

From `blast/TorusBlast` and live parameter toggles:

- Fast isolate/delete switch:
  - Use `negate` to flip between "delete selected" and "keep selected" without rebuilding groups.

- Reliable targeting:
  - Confirm `grouptype` before trusting results (point vs primitive vs edge can radically change outcome).

## 15. Merge Patterns

From `merge/MergeAttributes` and custom repro:

- Merge is structural, not corrective:
  - It combines streams and unifies attribute schemas, but does not semantically reconcile mismatched attributes for you.

- Build-safe habit:
  - Set critical attrs explicitly upstream on all branches instead of relying on implicit defaults.

## 16. Remesh Patterns

From `remesh/Squidremesh`:

- Mode selection heuristic:
  - Adaptive (`sizing=1`) for feature-following density.
  - Uniform (`sizing=0`) for predictable simulation-friendly triangle sizes.

- Density controls:
  - `targetsize` is the quickest coarse/fine control in uniform mode.
  - Use hard-edge constraints when silhouette or seam preservation matters.

## 17. Fuse Patterns

From `fuse/FuseHood`:

- Separate "snap" from "weld" mentally:
  - Snapping aligns positions.
  - `consolidatesnappedpoints` controls whether points are actually welded.

- Validation shortcut:
  - If vertex count stays same but point count drops, welding happened as intended.

## 18. Group Patterns

From `group/FeaturedEdges`:

- Group class correctness first:
  - Ensure `entity` matches downstream expectation (point/prim/edge).

- Feature-preserve pipeline:
  - Build edge group in `group` and feed it directly into downstream reducers preserving creases.

## 19. Switch Patterns

From live `switch` tests:

- Stable branch routing:
  - Treat input index as API; rewiring changes meaning of existing expressions/keyframes.

- Defensive usage:
  - Keep a known-good fallback on low index and select heavier/riskier branch on higher index.

## 20. PolyReduce Patterns

From `polyreduce/PolyreduceBatwing` and `group/FeaturedEdges`:

- Two-pass strategy:
  - Start with target percentage only.
  - Add feature constraints (`creases`, seam/boundary weights) only where quality drops.

- Locked asset caveat:
  - Official example HDAs may be non-editable; use an unlocked mirror network to test parameter sweeps.

## 21. Measure Patterns

From `measure/MeasureArea` and `measure/MeasureLaplacian`:

- Attribute-driven workflow:
  - Measure into named attrs (`area`, `laplacian`, etc.), then threshold/remap/use in groups/wrangles.

- Loop pattern for smoothing/sharpening:
  - Alternate measure + wrangle in foreach/repeat blocks using small iterative updates for stability.

## 22. Switch-If Patterns

From live `switchif` tests:

- Prefer data-aware branching over raw index switches:
  - Use element-count or attribute-presence tests to decide fallback vs primary branch.

- Keep test wiring explicit:
  - `testinput` can inspect one input while output still selects between both; document this to avoid confusion.

## 23. AttribPromote Patterns

From `attribpromote/AttribPromoteSphere`:

- Promotion as class handoff:
  - Promote analysis attrs (point->prim) for face-level decisions, then demote display attrs back (prim->point) when needed.

- Method matters:
  - Treat promotion method as semantic choice, not implementation detail.

## 24. Connectivity + Partition Patterns

From `connectivity/ConnectedBalls` and `partition/PartitionBall`:

- Piece pipeline:
  - `connectivity` first to generate per-piece ids (`class`/`piece`), then optional `partition` to materialize groups.

- Modern preference:
  - Prefer string piece attrs for scalable pipelines; use `partition` mainly when legacy group-based consumers require it.

## 25. Assemble Patterns

From `assemble/PackedFragments`:

- Fracture handoff pattern:
  - `voronoifracture` generates pieces, `assemble` standardizes metadata and packs for sim.

- Performance default:
  - For many fragments, packed output is usually the right baseline for memory/runtime.

## 26. Companion-Node Review Heuristic

When studying a target node from examples, capture strong companion-node findings in the same pass:

- Typical high-value companions in SOP examples:
  - fracture/distribution nodes (`voronoifracture`, `scatter`),
  - piece-labeling nodes (`connectivity`, `partition`, `name`),
  - routing/validation nodes (`switch`, `switchif`, `null/output`).

- If companion behavior materially informs production usage, create/update their node notes immediately rather than deferring.

## 27. Voronoi Fracture Patterns

From companion usage in `assemble/PackedFragments`:

- Piece count is seed-driven:
  - Scatter seed count is a fast first-order control on resulting fracture/piece count.

- Metadata handoff:
  - Keep `name` continuity from fracture into `assemble`/sim/export chains.

## 28. Scatter Stability Patterns

From `scatter/SpikyDeformingTorus` and `scatter/DoorWithPolkaDots`:

- Deforming topology-stable geo:
  - Emit `primnum`/`primuvw`, then use `attribinterpolate` downstream.

- Topology-changing geo:
  - Prefer texture-space scatter when UV correspondence is stable across model variants.

## 29. Name vs Groups Patterns

From live `name` + `groupsfromname` tests:

- Modern default:
  - Use `name` attrs for large disjoint sets.

- Legacy bridge:
  - Convert to groups only at boundaries where old tools/exporters require them.

## 30. Error/Validation Patterns

From live `error` tests:

- Severity policy:
  - Use warning for recoverable issues, error only for true stop conditions.

- Network behavior:
  - Error severity can intentionally halt downstream cook while preserving pass-through behavior for lower severities.

## 31. Partition Bridge Pattern

From `connectivity -> partition -> name -> groupsfromname`:

- Transitional chain:
  - `connectivity` creates stable piece ids,
  - `partition` materializes legacy groups,
  - `name` modernizes identity,
  - `groupsfromname` re-materializes groups only when needed.

## 32. Missing-Example Fallback Strategy

For nodes without `help/examples/nodes/sop/<node>/` folders:

- Completion criteria used in practice:
  - Official node docs reviewed,
  - at least one companion official example network inspected where the behavior appears,
  - focused live repro network built and validated with parameter/geometry probes.

- This keeps notes actionable while clearly documenting that coverage came from companion examples and repros rather than node-scoped example folders.

## 33. Switch Companion Pattern

From `copy/StampRandom`:

- `switch` is often driven by stamped or expression variables from upstream copy logic.
- Treat switch input index mapping as part of interface contract; random/animated selectors rely on stable wiring order.

## 34. Boolean Companion Pattern

From `foreach/cheese` and `surfsect/SurfsectBasic` companions:

- Boolean-style operations in production examples frequently appear inside iterative loops (`foreach + cookie`) or alternate boolean nodes (`surfsect`), not always as standalone `boolean::2.0` examples.
- Keep one direct `boolean::2.0` repro network for parameter semantics, and use companion examples to learn broader workflow context.

## 35. Vellum Solver Patterns

From `sop/vellumsolver` official examples (all local example assets reviewed one-by-one):

- Heavy-solver workflow hygiene:
  - Load one vellum example, inspect it, then delete it before loading the next to avoid unnecessary memory/cook pressure.

- Dynamic constraint pattern:
  - Example setups often create or update constraints inside `vellumsolver/dopnet/forces` with Vellum Constraints/Constraint Property DOPs (Attach, Stitch, Glue, rest/property animation).

- Per-point collision control:
  - Use attrs such as `collisionignore`, `collisiongroup`, and `disableexternal` to localize collision behavior without splitting into separate solves.

- Layered cloth stabilization:
  - Integer `layer` point attr with solver `layershock` gives predictable ordering for stacked garments/sleeves.

- Multi-res targeting:
  - Upscale low-res cloth motion via high-res soft pins (`targetweight` masks) to preserve macro motion while re-solving collisions/wrinkles.

- Fluid phase emission pattern:
  - Multi-fluid examples often feed source geometry/constraints through Vellum Source DOPs inside solver internals rather than SOP inputs 0/1 directly; early-frame direct solver output can be empty by design.
