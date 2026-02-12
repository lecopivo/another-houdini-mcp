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
