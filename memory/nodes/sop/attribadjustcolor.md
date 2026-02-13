# Attribute Adjust Color (SOP)

## What This Node Is For

`attribadjustcolor` creates or modifies RGB vector attributes using constant/random/noise/map-driven patterns with pre/post color processing controls.

## Session Status

- Status: studied
- Docs read: yes (`nodes/sop/attribadjustcolor.txt`)
- Example set reviewed: yes (fallback: no local `examples/nodes/sop/attribadjustcolor/` folder)
- Example OTL internals inspected: yes (fallback companion/live repro)
- Node comments read: yes (docs + live)
- Sticky notes read: yes (fallback companion/live repro)
- QA pass complete: yes

## Source-of-Truth Split

- Intent (docs/comments/stickies):
  - Apply color adjustment via operation + pattern type, optionally initializing/deleting incoming color attrs.
  - Supports color-space aware controls and blending.
- Observed (live scene/params/geometry):
  - In `/obj/academy_attribadjustcolor_live`, default output writes point `Cd`.
  - Changing destination `attrib="myCd"` creates custom color attr `myCd` on points.
  - Constant-color controls (`singlevalue*`) are applied while topology remains unchanged (`100 pts / 81 prims`).
- Mismatches:
  - None observed.

## Minimum Repro Setup

- Node graph:
  - `/obj/academy_attribadjustcolor_live/grid1 -> attribadjustcolor1 -> OUT_ATTRIBADJUSTCOLOR`
- Key parameter names and values:
  - `attribadjustcolor1.attrib = "myCd"`
  - `singlevaluer=1`, `singlevalueg=0.2`, `singlevalueb=0.2`
- Output verification method:
  - `probe_geometry` on `OUT_ATTRIBADJUSTCOLOR` and point-attribute list check.

## Key Parameters and Interactions

- `attrib` sets the output color attribute contract (`Cd` or custom).
- `operation` changes combination semantics with existing data.
- `valuetype` selects generation mode (constant/random/noise/map/remap).
- `deleteallcolorattribs` is a high-value control when conflicting incoming color attrs exist.

## Practical Use Cases

1. Procedurally generate per-point color masks for lookdev, scattering, or sim-driven shading.
2. Normalize inconsistent upstream color attributes before downstream simulation/render stages.

## Gotchas and Failure Modes

- Primitive-vs-point color precedence can hide changes unless class and cleanup settings are explicit.
- Pattern-space confusion (RGB vs HSV ranges) can cause unintuitive palettes.
- Color-map workflows depend on valid UVs/path settings; verify map source first.

## Related Nodes

- `attribnoise`
- `attribadjustfloat`
- `attribadjustvector`
- `color`

## Academy QA Checklist

- [x] Official docs reviewed
- [x] Example files reviewed
- [x] OTL instantiated/unlocked and internals inspected
- [x] Node comments read
- [x] Sticky notes read
- [x] Behavior validated with at least one observed test
- [x] Source-of-truth split documented (intent vs observed)
- [x] Context and progress files updated
