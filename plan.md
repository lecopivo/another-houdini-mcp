# Plan: Fix `primitive_generator` HDA After Restart

## Goal
Stabilize `tskrivan::primitive_generator_sop::1.0` so new instances are correct by default and shape controls behave consistently.

## Scope
- Definition-level parameter templates and defaults
- Internal bindings and mode-specific primitive behavior
- Runtime behavior validation on fresh instances
- Save/relock and final verification

## Steps

1. Verify definition and baseline state
- Use: `get_hda_definition_info`
- Use: `get_hda_parm_templates`
- Confirm expected type exists and has parameter templates.

2. Normalize exposed parameter interface on the definition
- Use: `set_hda_parm_templates` (authoritative template set)
- Ensure folder + parms exist:
  - `shape_menu`
  - sphere: `sphere_radius`, `sphere_rows`, `sphere_cols`
  - box: `box_size(x/y/z)`, `box_divs(x/y/z)`
  - torus: `torus_radius(1/2)`, `torus_rows`, `torus_cols`
- Use: `set_hda_parm_default`
  - Set `box_divs` default to `(2,2,2)`.

3. Re-apply internal behavior wiring on one editable instance
- Use: `instantiate_hda` (create clean test instance)
- Use: `set_hda_lock_state(locked=false)`
- Use: `set_hda_internal_binding`
  - `switch1.input <- ../shape_menu`
  - sphere radius/rows/cols bindings
  - torus radii/rows/cols bindings
- Use: `set_hda_internal_parm`
  - `output1.outputidx = 0`
  - `sphere1.type = polymesh`
  - `box1.type = polymesh`
  - `torus1.type = poly`
- Critical box fix:
  - bind `box_divsx/y/z` to `box1.divrate1/2/3` (polymesh mode)

4. Save definition and relock
- Use: `save_hda_from_instance`
- Use: `set_hda_lock_state(locked=true)`
- Re-check with `get_hda_definition_info`

5. Validate runtime behavior on a fresh instance
- Use: `instantiate_hda` (new node)
- Use: `validate_hda` with rules:
  - required parms
  - required internal nodes
  - expected primitive types
  - expected output index
- Use: `validate_hda_behavior` with cases:
  - sphere base vs dense: points increase
  - box base vs dense: points/prims increase
  - torus base vs dense: points increase
  - require point attribute `P`
- Use: `probe_geometry` for final per-mode stats report.

6. Cleanup
- Keep one canonical test setup in `/obj/hda_test_geo` or remove temporary nodes.
- Confirm no unlocked mismatched instances remain.

## Success Criteria
- Fresh instances expose full parameter UI (not empty).
- `box_divs` defaults to `(2,2,2)`.
- Output index is `0`.
- Primitive types are: sphere `polymesh`, box `polymesh`, torus `poly`.
- Box density controls change geometry in polymesh mode (via `divrate*` binding).
- `validate_hda` and `validate_hda_behavior` pass.
