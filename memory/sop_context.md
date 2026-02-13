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

## 36. SOP FLIP Network Patterns

From SOP FLIP companion studies:

- Core chain:
  - `flipcontainer -> (optional flipboundary/flipcollide) -> flipsolver -> fluidcompress -> filecache -> particlefluidsurface`.

- Input tri-stream contract:
  - FLIP family nodes pass three synchronized streams (sources, container, collisions) through inputs/outputs 0/1/2.
  - Keep these stream connections aligned between container/boundary/collide/solver/compress.

- Source/sink control:
  - `flipboundary` is for particle add/remove and boundary velocity/pressure transfer from custom geometry/volumes.

- Collision control:
  - `flipcollide` converts geometry to collision representation; pairing with proper solver collision mode is required for open vs closed colliders.

- Ocean/open boundary:
  - `oceanspectrum -> oceanevaluate` feeds solver input 3 for boundary motion in large/open-water style setups.
  - Keep solver inputs `0/1/2` coming directly from `flipcontainer` for pure ocean-boundary setups; do not route the main stream through `flipboundary` unless you intentionally need source/sink behavior.

- Whitewater extension:
  - Standard downstream branch is `whitewatersource -> whitewatersolver -> whitewaterpostprocess`, typically fed from compressed FLIP outputs.

- Adaptive-domain pattern:
  - VDB preprocessing subnets (`vdbactivate` + `volumewrangle` + masks) are used to shape/activate solve region before `flipcontainer`.

## 37. SOP Whitewater/Ocean Companion Pattern

From SOP FLIP ocean/whitewater companion studies:

- Ocean boundary workflow:
  - `oceanspectrum -> oceanevaluate -> flipsolver(input3)` is a common open-water coupling pattern.

- Whitewater chain contract:
  - `whitewatersource` expects liquid fields (`surface`, `vel`) and optionally particles/pressure,
  - `whitewatersolver` consumes source output + container + collisions,
  - `whitewaterpostprocess` converts particles to render-friendly particles/volume/mesh outputs.

- Compression-aware downstreaming:
  - `fluidcompress` can be inserted before caching and still feed `particlefluidsurface`/`whitewatersource` reliably when stream contract is respected.

## 38. Subdivide Practical Pattern

From `subdivide/SubdivideCrease` plus live repro:

- Local-detail-first heuristic:
  - Prefer driving `subdivide` with an explicit primitive group before raising `iterations` globally.

- Crease authoring options:
  - Interactive edge creases (`crease` SOP) are fast for lookdev.
  - Procedural second-input crease topology is better for reusable/automated setups.

## 39. File SOP Cache-Boundary Pattern

From `file/PackedPoints` plus live mode toggles:

- Mode-switch debugging rule:
  - Validate expected behavior by intentionally toggling `filemode` between write/read/no-op and observing output changes.
  - This quickly catches stale-cache mistakes where input rewires appear ignored.

- Packed workflow baseline:
  - Generate sample files upstream (ROP), read as packed primitives, then instance/copy for lightweight viewport and disk footprints.

## 40. Bound + Switch Proxy Pattern

From `bound/BoundingBox` example:

- Source-comparison setup:
  - Place `switch` directly before `bound` to compare how alternate input shapes affect proxies without rebuilding downstream.

- Metadata export habit:
  - Enable `addradiiattrib` and `addxformattrib` when downstream nodes need transform/extent data, not just proxy geometry.

## 41. Attribute-Field Authoring Pattern

From `attribfrommap`, `attribnoise`, and `attribadjustcolor` live studies:

- Establish destination attr contracts first:
  - Set destination names explicitly (`density`, `pscale`, `Cd`/custom) before tuning look parameters.
  - This prevents silent downstream breakage from unexpected attribute names/classes.

- Topology vs attribute separation:
  - These nodes are typically attribute-only modifiers; if topology changes, suspect upstream/downstream nodes instead.

- Missing example fallback:
  - For SOP utility nodes with no local node-scoped example folder, use docs + focused live repro + companion references and record that coverage path explicitly.

## 42. Analytic vs Explicit Primitive Rule

From `tube`/`sphere` studies:

- Many generators default to analytic/implicit primitive forms (`1 pt / 1 prim`) that are fast but sparse.
- For downstream topology-sensitive nodes (fracture, collision, deform), switch to polygon/mesh variants before processing.

## 43. VDB Pairing Pattern

From `vdbfrompolygons` + `vdbactivate` studies:

- Build foundational fields first (`surface` SDF and optionally `density` fog), then adjust active regions with `vdbactivate` before heavy volume operations.
- Activation edits often do not show dramatic primitive-count changes; verify intent with dedicated VDB visualization when debugging sparse regions.

## 44. Cache Safety Pattern

From `filecache` study:

- Treat `loadfromdisk` as a strict mode switch.
- If cache files are absent or stale, output can become empty or outdated while upstream network appears correct.
- Keep version/path policy explicit and documented per shot.

## 45. Subnetwork Contract Pattern

From `subnet` + `output` studies:

- Always define explicit output nodes and stable output indices when building reusable subnets/HDAs.
- Avoid dynamic/output-index expression tricks; use upstream switch logic for routing changes.

## 46. Point-Only Add Pattern

From `add` study:

- `Add` is a reliable bridge between full geometry and point-only representations.
- `keep` + `remove` interactions are high risk: misconfiguration can cull all geometry unexpectedly.

## 47. Box-Lattice Coupling Pattern

From `box/BoxSpring` example:

- When `box` is used as lattice cage source, keep division settings synchronized with downstream `lattice` requirements.
- Grouping top cage points + spring deformation is a reusable soft-cage setup.

## 48. One-by-One Example Validation Pattern

From the current academy sweep:

- For broad node coverage, instantiate one official example asset at a time, verify cook/output quickly, then delete it before loading the next.
- This avoids scene bloat and reduces cross-example contamination during long unattended study sessions.

## 49. Attribute Utility Cluster Pattern

From `attribcomposite`, `attribcopy`, `attribcreate`, `attribfill`, `attribfrompieces`, `attribfromvolume`, `attribpaint`, `attribremap`, `attribreorient`, `attribstringedit`, `attribtransfer`:

- Treat attribute names/types/classes as explicit contracts.
- Most failures are contract mismatches (wrong class, missing source attr, incompatible value type), not node algorithm failures.
- For dense or painted workflows, establish a quick probe habit at handoff points to ensure expected attrs remain present.

## 50. Crowd Example Baseline Pattern

From `agentlayer`, `agentrelationship`, `agentvellumunpack`:

- Crowd examples often encapsulate behavior in HDAs with OBJ-level orchestration; validate at object display outputs first, then dive deeper only when needed.
- Parent-child and cloth-unpack workflows rely on consistent agent data plumbing; keep packed-agent contracts stable before downstream simulation.

## 51. Missing-Doc Fallback Rule

From `apex--editgraph` pass:

- If `help/nodes/sop/<node>.txt` is missing but official examples exist, proceed with example-first study and clearly mark docs status as partial.
- Capture this explicitly in node note status to preserve traceability.

## 52. Foreach Block-End Reliability Pattern

From `block_end` examples:

- Treat `block_begin`/`block_end` pair wiring as a strict contract.
- Small miswires in feedback/merge mode can produce valid-looking but semantically wrong output; verify iteration intent explicitly.

## 53. CHOP-to-SOP Control Pattern

From `channel` example:

- CHOP-driven SOP control is effective for procedural motion shaping, but channel naming/path conventions must stay stable.
- Validate imported channel effects directly at the consuming SOP, not only at CHOP level.

## 54. Cloth Transfer Pattern

From `clothdeform` example:

- Use simulation on lower-res driver where possible, then transfer deformation to high-res target.
- This provides better scalability than simulating the final dense mesh directly.

## 55. Curve/Cap/Carve Construction Pattern

From `circle`, `circlefromedges`, `carve`, `cap`, `chain` examples:

- Build parametric curve structures first, then derive solid topology via cap/sweep/copy workflows.
- Keep curve parameterization predictable before extraction/carving to avoid unstable downstream segmentation.

## 56. Volume Noise Authoring Pattern

From `cloudbillowynoise` + `bakevolume`:

- Generate primary volumetric structure with procedural noise, then bake/transfer as needed for downstream lookdev or optimization.
- Keep density/noise resolution choices conservative early to avoid expensive iterative tuning.

## 57. Crowd Motion Path Stack Pattern

From `crowdmotionpath*` + `crowdsource` examples:

- Treat motion-path workflows as a layered stack:
  1) source agents, 2) base paths, 3) follow/avoid/layer/transition ops, 4) evaluate.
- Keep clip names, trigger logic, and transition graph assumptions consistent across the stack; subtle mismatches can silently degrade motion quality.

## 58. Conversion Tool Choice Pattern

From `convert`, `convertline`, `curve`, `circle`, `circlefromedges`:

- Convert as late as possible, after core modeling intent is established.
- Preserve clean curve parameterization before operations like carve/cap/copy-on-curve.

## 59. Legacy vs Modern Geometry Ops Pattern

From `cookie`, `copy`, `crease`, `creep` examples:

- Some legacy nodes remain useful for specific established setups, but behavior may differ from modern counterparts.
- In production maintenance, prefer matching existing tool lineage in a shot rather than mixing paradigms mid-network.

## 60. Attribute-Mask Distance Pattern

From `distancealonggeometry` and `distancefromgeometry` deep play:

- Treat `dist` and `mask` as separate outputs with distinct contracts.
- Toggling output-mask options can remove `mask` while keeping `dist`, which is useful to slim attribute payloads for downstream nodes.

## 61. Delete vs Dissolve Decision Rule

From `delete` and `dissolve` deep play:

- Use `delete` when you want explicit component culling (including random/number filters).
- Use `dissolve` when you want topological edge removal/merging while preserving surrounding surface continuity.
- Invert/non-selected modes on both nodes can drastically expand operation scope; verify with probes immediately.

## 62. Transform-vs-Topology Extrusion Rule

From `extrude` and `duplicate` deep play:

- Parameters like extrusion depth offset and duplicate transforms may change placement while preserving topology.
- Parameters controlling copy count (`ncy`) change topology linearly/additively; monitor output size growth.

## 63. Import-Record Payload Filtering Pattern

From `dopimportrecords` deep play:

- Field filtering can keep point counts stable while significantly shrinking imported attribute sets.
- This is an effective optimization when downstream nodes only need a subset of simulation record data.

## 64. Edge Toolkit Separation Pattern

From `edgecollapse`, `edgecusp`, `edgedivide`, `edgeequalize`, `edgeflip`, `edgefracture`, `edgestraighten` deep play:

- Distinguish topology-changing operations (`edgecollapse`, `edgedivide`, fracture stages) from topology-stable reshaping/ordering ops (`edgeequalize`, `edgestraighten`, many `edgeflip`/`edgecusp` uses).
- For topology-stable edge operations, probe counts will often stay fixed; validate by edge quality/shading/ordering expectations instead.

## 65. Degeneracy Control Rule

From `edgecollapse` and `dissolve`:

- Degenerate-cleanup toggles can materially affect primitive counts after edge operations.
- Keep cleanup intent explicit so downstream nodes receive expected manifold/non-manifold structures.

## 66. Transform-Metadata Extraction Pattern

From `extracttransform` deep play:

- `extracttransform` outputs metadata points (transform attrs), not transformed geometry meshes.
- Enabling distortion output is a practical QA signal for fit quality without changing point count.

## 67. Facet Pipeline Order Reminder

From `facet` example deep play:

- Facet operations are staged; toggles like cusp/unique/consolidate can alter shading and sharing contracts even when counts appear unchanged.
- Be explicit about whether your goal is render-normal behavior or watertight topology preservation.

## 68. Delete Stack-Debug Pattern

From deeper `delete` re-study:

- `delete` is a stacked filter node, not a single-selector node.
- When outputs look wrong, audit enabled sections in this order:
  1) entity, 2) operation/negate, 3) number mode, 4) bounding/normal/degenerate/random, 5) keep-points.
- For deterministic pattern/range workflows, temporarily disable random/bounding filters while tuning, then re-enable intentionally.

## 69. Falloff Weight Safety Pattern

From deep `falloff` study (`falloff_twisted_squab`):

- Treat falloff output attribute names as hard contracts for downstream wrangles/deformers.
- `Unbounded Distance` output can exceed 1.0 and overdrive blend math (for example `lerp` extrapolation).
- For blending masks, prefer normalized outputs or explicit clamping/remapping before use.
- Enable lead-point/group outputs when debugging influence scope (`falloff_leadpt`, `insideRad`).

## 70. Fillet Direction-First Pattern

From deep `fillet` study (`GridFillet`):

- Choose fillet direction (`U` vs `V`) before fine-tuning width/scale/order.
- Direction choice can change bridge topology density and span behavior more than fillet type alone.
- After direction is locked, tune `order` for smoothness and `lrwidth/lrscale` for footprint.
- Test `cut` only after direction is finalized; in some setups it dramatically changes resulting primitive count and whether source surfaces remain fully represented.

## 71. Fit Stability Pattern

From deep `fit` study (`FitCurves`, `FitSurfaces`):

- Choose `method` based on downstream stability requirements:
  - `Interpolation` for more stable CV counts when input count is stable.
  - `Approximation` for reduction/smoothing, accepting potential CV layout variability.
- `scope` and spline `type` can change point/CV density dramatically, especially on surfaces.
- Bezier + breakpoint-heavy interpolation can become very dense; validate counts early before committing in animated pipelines.

## 72. Pathfinding Cost-Model Pattern

From deep `findshortestpath` study (`DirectedEdgesPath`, `PathAnalysis`):

- Treat reachability and cost semantics as separate concerns:
  - reachability is mainly controlled by topology and directed/avoided constraints,
  - ranking of valid paths is controlled by distance/point/primitive/custom costs.
- `omitdistance` should only be used when an alternative cost model is intentionally provided; otherwise costs can collapse to non-informative values.
- For diagnostic workflows, always output explicit path metadata (`path group`, `start/end/pathcost`) so downstream nodes can distinguish routes from carrier geometry.

## 73. Font Tessellation Contract Pattern

From deep `font` study (`FontBasic`, `BubblyFont`):

- Treat `type` and `lod` as primary performance controls; they can change point density by an order of magnitude.
- Enable glyph metadata attributes (`textsymbol`, `textindex`) when downstream logic needs stable mapping from geometry back to characters.
- In animated demo networks, many font parameters are expression-driven; inspect time-dependency before manual edits.

## 74. Fluid Source Field-Contract Pattern

From deep `fluidsource` study (`TorusVolume`, `ColourAdvect`):

- Validate each emitted field by name and resolution, not just primitive count.
- `divsize` mainly controls voxel resolution, while branch-composed fields (for example `Cd.x/y/z`) may keep independent resolutions.
- `make_sdf` + `invert_sign` flips field semantics; keep sign conventions consistent with downstream sourcing/compositing.
- Noise toggles can materially change source amplitude; retune source scale/operations when enabling procedural noise.

## 75. Force-Attribute Gate Pattern

From deep `force` study:

- `force` is an attribute-authoring node for metaball fields; it is not a general geometry force/deform operator.
- Toggle gates are decisive:
  - `doradial` controls presence of `fradial`,
- `doaxis` controls directional attrs (`dir`, `fedge`, `fvortex`, `fspiral`).
- Directional behavior is metaball-local; upstream metaball transforms/orientation affect world-space force direction in simulation.

## 76. Fractal Roughness Control Pattern

From deep `fractal` study:

- Tune in this order for predictable results:
  1) `divs` for topology budget,
  2) `scale` for amplitude,
  3) `smooth` for jaggedness suppression,
  4) `seed` for pattern variation.
- Use `vtxnms=1` for surface-following breakup; use explicit `dir` when a directional bias is intentional.
- Compare outputs with both topology counts and geometric roughness metrics (bbox/variance), since count-only checks miss shape character changes.

## 77. Grid Representation Contract Pattern

From deep `grid` study:

- Distinguish sampling lattice (`rows/cols`) from representation (`type/surftype`).
- Same point lattice can map to very different primitive structures (quads, triangles, lines, single-surface, or points-only).
- For downstream tool compatibility, lock representation early (for example primitives required vs point-only source required).

## 78. Group Copy Conflict-Safety Pattern

From deep `groupcopy` study:

- Treat conflict policy as part of data contract:
  - `skip` for preservation,
  - `overwrite` for authoritative source replacement,
  - `addsuffix` for non-destructive merging.
- Apply prefixes in production pipelines to avoid accidental namespace collisions when many group producers feed one destination stream.

## 79. Group Expand Wavefront Pattern

From deep `groupexpand` study:

- Use positive/negative steps as a symmetric grow/shrink operator around a seed group.
- Enable step attributes when debugging region propagation; this gives an explicit wavefront index per element.
- Normal-angle constraints can intentionally localize growth to near-coplanar regions; tighten only after validating unconstrained spread.
