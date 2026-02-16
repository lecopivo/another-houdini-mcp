# Peak (SOP)

## Intent

`peak` displaces geometry along point normals or a custom point vector attribute, commonly for inflation/sharpening accents and directional sculpt-style tweaks.

## Core Behavior

- Moves selected elements by `dist` along a direction source.
- Default direction source is point normals.
- Optional custom vector attribute can drive direction and (optionally) magnitude.
- Optional mask attribute blends displacement strength per point.

## Key Parameters

- `group`, `grouptype`: scope selection for displacement.
- `dist`: displacement distance.
- `enablemaskattrib`, `maskattrib`, `mask`: per-point blend control.
- `usecustomattrib`, `customattrib`, `normalizeattrib`: custom directional field controls.
- `updatenmls`: recompute point normals after displacement when needed.

## Typical Workflow

```text
base mesh (+ N or custom vector attrib) -> peak -> optional subdivide/smooth -> downstream
```

- Establish reliable normals first (or author custom vector field).
- Constrain edits with groups/masks to avoid global swelling.
- Smooth/refine after peak if stylization introduces visible faceting.

## Production Usage

- Good for fast localized form pushes (ears, ridges, spikes).
- Use mask attributes for controllable falloff rather than hard groups only.
- Use custom vector attributes for directional effects not aligned to normals.

Measured outcomes (`PeakEars` + live `/obj/academy_peak_live`):
- Example setup:
  - `peak1` targets point group `65 189` (`grouptype=Points`) with `dist=0.146546`, then smooths via `subdivide`.
  - input/output topology at `peak1` unchanged (`1302 pts / 1216 prims`), confirming pure positional displacement.
- Live baseline (normal mode, `dist=0.2`): moved all `162/162` points with uniform max/mean displacement `0.2`.
- Group scoping (`group="100-161"`, points): moved `62/162` points; mean displacement dropped to `0.076543`.
- Mask attribute blend (`maskattrib=mask`): partial displacement (`130/162` moved), mean displacement `0.1` at same `dist`.
- Custom attribute mode (`customattrib=flow`, `dist=0.5`):
  - `normalizeattrib=0` used attribute magnitude (max disp `0.6`, mean `0.35`).
  - `normalizeattrib=1` used direction only (uniform disp `0.5`).
- `updatenmls` toggled on/off kept point `N` available in tested setup.

## Gotchas

- Missing/poor normals lead to unpredictable default displacement directions.
- Large `dist` on sparse topology can create self-intersection or pinching.
- Custom attribute mode is sensitive to vector magnitude unless normalization is enabled.
- Group type mismatch (points vs primitives/edges) can silently affect wrong elements.

## Companion Nodes

- `normal` for stable normal generation before peaking.
- `group` / painted masks for local control.
- `subdivide` / `smooth` for post-peak cleanup.

## Study Validation

- ✅ Read docs: `nodes/sop/peak.txt`
- ✅ Reviewed example: `examples/nodes/sop/peak/PeakEars.txt`
- ✅ Inspected stickies and companion chain (`file -> peak -> subdivide`)
- ✅ Ran live group/mask/custom-attribute/normalize behavior tests in `/obj/academy_peak_live`
