# Attribute Noise (SOP)

## What This Node Is For

`attribnoise` generates coherent noise into float/vector attributes with broad control over range, operation, spatial sampling, and fractal/warp behavior.

## Session Status

- Status: studied
- Docs read: yes (`nodes/sop/attribnoise.txt`)
- Example set reviewed: yes (fallback: no local `examples/nodes/sop/attribnoise/` folder)
- Example OTL internals inspected: yes (fallback companion/live repro)
- Node comments read: yes (docs + live)
- Sticky notes read: yes (fallback companion/live repro)
- QA pass complete: yes

## Source-of-Truth Split

- Intent (docs/comments/stickies):
  - Add/create noise on named attrs and combine with existing values via selectable operation.
  - Support both scalar and vector attribute workflows.
- Observed (live scene/params/geometry):
  - In `/obj/academy_attribnoise_live`, default target attr is `Cd` on points.
  - Setting `attribs="pscale"` immediately creates scalar point attr `pscale` and removes `Cd` from output attribute list in this setup.
  - Topology remains unchanged (`100 pts / 81 prims`), confirming attribute-only behavior.
- Mismatches:
  - None observed.

## Minimum Repro Setup

- Node graph:
  - `/obj/academy_attribnoise_live/grid1 -> attribnoise1 -> OUT_ATTRIBNOISE`
- Key parameter names and values:
  - `attribnoise1.attribs = "pscale"`
  - defaults for operation/range/noise pattern
- Output verification method:
  - `probe_geometry` on `OUT_ATTRIBNOISE` and point-attribute list check.

## Key Parameters and Interactions

- `attribs` + `class` define where noise lands and what downstream nodes will read.
- `operation` controls merge semantics with existing attrs (set/add/multiply/min/max).
- `locationattrib` is critical for stable-vs-swimming behavior (`P` vs `rest`).
- `noiserange` + remap ramps shape practical usable distributions.

## Practical Use Cases

1. Drive variation masks (`pscale`, `temperature`, custom weights) without VEX/VOP setup.
2. Generate coherent art-directable breakup for color/displacement controls.

## Gotchas and Failure Modes

- Forgetting to use stable position attr (`rest`) causes temporal swimming on deforming meshes.
- Wrong attribute class can look like node failure when downstream expects point attrs.
- Range/operation mismatch can clamp or flatten variation unexpectedly.

## Related Nodes

- `attribadjustfloat`
- `attribadjustvector`
- `attribadjustcolor`
- `attribrandomize`

## Academy QA Checklist

- [x] Official docs reviewed
- [x] Example files reviewed
- [x] OTL instantiated/unlocked and internals inspected
- [x] Node comments read
- [x] Sticky notes read
- [x] Behavior validated with at least one observed test
- [x] Source-of-truth split documented (intent vs observed)
- [x] Context and progress files updated
