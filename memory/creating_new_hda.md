# Creating a New HDA

This guide outlines a reliable workflow for building Houdini Digital Assets (HDAs), exposing clean parameters, and avoiding common pitfalls.

## 1. Build the Node Network First

Start by creating and wiring the internal SOP/OBJ network manually or with tools. Keep naming consistent (`switch1`, `output1`, `OUT`, etc.) because later automation depends on stable names.

Recommended tools:
- `create_node`
- `connect_nodes`
- `remove_connection`
- `get_folder_info`
- `get_node_connections`

Tips:
- Use a `switch` for shape variants (sphere/box/torus).
- Keep one clear output node.
- Lay out internal nodes early for readability.

## 2. Convert to HDA

Once the network works, convert it into an HDA and save to an `.hda` file.

Recommended tools:
- `create_digital_asset`
- `get_hda_definition_info`

Typical inputs to `create_digital_asset`:
- `node_path`
- `definition_name` (for example: `studio::primitive_generator::1.0`)
- `description`
- `hda_file_path`
- `min_inputs`, `max_inputs`

Gotchas:
- Use namespaces and versions from day one.
- Save to a stable shared path for team usage.

## 3. Manage Lock State During Edits

You generally edit internals while unlocked, then save and relock.

Recommended tools:
- `set_hda_lock_state` (`locked=false` before edits)
- `save_hda_from_instance`
- `set_hda_lock_state` (`locked=true` after edits)
- `get_hda_definition_info`

Gotchas:
- Forgetting to save definition means edits stay local to one instance.
- Relocking before saving can discard intended updates.

## 4. Build a Clean Parameter Interface

Create user-facing controls on the HDA definition, not just one instance.

Recommended tools:
- `get_hda_parm_templates`
- `set_hda_parm_templates`
- `set_hda_parm_default`

Parameter design checklist:
- Use one top-level folder (`Primitive Controls`, `Simulation`, etc.).
- Group controls by feature and execution order.
- Use meaningful ranges (`min/max`) and strict limits where needed.
- Use tuple naming schemes (`XYZW`, `Base1`, etc.) for vector-style parms.
- Prefer clear names (`sphere_radius`) over cryptic labels.

Conditional UI pattern:
- Add a menu parameter (for example `shape_menu`).
- Hide irrelevant groups with `hide_when` expressions:
  - Sphere controls: `{ shape_menu != sphere }`
  - Box controls: `{ shape_menu != box }`
  - Torus controls: `{ shape_menu != torus }`
  - Use menu tokens (`sphere`, `box`, `torus`), not display labels.
  - Always include spaces around operators (`!=`, `==`) or Houdini rejects the rule.

Gotchas:
- Parameter template name mismatches break expression links.
- Menu index assumptions can be fragile; compare menu tokens in conditionals.
- For tuple parms, `parm("name")` may return `None`; use `parmTuple("name")`.

## 5. Bind HDA Parameters to Internal Nodes

Drive internal node parameters from the HDA interface.

Recommended tools:
- `set_hda_internal_binding`
- `set_hda_internal_parm`
- `save_hda_from_instance`

Patterns:
- Use HScript expressions for simple channel refs (`ch("../parm")`).
- Keep binding map explicit and centralized.
- Verify each bound parm exists on the target node.

Gotchas:
- Internal parm names vary by node version/type (`radx` vs `rad`).
- Using wrong tuple component names (`box_sizex` vs `box_size`) causes silent failures.

## 6. Set Primitive Output and Type Correctly

For primitive generators, explicit output index and primitive type avoid many regressions.

Recommended tools:
- `set_hda_internal_parm`
- `set_hda_internal_binding`
- `set_hda_parm_default`

Best practices:
- Ensure output node index is correct (often `0` for primary output).
- Set primitive type by token (for example `polymesh`) instead of numeric index.
- Validate that exposed controls match the selected primitive mode.

## 7. Validate Before Handoff

Run structural and behavioral checks before declaring the HDA done.

Recommended tools:
- `validate_hda`
- `get_hda_definition_info`
- `get_hda_parm_templates`

Useful validation rules include:
- Required exposed parameters exist.
- Required internal nodes exist.
- Expected primitive type tokens are set.
- Expected output indices are set.
- HDA instance matches current definition.

## 8. Probe Resulting Geometry (Runtime QA)

After structural validation, test runtime geometry output from the HDA node itself.

Recommended tools:
- `probe_geometry`
- `set_parameter` (switch modes and test values)
- `validate_hda_behavior`

What to probe per mode:
- Point count and primitive count.
- Vertex count (optional but useful for topology changes).
- Point/primitive/detail attribute names.
- Behavior changes when key parameters are modified (rows/cols/divisions/radius).

Minimal acceptance checks:
- Geometry cooks without errors in each mode.
- Counts are greater than zero for each primitive mode.
- `P` attribute exists on points.
- Changing a key parameter changes point/primitive counts where expected.
- Defaults are checked on a fresh instance, not on a node you already modified during tests.

Example probe flow:
1. Set `shape_menu` to Sphere, Box, Torus one by one.
2. For each shape, record:
- `points`, `prims`, `vertices`
- `point_attributes`, `prim_attributes`, `detail_attributes`
3. Change one relevant control:
- Sphere: increase `rows`/`cols`
- Box: increase `divsx`/`divsy`/`divsz`
- Torus: increase `rows`/`cols`
4. Confirm counts change as expected.
5. If a control does not affect geometry, inspect internal mode-specific controls.
   Example: Box `polymesh` mode is driven by `divrate*`, while `poly` mode is driven by `divs*`.

Gotchas:
- Testing only internal nodes can miss subnet/HDA output wiring issues.
- Locked-state changes can make you think a fix is active when it is not saved.
- Output index mistakes (`outputidx`) can silently route wrong geometry.
- Some SOP controls are gated by extra toggles (for example Box `dodivs`), so exposed parms can look wired but do nothing.

## 9. Suggested End-to-End Tool Sequence

1. Build internals:
- `create_node`, `connect_nodes`, `get_folder_info`

2. Create HDA:
- `create_digital_asset`, `get_hda_definition_info`

3. Unlock and edit:
- `set_hda_lock_state(locked=false)`
- `set_hda_parm_templates`
- `set_hda_parm_default`
- `set_hda_internal_binding`
- `set_hda_internal_parm`

4. Save and relock:
- `save_hda_from_instance`
- `set_hda_lock_state(locked=true)`
- `get_hda_definition_info`

5. Validate:
- `validate_hda`
- `validate_hda_behavior`

## Common Gotchas Summary

- Exposed parameter names do not match internal expression references.
- Internal primitive mode does not match exposed controls.
- Output index is left at non-primary value.
- Asset was edited but definition was not updated.
- Locked/unlocked state confusion causes edits to appear lost.
- Validation is skipped, so regressions are found late.
- Hide/Disable conditionals use labels or indices instead of menu tokens.
- Tuple parm validation used `parm()` instead of `parmTuple()`.

## Practical Naming Conventions

- HDA type: `namespace::asset_name::major.minor`
- Do not append network type suffixes to the asset name (for example avoid `_sop`, `_obj`, `_lop` in the HDA type name).
- Prefer semantic names: `studio::primitive_generator::1.0` instead of `studio::primitive_generator_sop::1.0`.
- Internal nodes: predictable names (`sphere1`, `box1`, `switch1`, `output1`)
- Exposed parms: `feature_parameter` (`torus_rows`, `box_divsx`)

Consistent naming dramatically improves automation and maintenance.
