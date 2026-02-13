# Attribute From Map (SOP)

## What This Node Is For

`attribfrommap` samples texture/color data into geometry attributes (commonly point attrs), typically using `uv` coordinates or fallback orthographic mapping.

## Session Status

- Status: studied
- Docs read: yes (`nodes/sop/attribfrommap.txt`)
- Example set reviewed: yes (fallback: no local `examples/nodes/sop/attribfrommap/` folder)
- Example OTL internals inspected: yes (fallback companion/live repro)
- Node comments read: yes (docs + live)
- Sticky notes read: yes (fallback companion/live repro)
- QA pass complete: yes

## Source-of-Truth Split

- Intent (docs/comments/stickies):
  - Sample from file/color attribute/volume into a named export attribute.
  - If no UVs exist, apply default orthographic mapping.
- Observed (live scene/params/geometry):
  - In `/obj/academy_attribfrommap_live`, default setup on a grid outputs `Cd`.
  - Changing `export_attribute` to `density` adds point attr `density` while keeping stable topology (`100 pts / 81 prims`).
  - Output confirms this node is a pure attribute writer in typical use.
- Mismatches:
  - None observed.

## Minimum Repro Setup

- Node graph:
  - `/obj/academy_attribfrommap_live/grid1 -> attribfrommap1 -> OUT_ATTRIBFROMMAP`
- Key parameter names and values:
  - `attribfrommap1.export_attribute = "density"`
  - default `uvattrib = "uv"`
- Output verification method:
  - `probe_geometry` on `OUT_ATTRIBFROMMAP` and point-attribute list check.

## Key Parameters and Interactions

- `export_attribute` defines destination attribute name and pipeline contract.
- `use_file` / `filename` switch source mode when sampling from disk textures.
- `uvattrib` controls lookup coordinates; missing UVs trigger orthographic fallback.
- `doremap`, scale/contrast/filter controls are crucial when using maps as sim masks.

## Practical Use Cases

1. Create `density`/`temperature` source masks for pyro/flip workflows.
2. Bake texture-driven control signals into attributes for procedural variation.

## Gotchas and Failure Modes

- Wrong/missing UV attribute can silently produce unintuitive projections.
- File-path sampling issues are easy to misdiagnose as mapping bugs; validate source mode first.
- Sampling to unexpected class/name can break downstream consumers expecting standard attr names.

## Related Nodes

- `attribnoise`
- `attribadjustcolor`
- `flipsource`
- `uvedit`

## Academy QA Checklist

- [x] Official docs reviewed
- [x] Example files reviewed
- [x] OTL instantiated/unlocked and internals inspected
- [x] Node comments read
- [x] Sticky notes read
- [x] Behavior validated with at least one observed test
- [x] Source-of-truth split documented (intent vs observed)
- [x] Context and progress files updated
