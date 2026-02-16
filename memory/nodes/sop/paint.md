# Paint (SOP)

## Intent

`paint` interactively writes color or other attributes onto geometry using brush operations (paint/smooth/erase/eyedropper) and multiple merge modes.

## Core Behavior

- Uses brush-based viewport interaction to modify attribute values over selected geometry.
- Default display attributes are `Cd` and `Alpha`, but arbitrary attribute targets are supported via overrides.
- Supports accumulation/stencil workflows and flood operations (`Apply To All`).
- Can operate as color painting or as general attribute authoring with visualization.

## Key Parameters

- `operation` and `mergemode`: paint action and blend semantics.
- `accum` / stencil controls (`Apply & Clear Stencil`) for layered strokes.
- `createcd`: auto-creates `Cd`/`Alpha` where needed.
- `overridecd`, `overridea`: paint alternate target attributes.
- `accuma`: alpha accumulation behavior for glaze-like buildup.
- Attribute visualization parameters for non-color attribute feedback.

## Typical Workflow

```text
input mesh -> paint (Cd or custom attr) -> downstream deformer/material/scatter
```

- Paint masks/weights first, then consume in deformation/scatter/material nodes.
- Use override + visualize when authoring non-display attributes.

## Production Usage

- Fast manual art-direction for weights, masks, and direct color authoring.
- Useful for hybrid procedural workflows where painted attributes modulate node behavior.
- Official examples cover three practical variants:
  - color painting (`PaintColour`),
  - custom attribute painting for downstream modification (`PaintAttributes`),
  - painting scattered points with area control (`PaintPoints`).

Measured outcomes:
- Live Houdini geometry/attribute measurement is pending in this session (tool-access checkpoint recorded in `short_term_memory.md`).

## Gotchas

- Overriding attribute names does not automatically make them viewport color/transparency drivers (only `Cd`/`Alpha` are special by default).
- `Operation` parameter only controls flood/apply-all behavior; viewport RMB tool mode still governs active brush mode.
- Alpha accumulation often needs explicit initialization (e.g., reset `Alpha` to 0 upstream).

## Companion Nodes

- `attribblur` / `smooth` for post-paint smoothing.
- `attribwrangle` for procedural interpretation of painted masks.
- `uvbrush` for UV-space paint workflows.

## Study Validation

- ✅ Read docs: `help/nodes/sop/paint.txt`
- ✅ Reviewed examples: `help/examples/nodes/sop/paint/PaintColour.txt`, `help/examples/nodes/sop/paint/PaintAttributes.txt`, `help/examples/nodes/sop/paint/PaintPoints.txt`
- ⏳ Live parameter/geometry validation pending in this session
