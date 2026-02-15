# VOP Context Basics

## MaterialX viewport authoring pattern

- Prefer MaterialX networks in `/mat` for viewport-compatible custom looks, especially when Vulkan compatibility matters.
- Keep graphs strongly typed and explicit (float math, color math, branch/select, then surface output) rather than relying on implicit conversions.
- For reusable tools, wrap internal graphs in a subnet and expose only artist-facing controls on the subnet interface.

## Reliable output wiring

- In this build, a robust viewport pattern is:

```text
...look_logic... -> mtlxstandard_surface -> mtlxsurfacematerial
```

- Assign object `shop_materialpath` to the material output path used by that chain.
- If direct material assignment appears visually inconsistent, confirm the explicit `mtlxsurfacematerial` output node exists and is connected.

## Control-surface design heuristics

- Expose controls in meaningful units (world/sdf units, not normalized internals).
- Keep parameter semantics orthogonal (for example, spacing should not implicitly change width).
- Bind internal parameters via expressions to subnet parms so one control pane drives the full graph.

## Viewport readability vs physically lit look

- For technical visualization, reduce or disable `specular` to avoid highlight contamination.
- Balance `base` and `emission` depending on goal:
  - Higher `emission` for stable, unlit readout.
  - Higher `base` for form cues under scene lighting.

## Common failure modes and fixes

- Gray/flat viewport look:
  - verify material assignment path,
  - verify display uses materials,
  - verify graph reaches standard-surface inputs.
- Coupled controls (unexpected behavior when changing one parm):
  - convert internal normalized metrics back to exposed-unit domain before thresholding,
  - avoid reusing one parameter for unrelated dimensions.
- Ramp inconsistency across backends:
  - replace ramp dependency with explicit math blends when deterministic behavior is required.
